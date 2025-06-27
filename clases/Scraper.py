
from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright
from variables import *
from clases.VuelosObj import Vuelos

class WebScraper:
    def __init__(self):
        pass 
    
    @classmethod
    def scrape(self, url, fechaFlexible):
        with sync_playwright() as p:
            if RAILWAY_STATE:
                browser = p.chromium.connect(BROWSER_PLAYWRIGHT_ENDPOINT)
            else:
                browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            jwt_tokens = []

            # Interceptar requests salientes
            def on_request(request):
                auth_header = request.headers.get("authorization")
                if auth_header and "Bearer " in auth_header:
                    token = WebScraper.extract_jwt(auth_header)
                    if token and token not in jwt_tokens:
                        jwt_tokens.append(token)

            page.on("request", on_request)

            page.goto(url)

            # Espera a que cargue algún elemento clave (evita capturar una página vacía)
            if fechaFlexible:
                page.wait_for_selector("div.styled__ComponentWrapper-sc-1jsfikw-0", timeout=600000)
            if not fechaFlexible:
                page.wait_for_selector("label.styled__Fare-sc-l1i8es-3", timeout=600000)

            # Obtener el HTML final ya renderizado
            html = page.content()
            browser.close()

            for token in jwt_tokens:
                print(f"Token JWT encontrado: {token}")

            return html
    
    @classmethod
    def extract_jwt(cls, header_value):
        match = re.match(r"Bearer\s+(.+)", header_value)
        return match.group(1) if match else None

    @classmethod
    def guardar_archivo(self, ruta_archivo, contenido):
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as file:
                file.write(contenido)
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    @classmethod
    def leer_archivo(self, ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as file:
                contenido = file.read()
            return contenido
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return None

    @classmethod
    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup

