import os
import re
import json
import requests

# =====================
# ENV
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT STARTED")
print("TOKEN OK:", bool(BOT_TOKEN))
print("CHAT_ID:", CHAT_ID)


# =====================
# TELEGRAM
# =====================
def send_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("TELEGRAM RESPONSE:", r.text)


# =====================
# NEXT.JS DATA EXTRACTOR
# =====================
def get_next_data(url):
    r = requests.get(url)
    html = r.text

    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html
    )

    if not match:
        print("❌ NEXT_DATA NOT FOUND")
        return None

    try:
        data = json.loads(match.group(1))
        return data
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        return None


# =====================
# SEARCH IN JSON (recursive)
# =====================
def find_sklabina(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                result = find_sklabina(v)
                if result:
                    return result
            elif isinstance(v, str) and "Sklabin" in v:
                return v

    elif isinstance(data, list):
        for item in data:
            result = find_sklabina(item)
            if result:
                return result

    return None


# =====================
# FIND MATCHES (heuristic)
# =====================
def find_matches(data):
    matches = []

    def walk(obj):
        if isinstance(obj, dict):
            if "homeTeam" in obj and "awayTeam" in obj:
                matches.append(obj)

            for v in obj.values():
                walk(v)

        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return matches


# =====================
# TABLE EXTRACTION (simplified)
# =====================
def find_table_rows(data):
    rows = []

    def walk(obj):
        if isinstance(obj, dict):
            if "teamName" in obj and "points" in obj:
                rows.append(obj)

            for v in obj.values():
                walk(v)

        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return rows


# =====================
# MAIN
# =====================
def main():
    print("FETCHING SPORTNET DATA...")

    url = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/"

    data = get_next_data(url)

    if not data:
        send_message("❌ NEXT_DATA sa nenašlo")
        return

    # =====================
    # Sklabiná search
    # =====================
    sklabina = find_sklabina(data)
    print("SKLABINA DEBUG:", sklabina)

    # =====================
    # Matches
    # =====================
    matches = find_matches(data)
    print("MATCHES FOUND:", len(matches))

    last_match = "Žiadny zápas nenájdený"

    for m in matches:
        if "Koniec" in str(m):
            last_match = f"{m.get('homeTeam', '')} - {m.get('awayTeam', '')}"
            break

    # =====================
    # Table
    # =====================
    table = find_table_rows(data)

    table_text = []
    for t in table[:10]:
        name = t.get("teamName", "")
        points = t.get("points", "")
        table_text.append(f"{name} {points}")

    # =====================
    # MESSAGE
    # =====================
    message = f"""
⚽ Sklabiná report

📅 Zápas:
{last_match}

🏆 Tabuľka:
{chr(10).join(table_text) if table_text else "Tabuľka sa nenašla"}
"""

    send_message(message)


if __name__ == "__main__":
    main()
