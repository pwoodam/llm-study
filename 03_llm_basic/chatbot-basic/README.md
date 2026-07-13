# Chatbot Basic

OpenAI API를 활용하여 **대화의 맥락(Context)을 유지하는 Multi-turn Chatbot**을 구현한 프로젝트입니다.

단순히 한 번 질문하고 답변을 받는 방식이 아닌, 이전 대화 내용을 함께 전달하여 ChatGPT와 같은 연속적인 대화 경험을 구현하는 것을 목표로 하였습니다.

또한 실제 AI 서비스 개발 구조를 고려하여 **환경 설정, API Client, Prompt, Conversation 관리, Database, Chatbot 로직을 역할별로 분리**하여 유지보수성과 확장성을 고려한 구조로 설계하였습니다.

---

# 1. Project Overview

## 목적

LLM은 이전 대화 내용을 자동으로 기억하지 않습니다.

따라서 매 요청마다 이전 대화 기록을 함께 전달해야 사용자의 질문 의도와 대화 흐름을 유지할 수 있습니다.

본 프로젝트에서는 다음 기능을 구현하였습니다.

* Conversation History 관리
* Token 기반 Context Window 관리
* SQLite 기반 Conversation Memory 구현
* Session 기반 대화 관리
* System Prompt 분리 관리
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
* Token 기반 Context Window 관리 방식 이해
* SQLite 기반 LLM Memory 구현
* Session 기반 데이터 관리 구조 이해
* 객체지향(OOP) 기반 Chatbot 설계
* 환경 설정과 비즈니스 로직 분리
* LLM Application에서 Streaming Response 처리 방식 이해
* 실제 AI 서비스와 유사한 프로젝트 구조 설계

---

# 3. Tech Stack

## Development Environment

| Category | Technology |
| --- | --- |
| Language | Python 3.11 |
| Environment | Conda |
| IDE | Visual Studio Code |
| Version Control | Git / GitHub |

## Library

| Library | Purpose |
| --- | --- |
| openai | OpenAI API 호출 |
| python-dotenv | 환경 변수 관리 |
| sqlite3 | Conversation Memory 저장 |

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
│   ├── database.py       # SQLite Database 관리
│   │
│   └── prompts
│       └── system.txt    # System Prompt 관리
│
├── data
│   └── chatbot.db        # Conversation History 저장 DB (runtime 생성)
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

Conversation

↓

SQLite Database

↓

Conversation History 반환

↓

Chatbot

↓

System Prompt + Conversation History 조립


↓

OpenAI API

↓

Assistant Response

↓

SQLite Database 저장
```

각 구성 요소의 역할은 다음과 같습니다.

| Component | Role |
| --- | --- |
| main.py | 사용자 입력 및 출력 처리 |
| Chatbot | LLM 호출 및 서비스 로직 관리 |
| Conversation | 대화 흐름 관리 및 Message 구성 |
| Database | Conversation History 영구 저장 |
| Client | OpenAI API 연결 관리 |
| Config | 환경 변수 및 설정 관리 |
| Prompt | System Prompt 관리 |

---

# 6. Conversation History & SQLite Memory

LLM은 이전 대화를 자동으로 기억하지 않기 때문에 요청마다 이전 대화 내용을 함께 전달해야 합니다.

기존에는 Python 객체 내부의 List에 대화 내용을 저장했지만, 프로그램 종료 시 데이터가 사라지는 문제가 있었습니다.

이를 개선하기 위해 SQLite 기반 Conversation Memory를 구현하였습니다.

## 변경 전

```text
User

↓

Conversation

↓

Memory 저장

↓

프로그램 종료 시 데이터 삭제
```

## 변경 후

```text
User

↓

Conversation

↓

SQLite Database

↓

영구 저장
```

---

## Token 기반 Context Window

LLM은 이전 대화 내용을 모두 함께 전달할 수 있지만, 대화가 길어질수록 Token 사용량과 API 비용이 증가하고 응답 속도가 느려질 수 있습니다.

LLM은 Message 개수가 아니라 Token 수를 기준으로 Context Window를 관리합니다.

따라서 최근 N개의 Message를 전달하는 방식 대신, Token 제한을 초과하지 않는 범위에서 최근 Message를 선택하여 전달하도록 구현하였습니다.

### 처리 과정

```text
SQLite Database

↓

전체 Message 조회

↓

Conversation

↓

Token 계산

↓

Token 제한 이하의 Message 선택

↓

System Prompt 추가

↓

OpenAI API
```
Conversation 클래스에서 token기반으로 최근 Message만 선택하도록 구현하여 Database는 데이터 저장 및 조회만 담당하고, Conversation이 LLM에 전달할 Message를 구성하도록 역할을 분리하였습니다.

```python
for message in reversed(messages):

    message_tokens = self.tokenizer.count_tokens(
        message["content"]
    )

    if total_tokens + message_tokens > max_tokens:
        break

    selected_messages.insert(0, message)

    total_tokens += message_tokens
