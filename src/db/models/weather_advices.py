class WeatherAdviceModel:
    def __init__(self, db_connection):
        self.conn = db_connection.conn
        self.cursor = db_connection.cursor

    def add_advice(self, user_id, weather_type, activity):
        self.cursor.execute("INSERT INTO weather_preferences (user_id, weather_type, activity) VALUES (?, ?, ?)",
                            (user_id, weather_type, activity))
        self.conn.commit()

    def find_advice(self, user_id, weather):
        self.cursor.execute("SELECT activity FROM weather_preferences WHERE user_id = ? AND weather_type = ?", (user_id, weather))
        return self.cursor.fetchall()
