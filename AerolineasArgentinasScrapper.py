from datetime import datetime
from zoneinfo import ZoneInfo
import uuid
from variables import *
from VuelosObj import Vuelos

class AerolineasArgentinasScrapper:
    def __init__(self):
        pass

    @classmethod
    def ObtenerHtmlDeAerolineasArgentinas(self, html):
        return html.find_all("div", id="root")
    
    @classmethod
    def TransformaHtmlEnObjeto(self, html):
        horaActual = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%dT%H:%M:%S")
        id_unico = str(uuid.uuid4())

        vuelosHtml = html.find_all("div", class_="styled__Wrapper-sc-1aqn55i-0 dEpjuA")
        vueloIda = vuelosHtml[0] if vuelosHtml else None
        vueloVuelta = vuelosHtml[1] if len(vuelosHtml) > 1 else None

        listaVuelos = []

        if vueloIda:
            fechaVuelosIda = vueloIda.find_all("span", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["FECHA"])[0].get_text(strip=True)
            vuelos =  vueloIda.find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["VUELOS"])
            for vuelo in vuelos:
                vuelo_obj = Vuelos(DateTime= horaActual,
                                  FechaSalida= fechaVuelosIda,
                                  HoraSalida= vuelo.find_all("div", class_= NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["HORARIOS"])[0].get_text(strip=True),
                                  HoraLlegada= vuelo.find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["HORARIOS"])[1].get_text(strip=True),
                                  LugarSalida= vuelo.find_all("label", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["AEROPUERTOS"])[0].get_text(strip=True),
                                  LugarDestino= vuelo.find_all("label", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["AEROPUERTOS"])[1].get_text(strip=True),
                                  Precio1= vuelo.find_all("label",  class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["PRECIOS"])[0].get_text(strip=True),
                                  Precio2= vuelo.find_all("label",  class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["PRECIOS"])[1].get_text(strip=True),
                                  IdTrackRace= id_unico,
                                  nombreUsuario= None,
                                  TipoVuelo= "Ida"
                                  )
                #vuelo_obj.crear()
                listaVuelos.append(vuelo_obj)
        
        if vueloVuelta:
            fechaVuelosVuelta = vueloVuelta.find_all("span", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["FECHA"])[0].get_text(strip=True)
            vuelos =  vueloVuelta.find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["VUELOS"])
            for vuelo in vuelos:
                vuelo_obj = Vuelos(DateTime= horaActual,
                                  FechaSalida= fechaVuelosVuelta,
                                  HoraSalida= vuelo.find_all("div", class_= NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["HORARIOS"])[0].get_text(strip=True),
                                  HoraLlegada= vuelo.find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["HORARIOS"])[1].get_text(strip=True),
                                  LugarSalida= vuelo.find_all("label", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["AEROPUERTOS"])[0].get_text(strip=True),
                                  LugarDestino= vuelo.find_all("label", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["AEROPUERTOS"])[1].get_text(strip=True),
                                  Precio1= vuelo.find_all("label",  class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["PRECIOS"])[0].get_text(strip=True),
                                  Precio2= vuelo.find_all("label",  class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["PRECIOS"])[1].get_text(strip=True),
                                  IdTrackRace= id_unico,
                                  nombreUsuario= None,
                                  TipoVuelo= "Vuelta"
                                  )
                #vuelo_obj.crear()
                listaVuelos.append(vuelo_obj)
        
        return listaVuelos

    @classmethod
    def mostrar_vuelo(self, titulo, vuelo):
            print(f"\n{titulo}\n")
            print(f"Fecha: {vuelo.FechaSalida}")
            print(f"Hora de Salida: {vuelo.HoraSalida}")
            print(f"Hora de Llegada: {vuelo.HoraLlegada}")
            print(f"Lugar de Salida: {vuelo.LugarSalida}")
            print(f"Lugar de Destino: {vuelo.LugarDestino}")
            print(f"Precio 1: ${float(vuelo.Precio1):.3f}")
            print(f"Precio 2: ${float(vuelo.Precio2):.3f}")
            print("-" * 40)


    @classmethod
    def GenerarOfertaDeVuelos(cls, listaDeVuelos):
        comboVuelosBaratos =[]
        if not listaDeVuelos:
            print("No se encontraron vuelos.")
            return

        vuelosIda = [p for p in listaDeVuelos if p.TipoVuelo.strip().lower() == "ida"]
        vuelosVuelta = [p for p in listaDeVuelos if p.TipoVuelo.strip().lower() == "vuelta"]

        if not vuelosIda:
            print("No se encontraron vuelos de ida.")
            return
        if not vuelosVuelta:
            print("No se encontraron vuelos de vuelta.")
            return

        vuelo_ida = min(vuelosIda, key=lambda p: float(p.Precio1))
        vuelo_vuelta = min(vuelosVuelta, key=lambda p: float(p.Precio1))
        comboVuelosBaratos =[vuelo_ida, vuelo_vuelta]

        total = float(vuelo_ida.Precio1) + float(vuelo_vuelta.Precio1)
        print(f"\nPrecio paquete ida y vuelta: ${total:.3f}")
        
        return comboVuelosBaratos
