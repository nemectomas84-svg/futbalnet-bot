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
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(URL)

        # 🔥 počkaj kým sa načítajú zápasy
        await page.wait_for_selector("div.match, div[class*=match]", timeout=15000)

        matches = await page.query_selector_all("div.match, div[class*=match]")

        results = []

        for match in matches:
            text = await match.inner_text()

            if "Sklabin" in text:
                lines = [l.strip() for l in text.split("\n") if l.strip()]

                # očakávaná štruktúra:
                # dátum
                # status
                # tím1
                # skóre
                # tím2

                if len(lines) >= 5:
                    date = lines[0]
                    status = lines[1]
                    team1 = lines[2]
                    score = lines[3]
                    team2 = lines[4]

                    results.append(
                        f"{date} | {status}\n{team1} {score} {team2}"
                    )

        if not results:
            send("❌ Sklabiná sa nenašla")
        else:
            msg = "⚽ Sklabiná report\n\n" + "\n\n".join(results[:2])
            send(msg)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
