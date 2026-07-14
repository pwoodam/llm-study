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
        self.create_conversation_summary_table()


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
    
    def create_conversation_summary_table(self):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL UNIQUE,
                summary TEXT NOT NULL,
                last_message_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
            """
        )

        self.conn.commit()

    def save_summary(
        self,
        session_id: int,
        summary: str,
        last_message_id: int
    ):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            UPDATE conversation_summaries
            SET summary = ?,
                last_message_id = ?,
                created_at = CURRENT_TIMESTAMP
            WHERE session_id = ?
            """,
            (
                summary,
                last_message_id,
                session_id
            )
        )

        # UPDATE 실행한 뒤 변경된 행이 없으면 해당 session_id에 대한 요약이 존재하지 않으므로 새로 삽입
        if cursor.rowcount == 0:
            cursor.execute(
                """
                INSERT INTO conversation_summaries (
                    session_id,
                    summary,
                    last_message_id
                )
                VALUES (?, ?, ?)
                """,
                (
                    session_id,
                    summary,
                    last_message_id
                )
            )

        self.conn.commit()

    def get_summary(
        self,
        session_id: int
    ) -> str | None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT summary
            FROM conversation_summaries
            WHERE session_id = ?
            """,
            (session_id,)
        )

        # 각 session_id에 대한 요약은 하나만 존재하므로 LIMIT 1을 사용하지 않아도 됨.
        # 그것과는 별개로 cursor.execute(...)은 [(summary,)] 형태로 결과를 반환하기 때문에 fetchone()을 사용하여 첫 번째 결과(문자열)만 가져옴
        row = cursor.fetchone()

        return row[0] if row else None
    
    def get_last_message_id(
        self,
        session_id: int
    ) -> int | None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM messages
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (session_id,)
        )

        row = cursor.fetchone()

        return row[0] if row else None

    def get_last_summarized_message_id(
        self,
        session_id: int
    ) -> int | None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT last_message_id
            FROM conversation_summaries
            WHERE session_id = ?
            """,
            (session_id,)
        )

        row = cursor.fetchone()

        return row[0] if row else None
    
    def get_unsummarized_messages(
        self,
        session_id: int
    ) -> list[dict[str, str]]:
        cursor = self.conn.cursor()

        # 마지막으로 요약에 포함된 Message 이후의 대화 조회
        last_summarized_message_id = self.get_last_summarized_message_id(
            session_id
        )

        # last_summarized_message_id가 None이면 요약이 존재하지 않으므로 모든 메시지를 가져옴
        if last_summarized_message_id is None:
            cursor.execute(
                """
                SELECT role, content
                FROM messages
                WHERE session_id = ?
                ORDER BY id
                """,
                (session_id,)
            )
        else:
            cursor.execute(
                """
                SELECT role, content
                FROM messages
                WHERE session_id = ? AND id > ?
                ORDER BY id
                """,
                (session_id, last_summarized_message_id)
            )

        rows = cursor.fetchall()

        return [
            {
                "role": role,
                "content": content
            }
            for role, content in rows
        ]