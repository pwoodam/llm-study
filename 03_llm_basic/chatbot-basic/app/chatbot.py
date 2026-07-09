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


    def chat_stream(self, user_message: str):
        """
        사용자 입력을 받아
        LLM 응답 반환
        """

        # 1. 사용자 메시지 추가
        self.conversation.add_user_message(
            user_message
        )

        # 2. OpenAI API 호출 - 스트리밍 모드
        stream = client.responses.create(
            model=OPENAI_MODEL,
            input=self.conversation.get_messages(),
            stream=True
        )

        full_response = ""


        for event in stream:

            if event.type == "response.output_text.delta":

                # API 응답 구조 변경에 따라 event.delta가 None일 수 있으므로 체크 필요
                if event.delta:
                    full_response += event.delta
                    yield event.delta


        # 3. AI 응답 저장
        self.conversation.add_assistant_message(
            full_response
        )