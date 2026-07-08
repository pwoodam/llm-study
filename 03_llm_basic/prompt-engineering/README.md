# Prompt Engineering

LLM(Large Language Model)의 응답 품질을 향상시키기 위해 Prompt를 설계하고 관리하는 방법을 학습하는 프로젝트입니다.

단순히 사용자의 질문을 LLM에 전달하는 방식에서 벗어나, **System Prompt, User Prompt, Prompt Template, Variable Injection 구조를 구현**하여 실제 LLM Application 개발에서 사용하는 Prompt 관리 방식을 학습합니다.

---

# 1. Project Overview

## 목적

LLM은 동일한 질문이라도 Prompt의 구성 방식에 따라 다른 결과를 생성합니다.

따라서 LLM 서비스를 개발할 때는 단순한 API 호출보다:

* 모델의 역할 정의
* 답변 형식 지정
* 입력 데이터 관리
* Prompt 재사용 구조 설계

가 중요합니다.

본 프로젝트에서는 Prompt Engineering의 기본 개념을 학습하고, 유지보수가 가능한 Prompt Template 구조를 구현합니다.

---

# 2. Learning Objectives

이번 프로젝트의 목표는 다음과 같습니다.

* Prompt의 기본 개념 이해
* System Prompt와 User Prompt의 역할 이해
* Prompt Template 구조 구현
* Prompt와 Application Logic 분리
* Python에서 Template Variable Injection 구현
* 향후 RAG Pipeline으로 확장 가능한 구조 설계

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

| Library       | Purpose       |
| ------------- | ------------- |
| openai        | OpenAI API 호출 |
| python-dotenv | 환경 변수 관리      |

---

# 4. Project Structure

```text
prompt-engineering
│
├── app
│   │
│   ├── main.py                  # LLM API 호출 및 실행 코드
│   │
│   ├── prompt_loader.py         # Prompt Template 로딩 및 변수 치환
│   │
│   └── prompts
│       └── rag_explanation.txt  # Prompt Template 파일
│
├── tests
│   └── .gitkeep
│
├── .env
├── README.md
└── requirements.txt
```

---

# 5. Architecture

Prompt Engineering 프로젝트의 전체 흐름은 다음과 같습니다.

```text
User Input

    ↓

main.py

    ↓

Prompt Loader

    ↓

Prompt Template File

    ↓

Variable Injection

    ↓

Completed Prompt

    ↓

OpenAI API

    ↓

LLM Response
```

---

# 6. Prompt Engineering

## 6.1 Prompt란?

Prompt는 단순한 질문이 아니라 LLM에게 전달하는 전체 입력입니다.

Prompt에는 다음과 같은 정보를 포함할 수 있습니다.

* 역할(Role)
* 작업 목적(Task)
* 입력 데이터(Context)
* 출력 형식(Output Format)
* 제한 조건(Constraint)

---

## 6.2 Basic Prompt

예시:

```text
RAG가 무엇인지 설명해줘
```

단순 질문은 LLM이 답변 방향을 스스로 판단해야 합니다.

---

## 6.3 Structured Prompt

개선된 Prompt:

```text
너는 10년차 AI Engineer이다.

신입 개발자가 이해할 수 있도록 설명한다.

답변 형식:

1. 개념 설명
2. 동작 과정
3. 실제 활용 사례
4. 장점과 한계

질문:
RAG가 무엇인지 설명해줘
```

역할과 출력 형식을 명확하게 지정하여 더 일관된 응답을 얻을 수 있습니다.

---

# 7. System Prompt와 User Prompt

LLM Application에서는 Prompt를 역할에 따라 분리합니다.

## System Prompt

모델의 역할과 행동 방식을 정의합니다.

예:

```text
너는 10년차 AI Engineer이다.

답변은 신입 개발자가 이해하기 쉽게 작성한다.
```

---

## User Prompt

사용자가 실제 입력하는 질문입니다.

