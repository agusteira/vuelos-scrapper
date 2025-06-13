from AerolineasArgentinasScrapper import *
from VuelosObj import Vuelos
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from Scraper import WebScraper
from variables import *
from telebot import telebot

# Crear DB y tabla
Vuelos.crear_tabla()

scraper = WebScraper()
bot = telebot.TeleBot(TOKEN_BOT)
hora_actual = datetime.now().strftime("%H:%M:%S")
print("La hora actual es:", hora_actual)

print("Buscando vuelos con fecha flexible...")
if EN_LINEA:
    url = AerolineasArgentinasScrapper.GenerarUrl(AEROPUERTOS_IDA, AEROPUERTOS_VUELTA, FECHA_IDA, FECHA_VUELTA, True)
    html = scraper.scrape(url, True)
    scraper.guardar_archivo_html("pagina_scrapeada_fecha_flexible.html", html)
else:
    html = scraper.leer_archivo_html("pagina_scrapeada_fecha_flexible.html")

if html:
    html = scraper.parse(html)
    html = AerolineasArgentinasScrapper.ObtenerHtmlDeAerolineasArgentinas(html)
    html = html[0] if html else None 
    ofertasFlexibles = AerolineasArgentinasScrapper.ObtenerOfertaMasBarata(html)
    totalFechaFlexible = sum(oferta for oferta in ofertasFlexibles)
    precio_formateado = f"{totalFechaFlexible:,}".replace(",", ".")
    print(f"\nPrecio paquete mas baratos en fechas cercanas: ${precio_formateado}")
    print(f"Ida: ${ofertasFlexibles[0]:,}, Vuelta: {ofertasFlexibles[1]:,}".replace(",", "."))
    bot.send_message(CHAT_ID, f"\nPrecio paquete mas baratos en fechas cercanas: ${precio_formateado}")


#=======================================================================================
print("-" * 100)
print("\nBuscando vuelos con fecha específica...")
if EN_LINEA:
    url = AerolineasArgentinasScrapper.GenerarUrl(AEROPUERTOS_IDA, AEROPUERTOS_VUELTA, FECHA_IDA, FECHA_VUELTA, False)
    html = scraper.scrape(url, False)
    scraper.guardar_archivo_html("pagina_scrapeada.html", html)
else:
    html = scraper.leer_archivo_html("pagina_scrapeada.html")


if html:
    html = scraper.parse(html)
    html = AerolineasArgentinasScrapper.ObtenerHtmlDeAerolineasArgentinas(html)
    html = html[0] if html else None 
    listaDeVuelos = AerolineasArgentinasScrapper.TransformaHtmlEnObjeto(html)
    listaVuelosBaratos= Vuelos.GenerarOfertaDeVuelos(listaDeVuelos)
    for vuelo in listaVuelosBaratos:
        Vuelos.mostrar_vuelo(f"Vuelo de {vuelo.TipoVuelo} más barato", vuelo)
        if EN_LINEA:
            vuelo.crear()


#=======================================================================================

