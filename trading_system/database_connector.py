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
            CREATE TABLE IF NOT EXISTS offsets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                topic VARCHAR(255) NOT NULL,
                partition INT NOT NULL,
                offset BIGINT NOT NULL
            )
        """)
        self.connection.commit()
        cursor.close()

    def get_offset(self, topic, partition):
        cursor = self.connection.cursor()
        sql = "SELECT offset FROM offsets WHERE topic = %s AND partition = %s"
        cursor.execute(sql, (topic, partition))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def save_offset(self, topic, partition, offset):
        cursor = self.connection.cursor()
        sql = "INSERT INTO offsets (topic, partition, offset) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE offset = %s"
        cursor.execute(sql, (topic, partition, offset, offset))
        self.connection.commit()
        cursor.close()