```
Token 기반 Context Window를 적용함으로써 Message의 개수가 아니라 실제 LLM이 사용하는 Token 수를 기준으로 대화 기록을 관리하도록 개선하였습니다.

이를 통해 긴 Message가 포함된 경우에도 Context Window를 초과하지 않도록 제어할 수 있으며, 실제 LLM 서비스에서 사용하는 Memory 관리 방식과 유사한 구조를 구현하였습니다.

---

## Session 기반 Memory 구조

대화 기록은 Session 단위로 관리합니다.

하나의 Session은 여러 개의 Message를 가질 수 있습니다.

```text
sessions

id
created_at


messages

id
session_id
role
content
created_at
```

관계:

```text
Session (1)

    |

    | 1:N

    |

Messages (N)
```

---

## Database Schema

### sessions Table

| Column | Description |
| --- | --- |
| id | session 식별자 |
| created_at | session 생성 시간 |

### messages Table

| Column | Description |
| --- | --- |
| id | 메시지 식별자 |
| session_id | 연결된 Session ID |
| role | user / assistant |
| content | 메시지 내용 |
| created_at | 생성 시간 |

---

# 7. Role 기반 Message

OpenAI API는 Role 기반 Message 구조를 사용합니다.

| Role | 설명 |
| --- | --- |
| system | AI의 역할과 동작 규칙 정의 |
| user | 사용자 입력 |
| assistant | AI 응답 |

System Prompt는 Conversation Data와 분리하여 관리하며, 요청 시 Message 구조에 추가합니다.

---

# 8. 주요 클래스

## Conversation

Conversation History를 관리하는 클래스입니다.

주요 기능:

* Session 생성 및 관리
* User Message 추가
* Assistant Message 추가
* Database 연동
* Token 기반 Context Window 구성
* Token 제한 이하의 Message 반환

---

## Database

SQLite Database를 관리하는 클래스입니다.

주요 기능:

* SQLite 연결
* Session 테이블 생성
* messages 테이블 생성 및 조회
* Message 저장
* Conversation History 조회

---

## Tokenizer

Tokenizer는 OpenAI 모델의 Token 수를 계산하는 클래스입니다.

주요 기능

* 모델별 Tokenizer 생성
* 문자열 Token 개수 계산
* Conversation의 Context Window 계산 지원

---

## Chatbot

Chatbot 서비스 로직을 담당하는 핵심 클래스입니다.

주요 기능:

* 사용자 입력 처리
* OpenAI API 호출
* Conversation History 조립
* Streaming Response 처리
* Assistant 응답 저장

---

# 9. Streaming Response

기존 Chatbot은 OpenAI API 요청 후 LLM의 응답 생성이 완료될 때까지 기다린 뒤 전체 결과를 반환하는 방식이었습니다.

Streaming Response를 적용하여 LLM이 생성하는 응답을 chunk 단위로 전달받고, 사용자에게 실시간으로 출력하도록 개선하였습니다.

---

## 기존 Response 방식

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

`yield`는 값을 반환한 뒤 종료되는 `return`과 달리 실행 상태를 유지하며 다음 값을 요청할 때 이어서 실행됩니다.

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

# 10. 실행 방법

라이브러리 설치:

```bash
pip install -r requirements.txt
```

환경 변수 설정:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini
```

실행:

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

SQLite에 저장된 Conversation History를 활용하여 프로그램 재실행 이후에도 이전 대화 맥락을 유지할 수 있습니다.

---

# 12. 배운 점

이번 프로젝트를 통해 다음 내용을 학습하였습니다.

* Multi-turn Conversation 구현
* Conversation History 관리
* Token 기반 Context Window 관리
* tiktoken을 활용한 Token 계산
* LLM Context Window 관리 방식 이해
* 역할 분리를 고려한 Memory 관리 구조 설계
* SQLite 기반 Memory 구현
* Session 기반 데이터 모델링
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

* System Prompt를 포함한 Token 관리
* Output Token Reserve 적용
* Conversation Summary Memory
* FastAPI 기반 Chat API
* LangChain Memory 적용
* RAG 기반 Chatbot 확장

---

# 14. Conclusion

이번 프로젝트에서는 단순한 질문-응답 프로그램이 아닌 **대화의 맥락을 유지하고 영구 저장 및 실시간 응답이 가능한 Chatbot**을 구현하였습니다.

또한 Prompt, Conversation, Database, API Client를 역할별로 분리하여 유지보수성과 확장성을 고려한 LLM Application 구조를 설계하였습니다.

더 나아가 Token 기반 Context Window를 적용하여 실제 LLM 서비스와 유사한 Context 관리 방식을 구현하였으며, 이를 기반으로 FastAPI 기반 Chat API, RAG, AI Agent 등으로 확장 가능한 아키텍처를 구축하였습니다. 이번 프로젝트를 통해 실제 서비스 수준의 Chatbot을 단계적으로 설계하고 구현하는 과정을 경험하며, 향후 다양한 LLM Application 개발의 기반을 마련하였습니다.