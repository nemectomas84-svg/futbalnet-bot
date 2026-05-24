import os
import asyncio
from playwright.async_api import async_playwright
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )


async def get_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(URL)
        await page.wait_for_timeout(5000)  # počká na JS load

        content = await page.content()
        await browser.close()

        return content


def extract(html):
    # jednoduché hľadanie (robustné)
    if "Sklabin" not in html:
        return None

    lines = html.split("\n")

    for i, line in enumerate(lines):
        if "Sklabin" in line:
            return line.strip()

    return None


async def main():
    html = await get_data()

    match = extract(html)

    if not match:
        send("❌ Sklabiná sa nenašla")
        return

    send(f"⚽ Sklabiná report\n\n📅 Zápas:\n{match}")


if __name__ == "__main__":
    asyncio.run(main())
