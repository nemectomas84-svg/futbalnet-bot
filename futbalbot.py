import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

COMPETITION_ID = "vi-liga-ssfz"


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def get_matches():
    url = f"https://api.sportnet.online/v1/public/competitions/{COMPETITION_ID}/matches"
    r = requests.get(url)
    print("STATUS:", r.status_code)

    if r.status_code != 200:
        return None

    return r.json()


def find_sklabina(matches):
    for m in matches.get("matches", []):
        home = m.get("homeTeam", {}).get("name", "")
        away = m.get("awayTeam", {}).get("name", "")

        if "Sklabin" in home or "Sklabin" in away:
            return m
    return None


def main():
    data = get_matches()

    if not data:
        send("❌ API nedostupné")
        return

    match = find_sklabina(data)

    if not match:
        send("❌ Sklabiná zápas sa nenašiel")
        return

    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]

    score = match.get("score")

    if score:
        result = f'{score.get("home")}:{score.get("away")}'
    else:
        result = "ešte sa nehralo"

    msg = f"""⚽ Sklabiná report

📅 Zápas:
{home} - {away}

📊 Výsledok:
{result}
"""

    send(msg)


if __name__ == "__main__":
    main()
