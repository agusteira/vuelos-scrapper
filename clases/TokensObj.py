import sqlite3
from variables import *

class Tokens:
    CONN = sqlite3.connect("tokens.db")
    CURSOR = CONN.cursor()

    def __init__(self, DateTime, Token, FechaExpiracion, Aerolinea):
        self.DateTime = DateTime
        self.Token = Token
        self.FechaExpiracion = FechaExpiracion
        self.Aerolinea = Aerolinea

    @classmethod
    def crear_tabla(cls):
        cls.CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS vuelos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime DATETIME,
                token TEXT,
                fecha_expiracion TEXT,
                aerolinea TEXT
            )
        """)
        cls.CONN.commit()

    def crear(self):
        try:
            self.CURSOR.execute(
                """
                INSERT INTO vuelos (
                    datetime, token, fecha_expiracion, aerolinea
                ) VALUES (?, ?, ?, ?)
                """, (self.DateTime, self.Token, self.FechaExpiracion, self.Aerolinea)
            )
            self.CONN.commit()
        except sqlite3.Error as e:
            print(f"Error al insertar el token: {e}")

    @classmethod
    def leer(cls, aerolinea):
        cls.CURSOR.execute(
            "SELECT * FROM vuelos WHERE aerolinea = ? ORDER BY datetime DESC LIMIT 1",
            (aerolinea,)
        )
        fila = cls.CURSOR.fetchone()
        
        if fila:
            # fila[1] = datetime, fila[2] = token, fila[3] = fecha_expiracion, fila[4] = aerolinea
            return Tokens(fila[1], fila[2], fila[3], fila[4])
        else:
            return None