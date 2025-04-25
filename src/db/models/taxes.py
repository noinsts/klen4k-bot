class TaxModel:
    def __init__(self, db_connection):
        self.conn = db_connection.conn
        self.cursor = db_connection.cursor

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

    def set_taxes(self, action, amount):
        self.cursor.execute("""
            INSERT INTO taxes (action, amount)
            VALUES (?, ?)
            ON CONFLICT(action) DO UPDATE
            SET amount = excluded.amount
        """, (action, amount))
        self.conn.commit()
