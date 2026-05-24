import requests
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = "TOKEN"
CHAT_ID = "CHAT_ID"

URL_RESULTS = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"
URL_PROGRAM = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/program/"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_last_match():
    r = requests.get(URL_RESULTS)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text("\n")

    lines = [l.strip() for l in text.split("\n") if "Sklabiná" in l]

    return lines[0] if lines else None


def get_next_match():
    r = requests.get(URL_PROGRAM)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text("\n")

    lines = [l.strip() for l in text.split("\n") if "Sklabiná" in l]

    return lines[0] if lines else None


def main():
    last = get_last_match()
    next_match = get_next_match()

    msg = "⚽ Sklabiná report\n\n"

    if next_match:
        msg += f"📅 Najbližší zápas:\n{next_match}\n\n"
    else:
        msg += "📅 Najbližší zápas: nenájdený\n\n"

    if last:
        msg += f"📊 Posledný výsledok:\n{last}"
    else:
        msg += "📊 Posledný výsledok: nenájdený"

    send(msg)


if __name__ == "__main__":
    main()
