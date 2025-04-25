import sqlite3


class Schema:
    def __init__(self, cursor):
        self.cursor = cursor


    def create_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS birthdays (
                user_id INTEGER PRIMARY KEY, 
                birthday TEXT
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS balance (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                privacy INTEGER DEFAULT 0 
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS taxes (
                action TEXT PRIMARY KEY,
                amount INTEGER DEFAULT 0
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS show_logs(
                action TEXT UNIQUE,
                allow INTEGER DEFAULT 0
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS taxes_state(
                id INTEGER PRIMARY KEY CHECK (id = 1), -- Єдиний запис у таблиці
                enabled INTEGER NOT NULL CHECK (enabled IN (0, 1))
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS locations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS weather_preferences(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                weather_type TEXT CHECK (weather_type IN ('positive', 'negative')),
                activity TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES locations(user_id) ON DELETE CASCADE
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS phones(
                user_id INTEGER PRIMARY KEY, 
                brand TEXT NOT NULL,
                model TEXT NOT NULL
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS colors(
                user_id INTEGER PRIMARY KEY, 
                color TEXT NOT NULL
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS auction(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL
            )"""
        )
