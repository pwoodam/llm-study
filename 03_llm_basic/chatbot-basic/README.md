# Chatbot Basic

OpenAI API를 활용하여 **대화의 맥락(Context)을 유지하는 Multi-turn Chatbot**을 구현한 프로젝트입니다.

단순히 한 번 질문하고 답변을 받는 방식이 아닌, 이전 대화 내용을 함께 전달하여 ChatGPT와 같은 연속적인 대화 경험을 구현하는 것을 목표로 하였습니다.

또한 실제 AI 서비스 개발 구조를 고려하여 **환경 설정, API Client, Prompt, Conversation 관리, Chatbot 로직을 역할별로 분리**하여 유지보수성과 확장성을 고려한 구조로 설계하였습니다.

---

# 1. Project Overview

## 목적

LLM은 이전 대화 내용을 자동으로 기억하지 않습니다.

따라서 매 요청마다 이전 대화 기록을 함께 전달해야만 사용자의 질문 의도와 대화 흐름을 유지할 수 있습니다.

본 프로젝트에서는 다음 기능을 구현하였습니다.

* Conversation History 관리
* System Prompt 분리
* OpenAI Client 분리
* Config 관리
* Chatbot 클래스 설계
* Multi-turn Conversation 구현
* Streaming Response 구현

---

# 2. Learning Objectives

이번 프로젝트를 통해 다음 내용을 학습하는 것을 목표로 하였습니다.

* OpenAI API 사용 방법 이해
* Role 기반 Message 구조 이해
* Conversation History 관리 방식 이해
* 객체지향(OOP) 기반 Chatbot 설계
* 환경 설정과 비즈니스 로직 분리
* LLM Application에서 Streaming Response 처리 방식 이해
* 실제 AI 서비스와 유사한 프로젝트 구조 설계

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
chatbot-basic
│
├── .env                  # 로컬 환경 변수 (Git 제외)
├── .env.example          # 환경 변수 예시
│
├── app
│   ├── main.py           # 프로그램 실행 및 사용자 입력 처리
│   ├── config.py         # 환경 설정 관리
│   ├── client.py         # OpenAI Client 생성
│   ├── chatbot.py        # Chatbot 핵심 비즈니스 로직
│   ├── conversation.py   # Conversation History 관리
│   │
│   └── prompts
│       └── system.txt    # System Prompt 관리
│
├── tests
│   └── .gitkeep
│
├── README.md
└── requirements.txt
```

---

# 5. Architecture

프로젝트는 각 역할을 분리하여 구성하였습니다.

```text
User

↓

main.py

↓

Chatbot

↓

Conversation History

↓

OpenAI API

↓

Assistant Response

↓

Conversation History 저장
```

각 구성 요소의 역할은 다음과 같습니다.

| Component    | Role               |
| ------------ | ------------------ |
| main.py      | 사용자 입력 및 출력 처리     |
| Chatbot      | LLM 호출 및 서비스 로직 관리 |
| Conversation | 대화 기록 관리           |
| Client       | OpenAI API 연결 관리   |
| Config       | 환경 변수 및 설정 관리      |
| Prompt       | System Prompt 관리   |

---

# 6. Conversation History

LLM은 이전 대화를 자동으로 기억하지 않기 때문에 요청마다 이전 대화 내용을 함께 전달해야 합니다.

예를 들어 다음과 같은 대화가 있다고 가정합니다.

User

```text
RAG가 뭐야?
```

Assistant

```text
RAG는 Retrieval-Augmented Generation입니다.
```

사용자가 다음 질문을 입력합니다.

```text
장점은?
```

이때 OpenAI API에는 이전 대화 내용이 함께 전달됩니다.

```python
[
    {
        "role": "system",
        "content": "너는 친절한 AI Assistant이다."
    },
    {
        "role": "user",
        "content": "RAG가 뭐야?"
    },
    {
        "role": "assistant",
        "content": "RAG는 Retrieval-Augmented Generation입니다."
    },
    {
        "role": "user",
        "content": "장점은?"
    }
]
```

이를 통해 LLM이 이전 대화의 Context를 기반으로 응답할 수 있습니다.

---

# 7. Role 기반 Message

OpenAI API는 Role 기반 Message 구조를 사용합니다.

| Role      | 설명               |
| --------- | ---------------- |
| system    | AI의 역할과 동작 규칙 정의 |
| user      | 사용자 입력           |
| assistant | AI 응답            |

System Prompt를 활용하여 AI의 역할과 응답 방향을 제어할 수 있습니다.

---

# 8. 주요 클래스

## Conversation

Conversation History를 관리하는 클래스입니다.

주요 기능:

* System Prompt 저장
* User Message 추가
* Assistant Message 추가
* Message 목록 반환

---

## Chatbot

Chatbot 서비스 로직을 담당하는 핵심 클래스입니다.

주요 기능:

* 사용자 입력 처리
* OpenAI API 호출
* Conversation History 관리
* Streaming Response 처리
* Assistant 응답 저장

---

# 9. Streaming Response

기존 Chatbot은 OpenAI API 요청 후 LLM의 응답 생성이 완료될 때까지 기다린 뒤 전체 결과를 반환하는 방식이었습니다.

Streaming Response를 적용하여 LLM이 생성하는 응답을 chunk 단위로 전달받고, 사용자에게 실시간으로 출력하도록 개선하였습니다.

이를 통해 ChatGPT와 같이 응답이 생성되는 과정을 사용자에게 제공할 수 있습니다.

---

## 기존 Response 방식

전체 응답 생성이 완료된 후 결과를 반환합니다.

```text
User Input

