import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT STARTED")


def send_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    print("TELEGRAM RESPONSE:", r.text)


# =====================
# PRIAMA SÚŤAŽ (NEHĽADÁME KLUB)
# =====================
BASE_URL = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/"


def get_last_match():
    url = BASE_URL + "vysledky/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text(" ", strip=True)

    if "Koniec" in text:
        return "Nájdený ukončený zápas (Koniec)"

    return "Nenašiel sa zápas so statusom Koniec"


def get_table():
    url = BASE_URL + "tabulky/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.find_all("tr")

    table = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 6:
            table.append(" ".join(c.text.strip() for c in cols[:6]))

    return table[:10] if table else ["Tabuľka sa nenašla"]


def main():
    print("SCRAPING VI LIGA SSFZ")

    match = get_last_match()
    table = get_table()

    message = f"""
⚽ Sklabiná report

📅 Zápas:
{match}

🏆 Tabuľka:
{chr(10).join(table)}
"""

    send_message(message)


if __name__ == "__main__":
    main()
