class LogsModel:
    def __init__(self, db_connection):
        self.conn = db_connection.conn
        self.cursor = db_connection.cursor

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
