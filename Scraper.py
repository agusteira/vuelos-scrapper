import requests
from bs4 import BeautifulSoup
import json
import re
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid
from VuelosObj import Vuelos

#Hace falta un servicio de scrapeo que pueda ejecutar javascript, como Selenium o Playwright, si el contenido es dinámico.

class WebScraper:
    def __init__(self):
        pass 

    def scrape(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            # Espera a que cargue algún elemento clave (evita capturar una página vacía)
            page.wait_for_selector("label.styled__Fare-sc-l1i8es-3")

            # Obtener el HTML final ya renderizado
            html = page.content()
            browser.close()

            return html
        
    def guardar_archivo_html(self, ruta_archivo, contenido):
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as file:
                file.write(contenido)
            print(f"Archivo guardado en: {ruta_archivo}")
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

    '''
    def parseAerolineasArgentinas(self, html):

        # Ejemplo 1: Buscar todos los títulos en <h2 class="titulo">
        titulos = html.find_all("h2", class_="titulo")
        for titulo in titulos:
            print(titulo.get_text(strip=True))

        # Ejemplo 2: Buscar todos los enlaces <a>
        enlaces = html.find_all("a")
        for enlace in enlaces:
            url = enlace.get("href")
            texto = enlace.get_text(strip=True)
            print(f"Link: {url}, Texto: {texto}")

        # Ejemplo 3: Buscar un elemento específico por id
        header = html.find(id="header")
        if header:
            print(header.get_text(strip=True))

        # Podés devolver lo que quieras, por ejemplo un listado
        return {
            "titulos": [t.get_text(strip=True) for t in titulos],
            "enlaces": [(a.get("href"), a.get_text(strip=True)) for a in enlaces],
            "header_texto": header.get_text(strip=True) if header else None
        }
        '''