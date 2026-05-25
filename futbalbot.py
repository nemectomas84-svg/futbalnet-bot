import os
import asyncio
import requests
import re
from playwright.async_api import async_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/"


def send(msg):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )
    print(r.text)


def extract_matches(html):
    results = []

    # nájde bloky zápasov
    matches = re.findall(
        r"(\\d{2}\\.\\d{2}\\.\\s*\\d{2}:\\d{2}.*?TJ Družstevník Sklabiná.*?)(\\d+:\\d+)",
        html,
        re.DOTALL
    )

    for block, score in matches:

        # tímy
        teams = re.findall(r"TJ [A-Za-zÁ-ž ]+", block)

        if len(teams) >= 2:
            # dátum
            date_match = re.search(r"\\d{2}\\.\\d{2}\\.\\s*\\d{2}:\\d{2}", block)
            date = date_match.group(0) if date_match else ""

            # status
            status = "Koniec" if "Koniec" in block else ""

            results.append(
                f"{date} | {status}\n"
                f"{teams[0]} {score} {teams[1]}"
            )

    return list(dict.fromkeys(results))


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(URL)
        await page.wait_for_timeout(10000)

        html = await page.content()

        matches = extract_matches(html)

        if not matches:
            send("❌ Sklabiná sa nenašla")
        else:
            msg = "⚽ Sklabiná report\n\n" + "\n\n".join(matches[:2])
            send(msg)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
