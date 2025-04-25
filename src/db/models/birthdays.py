class BirthdayModel:
    def __init__(self, db_connection):
        self.conn = db_connection.conn
        self.cursor = db_connection.cursor

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
