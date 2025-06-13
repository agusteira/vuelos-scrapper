import sqlite3
from variables import *
from telebot import telebot

class Vuelos:
    CONN = sqlite3.connect("vuelos.db")
    CURSOR = CONN.cursor()

    def __init__(self, DateTime, FechaSalida, HoraSalida, HoraLlegada,
                 LugarSalida, LugarDestino, Precio1, Precio2,
                 IdTrackRace, nombreUsuario, TipoVuelo):
        self.DateTime = DateTime
        self.FechaSalida = FechaSalida
        self.HoraSalida = HoraSalida
        self.HoraLlegada = HoraLlegada
        self.LugarSalida = LugarSalida
        self.LugarDestino = LugarDestino
        self.Precio1 = Precio1
        self.Precio2 = Precio2
        self.IdTrackRace = IdTrackRace
        self.nombreUsuario = nombreUsuario
        self.TipoVuelo = TipoVuelo

    @classmethod
    def crear_tabla(cls):
        cls.CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS vuelos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime DATETIME,
                fecha_salida TEXT,
                hora_salida TEXT,
                hora_llegada TEXT,
                lugar_salida TEXT,
                lugar_destino TEXT,
                precio1 REAL,
                precio2 REAL,
                id_track_race TEXT,
                nombre_usuario TEXT,
                tipo_vuelo TEXT
            )
        """)
        cls.CONN.commit()

    def crear(self):
        self.CURSOR.execute(
            """
            INSERT INTO vuelos (
                datetime, fecha_salida, hora_salida, hora_llegada,
                lugar_salida, lugar_destino, precio1, precio2,
                id_track_race, nombre_usuario, tipo_vuelo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.DateTime, self.FechaSalida, self.HoraSalida,
                  self.HoraLlegada, self.LugarSalida, self.LugarDestino,
                  self.Precio1, self.Precio2,
                  self.IdTrackRace, self.nombreUsuario, self.TipoVuelo))
        self.CONN.commit()

    def leer(self):
        self.CURSOR.execute("SELECT * FROM vuelos ORDER BY datetime DESC")
        vuelo = self.CURSOR.fetchone()
        return vuelo

    @staticmethod
    def leer_todo():
        Vuelos.CURSOR.execute("SELECT * FROM vuelos ORDER BY datetime DESC")
        for row in Vuelos.CURSOR.fetchall():
            print(row)

    def actualizar(self, nuevo_precio1=None, nuevo_precio2=None):
        if nuevo_precio1 is not None:
            self.Precio1 = nuevo_precio1
        if nuevo_precio2 is not None:
            self.Precio2 = nuevo_precio2

        self.CURSOR.execute(
            """
            UPDATE vuelos SET precio1 = ?, precio2 = ? WHERE datetime = ?
            """, (self.Precio1, self.Precio2, self.DateTime))
        self.CONN.commit()

    def eliminar(self):
        self.CURSOR.execute("DELETE FROM vuelos WHERE datetime = ?",
                            (self.DateTime, ))
        self.CONN.commit()

    @classmethod
    def mostrar_vuelo(self, titulo, vuelo):
        bot = telebot.TeleBot(TOKEN_BOT)
        mensaje = (
            "-" * 40 + "\n"
            f"\n{titulo}\n"
            f"Fecha: {vuelo.FechaSalida}\n"
            f"Hora de Salida: {vuelo.HoraSalida}\n"
            f"Hora de Llegada: {vuelo.HoraLlegada}\n"
            f"Lugar de Salida: {vuelo.LugarSalida}\n"
            f"Lugar de Destino: {vuelo.LugarDestino}\n"
            f"Precio 1: ${float(vuelo.Precio1):.3f}\n"
            f"Precio 2: ${float(vuelo.Precio2):.3f}\n"
            + "-" * 40
        )
        print(mensaje)
        bot.send_message(CHAT_ID, mensaje)
              


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
        print(f"\nPrecio paquete para ese dia ida y vuelta: ${total:.3f}")

        bot = telebot.TeleBot(TOKEN_BOT)
        bot.send_message(CHAT_ID, f"\nPrecio paquete para ese dia ida y vuelta: ${total:.3f}")
        return comboVuelosBaratos
