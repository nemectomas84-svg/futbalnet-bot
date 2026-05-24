import os
import requests
from telegram import Bot

# =====================
# ENV VARIABLES
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# =====================
# DEBUG INFO
# =====================
print("BOT STARTED")
print("TOKEN OK:", bool(BOT_TOKEN))
print("CHAT_ID:", CHAT_ID)


# =====================
# TELEGRAM FUNCTION
# =====================
def send_message(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        raise Exception("Missing BOT_TOKEN or CHAT_ID")

    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=text)
    print("MESSAGE SENT")


# =====================
# SCRAPER PLACEHOLDER
# (sem potom dáme Sportnet logiku)
# =====================
def get_sklabina_data():
    print("FETCHING DATA...")

    # TEMP TEST DATA (aby si videl že bot funguje)
    match = "TJ Družstevník Sklabiná - TEST"
    result = "TEST 3:0"

    table = [
        "1. TJ Slovan Tomášovce 19 17 1 1 89:18 52b",
        "2. Sklabiná 19 12 3 4 40:20 39b"
    ]

    return match, result, table


# =====================
# MAIN LOGIC
# =====================
def main():
    match, result, table = get_sklabina_data()

    print("MATCH:", match)
    print("RESULT:", result)

    message = f"""
⚽ *Sklabiná report*

📅 Zápas:
{match}

📊 Výsledok:
{result}

🏆 Tabuľka:
{chr(10).join(table)}
"""

    print("SENDING MESSAGE...")
    send_message(message)


if __name__ == "__main__":
    main()
