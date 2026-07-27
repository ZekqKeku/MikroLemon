import sqlite3
import os

class Database:
    def __init__(self, data_dir: str, db_name: str):
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.db_path = os.path.join(data_dir, db_name)
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS authorized_users (
                    user_id INTEGER PRIMARY KEY
                )
            """)
            conn.commit()

    def add_user(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR IGNORE INTO authorized_users (user_id) VALUES (?)", (user_id,))
            conn.commit()

    def remove_user(self, user_id: int) -> bool:
        if self.get_users_count() <= 1:
            return False # Cannot remove the last user
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM authorized_users WHERE user_id = ?", (user_id,))
            conn.commit()
        return True

    def is_authorized(self, user_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT 1 FROM authorized_users WHERE user_id = ?", (user_id,))
            return cur.fetchone() is not None

    def get_users_count(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT COUNT(*) FROM authorized_users")
            return cur.fetchone()[0]

    def get_all_users(self) -> list[int]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT user_id FROM authorized_users")
            return [row[0] for row in cur.fetchall()]
