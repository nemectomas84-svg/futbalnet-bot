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
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    results = []

    for i, line in enumerate(lines):
        if "Sklabin" in line:
            block = lines[max(0, i - 4): i + 6]

            unique = []
            for b in block:
                if b not in unique:
                    unique.append(b)

            try:
                kolo = next((x for x in unique if "kolo" in x), "")
                datum = next((x for x in unique if ":" in x and "." in x), "")
                status = next((x for x in unique if x in ["Koniec", "LIVE", "Koniec zápasu"]), "")

                teams = [x for x in unique if "Sklabin" in x or "TJ" in x]

                score_nums = [x for x in unique if x.isdigit()]
                score = ""
                if len(score_nums) >= 2:
                    score = f"{score_nums[0]}:{score_nums[1]}"

                match_line = (
                    f"{kolo} | {datum} | {status}\n"
                    f"{teams[0]} {score} {teams[1]}"
                )

                results.append(match_line)

            except:
                results.append(" | ".join(unique))

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

        text = await page.evaluate("document.body.innerText")

        print("TEXT LENGTH:", len(text))

        # -------------------------
        # ZÁPASY
        # -------------------------
        if "Sklabin" not in text:
            send("❌ Sklabiná sa nenašla")
            await browser.close()
            return

        blocks = extract_blocks(text)

        # -------------------------
        # TABUĽKA
        # -------------------------
        table_text = ""

        try:
            rows = await page.query_selector_all("table tbody tr")

            for r in rows[:10]:
                row = await r.inner_text()
                table_text += row + "\n"

        except:
            table_text = "Tabuľka nedostupná"

        # -------------------------
        # SPRÁVA
        # -------------------------
        if not blocks:
            send("❌ Sklabiná existuje, ale nepodarilo sa spracovať")
        else:
            msg = (
                "⚽ Sklabiná report\n\n"
                + "\n\n".join(blocks[:5])
                + "\n\n🏆 Tabuľka:\n"
                + table_text.strip()
            )

            send(msg)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
