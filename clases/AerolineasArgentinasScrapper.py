from datetime import datetime
from zoneinfo import ZoneInfo
import uuid
from variables import *
from clases.VuelosObj import Vuelos
import re

class AerolineasArgentinasScrapper:
    def __init__(self):
        pass

    @classmethod
    def ObtenerHtmlDeAerolineasArgentinas(self, html):
        return html.find_all("div", id="root")
    
    @classmethod
    def TransformaHtmlEnObjeto(self, html, tracker_id):
        horaActual = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%dT%H:%M:%S")

        vuelosHtml = html.find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["VUELOS_HTML"])
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
                                    IdTrackRace= tracker_id,
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
                                    IdTrackRace= tracker_id,
                                    nombreUsuario= None,
                                    TipoVuelo= "Vuelta"
                                    )
                #vuelo_obj.crear()
                listaVuelos.append(vuelo_obj)
        
        return listaVuelos

    
    @classmethod
    def GenerarUrl(self, origen, destino, fechaIda, fechaVuelta, fechaFlexible=False):
        ida= "{origen}-{destino}-{fechaIda}".format(
            origen=origen, 
            destino=destino, 
            fechaIda=datetime.strptime(fechaIda, "%Y-%m-%d").strftime("%Y%m%d")
        )
        vuelta = "{destino}-{origen}-{fechaVuelta}".format(
            origen=origen, 
            destino=destino, 
            fechaVuelta=datetime.strptime(fechaVuelta, "%Y-%m-%d").strftime("%Y%m%d")
        )
        #
        if(fechaFlexible):
            url_base = f"{NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["URL_BASE_FECHA_FLEXIBLE"]}&leg={ida}&leg={vuelta}"
        else:
            url_base = f"{NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["URL_BASE_FECHA_ESPECIFICA"]}&leg={ida}&leg={vuelta}"
        return url_base
    
    @classmethod
    def ObtenerOfertaMasBarata(self, html):
        ida = html.find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["PRECIOS_IDA_FLEXIBLE"])
        vuelta = html.find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["PRECIOS_VUELTA_FLEXIBLE"])

        arrayTodosLosPreciosDeIda = ida[0].find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["PRECIOS_FINALES_FLEXIBLES"])
        arrayTodosLosPreciosDeVuelta = vuelta[0].find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["PRECIOS_FINALES_FLEXIBLES"])
        
        precioIda = self.ObtenerVueloMasBaratoDeUnArrayDePrecios(arrayTodosLosPreciosDeIda)
        precioVuelta = self.ObtenerVueloMasBaratoDeUnArrayDePrecios(arrayTodosLosPreciosDeVuelta)


        return [precioIda, precioVuelta]
        #print(ida)
    
    def ObtenerVueloMasBaratoDeUnArrayDePrecios(arrayTodosLosPrecios):
        precios_numericos = []

        for precio in arrayTodosLosPrecios:
            texto = precio.get_text(strip=True)
            numero = re.sub(r"[^\d]", "", texto)
            if numero:
                precios_numericos.append(int(numero))

        if precios_numericos:
            precio_minimo = min(precios_numericos)
            return precio_minimo
        