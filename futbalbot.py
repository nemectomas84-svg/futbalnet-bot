import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Bot

BOT_TOKEN = "SEM_DAJ_TOKEN"
CHAT_ID = "SEM_DAJ_CHAT_ID"

bot = Bot(token=BOT_TOKEN)

URL_FEED = "https://sportnet.sme.sk/futbalnet/s/"
URL_TABLE = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/tabulky/"

LAST_MATCH_FILE = "last_match.txt"


def get_page(url):
    return requests.get(url).text


def find_sklabina_match(html):
    soup = BeautifulSoup(html, "html.parser")

    matches = soup.find_all("a")

    for m in matches:
        text = m.get_text()

        if "Sklabiná" in text and "Koniec" in text:
            link = m.get("href")
            return text.strip(), "https://sportnet.sme.sk" + link

    return None, None


def was_sent(match_text):
    try:
        with open(LAST_MATCH_FILE, "r") as f:
            return f.read() == match_text
    except:
        return False


def save_match(match_text):
    with open(LAST_MATCH_FILE, "w") as f:
        f.write(match_text)


def get_table():
    html = get_page(URL_TABLE)
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find_all("tr")

    table = []

    for row in rows[1:]:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]

        if len(cols) < 8:
            continue

        pos = cols[0]
        team = cols[1]
        played = cols[2]
        wins = cols[3]
        draws = cols[4]
        losses = cols[5]
        score = cols[6]
        points = cols[7]

        line = f"{pos}. {team} {played} {wins} {draws} {losses} {score} {points}b"

        if "Sklabiná" in team:
            line = f"{pos}. **{team}** {played} {wins} {draws} {losses} {score} {points}b"

        table.append(line)

    return "\n".join(table)


def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="Markdown")


def main():
    html = get_page(URL_FEED)

    match_text, link = find_sklabina_match(html)

    if not match_text:
        print("Ziadny zapas")
        return

    if was_sent(match_text):
        print("Uz odoslany")
        return

    table = get_table()

    message = f"""⚽ Sklabiná – posledný zápas

{match_text}

📊 Tabuľka:

{table}
"""

    send_message(message)
    save_match(match_text)


if __name__ == "__main__":
    main()
