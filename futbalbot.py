import os
import requests

# =====================
# ENV
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT STARTED")


# =====================
# TELEGRAM
# =====================
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("TELEGRAM:", r.text)


# =====================
# API (natvrdo – funguje)
# =====================
API_URL = "https://sportnet.sme.sk/api/competition/2458/results"
TABLE_URL = "https://sportnet.sme.sk/api/competition/2458/table"


# =====================
# GET LAST MATCH
# =====================
def get_last_match():
    try:
        r = requests.get(API_URL)
        data = r.json()

        for match in data.get("matches", []):
            home = match.get("homeTeam", {}).get("name", "")
            away = match.get("awayTeam", {}).get("name", "")
            status = match.get("status", "")
            score = match.get("score", "")

            if "Sklabin" in home or "Sklabin" in away:
                if status == "FINISHED":
                    return f"{home} - {away}\n{score}"

        return "Zápas nenájdený"

    except Exception as e:
        print("MATCH ERROR:", e)
        return "Chyba pri zápase"


# =====================
# TABLE
# =====================
def get_table():
    try:
        r = requests.get(TABLE_URL)
        data = r.json()

        table = []

        for team in data.get("table", []):
            name = team.get("team", {}).get("name", "")
            points = team.get("points", "")

            table.append(f"{name} {points}b")

        return table[:10]

    except Exception as e:
        print("TABLE ERROR:", e)
        return []


# =====================
# MAIN
# =====================
def main():
    match = get_last_match()
    table = get_table()

    message = f"""
⚽ Sklabiná report

📅 Zápas:
{match}

🏆 Tabuľka:
{chr(10).join(table) if table else "Tabuľka nedostupná"}
"""

    send_message(message)


if __name__ == "__main__":
    main()
