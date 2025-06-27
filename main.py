from clases.AerolineasArgentinas.AerolineasArgentinasScrapper import *
from clases.AerolineasArgentinas.ObternetTokenAA import ObtenerTokenAA
from clases.VuelosObj import Vuelos
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from clases.Scraper import WebScraper
from variables import *
from telebot import telebot
from clases.BusquedaDeVuelos import BusquedaDeVuelos
from clases.BusquedasObj import Busquedas
from clases.TokensObj import Tokens

#Inicializacion de objetos
Vuelos.crear_tabla()
scraper = WebScraper()
bot = telebot.TeleBot(TOKEN_BOT)
busquedas = Busquedas.traer_todo()

#=======================================================================================
token = None
#=======================================================================================
for busqueda in busquedas:
    if not busqueda.Active:
        continue
    if token is None:
        token = ObtenerTokenAA.obtener_token(busqueda.AepIda, busqueda.AepVuelta, busqueda.FechaIda, busqueda.FechaVuelta,)
        #BusquedaDeVuelos.ObtenerPreciosAerolineasArgentinas(bot,"BUE", "CPC", "2025-12-06", "2025-12-06", busqueda.id, busqueda.IdChatTelegram,token)
        BusquedaDeVuelos.ObtenerPreciosAerolineasArgentinas(bot, busqueda.AepIda, busqueda.AepVuelta, busqueda.FechaIda, busqueda.FechaVuelta, busqueda.id, busqueda.IdChatTelegram,token)
if EN_LINEA: time.sleep(60)
#=======================================================================================

