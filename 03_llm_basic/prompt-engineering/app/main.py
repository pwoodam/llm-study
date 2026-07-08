import os

from dotenv import load_dotenv
from openai import OpenAI

from prompt_loader import load_prompt

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY가 없습니다.")


client = OpenAI(api_key=api_key)


question = input("질문 입력: ")

prompt = load_prompt(
    "rag_explanation.txt",
    question=question
)

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)


print("\n===== Answer =====")
print(response.output_text)