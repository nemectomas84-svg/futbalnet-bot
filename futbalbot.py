import requests
import re

BOT_TOKEN = "TOKEN"
CHAT_ID = "CHAT_ID"

URL = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def main():
    r = requests.get(URL)
    html = r.text

    # 🔥 nájdi všetky riadky obsahujúce Sklabiná (aj v HTML)
    matches = re.findall(r'.{0,80}Sklabiná.{0,80}', html)

    if not matches:
        send("❌ Sklabiná sa nenašla (stránka je JS / dynamická)")
        return

    # vyber prvý relevantný výskyt
    result = matches[0]

    # očistenie HTML tagov
    result = re.sub('<.*?>', '', result)

    msg = f"""⚽ Sklabiná report

📊 Nález:
{result.strip()}
"""

    send(msg)


if __name__ == "__main__":
    main()
