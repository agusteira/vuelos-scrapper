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
            fechaVuelosIda = vueloIda.find_all("span", class_="styled__FlightDate-sc-1aqn55i-7 fYVZMx header-date")[0].get_text(strip=True)
            vuelos =  vueloIda.find_all("div", class_="FlightOfferCard__CardWrapper-sc-122jx93-0 jyaLjo")
            for vuelo in vuelos:
                vuelo_obj = Vuelos(DateTime= horaActual,
                                  FechaSalida= fechaVuelosIda,
                                  HoraSalida= vuelo.find_all("div", class_= NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["HORARIOS"])[0].get_text(strip=True),
                                  HoraLlegada= vuelo.find_all("div", class_=NOMBRES_DE_CLASES_AEROLINEAS_ARGENTINAS["HORARIOS"])[1].get_text(strip=True),
                                  LugarSalida= vuelo.find_all("label", class_="styled__Airport-sc-sbx95d-9 styled__ExtendedAirport-sc-19e0rpm-10 bgThxl gvxCKn label-airport")[0].get_text(strip=True),
                                  LugarDestino= vuelo.find_all("label", class_="styled__Airport-sc-sbx95d-9 styled__ExtendedAirport-sc-19e0rpm-10 bgThxl gvxCKn label-airport")[1].get_text(strip=True),
                                  Precio1= vuelo.find_all("label", class_="styled__Fare-sc-l1i8es-3 hGtoJE label-fare")[0].get_text(strip=True),
                                  Precio2= vuelo.find_all("label", class_="styled__Fare-sc-l1i8es-3 hGtoJE label-fare")[1].get_text(strip=True),
                                  IdTrackRace= id_unico,
                                  nombreUsuario= None,
                                  TipoVuelo= "Ida"
                                  )
                vuelo_obj.crear()
                listaVuelos.append(vuelo_obj)
        
        if vueloVuelta:
            fechaVuelosVuelta = vueloVuelta.find_all("span", class_="styled__FlightDate-sc-1aqn55i-7 fYVZMx header-date")[0].get_text(strip=True)
            vuelos =  vueloVuelta.find_all("div", class_="FlightOfferCard__CardWrapper-sc-122jx93-0 jyaLjo")
            for vuelo in vuelos:
                vuelo_obj = Vuelos(DateTime= horaActual,
                                  FechaSalida= fechaVuelosVuelta,
                                  HoraSalida= vuelo.find_all("div", class_="styled__DateWrapper-sc-19e0rpm-5 hibji")[0].get_text(strip=True),
                                  HoraLlegada= vuelo.find_all("div", class_="styled__DateWrapper-sc-19e0rpm-5 hibji")[1].get_text(strip=True),
                                  LugarSalida= vuelo.find_all("label", class_="styled__Airport-sc-sbx95d-9 styled__ExtendedAirport-sc-19e0rpm-10 bgThxl gvxCKn label-airport")[0].get_text(strip=True),
                                  LugarDestino= vuelo.find_all("label", class_="styled__Airport-sc-sbx95d-9 styled__ExtendedAirport-sc-19e0rpm-10 bgThxl gvxCKn label-airport")[1].get_text(strip=True),
                                  Precio1= vuelo.find_all("label", class_="styled__Fare-sc-l1i8es-3 hGtoJE label-fare")[0].get_text(strip=True),
                                  Precio2= vuelo.find_all("label", class_="styled__Fare-sc-l1i8es-3 hGtoJE label-fare")[1].get_text(strip=True),
                                  IdTrackRace= id_unico,
                                  nombreUsuario= None,
                                  TipoVuelo= "Vuelta"
                                  )
                vuelo_obj.crear()
                listaVuelos.append(vuelo_obj)
