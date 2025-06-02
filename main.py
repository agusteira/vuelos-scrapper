from VuelosObj import Vuelos
import time
from datetime import datetime
from zoneinfo import ZoneInfo
# Crear DB y tabla
Vuelos.crear_tabla()

# Insertar datos

while(True):
    ahora = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    formateado = ahora.strftime("%Y-%m-%dT%H:%M:%S")
    vuelo_obj = Vuelos(DateTime= ahora,
                                      FechaSalida="2025-07-01",
                                      HoraSalida="08:00",
                                      HoraLlegada="14:00",
                                      LugarSalida="Buenos Aires",
                                      LugarDestino="Miami",
                                      Precio1=105000.00,
                                      Precio2=125000.00)


# Consultar
    vuelo_obj.crear()
    Vuelos.leer_todo()
    time.sleep(100)
