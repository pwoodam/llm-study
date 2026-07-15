from openai import APIError

from client import client
from config import OPENAI_MODEL, MAX_CONTEXT_TOKENS, OUTPUT_TOKEN_RESERVE, SUMMARY_TRIGGER_TOKENS, SUMMARY_MAX_OUTPUT_TOKENS
from conversation import Conversation
from tokenizer import Tokenizer


class Chatbot:
    """
    대화형 LLM Chatbot 관리 클래스
    """
    
    def __init__(
        self,
        system_prompt: str,
        summary_prompt: str
    ):

        self.system_prompt = system_prompt
        self.summary_prompt = summary_prompt

        self.tokenizer = Tokenizer()

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

        system_prompt_tokens = self.tokenizer.count_tokens(
            self.system_prompt
        )

        summary = self.conversation.get_summary()

        summary_context = f"""
        이전 대화 요약:
        {summary}
        """

        summary_prompt_tokens = 0

        if summary:
            summary_prompt_tokens = self.tokenizer.count_tokens(summary_context)

        available_tokens = max(
            0,
            MAX_CONTEXT_TOKENS
            - system_prompt_tokens
            - OUTPUT_TOKEN_RESERVE # 응답 생성을 위한 Output Token 공간을 미리 확보
            - summary_prompt_tokens
        )
        
        # OpenAI API에 전달할 messages에 system_prompt 조립
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        if summary:
            messages.append(
                {
                    "role": "system",
                    "content": summary_context
                }
            )

        conversation_history = self.conversation.get_context_messages(
            max_tokens=available_tokens
        )

        messages.extend(conversation_history)

        full_response = ""

        try:
            stream = client.responses.create(
                model=OPENAI_MODEL,
                input=messages,
                stream=True
            )

            for event in stream:

                if event.type == "response.output_text.delta":

                    # API 응답 구조 변경에 따라 event.delta가 None일 수 있으므로 체크 필요
                    if event.delta:
                        full_response += event.delta
                        yield event.delta

        except APIError as e:
            print(f"[Chatbot] OpenAI API 호출 중 오류 발생: {e}")
            yield "\n[오류: 응답을 생성하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.]"
            # 응답이 불완전하므로 저장하지 않고 종료
            return

        # 3. AI 응답 저장 (스트리밍이 정상적으로 끝난 경우에만)
        if full_response:
            self.conversation.add_message(
                role="assistant",
                content=full_response
            )

        # 4. 대화 요약이 필요한지 확인하고 필요하면 요약 생성
        # 요약 실패가 대화 자체를 중단시키지 않도록 별도로 감싼다
        try:
            if self.should_summarize():
                print("SUMMARY 실행")
                self.summarize_conversation()
        except APIError as e:
            print(f"[Chatbot] 대화 요약 중 오류 발생 (다음 턴에 재시도됩니다): {e}")
    
    def summarize_conversation(self):
        """
        대화 요약 생성
        """

        # OpenAI API 호출 - 요약 생성
        messages = [
            {
                "role": "system",
                "content": self.summary_prompt
            }
        ]

        previous_summary = self.conversation.get_summary()

        if self.conversation.get_summary():
            messages.append(
                {
                    "role": "system",
                    "content": f"""
                    이전 대화 요약:
                    {previous_summary}
                    """
                }
            )

        conversation_history = self.conversation.get_unsummarized_messages()

        messages.extend(conversation_history)

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=messages,
            max_output_tokens=SUMMARY_MAX_OUTPUT_TOKENS
        )

        summary = response.output_text

        # 요약 저장
        self.conversation.save_summary(summary)

    def should_summarize(self) -> bool:
        """
        Conversation Summary 생성 필요 여부 판단
        """

        # 메시지가 누적되면 한 번씩 요약하도록 요약되지 않은 메시지만 불러옴
        messages = self.conversation.get_unsummarized_messages()

        total_tokens = 0

        for message in messages:
            total_tokens += self.tokenizer.count_tokens(
                message["content"]
            )
            if total_tokens > SUMMARY_TRIGGER_TOKENS:
                break

        return total_tokens > SUMMARY_TRIGGER_TOKENS