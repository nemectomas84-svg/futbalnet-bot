import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("TELEGRAM STATUS:", r.status_code)
    print("TELEGRAM RESPONSE:", r.text)


def get_page():
    url = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"
    r = requests.get(url)

    print("PAGE STATUS:", r.status_code)

    return r.text


def extract_match(html):
    lines = html.splitlines()

    for line in lines:
        if "Sklabin" in line:
            clean = re.sub("<.*?>", "", line)

            if "Koniec" in clean or ":" in clean:
                return clean.strip()

    return "❌ Zápas nenájdený"


def extract_table(html):
    table = []
    lines = html.splitlines()

    for line in lines:
        if "Sklabin" in line:
            clean = re.sub("<.*?>", "", line)
            if len(clean.strip()) > 5:
                table.append(clean.strip())

    return table[:5]


def main():
    try:
        html = get_page()

        if not html:
            send_message("❌ HTML je prázdne")
            return

        match = extract_match(html)
        table = extract_table(html)

        message = f"""
⚽ Sklabiná report

📅 Zápas:
{match}

🏆 Tabuľka:
{chr(10).join(table) if table else "❌ Nenájdená"}
"""

        send_message(message)

    except Exception as e:
        send_message(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    main()
