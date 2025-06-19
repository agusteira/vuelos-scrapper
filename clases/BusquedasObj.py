import sqlite3
from variables import *
from telebot import telebot

class Busquedas:
    CONN = sqlite3.connect("busquedas.db")
    CURSOR = CONN.cursor()

    def __init__(self, DateTime, IdChatTelegram, AepIda, AepVuelta, FechaIda, FechaVuelta, Active=True, id=None):
        self.DateTime = DateTime
        self.IdChatTelegram = IdChatTelegram
        self.AepIda = AepIda
        self.AepVuelta = AepVuelta
        self.FechaIda = FechaIda
        self.FechaVuelta = FechaVuelta
        self.Active = Active
        self.id=id

    @classmethod
    def crear_tabla(cls):
        cls.CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS busquedas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime DATETIME,
                id_chat_telegram TEXT,
                aep_ida TEXT,
                aep_vuelta TEXT,
                fecha_ida TEXT,
                fecha_vuelta TEXT,
                active BOOLEAN DEFAULT 1
            )
        """)
        cls.CONN.commit()

    def crear(self):
        self.CURSOR.execute("""
            INSERT INTO busquedas (
                datetime, id_chat_telegram, aep_ida, aep_vuelta,
                fecha_ida, fecha_vuelta, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.DateTime, self.IdChatTelegram, self.AepIda, self.AepVuelta,
            self.FechaIda, self.FechaVuelta, int(self.Active)
        ))
        self.CONN.commit()

    def leer(self):
        self.CURSOR.execute("SELECT * FROM busquedas ORDER BY datetime DESC")
        vuelo = self.CURSOR.fetchone()
        return vuelo

    @staticmethod
    def leer_todo():
        Busquedas.CURSOR.execute("SELECT * FROM busquedas ORDER BY datetime DESC")
        for row in Busquedas.CURSOR.fetchall():
            print(row)

    @staticmethod
    def traer_todo():
        Busquedas.CURSOR.execute("SELECT * FROM busquedas ORDER BY datetime DESC")
        filas = Busquedas.CURSOR.fetchall()
        objetos = []
        for fila in filas:
            # fila = (id, datetime, id_chat_telegram, aep_ida, aep_vuelta, fecha_ida, fecha_vuelta, active)
            obj = Busquedas(
                DateTime=fila[1],
                IdChatTelegram=fila[2],
                AepIda=fila[3],
                AepVuelta=fila[4],
                FechaIda=fila[5],
                FechaVuelta=fila[6],
                Active=bool(fila[7]), 
                id= int(fila[0])  # Asignar el id de la fila
            )
            obj.id = int(fila[0])
            objetos.append(obj)
        return objetos


    def eliminar(self):
        self.CURSOR.execute(
            """
            UPDATE busquedas SET active = 0 where id = ?
            """, (self.id,))
        self.CONN.commit()

