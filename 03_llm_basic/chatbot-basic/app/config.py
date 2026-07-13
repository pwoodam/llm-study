import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL"
    )


if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY가 설정되지 않았습니다."
    )

MAX_CONTEXT_TOKENS = int(
    os.getenv(
        "MAX_CONTEXT_TOKENS"
    )
)