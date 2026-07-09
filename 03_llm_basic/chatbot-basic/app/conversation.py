from database import Database

class Conversation:
    """
    대화 기록을 관리하는 클래스
    SQLite 기반 영구 저장
    """

    def __init__(self):

        self.database = Database()

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


    def get_messages(self, system_prompt: str):
        """
        OpenAI API 전달용 messages 반환
        """

        # OpenAI API에 전달할 messages에 system_prompt 조립
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(
            self.database.get_messages()
        )
        
        return messages
