# Chatbot Basic

OpenAI API를 활용하여 **대화의 맥락(Context)을 유지하는 Multi-turn Chatbot**을 구현한 프로젝트입니다.

단순히 한 번 질문하고 답변을 받는 것이 아니라, 이전 대화 내용을 함께 전달하여 ChatGPT와 같은 연속적인 대화 경험을 구현하는 것을 목표로 했습니다.

또한 실무 프로젝트 구조를 고려하여 **환경 설정, API Client, 대화 관리, 비즈니스 로직을 분리**하는 방식으로 설계했습니다.

---

# 1. Project Overview

## 목적

LLM은 이전 대화를 자동으로 기억하지 않습니다.

따라서 매 요청마다 이전 대화 내용을 함께 전달해야만 연속적인 대화(Context)를 유지할 수 있습니다.

이번 프로젝트에서는 다음과 같은 구조를 구현했습니다.

* Conversation History 관리
* System Prompt 분리
* OpenAI Client 분리
* Config 분리
* Chatbot 클래스 설계
* Multi-turn Conversation 구현

---

# 2. Learning Objectives

이번 프로젝트의 목표는 다음과 같습니다.

* OpenAI Chat API 사용 방법 이해
* Role 기반 Message 구조 이해
* Conversation History 관리
* 객체지향(OOP) 기반 Chatbot 설계
* 설정(Configuration)과 비즈니스 로직 분리
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
│   ├── main.py           # 프로그램 실행
│   ├── config.py         # 환경 설정
│   ├── client.py         # OpenAI Client 생성
│   ├── chatbot.py        # Chatbot 핵심 로직
│   ├── conversation.py   # 대화 기록 관리
│   │
│   └── prompts
│       └── system.txt    # System Prompt
│
├── tests
│   └── .gitkeep
│
├── README.md
└── requirements.txt
```

---

# 5. Architecture

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

---

# 6. Conversation History

LLM은 이전 대화를 자동으로 기억하지 않기 때문에, 모든 요청마다 이전 대화를 함께 전달해야 합니다.

예를 들어 다음과 같은 대화가 있다고 가정합니다.

User

```text
RAG가 뭐야?
```

Assistant

```text
RAG는 Retrieval-Augmented Generation입니다.
```

다음 질문이

```text
장점은?
```

이라면 OpenAI API에는 다음과 같이 전달됩니다.

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

이러한 방식으로 이전 대화의 맥락(Context)을 유지할 수 있습니다.

---

# 7. Role 기반 Message

OpenAI API는 Role 기반 Message 구조를 사용합니다.

| Role      | 설명               |
| --------- | ---------------- |
| system    | AI의 역할과 동작 규칙 정의 |
| user      | 사용자 입력           |
| assistant | AI 응답            |

Role을 적절히 구성하면 AI의 행동과 응답 방식을 제어할 수 있습니다.

---

# 8. 주요 클래스

## Conversation

대화 기록을 관리하는 클래스입니다.

주요 기능

* System Prompt 저장
* User Message 추가
* Assistant Message 추가
* Message 목록 반환

---

## Chatbot

Chatbot의 핵심 로직을 담당합니다.

처리 과정

```text
사용자 입력

↓

Conversation History 저장

↓

OpenAI API 호출

↓

Assistant 응답 저장

↓

응답 반환
```

---

# 9. 실행 방법

필요한 라이브러리 설치

```bash
pip install -r requirements.txt
```

환경 변수 설정

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini
```

실행

```bash
python app/main.py
```

종료

```text
exit
```

---

# 10. 실행 예시

```text
User: RAG가 뭐야?

Assistant:
RAG는 Retrieval-Augmented Generation의 약자로...

User:
장점은?

Assistant:
RAG의 주요 장점은...
```

이전 대화 내용을 함께 전달하기 때문에 두 번째 질문도 자연스럽게 이해합니다.

---

# 11. 배운 점

이번 프로젝트를 통해 다음 내용을 학습했습니다.

* Multi-turn Conversation 구현
* Conversation History 관리
* Role 기반 Message 구성
* OpenAI API 활용
* 환경 설정 분리
* API Client 분리
* 객체지향 기반 Chatbot 설계

---

# 12. Future Improvements

향후 다음 기능을 추가할 예정입니다.

* Streaming Response
* 대화 기록 저장(SQLite)
* Conversation 길이 제한
* Token 관리
* FastAPI 기반 Chat API
* LangChain Memory 적용
* RAG 기반 Chatbot 확장

---

# 13. Conclusion

이번 프로젝트에서는 단순한 질문-응답 프로그램이 아닌 **대화의 맥락을 유지하는 Chatbot**을 구현했습니다.

또한 프로젝트 구조를 역할별로 분리하여 유지보수성과 확장성을 고려한 구조를 설계했으며, 이후 구현할 RAG와 AI Agent 프로젝트의 기반이 되는 Conversation 관리 방식을 익혔습니다.
