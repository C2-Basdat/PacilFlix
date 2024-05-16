import psycopg2
from collections import namedtuple
from psycopg2 import Error
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self):
        self.dbname = 'railway'
        self.user = 'postgres'
        self.password = 'ANMavstJLrMuDfYHHAYWlbiJbJrYNkLh'
        self.host = 'monorail.proxy.rlwy.net'
        self.port = '39869'
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def map_cursor(self, cursor):
        desc = cursor.description
        nt_result = namedtuple("Result", [col[0] for col in desc])
        return [dict(row) for row in cursor.fetchall()]


    def query(self, query_str: str):
        self.connect()
        hasil = []
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SET SEARCH_PATH TO PACILFLIX")
            try:
                cursor.execute(query_str)

                if query_str.strip().upper().startswith("SELECT") or query_str.strip().upper().startswith("WITH"):
                    # Kalau ga error, return hasil SELECT
                    hasil = self.map_cursor(cursor)
                else:
                    # Kalau ga error, return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE
                    hasil = cursor.rowcount
                    self.connection.commit()
            except Exception as e:
                # Ga tau error apa
                hasil = e
        
        self.disconnect()
        return hasil