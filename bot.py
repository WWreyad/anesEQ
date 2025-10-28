import os
import time
import requests
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

offset = 0
print("Bot running...")

while True:
    try:
        res = requests.get(f"{BASE}/getUpdates", params={"offset": offset}).json()
        for upd in res.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message")
            if not msg:
                continue
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")
            print("Received:", text)

            # Ask GPT
            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text}]
            ).choices[0].message["content"]

            requests.post(f"{BASE}/sendMessage", json={"chat_id": chat_id, "text": reply})
    except Exception as e:
        print("Error:", e)
    time.sleep(2)
