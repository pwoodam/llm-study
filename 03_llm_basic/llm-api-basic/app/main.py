import os

from dotenv import load_dotenv
from openai import OpenAI


# .env 파일 로드
load_dotenv()

# API Key 확인
api_key = os.getenv("OPENAI_API_KEY")

# API Key가 설정되지 않은 경우 예외 처리
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

# OpenAI Client 생성
client = OpenAI(api_key=api_key)

user_input = input("질문을 입력하세요: ")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=user_input
)

print("\n답변:")
print(response.output_text)