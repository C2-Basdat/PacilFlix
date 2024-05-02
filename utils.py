import psycopg2

class DatabaseConnection:
    def __init__(self):
        self.dbname = 'railway'
        self.user = 'postgres'
        self.password = 'ANMavstJLrMuDfYHHAYWlbiJbJrYNkLh'
        self.host = 'monorail.proxy.rlwy.net'
        self.port = '39869'
        self.connection = None

        # Membuka koneksi saat objek dibuat
        self.connect()

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
        cursor = self.connection.cursor()
        cursor.execute("SET search_path TO sistel")
        cursor.execute(query)
        self.connection.commit()

        result = None
        if fetch:
            result = cursor.fetchall()

        cursor.close()

        return result

    def execute_sql_query_no_fetch(self, query):
        cursor = self.connection.cursor()
        cursor.execute("SET search_path TO sistel")
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
