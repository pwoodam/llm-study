# Structured Output

LLM(Large Language Model)의 응답을 자유로운 자연어 형태가 아닌 **구조화된 JSON 형태로 생성하고, Python Application에서 활용하는 방법을 학습하는 프로젝트**입니다.

일반적인 LLM 응답은 사람이 읽기에는 적합하지만, 실제 서비스에서는 Backend 로직에서 활용하기 어렵습니다.

따라서 이번 프로젝트에서는:

* Prompt Template 분리
* Prompt 변수 주입
* JSON 형태 응답 설계
* LLM 응답 Parsing

구조를 구현하여 실제 LLM Application 개발 방식에 가까운 형태로 개선합니다.

---

# 1. Project Overview

## 목적

LLM은 기본적으로 자연어(Text)를 생성하는 모델입니다.

예를 들어:

```
RAG가 무엇인지 설명해줘
```

라는 질문에 대해 LLM은 다음과 같은 형태로 답변합니다.

```
RAG는 Retrieval-Augmented Generation의 약자로 ...
```

하지만 이런 형태는 프로그램에서 특정 데이터를 추출하거나 Backend API 응답으로 활용하기 어렵습니다.

실제 AI 서비스에서는 다음과 같이 구조화된 데이터 형태로 응답을 관리합니다.

```json
{
    "topic": "RAG",
    "summary": "검색 기반으로 LLM 응답 품질을 향상시키는 기술",
    "key_points": [
        "외부 문서 검색",
        "Context 기반 답변 생성"
    ]
}
```

이를 통해 Python 코드에서 필요한 데이터만 선택적으로 활용할 수 있습니다.

---

# 2. Learning Objectives

이번 프로젝트의 목표는 다음과 같습니다.

* LLM 출력 형식 제어 방법 이해
* Prompt Template 구조 설계
* Prompt와 Application Logic 분리
* Keyword Arguments를 활용한 Prompt 변수 주입
* JSON Response 생성 및 Parsing
* AI Backend에서 사용하는 데이터 처리 방식 이해

---

# 3. Tech Stack

## Development Environment

| Category        | Technology         |
| --------------- | ------------------ |
| Language        | Python 3.11        |
| Environment     | Conda              |
| IDE             | Visual Studio Code |
| Version Control | Git / GitHub       |

## Library

| Library       | Purpose          |
| ------------- | ---------------- |
| openai        | OpenAI API 호출    |
| python-dotenv | 환경 변수 관리         |
| json          | JSON 데이터 Parsing |

---

# 4. Project Structure

```
structured-output
│
├── .env
│
├── app
│   ├── main.py                 # Application 실행 및 LLM 호출
│   ├── prompt_loader.py        # Prompt Template 로딩 및 변수 치환
│   ├── response_parser.py      # LLM 응답 JSON Parsing
│   │
│   └── prompts
│       └── json_output.txt     # JSON Response Prompt Template
│
├── tests
│   └── .gitkeep
│
├── README.md
└── requirements.txt
```

---

# 5. Architecture

전체 실행 흐름:

```
User Input

↓

main.py

↓

Prompt Loader

↓

Prompt Template

↓

Variable Injection

↓

OpenAI API

↓

JSON Response

↓

Response Parser

↓

Python Dictionary
```

---

# 6. Prompt Template 구조

## Prompt 분리 이유

초기 구현에서는 Python 코드 내부에 Prompt를 직접 작성했습니다.

```python
prompt = """
너는 AI 기술 분석 전문가이다.
질문:
{question}
"""
```

하지만 실제 서비스에서는 Prompt를 코드와 분리하여 관리합니다.

장점:

* Prompt 수정 시 코드 변경 최소화
* Prompt 버전 관리 가능
* 다양한 Prompt 실험 가능
* 프로젝트 규모 확장 용이

---

# 7. Prompt Template Example

파일:

```
app/prompts/json_output.txt
```

내용:

```
너는 AI 기술 분석 전문가이다.

사용자의 질문을 분석하고 반드시 JSON 형식으로 답변한다.

출력 형식:

{
    "topic": "주제",
    "summary": "요약",
    "key_points": [
        "핵심 내용1",
        "핵심 내용2"
    ]
}

질문:
{question}
```

---

# 8. Prompt Variable Injection

