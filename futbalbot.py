import os
import requests

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


def get_matches():
    url = "https://sportnet.sme.sk/api/matches?competition=ssfz-vi-liga"

    try:
        r = requests.get(url)
        return r.json()
    except:
        return None


def main():
    try:
        data = get_matches()

        if not data:
            send_message("❌ Dáta sa nepodarilo načítať")
            return

        matches = data.get("matches", [])

        skl_match = None

        for m in matches:
            home = m.get("homeTeam", {}).get("name", "")
            away = m.get("awayTeam", {}).get("name", "")

            if "Sklabin" in home or "Sklabin" in away:
                skl_match = m
                break

        if not skl_match:
            send_message("❌ Sklabiná zápas sa nenašiel")
            return

        home = skl_match["homeTeam"]["name"]
        away = skl_match["awayTeam"]["name"]
        score = skl_match.get("score", "N/A")
        status = skl_match.get("status", "N/A")

        message = f"""⚽ Sklabiná report

📅 Zápas:
{home} - {away}

📊 Výsledok:
{score}

📌 Stav:
{status}
"""

        send_message(message)

    except Exception as e:
        send_message(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    main()
