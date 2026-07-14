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
* SQLite 기반 Conversation Memory 구현
* Session 기반 대화 관리
* Token Budget 기반 Context Window 관리
* Conversation Summary 기반 Long-term Memory 구현
* Summary + Recent Message 기반 Context 구성
* System Prompt 분리 관리
* Summary Prompt 분리 관리
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
* Conversation Summary 기반 Long-term Memory 설계
* Summary Trigger 기반 자동 요약 처리
* Incremental Summary 방식 이해
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
│       ├── system.txt    # Chatbot System Prompt
│       └── summary.txt   # Conversation Summary Prompt
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

Message History 조회

↓

Conversation

↓

Token 기반 Context Message 선택

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

↓

Summary Trigger 조건 확인

↓

Conversation Summary 생성

↓

Summary Memory 저장
```

각 구성 요소의 역할은 다음과 같습니다.

| Component | Role |
| --- | --- |
| main.py | 사용자 입력 및 출력 처리 |
| Chatbot | LLM 호출 및 서비스 로직 관리 |
| Conversation | 대화 흐름 관리, Context Message 구성, Summary Memory 관리 |
| Database | Session, Message, Conversation Summary 영구 저장 |
| Client | OpenAI API 연결 관리 |
| Config | 환경 변수 및 설정 관리 |
| Prompt | System Prompt, Summary Prompt 관리 |

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

또한 LLM의 응답 생성을 위한 Output Token 공간을 확보하기 위해 전체 Context Window에서 Output Token Reserve를 제외한 Token Budget을 계산합니다.

이를 통해 입력 Message가 Context Window 전체를 차지하는 것을 방지하고, 안정적인 응답 생성을 보장합니다.

대화 기록의 Token 수가 설정한 Summary Trigger 기준을 초과하는 경우,
기존 대화 전체를 유지하는 대신 Conversation Summary를 생성하여
중요한 대화 정보를 압축 저장합니다.

이후 LLM 요청 시:

System Prompt
+
Summary Memory
+
Recent Conversation History

구조로 Context를 구성합니다.

### 처리 과정

```text
SQLite Database

↓

Conversation History 조회

↓

Summary Memory 확인

↓

Token Budget 계산

↓

최근 Message 선택

↓

System Prompt
+
Conversation Summary
+
Recent Conversation History 조립

↓

OpenAI API
```
Conversation 클래스는 Tokenizer를 활용하여 Message Token을 계산하고, Context Window 제한 내에서 LLM에 전달할 Message를 구성하도록 구현하였습니다.

대화가 길어져 Summary가 생성된 경우에는 기존 대화 전체를 전달하지 않고, Conversation Summary와 Summary 이후의 최근 Message를 함께 전달하여 Context Window를 효율적으로 관리합니다.

Database는 Session, Message, Conversation Summary 데이터의 저장 및 조회만 담당하고, Conversation 클래스가 LLM 요청에 필요한 Context 구조를 구성하도록 역할을 분리하였습니다.

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

이를 통해 긴 대화에서도 전체 Message를 계속 전달하지 않고 Summary와 최근 Context를 조합하여 관리할 수 있으며, 실제 LLM 서비스에서 사용하는 Long-term Memory 관리 방식과 유사한 구조를 구현하였습니다.

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

### conversation_summaries

| Column | Description |
| --- | --- |
| id | summary 식별자 |
| session_id | 연결된 Session ID |
| summary | 누적 대화 요약 내용 |
| last_message_id | Summary 생성에 포함된 마지막 Message ID |
| created_at | Summary 생성 시간 |

### 관계

```text
Session (1)

 |

 | 1:1

 |

Conversation Summary (1)


Session (1)

 |

 | 1:N

 |

