from clases.AerolineasArgentinasScrapper import *
from clases.VuelosObj import Vuelos
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from clases.Scraper import WebScraper
from variables import *
from telebot import telebot
from clases.BusquedaDeVuelos import BusquedaDeVuelos
from clases.BusquedasObj import Busquedas

#Inicializacion de objetos
Vuelos.crear_tabla()
scraper = WebScraper()
bot = telebot.TeleBot(TOKEN_BOT)
busquedas = Busquedas.traer_todo()
#=======================================================================================
for busqueda in busquedas:
    if not busqueda.Active:
        continue
    BusquedaDeVuelos.ObtenerPreciosGenerales(bot, busqueda.AepIda, busqueda.AepVuelta, busqueda.FechaIda, busqueda.FechaVuelta, busqueda.IdChatTelegram)
    BusquedaDeVuelos.ObtenerPreciosEspecificos(bot, busqueda.AepIda, busqueda.AepVuelta, busqueda.FechaIda, busqueda.FechaVuelta, busqueda.id,  busqueda.IdChatTelegram)
    if EN_LINEA: time.sleep(60)
#=======================================================================================

