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
    return [l.strip() for l in text.split("\n") if l.strip()]


def format_matches(lines):
    results = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if "Sklabin" in line:
            block = lines[i:i+10]

            # dátum + čas (napr. 24.05. 15:00)
            date = next((l for l in block if "." in l and ":" in l), "")

            # status
            status = "Koniec" if any("Koniec" in l for l in block) else ""

            # tímy
            teams = [l for l in block if "TJ" in l]

            # skóre (iba X:Y kde sú čísla)
            score = next(
                (l for l in block if ":" in l and l.replace(":", "").isdigit()),
                "N/A"
            )

            if len(teams) >= 2:
                results.append(
                    f"{date} | {status}\n"
                    f"{teams[0]} {score} {teams[1]}"
                )

            i += 10
        else:
            i += 1

    # odstráni duplicity
    return list(dict.fromkeys(results))


async def main():
    print("BOT STARTED")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("OPENING PAGE...")
        await page.goto(URL, wait_until="networkidle")

        print("WAITING FOR DATA...")
        await page.wait_for_timeout(8000)

        text = await page.evaluate("document.body.innerText")

        lines = clean_lines(text)

        matches = format_matches(lines)

        if not matches:
            send("❌ Sklabiná sa nenašla")
        else:
            msg = "⚽ Sklabiná report\n\n" + "\n\n".join(matches[:2])
            send(msg)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
