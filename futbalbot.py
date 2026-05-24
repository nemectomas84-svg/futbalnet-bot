import os
import asyncio
import requests

print("BOT STARTED")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("ENV OK:", bool(BOT_TOKEN), bool(CHAT_ID))


def send(msg):
    print("SENDING:", msg)
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )
    print("TELEGRAM RESPONSE:", r.text)


async def main():
    print("ASYNC START")

    # 🔥 TEST BEZ PLAYWRIGHT
    send("⚽ TEST BOT FUNGUJE")

    print("DONE")


if __name__ == "__main__":
    asyncio.run(main())
