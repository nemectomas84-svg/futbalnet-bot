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

        print("OPEN PAGE")
        await page.goto(URL, wait_until="networkidle")

        print("WAIT FOR TABLE")

        # 🔥 čakať na linky zápasov (kľúčové!)
        await page.wait_for_selector("a", timeout=15000)

        links = await page.query_selector_all("a")

        sklabina_matches = []

        for link in links:
            text = await link.inner_text()
            if text and "Sklabin" in text:
                sklabina_matches.append(text.strip())

        await browser.close()

        if not sklabina_matches:
            send("❌ Sklabiná sa nenašla")
            return

        msg = "⚽ Sklabiná report\n\n"

        for m in sklabina_matches[:5]:
            msg += f"• {m}\n"

        send(msg)


if __name__ == "__main__":
    asyncio.run(main())p
