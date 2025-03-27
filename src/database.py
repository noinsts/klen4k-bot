import sqlite3
import re

class Database:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.add_default_logs()
        self.add_default_taxes()
        self.fix_null()

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

        self.conn.commit()

    def add_default_logs(self):
        self.cursor.executemany(
            """INSERT INTO show_logs (action, allow)
               VALUES (?, ?)
               ON CONFLICT(action) DO NOTHING""",
            [("voice_logs", 0), ("tax_logs", 0)]
        )

        self.conn.commit()

    def add_default_taxes(self):
        self.cursor.executemany(
            """INSERT INTO taxes (action, amount)
            VALUES (?, ?)
            ON CONFLICT(action) DO NOTHING""",
            [("join_voice", 0), ("send_message", 0)]

        )

        self.conn.commit()

    def fix_null(self):  # замінює значення 'null' в балансах на 0
        self.cursor.execute("""
            UPDATE balance
            SET balance = 0
            WHERE balance IS NULL;
        """)
        self.conn.commit()

    # Запити пов'язані з днями народження 🎂
    def add_birthday(self, user_id, birthday):
        self.cursor.execute("INSERT OR REPLACE INTO birthdays VALUES (?, ?)", (user_id, birthday))
        self.conn.commit()

    def update_birthday(self, user_id, birthday):
        self.cursor.execute("UPDATE birthdays SET birthday = ? WHERE user_id = ?", (birthday, user_id))
        self.conn.commit()

    def remove_birthday(self, user_id):
        self.cursor.execute("DELETE FROM birthdays WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def get_birthday(self, user_id):
        self.cursor.execute("SELECT birthday FROM birthdays WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def get_all_birthdays(self):
        self.cursor.execute("SELECT user_id, birthday FROM birthdays")
        return self.cursor.fetchall()

    def get_birthdays_by_date(self, month_day):
        self.cursor.execute("SELECT user_id FROM birthdays WHERE strftime('%m-%d', birthday) = ?", (month_day,))
        return self.cursor.fetchall()

    # Запити пов'язані з балансом 💸
    def update_balance(self, user_id, amount):
        self.cursor.execute("""
            INSERT INTO balance (user_id, balance) 
            VALUES (?, COALESCE(?, 0)) 
            ON CONFLICT(user_id) DO UPDATE 
            SET balance = COALESCE(balance, 0) + excluded.balance
        """, (user_id, amount))
        self.conn.commit()

    def get_balance(self, user_id):
        self.cursor.execute("SELECT balance FROM balance WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()

        if not result:
            self.cursor.execute("INSERT INTO balance (user_id, balance, privacy) VALUES (?, ?, ?)", (user_id, 0, 0))
            self.conn.commit()
            return 0

        return result[0]


    def set_taxes(self, action, amount):
        self.cursor.execute("""
            INSERT INTO taxes (action, amount)
            VALUES (?, ?)
            ON CONFLICT(action) DO UPDATE
            SET amount = excluded.amount
        """, (action, amount))
        self.conn.commit()

    def amount_tax(self, action):
        self.cursor.execute("SELECT amount FROM taxes WHERE action = ?", (action, ))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def balance_tier_list(self):
        self.cursor.execute("SELECT user_id, balance FROM balance WHERE privacy = ? ORDER BY balance DESC", (False, ))
        result = self.cursor.fetchall()
        return result
    
    def clear_balances(self):
        self.cursor.execute("DELETE FROM balance")
        self.conn.commit()
        self.cursor.execute("VACUUM")
        self.conn.commit()

    def set_balance_privacy(self, state, user_id):
        self.cursor.execute("""
            INSERT INTO balance (user_id, privacy) 
            VALUES (?, ?) 
            ON CONFLICT(user_id) DO UPDATE SET privacy = excluded.privacy
        """, (user_id, state))
        self.conn.commit()

    def get_balance_privacy(self, user_id):
        self.cursor.execute("SELECT privacy FROM balance WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()

        if not result:
            self.cursor.execute("INSERT INTO balance (user_id, balance, privacy) VALUES (?, ?, ?)", (user_id, 0, 0))
            self.conn.commit()
            return 0

        return result[0]

    # Запити пов'язані з логуванням 🗒️

    def set_log_visibility(self, action: str, allow: bool):
        self.cursor.execute("""
            INSERT INTO show_logs (action, allow)
            VALUES (?, ?)
            ON CONFLICT(action) DO UPDATE SET allow = excluded.allow
        """, (action, int(allow)))
        self.conn.commit()


    def is_log_allowed(self, action: str) -> bool:
        self.cursor.execute("SELECT allow FROM show_logs WHERE action = ?", (action,))
        row = self.cursor.fetchone()
        return row[0] == 1 if row else False


    def delete_log_action(self, action: str):
        self.cursor.execute("DELETE FROM show_logs WHERE action = ?", (action,))
        self.conn.commit()

    # Запити пов'язані з податками

    def get_taxes(self):
        self.cursor.execute("SELECT action, amount FROM taxes")
        result = self.cursor.fetchall()
        return result

    def get_tax_state(self):
        self.cursor.execute("SELECT enabled FROM taxes_state LIMIT 1")
        result = self.cursor.fetchone()

        if not result:
            self.cursor.execute("INSERT INTO taxes_state (enabled) VALUES (0)")
            self.conn.commit()
            return 0

        return result[0]

    def set_tax_state(self, state: int):
        self.cursor.execute("UPDATE taxes_state SET enabled = ? WHERE id = 1", (state,))
        self.conn.commit()

    # Запити пов'язані з локацією ☀️

    def add_location(self, user_id, city, country):
        self.cursor.execute("INSERT INTO locations (user_id, city, country) VALUES (?, ?, ?)", (user_id, city, country))
        self.conn.commit()

    def edit_location(self, user_id, city, country):
        self.cursor.execute("UPDATE locations SET city = ?, country = ? WHERE user_id = ?", (city, country, user_id))
        self.conn.commit()

    def delete_location(self, user_id):
        self.cursor.execute("DELETE FROM locations WHERE user_id = ?", (user_id, ))
        self.conn.commit()

    def get_city(self, user_id):
        self.cursor.execute("SELECT city FROM locations WHERE user_id = ?", (user_id, ))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_country(self, user_id):
        self.cursor.execute("SELECT country FROM locations WHERE user_id = ?", (user_id, ))
        result = self.cursor.fetchone()
        return result[0] if result else None

    # Запити пов'язані з персоналізованими погодними порадами 🔮               

    def add_advice(self, user_id, weather_type, activity):
        self.cursor.execute("INSERT INTO weather_preferences (user_id, weather_type, activity) VALUES (?, ?, ?)",
                            (user_id, weather_type, activity))
        self.conn.commit()

    def find_advice(self, user_id, weather):
        self.cursor.execute("SELECT activity FROM weather_preferences WHERE user_id = ? AND weather_type = ?", (user_id, weather))
        return self.cursor.fetchall()
    
    # Запити пов'язані з смартфонами 📱

    def add_phone(self, user_id, brand, model):
        self.cursor.execute("INSERT INTO phones (user_id, brand, model) VALUES (?, ?, ?)", (user_id, brand, model))
        self.conn.commit()

    def edit_phone(self, user_id, brand, model):
        self.cursor.execute("UPDATE phones SET brand = ?, model = ? WHERE user_id = ?", (brand, model, user_id))
        self.conn.commit()

    def delete_phone(self, user_id):
        self.cursor.execute("DELETE FROM phones WHERE user_id = ?", (user_id, ))
        self.conn.commit()

    def get_phone(self, user_id):
        self.cursor.execute("SELECT brand, model FROM phones WHERE user_id = ?", (user_id, ))
        result = self.cursor.fetchone()

        if result:
            return result
        else:
            return None
        
    # Запити пов'язані з кольорами 🎨

    def color_test(self, color):
        if color.startswith("#"):
            color = color[1:]

        if not re.match(r"^#?[0-9A-Fa-f]{6}$", color):
            return False
        
        return color

    def add_color(self, user_id, color): 
        color = self.color_test(color)
        if not color: return None
        
        self.cursor.execute("INSERT INTO colors (user_id, color) VALUES (?, ?)", (user_id, color))
        self.conn.commit()
        return True

    def edit_color(self, user_id, color):
        color = self.color_test(color)
        if not color: return None

        self.cursor.execute("UPDATE colors SET color = ? WHERE user_id = ?", (color, user_id))
        self.conn.commit()
        return True

    def delete_color(self, user_id):
        self.cursor.execute("DELETE FROM colors WHERE user_id = ?", (user_id, ))
        self.conn.commit()
        return True

    def get_color(self, user_id):
        self.cursor.execute("SELECT color FROM colors WHERE user_id = ?", (user_id, ))
        result = self.cursor.fetchone()
        return result[0] if result else None

    # Закриття бд

    def close(self):
        self.conn.close()
