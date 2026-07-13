from client import client
from config import OPENAI_MODEL, MAX_CONVERSATION_MESSAGES
from conversation import Conversation


class Chatbot:
    """
    대화형 LLM Chatbot 관리 클래스
    """
    
    def __init__(
        self,
        system_prompt: str
    ):

        self.system_prompt = system_prompt

        self.conversation = Conversation()


    def chat_stream(self, user_message: str):
        """
        사용자 입력을 받아
        LLM 응답 반환
        """

        # 1. 사용자 메시지 추가
        self.conversation.add_message(
            role="user",
            content=user_message
        )

        # 2. OpenAI API 호출 - 스트리밍 모드
        
        # OpenAI API에 전달할 messages에 system_prompt 조립
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        conversation_history = self.conversation.get_messages(
            limit=MAX_CONVERSATION_MESSAGES
        )

        messages.extend(conversation_history)

        stream = client.responses.create(
            model=OPENAI_MODEL,
            input=messages,
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
        self.conversation.add_message(
            role="assistant",
            content=full_response
        )
