import os
import requests
from bs4 import BeautifulSoup

# =====================
# ENV
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT STARTED")
print("TOKEN OK:", bool(BOT_TOKEN))
print("CHAT_ID:", CHAT_ID)


# =====================
# TELEGRAM SEND
# =====================
def send_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("TELEGRAM RESPONSE:", r.text)


# =====================
# 1. NAJDI KLUB SKLABINÁ
# =====================
def find_sklabina_team():
    url = "https://sportnet.sme.sk/futbalnet/s/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a")

    for a in links:
        text = a.text.strip()
        href = a.get("href", "")

        if "Sklabiná" in text and href:
            full_url = "https://sportnet.sme.sk" + href
            print("FOUND TEAM:", full_url)
            return full_url

    print("Sklabiná NOT FOUND")
    return None


# =====================
# 2. POSLEDNÝ ZÁPAS (HEURISTIKA)
# =====================
def get_last_finished_match(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        if "Koniec" in text:
            return "Posledný odohraný zápas (nájdený status: Koniec)"

        return "Žiadny ukončený zápas nenájdený"

    except Exception as e:
        return f"Error match parsing: {e}"


# =====================
# 3. TABUĽKA (basic parser)
# =====================
def get_table(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        rows = soup.find_all("tr")

        table = []

        for row in rows:
            cols = row.find_all("td")

            if len(cols) >= 6:
                row_text = " ".join(c.text.strip() for c in cols[:6])
                table.append(row_text)

        if not table:
            return ["Tabuľka sa nepodarila načítať"]

        return table[:10]

    except Exception as e:
        return [f"Error table: {e}"]


# =====================
# MAIN
# =====================
def main():
    print("SCRAPING START")

    team_url = find_sklabina_team()

    if not team_url:
        send_message("❌ Sklabiná klub sa nenašiel")
        return

    print("TEAM URL:", team_url)

    match = get_last_finished_match(team_url)

    table = get_table(team_url + "/tabulky/")

    message = f"""
⚽ Sklabiná report

📅 Zápas:
{match}

🏆 Tabuľka:
{chr(10).join(table)}
"""

    print("SENDING MESSAGE...")
    send_message(message)


if __name__ == "__main__":
    main()
