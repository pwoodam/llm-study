class Conversation:
    """
    대화 기록을 관리하는 클래스
    """

    def __init__(self, system_prompt: str):
        self.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]


    def add_user_message(self, content: str):
        """
        사용자 메시지 추가
        """
        self.messages.append(
            {
                "role": "user",
                "content": content
            }
        )


    def add_assistant_message(self, content: str):
        """
        AI 응답 추가
        """
        self.messages.append(
            {
                "role": "assistant",
                "content": content
            }
        )


    def get_messages(self):
        """
        OpenAI API 전달용 messages 반환
        """
        return self.messages


    def clear(self):
        """
        대화 초기화
        """
        self.messages = []