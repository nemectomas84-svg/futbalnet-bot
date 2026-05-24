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


def clean_lines(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return lines


def format_matches(lines):
    """
    Zoberie rozbitý text a spraví čitateľný výstup
    """

    results = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # hľadáme Sklabiná
        if "Sklabin" in line:
            block = lines[i:i+7]  # vezmeme pár riadkov okolo

            date = block[0] if len(block) > 0 else ""
            status = block[1] if len(block) > 1 else ""
            home = block[2] if len(block) > 2 else ""
            away = block[3] if len(block) > 3 else ""
            score_home = block[4] if len(block) > 4 else ""
            score_away = block[5] if len(block) > 5 else ""

            score = ""
            if score_home.isdigit() and score_away.isdigit():
                score = f"{score_home}:{score_away}"

            results.append(
                f"📅 {date}\n"
                f"{status}\n\n"
                f"{home} {score} {away}"
            )

            i += 7
        else:
            i += 1

    return "\n\n".join(results)


async def main():
    print("BOT STARTED")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("OPENING PAGE...")
        await page.goto(URL, wait_until="networkidle")

        print("WAITING FOR DATA...")
        await page.wait_for_timeout(8000)

        html = await page.content()

        print("HTML SIZE:", len(html))

        lines = clean_lines(html)

        matches = format_matches(lines)

        if not matches:
            send("❌ Sklabiná sa nenašla")
        else:
            msg = "⚽ Sklabiná report\n\n" + matches
            send(msg)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
