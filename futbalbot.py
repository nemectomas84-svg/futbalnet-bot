import os
import requests
import re
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    if len(text) > 4000:
        text = text[:4000]

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("TELEGRAM:", r.text)


def get_data():
    url = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"

    r = requests.get(url)
    html = r.text

    # 🔥 hľadáme NEXT_DATA JSON
    match = re.search(r'<script id="__NEXT_DATA__".*?>(.*?)</script>', html)

    if not match:
        return None

    json_text = match.group(1)

    try:
        data = json.loads(json_text)
        return data
    except:
        return None


def main():
    try:
        data = get_data()

        if not data:
            send_message("❌ Nepodarilo sa nájsť NEXT_DATA")
            return

        # DEBUG výpis
        text = str(data)[:3000]

        send_message("⚽ DEBUG DATA:\n\n" + text)

    except Exception as e:
        send_message(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    main()
