class AuctionModel:
    def __init__(self, db_connection):
        self.conn = db_connection.conn
        self.cursor = db_connection.cursor

    def add_auc_item(self, user_id, name):
        self.cursor.execute("INSERT INTO auction (user_id, name) VALUES (?, ?)", (user_id, name))
        self.conn.commit()

    def get_auction_id(self, user_id, name):
        self.cursor.execute("SELECT id FROM auction WHERE user_id = ? AND name = ?", (user_id, name))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def auc_list(self):
        self.cursor.execute("SELECT * FROM auction")
        result = self.cursor.fetchall()
        return result

    def user_auc_list(self, user_id):
        self.cursor.execute("SELECT id, name FROM auction WHERE user_id = ?", (user_id, ))
        return self.cursor.fetchall()


    def delete_auc(self, id_id, user_id) -> bool:
        self.cursor.execute("DELETE FROM auction WHERE id = ? AND user_id = ?", (id_id, user_id))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False
