import tiktoken

from config import OPENAI_MODEL


class Tokenizer:
    """
    OpenAI Token 계산 관리 클래스
    """

    # tiktoken이 모델명을 인식하지 못할 때 사용할 기본 인코딩
    # o200k_base: GPT-4o 이후 최신 모델 계열이 사용하는 인코딩
    FALLBACK_ENCODING = "o200k_base"

    def __init__(self):

        try:
            self.encoding = tiktoken.encoding_for_model(
                OPENAI_MODEL
            )
        except KeyError:
            # tiktoken이 아직 모델명을 인식하지 못하는 경우
            # (신규 모델이거나 tiktoken 버전이 뒤처진 경우) fallback 인코딩 사용
            print(
                f"[Tokenizer] '{OPENAI_MODEL}'에 대한 인코딩을 찾을 수 없어 "
                f"'{self.FALLBACK_ENCODING}'로 대체합니다."
            )
            self.encoding = tiktoken.get_encoding(
                self.FALLBACK_ENCODING
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