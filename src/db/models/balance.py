class BalanceModel:
    def __init__(self, db_connection):
        self.conn = db_connection.conn
        self.cursor = db_connection.cursor

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

    def amount_tax(self, action):
        self.cursor.execute("SELECT amount FROM taxes WHERE action = ?", (action,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def balance_tier_list(self):
        self.cursor.execute("SELECT user_id, balance FROM balance WHERE privacy = ? ORDER BY balance DESC", (False,))
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