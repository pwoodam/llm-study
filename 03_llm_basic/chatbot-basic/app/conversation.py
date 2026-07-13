from database import Database

from tokenizer import Tokenizer

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
        self.tokenizer = Tokenizer()

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

    def get_messages(
        self,
        max_tokens: int
    ) -> list[dict[str, str]]:
        """
        Token 제한 기반 Message 반환
        """

        messages = self.database.get_messages(
            self.session_id
        )

        selected_messages = []

        total_tokens = 0

        # 최신 Message부터 확인
        for message in reversed(messages):

            message_tokens = self.tokenizer.count_tokens(
                message["content"]
            )


            if total_tokens + message_tokens > max_tokens:
                break


            selected_messages.insert(
                0, # 순서를 유지하기 위해 맨 앞에 삽입
                message
            )

            total_tokens += message_tokens


        return selected_messages