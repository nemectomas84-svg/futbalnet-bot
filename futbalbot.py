import os
import requests

# =====================
# ENV
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT STARTED")
print("TOKEN OK:", bool(BOT_TOKEN))
print("CHAT_ID:", CHAT_ID)


# =====================
# TELEGRAM (stále funkčný test)
# =====================
def send_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("TELEGRAM RESPONSE:", r.text)


# =====================
# API / ENDPOINT HUNT
# =====================
def debug_network_hunt():
    urls = [
        "https://sportnet.sme.sk/futbalnet/s/",
        "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/",
        "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/vysledky/",
        "https://sportnet.sme.sk/futbalnet/z/ssfz/s/vi-liga-ssfz/tabulky/",
    ]

    for url in urls:
        print("\n========================")
        print("URL:", url)

        try:
            r = requests.get(url, timeout=10)

            print("STATUS:", r.status_code)
            print("CONTENT-TYPE:", r.headers.get("Content-Type"))

            text_sample = r.text[:500]

            print("SAMPLE:")
            print(text_sample)

            # jednoduchá detekcia JSON / API
            if "application/json" in str(r.headers.get("Content-Type")):
                print(">>> JSON API DETECTED")

            if "Koniec" in r.text:
                print(">>> FOUND 'Koniec' STRING")

        except Exception as e:
            print("ERROR:", e)


# =====================
# MAIN
# =====================
def main():
    print("STARTING SPORTNET DEBUG HUNT")

    debug_network_hunt()

    send_message("⚽ Debug hotový – pozri logy GitHub Actions")


if __name__ == "__main__":
    main()
