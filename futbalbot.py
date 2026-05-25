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


def extract_matches(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    results = []

    for i in range(len(lines)):
        if "Sklabin" in lines[i]:

            block = lines[max(0, i-3):i+5]
            joined = " | ".join(block)

            # 🎯 SKÓRE (ignoruje čas typu 15:00)
            score = "N/A"
            all_scores = re.findall(r"\b(\d{1,2}):(\d{1,2})\b", joined)

            for a, b in all_scores:
                if int(a) <= 10 and int(b) <= 10:
                    score = f"{a}:{b}"
                    break

            # 📅 dátum
            date = next((x for x in block if "." in x and ":" in x), "")

            # ⏱ status
            status = next((x for x in block if "Koniec" in x or "LIVE" in x), "")

            # 🏟 tímy
            teams = [x for x in block if "TJ" in x]

            if len(teams) >= 2:
                match = (
                    f"{date} | {status}\n"
                    f"{teams[0]} {score} {teams[1]}"
                )
                results.append(match)

    # odstráni duplicity
    return list(dict.fromkeys(results))


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(URL)
        await page.wait_for_timeout(10000)

        text = await page.evaluate("document.body.innerText")

        matches = extract_matches(text)

        if not matches:
            send("❌ Sklabiná sa nenašla")
        else:
            msg = "⚽ Sklabiná report\n\n" + "\n\n".join(matches[:2])
            send(msg)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
