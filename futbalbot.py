import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


def get_page():
    url = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"
    r = requests.get(url)
    return r.text


def extract_match(html):
    # nájdi riadok kde je Sklabiná
    lines = html.splitlines()

    for line in lines:
        if "Sklabin" in line and "Koniec" in line:
            clean = re.sub("<.*?>", "", line)
            return clean.strip()

    return "Zápas Sklabine nenájdený"


def extract_table(html):
    table = []
    lines = html.splitlines()

    for line in lines:
        if "Sklabin" in line:
            clean = re.sub("<.*?>", "", line)
            table.append(clean.strip())

    return table[:5]


def main():
    html = get_page()

    match = extract_match(html)
    table = extract_table(html)

    msg = f"""
⚽ Sklabiná report

📅 Zápas:
{match}

🏆 Tabuľka:
{chr(10).join(table) if table else "Nenájdená"}
"""

    send_message(msg)


if __name__ == "__main__":
    main()
