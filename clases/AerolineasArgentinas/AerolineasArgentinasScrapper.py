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

    @staticmethod
    def GenerarUrlApi(origen, destino, fechaIda, fechaVuelta):
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
        return f"{NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["URL_API"]}&leg={ida}&leg={vuelta}"

    @staticmethod
    def GenerarUrl(origen, destino, fechaIda, fechaVuelta, fechaFlexible=False):
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
    
    @staticmethod
    def generar_mensaje_oferta_con_fechas(json_data, fecha_ida_fija, fecha_vuelta_fija, idTrackRace, nombreUsuario):
        def buscar_por_fecha(ofertas, fecha_deseada):
            for item in ofertas:
                if item.get("departure") == fecha_deseada and item.get("offerDetails") and not item.get("soldOut"):
                    return item
            return None

        def obtener_mejor_oferta(ofertas):
            mejores = []
            for item in ofertas:
                if item.get("offerDetails") and not item.get("soldOut"):
                    total = item["offerDetails"]["fare"]["total"]
                    mejores.append((total, item))
            return min(mejores, key=lambda x: x[0])[1] if mejores else None

        def formatear(oferta, tipo):
            seg = oferta["leg"]["segments"][0]
            fecha_fmt = datetime.strptime(oferta["departure"], "%Y-%m-%d").strftime("%d/%m/%Y")
            vuelo = seg["flightNumber"]
            salida = seg["departure"].split("T")[1][:5]
            llegada = seg["arrival"].split("T")[1][:5]
            origen = seg["origin"]
            destino = seg["destination"]
            precio = oferta["offerDetails"]["fare"]["total"]
            return (
                f"*{tipo}* ({fecha_fmt}) - Vuelo {seg['airline']}{vuelo}\n"
                f"{origen} {salida} → {destino} {llegada} | 💰 ${precio:,.0f}".replace(",", ".")
            )

        ida_ofertas = json_data.get("calendarOffers", {}).get("0", [])
        vuelta_ofertas = json_data.get("calendarOffers", {}).get("1", [])

        mejor_ida = obtener_mejor_oferta(ida_ofertas)
        mejor_vuelta = obtener_mejor_oferta(vuelta_ofertas)

        fija_ida = buscar_por_fecha(ida_ofertas, fecha_ida_fija)
        fija_vuelta = buscar_por_fecha(vuelta_ofertas, fecha_vuelta_fija)

        if not mejor_ida or not mejor_vuelta:
            return "❌ No hay suficientes datos para calcular el mejor combo.", []

        mejor_total = mejor_ida["offerDetails"]["fare"]["total"] + mejor_vuelta["offerDetails"]["fare"]["total"]
        mensaje = f"💸 *Combo más barato encontrado:* ${mejor_total:,.0f}".replace(",", ".")

        vuelos = []
        if fija_ida and fija_vuelta:
            total_fijo = fija_ida["offerDetails"]["fare"]["total"] + fija_vuelta["offerDetails"]["fare"]["total"]
            mensaje += (
                f"\n\n📅 *Combo para fechas fijas:*\n"
                f"{formatear(fija_ida, 'IDA')}\n"
                f"{formatear(fija_vuelta, 'VUELTA')}\n"
                f"🔢 *Total fijo:* ${total_fijo:,.0f}".replace(",", ".")
            )

            horaActual = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%dT%H:%M:%S")
            def crear_vuelo(oferta, tipo):
                seg = oferta["leg"]["segments"][0]
                return Vuelos(
                    DateTime=horaActual,
                    FechaSalida=oferta["departure"],
                    HoraSalida=seg["departure"].split("T")[1][:5],
                    HoraLlegada=seg["arrival"].split("T")[1][:5],
                    LugarSalida=seg["origin"],
                    LugarDestino=seg["destination"],
                    Precio1=oferta["offerDetails"]["fare"]["total"],
                    Precio2=0,
                    IdTrackRace=idTrackRace,
                    nombreUsuario=nombreUsuario,
                    TipoVuelo=tipo
                )

            vuelos.append(crear_vuelo(fija_ida, "IDA"))
            vuelos.append(crear_vuelo(fija_vuelta, "VUELTA"))

        else:
            mensaje += "\n\n❗ Alguna de las fechas fijas no tiene oferta disponible."

        return mensaje, vuelos
