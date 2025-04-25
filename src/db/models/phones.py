class PhoneModel:
    def __init__(self, db_connection):
        self.conn = db_connection.conn
        self.cursor = db_connection.cursor

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

        return result if result else None
