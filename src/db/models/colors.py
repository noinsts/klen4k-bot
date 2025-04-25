from src.utils.color_checker import color_test

class ColorModel:
    def __init__(self, db_connection):
        self.conn = db_connection.conn
        self.cursor = db_connection.cursor

    def add_color(self, user_id, color):
        color = color_test(color)
        if not color: return None

        self.cursor.execute("INSERT INTO colors (user_id, color) VALUES (?, ?)", (user_id, color))
        self.conn.commit()
        return True

    def edit_color(self, user_id, color):
        color = color_test(color)
        if not color: return None

        self.cursor.execute("UPDATE colors SET color = ? WHERE user_id = ?", (color, user_id))
        self.conn.commit()
        return True

    def delete_color(self, user_id):
        self.cursor.execute("DELETE FROM colors WHERE user_id = ?", (user_id,))
        self.conn.commit()
        return True

    def get_color(self, user_id):
        self.cursor.execute("SELECT color FROM colors WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None