Messages (N)
```

---

# 7. Conversation Summary Memory

긴 대화가 지속되면 모든 Conversation History를 Context에 포함하는 방식은 Token 사용량 증가와 Context Window 초과 문제를 발생시킬 수 있습니다.

이를 해결하기 위해 Conversation Summary Memory를 구현하였습니다.

Conversation Summary Memory는 기존 대화 내용을 요약하여 저장하고, 이후 LLM 요청 시 전체 대화 대신 Summary와 최근 대화 내용만 전달하는 Long-term Memory 방식입니다.

이를 통해 긴 대화에서도 중요한 맥락을 유지하면서 Token 사용량을 효율적으로 관리할 수 있습니다.

---

## Summary Trigger 기반 자동 요약

모든 대화마다 Summary를 생성하면 불필요한 API 호출과 비용이 발생합니다.

따라서 Conversation History의 Token 수를 기준으로 Summary 생성 여부를 판단하는 Trigger 방식을 적용하였습니다.

처리 과정:

```text
User Message 추가

↓

Assistant Response 저장

↓

전체 Conversation Token 계산

↓

Summary Trigger Threshold 확인

↓

Threshold 초과 시 Summary 생성
```

Summary Trigger 조건을 만족하면 기존 Summary와 새로운 대화 내용을 함께 전달하여 최신 Summary를 생성합니다.

---

## Incremental Summary 방식

Summary 생성 시 매번 전체 Conversation History를 다시 요약하지 않고, 기존 Summary와 Summary 이후의 새로운 Message만 활용하는 Incremental Summary 방식을 적용하였습니다.

기존 방식:

```text
전체 Conversation History

↓

LLM Summary 생성

↓

Summary 저장
```

문제점:

- 대화가 길어질수록 입력 Token 증가
- 불필요한 이전 Message 반복 전달
- Summary 생성 비용 증가

개선 방식:

```text
기존 Summary

+

Summary 이후 새로운 Message

↓

LLM Summary 생성

↓

업데이트된 Summary 저장
```

이를 통해 이전 대화의 핵심 정보는 유지하면서 새롭게 추가된 대화 내용만 반영하여 효율적으로 Summary Memory를 갱신합니다.

---

## Conversation Summary Database 구조

Summary Memory는 기존 Message Table과 분리하여 별도의 테이블로 관리합니다.

```text
conversation_summaries

id
session_id
summary
last_message_id
created_at
```

각 Column 역할:

| Column | Description |
| --- | --- |
| id | Summary 식별자 |
| session_id | 연결된 Session ID |
| summary | 누적 대화 요약 내용 |
| last_message_id | Summary 생성에 포함된 마지막 Message ID |
| created_at | Summary 생성 시간 |

---

## Summary 기준 Message 관리

Summary가 생성된 이후에는 이전 Message 전체를 다시 전달하지 않습니다.

`last_message_id`를 기준으로 Summary 이후에 추가된 Message만 조회합니다.

처리 과정:

```text
conversation_summaries

↓

last_message_id 조회

↓

last_message_id 이후 Message 조회

↓

기존 Summary + 새로운 Message

↓

새로운 Summary 생성
```

이를 통해 이미 Summary에 포함된 Message가 반복적으로 Context에 포함되는 것을 방지합니다.

---

## Summary 기반 Context 구성 방식

Summary가 존재하는 경우 LLM 요청 Context는 다음 구조로 구성됩니다.

```text
System Prompt

+

Conversation Summary

+

Recent Conversation History

↓

OpenAI API
```

예시:

```text
System:
너는 AI Assistant이다.

Summary:
사용자는 RAG 시스템 구축 방법에 관심이 있으며,
Embedding과 Vector Database에 대해 학습 중이다.

Recent Messages:
User:
Vector Database 종류를 알려줘.

Assistant:
대표적인 Vector Database에는...
```

LLM은 전체 대화를 전달받지 않더라도 Summary Memory를 통해 이전 대화의 핵심 정보를 유지할 수 있습니다.

---

## Summary Memory Architecture

```text
User

↓

Conversation

↓

Message 저장

↓

Summary Trigger 확인

↓

Conversation Summary 생성

