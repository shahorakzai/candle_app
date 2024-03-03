import mysql.connector

class MySQLConnector:
    def __init__(self, host, port, username, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        )
        self.create_offsets_table()

    def create_offsets_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS algorithm_state (
                id INT AUTO_INCREMENT PRIMARY KEY,
                last_timestamp DATETIME NOT NULL
            )
        """)
        self.connection.commit()
        cursor.close()

    def get_offset(self):
        cursor = self.connection.cursor()
        sql = "SELECT last_timestamp FROM algorithm_state order by last_timestamp DESC limit 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def save_offset(self, stat):
        cursor = self.connection.cursor()
        sql = "INSERT INTO algorithm_state (last_timestamp) VALUES (%s)"
        cursor.execute(sql, (stat, ))
        self.connection.commit()
        cursor.close()
