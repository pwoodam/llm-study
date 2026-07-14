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

    def get_context_messages(
        self,
        max_tokens: int
    ) -> list[dict[str, str]]:
        """
        Token 제한 내에서 OpenAI API 전달용 Context Message 반환
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
    
    def get_summary(self) -> str | None:
        """
        대화 요약 반환
        """

        return self.database.get_summary(
            self.session_id
        )
    
    def save_summary(
        self,
        summary: str
    ):
        """
        대화 요약 저장
        """

        # 마지막으로 DB에 저장된 Message의 id 조회 -> conversation_summaries 테이블의 last_message_id 업데이트 
        last_message_id = self.database.get_last_message_id(
            self.session_id
        )

        self.database.save_summary(
            self.session_id,
            summary,
            last_message_id
        )

    def get_all_messages(
        self
    ) -> list[dict[str,str]]:

        return self.database.get_messages(
            self.session_id
        )
    
    def get_unsummarized_messages(self) -> list[dict[str,str]]:
        """
        요약 이후의 최근 대화 내용 반환
        """

        return self.database.get_unsummarized_messages(
            self.session_id
        )