예:

```text
RAG와 Fine-tuning의 차이를 설명해줘
```

---

구조:

```text
System Prompt

↓

LLM 역할 및 규칙 정의


User Prompt

↓

실제 사용자 요청
```

---

# 8. Prompt Template

## Prompt 분리의 필요성

초기에는 Python 코드 내부에 Prompt를 직접 작성했습니다.

```python
prompt = """
너는 AI Engineer이다.

질문:
{question}
"""
```

하지만 실제 서비스에서는 Prompt를 코드와 분리하여 관리합니다.

장점:

* Prompt 수정 시 코드 변경 불필요
* Prompt 버전 관리 가능
* 다양한 Prompt 실험 가능
* 서비스별 Prompt 관리 가능

---

# 9. Prompt Template Example

파일:

```
app/prompts/rag_explanation.txt
```

내용:

```text
너는 10년차 AI Engineer이다.

신입 개발자가 이해할 수 있도록 설명한다.

답변 형식:

1. 개념 설명
2. 동작 과정
3. 실제 활용 사례
4. 장점과 한계

질문:
{question}
```

---

# 10. Variable Injection

Prompt Template 내부의 변수는 실행 시점에 실제 값으로 치환됩니다.

Template:

```text
질문:
{question}
```

실제 입력:

```python
question = "RAG란 무엇인가?"
```

결과:

```text
질문:
RAG란 무엇인가?
```

---

# 11. Prompt Loader 구현

`prompt_loader.py`

```python
from pathlib import Path


def load_prompt(prompt_name: str, **kwargs):
    """
    Prompt Template 파일을 읽고
    전달받은 keyword arguments를 활용하여
    Template 내부 변수를 치환한다.
    """

    prompt_path = Path(__file__).parent / "prompts" / prompt_name

    with open(prompt_path, "r", encoding="utf-8") as file:
        template = file.read()

    return template.format(**kwargs)
```

---

## **kwargs 동작 방식

`**kwargs`는 함수 호출 시 전달되는 keyword arguments를 dictionary 형태로 저장합니다.

예:

```python
load_prompt(
    "rag_explanation.txt",
    question="RAG란 무엇인가?"
)
```

내부:

```python
kwargs = {
    "question": "RAG란 무엇인가?"
}
```

이후:

```python
template.format(**kwargs)
```

를 통해 Template 내부 `{question}` 값이 치환됩니다.

---

# 12. Execution

실행:

```bash
python app/main.py
```

입력:

```text
RAG와 Fine-tuning의 차이를 설명해줘
```

처리 과정:

```text
사용자 질문

↓

Prompt Template 로딩

↓

question 변수 삽입

↓

완성된 Prompt 생성

↓

OpenAI API 호출

↓

LLM Response 반환
```

---


# 13. RAG와의 연결

Prompt Template 구조는 이후 RAG Pipeline에서 그대로 활용됩니다.

RAG 구조:

```text
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

Answer
```

예:

```text
너는 문서 기반 QA Assistant이다.

참고 문서:
{context}

사용자 질문:
{question}
```

Python:

```python
load_prompt(
    "rag_qa.txt",
    context=document,
    question=user_question
)
```

---

# 14. Future Improvements

추가 학습 예정:

* Few-shot Prompt 구현
* Structured Output(JSON Response)
* Prompt Version Management
* LangChain Prompt Template 적용
* Embedding 기반 검색
* RAG Pipeline 구축

---

# 15. Conclusion

이번 프로젝트에서는 LLM Application 개발의 기본 요소인 Prompt Engineering을 학습했습니다.

단순 API 호출에서 발전하여:

* 역할 기반 Prompt 설계
* Prompt Template 분리
* 변수 기반 Prompt 생성
* 유지보수 가능한 구조 설계

를 구현했습니다.

이 구조는 이후 Embedding, Retrieval, RAG 시스템 개발의 기반이 됩니다.
