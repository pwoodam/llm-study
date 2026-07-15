import os

from dotenv import load_dotenv


load_dotenv()

def _get_required_env(key: str) -> str:
    """
    필수 환경변수를 읽어오되, 없으면 어떤 키가 문제인지 명확히 알려준다.
    """
    value = os.getenv(key)

    if not value:
        raise ValueError(
            f"{key}가 설정되지 않았습니다. .env 파일을 확인하세요."
        )

    return value


def _get_required_int_env(key: str) -> int:
    """
    필수 정수형 환경변수를 읽어온다.
    """
    value = _get_required_env(key)

    try:
        return int(value)
    except ValueError:
        raise ValueError(
            f"{key} 값이 올바른 정수가 아닙니다: '{value}'"
        )

OPENAI_API_KEY = _get_required_env("OPENAI_API_KEY")
OPENAI_MODEL = _get_required_env("OPENAI_MODEL")

MAX_CONTEXT_TOKENS = _get_required_int_env("MAX_CONTEXT_TOKENS")
OUTPUT_TOKEN_RESERVE = _get_required_int_env("OUTPUT_TOKEN_RESERVE")
SUMMARY_TRIGGER_TOKENS = _get_required_int_env("SUMMARY_TRIGGER_TOKENS")
SUMMARY_MAX_OUTPUT_TOKENS = _get_required_int_env("SUMMARY_MAX_OUTPUT_TOKENS")