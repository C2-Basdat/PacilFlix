import psycopg2

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

    def execute_sql_query(self, query, fetch=True):
        # Membuka koneksi saat objek dibuat
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SET search_path TO pacilflix")
        cursor.execute(query)
        self.connection.commit()

        result = None
        if fetch:
            result = cursor.fetchall()

        cursor.close()

        self.disconnect()

        return result

    def execute_sql_query_no_fetch(self, query):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SET search_path TO pacilflix")
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        self.disconnect()
