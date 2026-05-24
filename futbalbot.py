import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # 🔥 LIMIT (Telegram max ~4096)
    if len(text) > 4000:
        text = text[:4000] + "\n\n...skrátené"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("TELEGRAM:", r.text)


def get_page():
    url = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"

    try:
        r = requests.get(url, timeout=10)
        print("PAGE STATUS:", r.status_code)
        return r.text
    except Exception as e:
        print("PAGE ERROR:", e)
        return None


def extract_info(html):
    if not html:
        return "❌ Nepodarilo sa načítať stránku", []

    # ak stránka používa JS
    if "Sklabin" not in html:
        return "⚠️ Sklabiná sa nenašla (JS stránka)", []

    lines = html.splitlines()

    match = "❌ Zápas nenájdený"
    table = []

    for line in lines:
        if "Sklabin" in line:
            clean = re.sub("<.*?>", "", line).strip()

            # zápas
            if ":" in clean and len(clean) < 100:
                match = clean

            # tabuľka riadky
            if len(clean) > 5:
                table.append(clean)

    return match, table[:5]  # 🔥 max 5 riadkov


def main():
    try:
        html = get_page()

        match, table = extract_info(html)

        message = f"""⚽ Sklabiná report

📅 Zápas:
{match}

🏆 Tabuľka:
{chr(10).join(table) if table else "❌ Nedostupná"}
"""

        send_message(message)

    except Exception as e:
        send_message(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    main()