↓

SQLite Summary Memory 저장


LLM 요청 시

↓

System Prompt

+

Summary Memory

+

Recent Conversation History

↓

OpenAI API
```

Conversation Summary Memory를 적용함으로써 단순한 단기 Conversation History 관리에서 벗어나, 긴 대화를 지원하는 Long-term Memory 구조를 구현하였습니다.

---

# 8. Role 기반 Message

OpenAI API는 Role 기반 Message 구조를 사용합니다.

| Role | 설명 |
| --- | --- |
| system | AI의 역할과 동작 규칙 정의 |
| user | 사용자 입력 |
| assistant | AI 응답 |

System Prompt는 Conversation Data와 분리하여 관리하며, 요청 시 Message 구조에 추가합니다.

---
# 9. 주요 클래스

## Conversation

Conversation History를 관리하는 클래스입니다.

주요 기능:

* Session 생성 및 관리
* User Message 추가
* Assistant Message 추가
* Database 연동
* Token 기반 Context Window 구성
* Token Budget 기반 Context Message 구성
* Conversation Summary 조회 및 저장
* Summary 이후 Message 조회

---

## Database

SQLite Database를 관리하는 클래스입니다.

주요 기능:

* SQLite 연결
* Session 테이블 생성
* messages 테이블 생성 및 조회
* Conversation Summary 테이블 생성
* Session 생성
* Message 저장 및 조회
* Summary 저장 및 조회
* Summary 기준 이후 Message 조회

---

## Tokenizer

Tokenizer는 OpenAI 모델의 Token 수를 계산하는 클래스입니다.

주요 기능

* 모델별 Tokenizer 생성
* 문자열 Token 개수 계산
* Context Window 관리를 위한 Token 정보 제공

---

## Chatbot

Chatbot 서비스 로직을 담당하는 핵심 클래스입니다.

주요 기능:

* 사용자 입력 처리
* OpenAI API 호출
* Conversation History 조립
* System Prompt 및 Output Token Reserve를 고려한 Context Budget 계산
* Streaming Response 처리
* Assistant 응답 저장
* Token Threshold 기반 Summary Trigger 판단
* Conversation Summary 생성
* Summary Memory 기반 Context 구성
* Incremental Summary 생성

---

# 10. Streaming Response

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

# 11. 실행 방법

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

# 12. 실행 예시

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

# 13. 배운 점

이번 프로젝트를 통해 다음 내용을 학습하였습니다.

* Multi-turn Conversation 구현
* Conversation History 관리
* Token 기반 Context Window 관리
* tiktoken을 활용한 Token 계산
* LLM Context Window 관리 방식 이해
* Input Token과 Output Token Budget 분리 설계
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

# 14. Future Improvements

향후 다음 기능을 추가할 예정입니다.

* FastAPI 기반 Chat API 서버 구현
* Vector Database 기반 Retrieval 구현
* RAG 기반 Knowledge Chatbot 확장
* LangChain 기반 Memory 관리 적용
* 중요도 기반 Dynamic Context Selection
* Message Importance Scoring 기반 Memory Optimization
* Adaptive Context Window Management
* AI Agent Workflow 확장

---

# 15. Conclusion

이번 프로젝트에서는 **Conversation Memory와 Conversation Summary Memory를 구현하여
긴 대화에서도 핵심 정보를 유지하면서 Context Window를 효율적으로 관리하고 영구 저장 및 실시간 응답이 가능한 LLM Chatbot** 구조를 설계하였습니다.

이번 프로젝트를 통해 LLM Application에서 필요한 Conversation Memory, Context Window 관리, Streaming Response 구조를 단계적으로 구현하였습니다.

또한 역할별 모듈 분리를 통해 확장 가능한 Chatbot 아키텍처를 설계하였으며, 이후 FastAPI 기반 API 서버, RAG, AI Agent 등 다양한 LLM Application으로 확장할 수 있는 기반을 마련하였습니다.