import os
import requests

# =====================
# ENV VARIABLES (GitHub Actions secrets)
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# =====================
# DEBUG
# =====================
print("BOT STARTED")
print("TOKEN OK:", bool(BOT_TOKEN))
print("CHAT_ID:", CHAT_ID)


# =====================
# TELEGRAM SEND (FIXED - NO LIBRARY)
# =====================
def send_message(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        raise Exception("Missing BOT_TOKEN or CHAT_ID")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("TELEGRAM RESPONSE:", response.text)


# =====================
# SCRAPER (TEMP TEST DATA)
# =====================
def get_sklabina_data():
    print("FETCHING DATA...")

    # TEMP DATA (kým nenapojíme Sportnet)
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

    text = f"""
⚽ Sklabiná report

📅 Zápas:
{match}

📊 Výsledok:
{result}

🏆 Tabuľka:
{chr(10).join(table)}
"""

    print("SENDING MESSAGE...")
    send_message(text)


# =====================
# ENTRY POINT
# =====================
if __name__ == "__main__":
    main()
