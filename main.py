import requests
import time
from bs4 import BeautifulSoup

BOT_TOKEN = '7634342147:AAF-FEVUdJLsmJj5WPMUkVmVyEujsxZ9znk'
CHAT_ID = '196652611'
FANSALE_URL = 'https://www.fansale.it/tickets/all/olly/785187'
CHECK_INTERVAL = 30

notificati = set()

def invia_notifica(messaggio):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": messaggio}
    requests.post(url, data=payload)

# Messaggio all'avvio
invia_notifica("🤖 Bot attivo su Render! Controllo biglietti in corso...")

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

while True:
    try:
        controlla_biglietti()
    except Exception as e:
        print("Errore:", e)
    time.sleep(CHECK_INTERVAL)