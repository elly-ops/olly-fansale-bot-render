import os
import sys
import requests
import time
from bs4 import BeautifulSoup

# === Config ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
print("🎯 BOT_TOKEN presente:", bool(BOT_TOKEN), flush=True)
CHAT_ID = '196652611'
FANSALE_URL = 'https://www.fansale.it/tickets/all/olly/785187'
CHECK_INTERVAL = 30
notificati = set()

# === Telegram ===
def invia_notifica(messaggio):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": messaggio}
        response = requests.post(url, data=payload)
        print("📨 Risposta Telegram:", response.text, flush=True)
    except Exception as e:
        print("❌ Errore nell'invio notifica:", e, flush=True)

#def invia_notifica(messaggio):
    #url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    #payload = {"chat_id": CHAT_ID, "text": messaggio}
    #requests.post(url, data=payload)

# === Controllo biglietti ===
def controlla_biglietti():
    response = requests.get(FANSALE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Debug: stampa i primi 1000 caratteri dell'HTML per vedere la struttura
    print("📝 Contenuto HTML ricevuto:", soup.prettify()[:1000])  # Stampa i primi 1000 caratteri

    eventi = soup.find_all("div", class_="ticketListElement")

    if not eventi:
        print("❗ Nessun evento trovato nella pagina!")

    for evento in eventi:
        data_el = evento.find("div", class_="eventDate")
        luogo_el = evento.find("div", class_="eventLocation")
        if data_el and luogo_el:
            data = data_el.get_text(strip=True)
            print(f"📅 Data trovata: {data}")  # Aggiungi il debug per la data
            if ("mar" in data.lower() or "mag" in data.lower()) and data not in notificati:
                luogo = luogo_el.get_text(strip=True)
                messaggio = f"🎟️ Biglietti disponibili per OLLY il {data} a {luogo}!\n{FANSALE_URL}"
                invia_notifica(messaggio)
                notificati.add(data)

# === Avvio del bot ===
invia_notifica("🤖 Bot attivo su Render! Controllo biglietti in corso...")

while True:
    try:
        controlla_biglietti()
        print("✅ Controllo effettuato.", flush=True)
        sys.stdout.flush()
    except Exception as e:
        print("❌ Errore:", e, flush=True)
        sys.stdout.flush()
    time.sleep(CHECK_INTERVAL)

#while True:
    #try:
        #controlla_biglietti()
    #except Exception as e:
        #print("Errore:", e)
    #time.sleep(CHECK_INTERVAL)
    
    