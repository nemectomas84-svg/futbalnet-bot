import os
import asyncio
import requests
from playwright.async_api import async_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(URL, wait_until="networkidle")
        await page.wait_for_timeout(8000)

        text = await page.evaluate("document.body.innerText")

        if "Sklabin" not in text:
            send("❌ Sklabiná sa nenašla")
            return

        lines = [l for l in text.split("\n") if "Sklabin" in l]

        msg = "⚽ Sklabiná report\n\n" + "\n".join(lines[:10])

        send(msg)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
