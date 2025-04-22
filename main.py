import os
import requests
import time
from bs4 import BeautifulSoup
from flask import Flask, request
from threading import Thread

# === Config ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = '196652611'
FANSALE_URL = 'https://www.fansale.it/tickets/all/olly/785187'
CHECK_INTERVAL = 30
notificati = set()

# === Flask per endpoint Telegram ===
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    if 'message' in data:
        message = data['message']
        text = message.get('text', '')
        chat_id = message['chat']['id']
        if text.lower() == '/test' and str(chat_id) == CHAT_ID:
            controlla_biglietti()
            invia_notifica("✅ Test ricevuto! Controllo biglietti effettuato.")
    return {'ok': True}

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# === Funzioni bot ===
def invia_notifica(messaggio):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": messaggio}
    requests.post(url, data=payload)

def controlla_biglietti():
    response = requests.get(FANSALE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    eventi = soup.find_all("div", class_="ticketListElement")

    for evento in eventi:
        data_el = evento.find("div", class_="eventDate")
        luogo_el = evento.find("div", class_="eventLocation")
        if data_el and luogo_el:
            data = data_el.get_text(strip=True)
            if "mag" in data.lower() and data not in notificati:
                luogo = luogo_el.get_text(strip=True)
                messaggio = f"🎟️ Biglietti disponibili per OLLY il {data} a {luogo}!\n{FANSALE_URL}"
                invia_notifica(messaggio)
                notificati.add(data)

# === Avvio ===
keep_alive()
invia_notifica("🤖 Bot attivo su Render con endpoint test!")

while True:
    try:
        controlla_biglietti()
        print("✅ Controllo effettuato.")
    except Exception as e:
        print("❌ Errore:", e)
    time.sleep(CHECK_INTERVAL)

#while True:
    #try:
        #controlla_biglietti()
    #except Exception as e:
        #print("Errore:", e)
    #time.sleep(CHECK_INTERVAL)
    