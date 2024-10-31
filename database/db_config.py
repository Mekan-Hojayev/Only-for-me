import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='servers.db'):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS server_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    content TEXT,
                    created_at TIMESTAMP
                )
            ''')
            conn.commit()

    def save_server_data(self, filename, content):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO server_logs (filename, content, created_at) VALUES (?, ?, ?)',
                (filename, content, datetime.now())
            )
            conn.commit()
