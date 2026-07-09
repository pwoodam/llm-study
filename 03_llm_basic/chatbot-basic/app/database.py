import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        db_path = (
            Path(__file__).parent.parent
            / "data"
            / "chatbot.db"
        )

        db_path.parent.mkdir(
            exist_ok=True
        )

        self.conn = sqlite3.connect(
            db_path
        )

        self.create_table()


    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.conn.commit()


    def save_message(
        self,
        role: str,
        content: str
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages (
                role,
                content
            )
            VALUES (?, ?)
            """,
            (
                role,
                content
            )
        )

        self.conn.commit()


    def get_messages(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT role, content
            FROM messages
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "role": role,
                "content": content
            }
            for role, content in rows
        ]