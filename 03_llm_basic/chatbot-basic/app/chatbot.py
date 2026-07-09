from client import client
from config import OPENAI_MODEL
from conversation import Conversation


class Chatbot:
    """
    대화형 LLM Chatbot 관리 클래스
    """

    def __init__(self, system_prompt: str):
        self.conversation = Conversation(
            system_prompt
        )


    def chat(self, user_message: str):
        """
        사용자 입력을 받아
        LLM 응답 반환
        """

        # 1. 사용자 메시지 추가
        self.conversation.add_user_message(
            user_message
        )


        # 2. OpenAI API 호출
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=self.conversation.get_messages()
        )


        # 3. 응답 추출
        assistant_message = response.output_text


        # 4. AI 응답 저장
        self.conversation.add_assistant_message(
            assistant_message
        )


        return assistant_message