↓

OpenAI API 요청

↓

LLM 응답 생성 완료 대기

↓

전체 응답 반환
```

---

## Streaming Response 방식

생성되는 응답을 작은 단위(chunk)로 나누어 순차적으로 전달합니다.

```text
User Input

↓

OpenAI Streaming API 요청

↓

chunk 단위 응답 수신

↓

실시간 출력
```

---

## Generator 기반 구현

Python Generator의 `yield`를 활용하여 Streaming 구조를 구현하였습니다.

```python
def stream_text(text):

    for char in text:
        yield char
```

`yield`는 값을 반환한 뒤 함수가 종료되는 `return`과 달리 실행 상태를 유지하며, 다음 값을 요청할 때 이전 실행 위치부터 이어서 실행됩니다.

---

## OpenAI Streaming API 적용

기존 방식:

```python
response = client.responses.create(
    model=OPENAI_MODEL,
    input=messages
)

return response.output_text
```

변경 후:

```python
stream = client.responses.create(
    model=OPENAI_MODEL,
    input=messages,
    stream=True
)

for event in stream:

    if event.type == "response.output_text.delta":

        yield event.delta
```

`stream=True` 옵션을 사용하여 응답 이벤트를 순차적으로 전달받고, `event.delta`를 통해 생성된 텍스트 일부를 처리합니다.

---

## 응답 저장 처리

Streaming 방식에서는 응답이 여러 chunk로 전달되기 때문에 사용자에게 실시간 출력하는 동시에 Conversation 저장을 위해 전체 응답을 누적합니다.

```python
full_response = ""

for event in stream:

    if event.delta:

        full_response += event.delta

        yield event.delta
```

동작 과정:

```text
LLM 생성

↓

chunk 전달

↓

사용자 화면 실시간 출력

↓

전체 응답 완성

↓

Conversation History 저장
```

---

# 10. 실행 방법

필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

환경 변수를 설정합니다.

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini
```

실행합니다.

```bash
python app/main.py
```

종료:

```text
exit
```

---

# 11. 실행 예시

```text
AI Chatbot 시작

User:
RAG가 뭐야?

Assistant:
RAG는 Retrieval-Augmented Generation의 약자로...

User:
장점은?

Assistant:
RAG의 주요 장점은...
```

이전 Conversation History를 함께 전달하기 때문에 두 번째 질문에서도 대화 맥락을 유지할 수 있습니다.

---

# 12. 배운 점

이번 프로젝트를 통해 다음 내용을 학습하였습니다.

* Multi-turn Conversation 구현
* Conversation History 관리
* Role 기반 Message 구성
* OpenAI API 활용 방법
* Prompt 분리 및 관리
* 환경 설정 분리
* API Client 분리
* 객체지향 기반 Chatbot 설계
* Generator 기반 Streaming Response 구현

---

# 13. Future Improvements

향후 다음 기능을 추가할 예정입니다.

* 대화 기록 저장(SQLite)
* Conversation 길이 제한
* Token 관리
* FastAPI 기반 Chat API
* LangChain Memory 적용
* RAG 기반 Chatbot 확장

---

# 14. Conclusion

이번 프로젝트에서는 단순한 질문-응답 프로그램이 아닌 **대화의 맥락을 유지하고 실시간 응답이 가능한 Chatbot**을 구현하였습니다.

또한 프로젝트 구조를 역할별로 분리하여 유지보수성과 확장성을 고려하였으며, 이후 구현할 SQLite Memory, RAG, AI Agent 프로젝트의 기반이 되는 LLM Application 구조를 학습하였습니다.
