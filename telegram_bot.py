import requests

TOKEN = "8081302753:AAEha2MufUxxU9AXObrhIRSVOY3vRgIX78I"
CHAT_ID = "687511965"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

send_telegram_message("✅ Bot ishga tushdi!")
