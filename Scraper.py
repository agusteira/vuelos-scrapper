import requests
from bs4 import BeautifulSoup
import json
import re
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from variables import *
from VuelosObj import Vuelos

class WebScraper:
    def __init__(self):
        pass 

    def scrape(self, url, fechaFlexible):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            # Espera a que cargue algún elemento clave (evita capturar una página vacía)
            if fechaFlexible:
                page.wait_for_selector("div.styled__ComponentWrapper-sc-1jsfikw-0", timeout=600000)
            if not fechaFlexible:
                page.wait_for_selector("label.styled__Fare-sc-l1i8es-3", timeout=600000)

            # Obtener el HTML final ya renderizado
            html = page.content()
            browser.close()

            return html
        
    def guardar_archivo_html(self, ruta_archivo, contenido):
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as file:
                file.write(contenido)
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def leer_archivo_html(self, ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as file:
                contenido = file.read()
            return contenido
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return None

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup
