from clases.AerolineasArgentinasScrapper import *
from clases.VuelosObj import Vuelos
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from clases.Scraper import WebScraper
from variables import *
from telebot import telebot


class BusquedaDeVuelos:
    def __init__(self):
        pass

    @classmethod
    def ObtenerPreciosGenerales(self, bot, aep_ida, aep_vuelta, fecha_ida, fecha_vuelta, IdChatTelegram):
        print("Buscando vuelos con fecha flexible...")

        if EN_LINEA:
            url = AerolineasArgentinasScrapper.GenerarUrl(aep_ida, aep_vuelta, fecha_ida, fecha_vuelta, True)
            html = WebScraper.scrape(url, True)
            WebScraper.guardar_archivo_html("htmls/pagina_scrapeada_fecha_flexible.html", html)
        else:
            html = WebScraper.leer_archivo_html("htmls/pagina_scrapeada_fecha_flexible.html")

        if html:
            html = WebScraper.parse(html)
            html = AerolineasArgentinasScrapper.ObtenerHtmlDeAerolineasArgentinas(html)
            html = html[0] if html else None 
            ofertasFlexibles = AerolineasArgentinasScrapper.ObtenerOfertaMasBarata(html)
            totalFechaFlexible = sum(oferta for oferta in ofertasFlexibles)
            precio_formateado = f"{totalFechaFlexible:,}".replace(",", ".")
            print(f"\nPrecio paquete mas baratos en fechas cercanas: ${precio_formateado}")
            print(f"Ida: ${ofertasFlexibles[0]:,}, Vuelta: {ofertasFlexibles[1]:,}".replace(",", "."))
            if EN_LINEA: bot.send_message(IdChatTelegram, f"\nPrecio paquete mas baratos en fechas cercanas: ${precio_formateado}")

    @classmethod
    def ObtenerPreciosEspecificos(self, bot, aep_ida, aep_vuelta, fecha_ida, fecha_vuelta, tracker_id, IdChatTelegram):
        print("-" * 100)
        print("\nBuscando vuelos con fecha específica...")

        if EN_LINEA:
            url = AerolineasArgentinasScrapper.GenerarUrl(aep_ida, aep_vuelta, fecha_ida, fecha_vuelta, False)
            html = WebScraper.scrape(url, False)
            WebScraper.guardar_archivo_html("htmls/pagina_scrapeada.html", html)
        else:
            html = WebScraper.leer_archivo_html("htmls/pagina_scrapeada.html")


        if html:
            html = WebScraper.parse(html)
            html = AerolineasArgentinasScrapper.ObtenerHtmlDeAerolineasArgentinas(html)
            html = html[0] if html else None 
            listaDeVuelos = AerolineasArgentinasScrapper.TransformaHtmlEnObjeto(html, tracker_id)
            listaVuelosBaratos= Vuelos.GenerarOfertaDeVuelos(listaDeVuelos)
            total = sum(float(vuelo.Precio1) for vuelo in listaVuelosBaratos[:2])

            esDiferenteALaUltimaVez = Vuelos.traer_ultima_oferta(tracker_id, total)

            for vuelo in listaVuelosBaratos:
                if esDiferenteALaUltimaVez: Vuelos.mostrar_vuelo(f"Vuelo de {vuelo.TipoVuelo} más barato", vuelo, bot, IdChatTelegram)
                if EN_LINEA: vuelo.crear()

            # Calcular el precio total del paquete ida y vuelta        
            
            if esDiferenteALaUltimaVez:
                enlace = f"\n🔗 [Ver detalles]({url})" 
            else:
                enlace = ""
            mensaje = f"\nDia especifico: {'NUEVO PRECIO' if esDiferenteALaUltimaVez else 'NO HAY CAMBIOS'}  (${total:.3f}) {enlace}"
            print(mensaje)
            if EN_LINEA:
                bot.send_message(IdChatTelegram, mensaje, parse_mode="Markdown")

            

