import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from prompt_loader import load_prompt
from response_parser import parse_response


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY가 없습니다.")


client = OpenAI(api_key=api_key)


question = input("질문 입력: ")

prompt = load_prompt(
    "json_output.txt", 
    question=question
    )

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)


result = response.output_text

parsed = parse_response(result)

print("\n===== Parsed Result =====")
print(parsed)

print("\n===== Topic =====")
print(parsed["topic"])

print("\n===== Summary =====")
print(parsed["summary"])