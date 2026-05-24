import os
import requests
from bs4 import BeautifulSoup

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
# DEBUG: RAW PAGE CONTENT
# =====================
def debug_page():
    url = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"
    r = requests.get(url)

    print("STATUS CODE:", r.status_code)
    print("=== RAW HTML START ===")
    print(r.text[:3000])  # prvé 3000 znakov
    print("=== RAW HTML END ===")


# =====================
# MATCH DETECTION (TEMP)
# =====================
def get_last_match():
    url = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text(" ", strip=True)

    print("TEXT SAMPLE:", text[:1000])

    if "Koniec" in text:
        return "Nájdený zápas so statusom Koniec (nešpecifikovaný)"

    return "Žiadny zápas s Koniec v texte"


# =====================
# TABLE DEBUG
# =====================
def get_table_debug():
    url = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/tabulky/"
    r = requests.get(url)

    print("TABLE STATUS:", r.status_code)

    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.find_all("tr")

    print("ROWS FOUND:", len(rows))

    table = []

    for row in rows:
        cols = row.find_all("td")

        if len(cols) > 0:
            row_text = " | ".join(c.text.strip() for c in cols)
            print("ROW:", row_text)
            table.append(row_text)

    return table[:10]


# =====================
# MAIN
# =====================
def main():
    print("SCRAPING START (DEBUG MODE)")

    # 🔥 1. DEBUG RAW PAGE
    debug_page()

    # ⚽ 2. MATCH TEST
    match = get_last_match()

    # 📊 3. TABLE DEBUG
    table = get_table_debug()

    message = f"""
⚽ DEBUG Sklabiná report

📅 Zápas:
{match}

🏆 Tabuľka (debug):
{chr(10).join(table) if table else "EMPTY"}
"""

    send_message(message)


if __name__ == "__main__":
    main()
