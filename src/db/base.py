import os
import sqlite3

from src.db.schema import Schema


class DatabaseConnection:
    """Базовий клас для роботи з підключенням до бази даних"""

    def __init__(self, db_name="database.db"):
        db_path = os.path.join(os.path.dirname(__file__), "..", "..", "db", db_name)
        self.db_name = os.path.abspath(db_path)
        self.conn = sqlite3.connect(self.db_name)

        self.cursor = self.conn.cursor()

        # Ініціалізація бази даних
        Schema(self.cursor).create_tables()
        self.conn.commit()

    def close(self):
        """Закриття з'єднання з базою даних"""
        self.conn.close()
