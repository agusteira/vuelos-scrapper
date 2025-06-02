import sqlite3


class Vuelos:
    CONN = sqlite3.connect("vuelos.db")
    CURSOR = CONN.cursor()

    def __init__(self, DateTime, FechaSalida, HoraSalida, HoraLlegada,
                 LugarSalida, LugarDestino, Precio1, Precio2):
        self.DateTime = DateTime
        self.FechaSalida = FechaSalida
        self.HoraSalida = HoraSalida
        self.HoraLlegada = HoraLlegada
        self.LugarSalida = LugarSalida
        self.LugarDestino = LugarDestino
        self.Precio1 = Precio1
        self.Precio2 = Precio2

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
                precio2 REAL
            )
        """)
        cls.CONN.commit()

    def crear(self):
        self.CURSOR.execute(
            """
            INSERT INTO vuelos (
                datetime, fecha_salida, hora_salida, hora_llegada,
                lugar_salida, lugar_destino, precio1, precio2
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.DateTime, self.FechaSalida, self.HoraSalida,
                  self.HoraLlegada, self.LugarSalida, self.LugarDestino,
                  self.Precio1, self.Precio2))
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
