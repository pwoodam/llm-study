import tiktoken

from config import OPENAI_MODEL


class Tokenizer:
    """
    OpenAI Token 계산 관리 클래스
    """

    def __init__(self):

        self.encoding = tiktoken.encoding_for_model(
            OPENAI_MODEL
        )


    def count_tokens(
        self,
        text: str
    ) -> int:
        """
        문자열 Token 개수 계산
        """

        tokens = self.encoding.encode(
            text
        )

        return len(tokens)