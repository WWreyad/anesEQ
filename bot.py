import os
from flask import Flask, request
import requests
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is alive!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("DEBUG: Received update:", data, flush=True)

    if not data or "message" not in data:
        return "no message", 200

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        reply = completion.choices[0].message["content"]
    except Exception as e:
        reply = f"Error: {e}"

    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(send_url, json={"chat_id": chat_id, "text": reply})
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