Prompt Template에서는 변수 영역을 정의합니다.

예:

```
질문:
{question}
```

Python에서:

```python
prompt = load_prompt(
    "json_output.txt",
    question="RAG를 설명해줘"
)
```

호출하면 내부적으로:

```python
kwargs = {
    "question": "RAG를 설명해줘"
}
```

형태로 전달됩니다.

이후:

```python
template.format(**kwargs)
```

를 통해 Prompt 내부의 `{question}` 값이 실제 질문으로 변경됩니다.

---

# 9. Prompt Loader

`prompt_loader.py`

```python
from pathlib import Path


def load_prompt(prompt_name: str, **kwargs):

    prompt_path = (
        Path(__file__).parent
        / "prompts"
        / prompt_name
    )

    with open(prompt_path, "r", encoding="utf-8") as file:
        template = file.read()

    return template.format(**kwargs)
```

역할:

* Prompt 파일 읽기
* Template 변수 확인
* 실제 입력값 치환

---

# 10. Structured Output 설계

LLM에게 원하는 출력 형식을 Prompt에서 정의합니다.

예:

```text
반드시 JSON 형식으로 답변한다.

{
    "topic": "...",
    "summary": "...",
    "key_points": [
        "..."
    ]
}
```

이를 통해 LLM 응답 형태를 일정하게 유지할 수 있습니다.

---

# 11. Response Parser

LLM API 응답은 문자열 형태입니다.

예:

```python
response.output_text
```

결과:

```text
{
    "topic": "RAG",
    "summary": "...",
    "key_points": [...]
}
```

이를 Python 객체로 변환합니다.

```python
json_result = json.loads(response_text)
```

변환 결과:

```python
{
    "topic": "RAG",
    "summary": "...",
    "key_points": [...]
}
```

이후 Python Dictionary처럼 활용할 수 있습니다.

---

# 12. Execution

실행:

```bash
python app/main.py
```

입력:

```
RAG를 설명해줘
```

처리 과정:

```
사용자 질문 입력

↓

Prompt Template 로딩

↓

question 변수 치환

↓

OpenAI API 호출

↓

JSON Response 반환

↓

Python Dictionary 변환

↓

데이터 활용
```

---

# 13. Example Response

입력:

```
RAG를 설명해줘
```

출력 예시:

```json
{
    "topic": "RAG",
    "summary": "검색 기반으로 LLM 응답 품질을 개선하는 기술",
    "key_points": [
        "외부 데이터 검색",
        "Context 기반 생성",
        "Hallucination 감소"
    ]
}
```

Python 활용:

```python
print(result["topic"])
print(result["summary"])
```

---

# 14. Practical Applications

Structured Output은 실제 AI 서비스에서 다양한 형태로 활용됩니다.

* AI Chatbot Backend Response
* RAG Answer Format
* Document Analysis
* AI Agent Workflow
* 자동 데이터 추출
* Frontend API Response
* Database 저장

---

# 15. RAG와의 연결

Structured Output은 이후 구현할 RAG 시스템에서 중요한 역할을 합니다.

예:

```json
{
    "answer": "휴가 신청 방법은 ...",
    "sources": [
        "company_policy.pdf"
    ]
}
```

RAG 시스템에서는:

```
User Question

↓

Retriever

↓

Relevant Documents

↓

Prompt Template

↓

LLM

↓

Structured Response
```

형태로 확장됩니다.

---

# 16. Future Improvements

추후 구현 예정:

* OpenAI Structured Output(JSON Schema)
* Pydantic 기반 데이터 검증
* Function Calling
* Tool Calling
* LangChain Output Parser
* RAG Pipeline 구현
* AI Agent Workflow 구축

---

# 17. Conclusion

이번 프로젝트에서는 LLM 응답을 단순 Text 형태로 사용하는 것이 아니라, **Application에서 활용 가능한 JSON 구조로 변환하는 방법**을 학습했습니다.

또한 Prompt를 코드와 분리하고 Loader 구조를 적용하여 유지보수 가능한 LLM Application 구조를 구현했습니다.

이를 통해:

* Prompt Template 관리
* 변수 기반 Prompt 생성
* Structured Response 설계
* JSON Parsing

을 경험했으며, 이후 구현할 RAG와 AI Agent 시스템의 기반을 마련했습니다.
