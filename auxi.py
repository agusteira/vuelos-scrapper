from clases.BusquedasObj import Busquedas
from clases.Scraper import WebScraper
from clases.VuelosObj import Vuelos
from datetime import datetime
from zoneinfo import ZoneInfo
from telebot import telebot
from variables import TOKEN_BOT


WebScraper.scrape("https://www.aerolineas.com.ar/flex-dates-calendar?adt=1&inf=0&chd=0&flexDates=true&cabinClass=Economy&flightType=ROUND_TRIP&leg=EZE-MAD-20250716&leg=MAD-EZE-20250719", True)


"""
Busquedas.crear_tabla()
Busquedas.leer_todo()



hola = Busquedas.traer_todo()


hola[0].eliminar()

Busquedas.leer_todo()


busqueda = Busquedas(
    DateTime=datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%dT%H:%M:%S"),
    IdChatTelegram="484652305",
    AepIda="BUE",
    AepVuelta="USH",
    FechaIda="2026-03-30",
    FechaVuelta="2026-04-03"
)

busqueda.crear()

Busquedas.leer_todo()

=======================================================================================

enlace = "\n🔗 [Ver detalles](https://tu-sitio.com/vuelos.html)"
mensaje = f"\n NUEVO PRECIO: {enlace}"

bot = telebot.TeleBot(TOKEN_BOT)
bot.send_message(484652305, mensaje, parse_mode="Markdown")


"""