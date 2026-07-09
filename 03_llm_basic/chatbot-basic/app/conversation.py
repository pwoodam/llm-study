from database import Database

class Conversation:
    """
    대화 기록을 관리하는 클래스
    SQLite 기반 영구 저장
    """

    def __init__(self, system_prompt: str):

        self.database = Database()

        messages = self.database.get_messages()

        # 최초 실행 시 system prompt 저장
        if not messages:
            self.database.save_message(
                "system",
                system_prompt
            )

    def add_user_message(self, content: str):
        """
        사용자 메시지 추가
        """
        self.database.save_message(
            "user",
            content
        )


    def add_assistant_message(self, content: str):
        """
        AI 응답 추가
        """
        self.database.save_message(
            "assistant",
            content
        )


    def get_messages(self):
        """
        OpenAI API 전달용 messages 반환
        """
        return self.database.get_messages()
