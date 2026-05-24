import os
import asyncio
import requests
from playwright.async_api import async_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"


def send(msg):
    print("SENDING MESSAGE...")
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )
    print("TELEGRAM RESPONSE:", r.text)


def extract_blocks(text):
    """
    Nájde Sklabiná a zoberie okolie textu (kontext zápasu)
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    results = []

    for i, line in enumerate(lines):
        if "Sklabin" in line:
            block = lines[max(0, i - 3): i + 6]

            cleaned = " | ".join(block)
            results.append(cleaned)

    return results


async def main():
    print("BOT STARTED")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("OPENING PAGE...")
        await page.goto(URL, wait_until="domcontentloaded")

        print("WAITING FOR RENDER...")
        await page.wait_for_timeout(10000)

        # 🔥 najst reálny text z DOM (nie HTML)
        text = await page.evaluate("document.body.innerText")

        print("TEXT LENGTH:", len(text))

        if "Sklabin" not in text:
            send("❌ Sklabiná sa nenašla")
            await browser.close()
            return

        blocks = extract_blocks(text)

        if not blocks:
            send("❌ Sklabiná existuje, ale neviem vybrať zápas")
            await browser.close()
            return

        msg = "⚽ Sklabiná report\n\n" + "\n\n".join(blocks[:5])

        send(msg)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
