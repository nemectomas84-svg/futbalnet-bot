import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("TELEGRAM:", r.text)


def main():
    match = "TJ Družstevník Sklabiná - Súper"
    result = "3:1"
    table = [
        "1. Tím A 52b",
        "2. Sklabiná 39b",
        "3. Tím C 35b"
    ]

    message = (
        "⚽ Sklabiná report\n\n"
        "📅 Zápas:\n"
        f"{match}\n\n"
        "📊 Výsledok:\n"
        f"{result}\n\n"
        "🏆 Tabuľka:\n"
        + "\n".join(table)
    )

    send_message(message)


if __name__ == "__main__":
    main()
