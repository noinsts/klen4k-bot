class LocationModel:
    def __init__(self, db_connection):
        self.conn = db_connection.conn
        self.cursor = db_connection.cursor

    def add_location(self, user_id, city, country):
        self.cursor.execute("INSERT INTO locations (user_id, city, country) VALUES (?, ?, ?)", (user_id, city, country))
        self.conn.commit()

    def edit_location(self, user_id, city, country):
        self.cursor.execute("UPDATE locations SET city = ?, country = ? WHERE user_id = ?", (city, country, user_id))
        self.conn.commit()

    def delete_location(self, user_id):
        self.cursor.execute("DELETE FROM locations WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def get_city(self, user_id):
        self.cursor.execute("SELECT city FROM locations WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_country(self, user_id):
        self.cursor.execute("SELECT country FROM locations WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
