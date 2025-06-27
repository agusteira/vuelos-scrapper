from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from zoneinfo import ZoneInfo
from clases.AerolineasArgentinas.AerolineasArgentinasScrapper import AerolineasArgentinasScrapper
from clases.Scraper import WebScraper
from playwright.sync_api import sync_playwright
from zoneinfo import ZoneInfo
from variables import *
from clases.TokensObj import Tokens
import jwt as pyjwt

class ObtenerTokenAA:
    def __init__(self):
        pass

    @staticmethod
    def obtener_token(aep_ida, aep_vuelta, fecha_ida, fecha_vuelta):
        tokenObj = ObtenerTokenAA.obtener_token_en_bd()
        if tokenObj is not None:
            zona = ZoneInfo("America/Argentina/Buenos_Aires")
            fecha_exp_aware = datetime.strptime(tokenObj.FechaExpiracion, "%Y-%m-%d %H:%M:%S").replace(tzinfo=zona)

            if fecha_exp_aware > datetime.now(zona):
                return tokenObj.Token


        if EN_LINEA:
            url = AerolineasArgentinasScrapper.GenerarUrl(aep_ida, aep_vuelta, fecha_ida, fecha_vuelta, True)
            jwt= ObtenerTokenAA.scrapeToken(url)
            fecha_expiracion = ObtenerTokenAA.decode_jwt(jwt)
            if jwt and fecha_expiracion:
                ObtenerTokenAA.guardar_token_en_bd(jwt, fecha_expiracion)
                return jwt
            else:
                raise Exception("No se pudo obtener o decodificar el token JWT.")
        else:
            Exception("No se puede obtener el token en modo offline. Por favor, activa el modo en línea para realizar esta operación.")


    @staticmethod
    def scrapeToken(url):
        print(url)
        with sync_playwright() as p:
            if RAILWAY_STATE:
                browser = p.chromium.connect(BROWSER_PLAYWRIGHT_ENDPOINT)
            else:
                browser = p.chromium.launch(headless=False)
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
            page.wait_for_selector("div.styled__ComponentWrapper-sc-1jsfikw-0", timeout=600000)

            for token in jwt_tokens:
                print(f"Token JWT encontrado: {token}")
                browser.close()
                return token

            print("No se encontró ningún token JWT en la página.")
            browser.close()
            return None
        

    @staticmethod
    def decode_jwt(token):
        if token:
            try:
                # Si el token no está firmado o no tenés la clave secreta, poné `options={"verify_signature": False}`
                payload = pyjwt.decode(token, options={"verify_signature": False})
                fecha_expiracion = payload.get("exp")  # esto está en formato timestamp (segundos UNIX)
                fecha_expiracion_dt = datetime.fromtimestamp(fecha_expiracion) - timedelta(hours=1)  # Ajustar a la zona horaria de Argentina (UTC-3)
                print("Expira el:", fecha_expiracion_dt)
                return fecha_expiracion_dt
            except Exception as e:
                print("Error al decodificar el JWT:", str(e))
        else:
            print("No se pudo obtener el token.")

    @staticmethod
    def guardar_token_en_bd(token, fecha_expiracion):
        token_obj = Tokens(
            DateTime=datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")),
            Token=token,
            FechaExpiracion=fecha_expiracion,
            Aerolinea="Aerolineas Argentinas"
        )
        token_obj.crear()
    
    @staticmethod
    def obtener_token_en_bd():
        Tokens.crear_tabla()
        return Tokens.leer("Aerolineas Argentinas")