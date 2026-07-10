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

        # 존재하지 않는 세션에 저장하려할 때 오류 발생시키기 위해 foreign key 제약 조건 활성화
        self.conn.execute(
            "PRAGMA foreign_keys = ON"
                )

        self.create_table_sessions()
        self.create_table()


    def create_table_sessions(self):
        
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.conn.commit()


    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
            """
        )

        self.conn.commit()

        
    
    def create_session(self) -> int:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO sessions DEFAULT VALUES
            """
        )

        self.conn.commit()

        # 방금 생성된 id를 가져오기 위해 lastrowid를 반환
        return cursor.lastrowid

    def session_exists(
        self,
        session_id: int
    ) -> bool:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM sessions
            WHERE id = ?
            """,
            (session_id,)
        )

        return cursor.fetchone() is not None

    def save_message(
        self,
        session_id: int,
        role: str,
        content: str
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages (
                session_id,
                role,
                content
            )
            VALUES (?, ?, ?)
            """,
            (
                session_id,
                role,
                content
            )
        )

        self.conn.commit()


    def get_messages(
        self, 
        session_id: int
    ) -> list[dict[str, str]]:

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT role, content
            FROM messages
            WHERE session_id = ?
            ORDER BY id
            """,
            (session_id,)
        )

        rows = cursor.fetchall()

        return [
            {
                "role": role,
                "content": content
            }
            for role, content in rows
        ]