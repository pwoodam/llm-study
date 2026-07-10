from database import Database

class Conversation:
    """
    대화 기록을 관리하는 클래스
    SQLite 기반 영구 저장
    """

    def __init__(
        self,
        session_id: int | None = None
    ):

        self.database = Database()

        if session_id is None:
            # session_id가 주어지지 않으면 새 세션 생성
            self.session_id = self.database.create_session()

        elif not self.database.session_exists(session_id):
            raise ValueError(
                f"Session ID {session_id} does not exist."
            )
        
        else:
            # 기존 session_id가 주어지면 해당 세션 사용
            self.session_id = session_id    
        
    def add_message(
        self,
        role: str,
        content: str
    ):
        """
        대화 내용 추가
        """
        self.database.save_message(
            self.session_id,
            role,
            content
        )

    def get_messages(self) -> list[dict[str, str]]:
        """
        OpenAI API 전달용 messages 반환
        """

        return self.database.get_messages(self.session_id)