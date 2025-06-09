from AerolineasArgentinasScrapper import *
from VuelosObj import Vuelos
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from Scraper import WebScraper
from variables import *

# Crear DB y tabla
Vuelos.crear_tabla()

scraper = WebScraper()
if EN_LINEA:
    url = "https://www.aerolineas.com.ar/flights-offers?adt=1&inf=0&chd=0&flexDates=false&cabinClass=Economy&flightType=ROUND_TRIP&leg=BUE-CPC-20251206&leg=CPC-BUE-20251213"
    html = scraper.scrape(url)
    scraper.guardar_archivo_html("pagina_scrapeada.html", html)
else:
    html = scraper.leer_archivo_html("pagina_scrapeada.html")


if html:
    html = scraper.parse(html)
    html = AerolineasArgentinasScrapper.ObtenerHtmlDeAerolineasArgentinas(html)
    html = html[0] if html else None 
    listaDeVuelos = AerolineasArgentinasScrapper.TransformaHtmlEnObjeto(html)
    listaVuelosBaratos= AerolineasArgentinasScrapper.GenerarOfertaDeVuelos(listaDeVuelos)
    for vuelo in listaVuelosBaratos:
        AerolineasArgentinasScrapper.mostrar_vuelo(f"Vuelo de {vuelo.TipoVuelo} más barato", vuelo)
        if EN_LINEA:
            vuelo.crear()

Vuelos.leer_todo()

'''


# Insertar datos
ahora = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%dT%H:%M:%S")

vuelo_obj = Vuelos(DateTime= ahora,
                                  FechaSalida="2025-07-01",
                                  HoraSalida="08:00",
                                  HoraLlegada="14:00",
                                  LugarSalida="Buenos Aires",
                                  LugarDestino="Miami",
                                  Precio1=105000.00,
                                  Precio2=125000.00)


# Consultar
vuelo_obj.crear()
Vuelos.leer_todo()
'''