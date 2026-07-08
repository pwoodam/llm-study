# LLM API Basic

Python 환경에서 OpenAI API를 활용하여 LLM(Large Language Model)을 호출하고, 사용자 입력에 대한 AI 응답을 생성하는 기본 프로젝트입니다.

단순한 API 사용법 학습을 넘어, LLM 기반 서비스가 동작하는 전체 흐름인 **환경 변수 관리 → API 요청 → 응답 처리 → 결과 출력** 과정을 이해하는 것을 목표로 합니다.

---

## 1. Project Overview

### 목적

LLM 기반 서비스를 개발하기 위한 첫 번째 단계로, Python 애플리케이션에서 외부 AI 모델 API를 호출하는 방법을 학습합니다.

본 프로젝트에서는 OpenAI API를 활용하여 다음 과정을 구현합니다.

* API Key 안전한 관리 방법 학습
* Python 기반 LLM API 호출
* 사용자 입력 기반 AI 응답 생성
* API Response 데이터 처리

---

## 2. Tech Stack

### Development Environment

| Category        | Technology         |
| --------------- | ------------------ |
| Language        | Python 3.11        |
| Environment     | Conda              |
| IDE             | Visual Studio Code |
| Version Control | Git / GitHub       |

### Library

| Library       | Purpose                      |
| ------------- | ---------------------------- |
| openai        | OpenAI API 호출을 위한 Python SDK |
| python-dotenv | 환경 변수(.env) 관리               |
| requests      | HTTP 통신 구조 이해 및 API 요청 실습    |

---

## 3. Project Structure

```text
llm-api-basic
│
├── app
│   └── main.py              # LLM API 호출 실행 코드
│
├── tests
│   └── .gitkeep
│
├── .env.example             # 환경 변수 예시 파일
├── README.md                # 프로젝트 설명
└── requirements.txt         # 프로젝트 의존성 관리
```

---

## 4. Architecture

LLM API 호출 과정은 다음과 같은 구조로 동작합니다.

```text
User Input

    ↓

Python Application

    ↓

OpenAI SDK

    ↓

HTTP Request

    ↓

OpenAI API Server

    ↓

LLM Model

    ↓

Response

    ↓

Generated Answer
```

---

## 5. Environment Setup

### 1) Virtual Environment

Conda 환경 생성

```bash
conda create -n llm-study python=3.11

conda activate llm-study
```

---

### 2) Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. API Key Configuration

OpenAI API Key는 보안을 위해 코드에 직접 작성하지 않고 환경 변수로 관리합니다.

### .env 파일 생성

프로젝트 root 위치에 `.env` 파일을 생성합니다.

```text
llm-api-basic
├── .env
```

작성 내용:

```env
OPENAI_API_KEY=your_api_key
```

---

### 환경 변수 관리 이유

잘못된 방식:

```python
client = OpenAI(
    api_key="sk-xxxxxxxx"
)
```

문제점:

* GitHub 업로드 시 API Key 노출 위험
* 보안 사고 발생 가능
* 프로젝트 관리 어려움

개선 방식:

```text
.env

↓

python-dotenv

↓

os.getenv()

↓

OpenAI Client
```

환경 변수를 통해 민감한 정보를 안전하게 관리합니다.

---

## 7. Implementation

### 1) Environment Variable Load

```python
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
```

`.env` 파일에 저장된 API Key를 Python 환경 변수로 불러옵니다.

---

### 2) OpenAI Client 생성

```python
client = OpenAI(
    api_key=api_key
)
```

OpenAI API와 통신하기 위한 Client 객체를 생성합니다.

---

### 3) LLM API 호출

```python
response = client.responses.create(
    model="gpt-4.1-mini",
    input=user_input
)
```

사용자의 Prompt를 LLM 모델에 전달하고 생성된 응답을 반환받습니다.

---

### 4) Response 출력

```python
print(response.output_text)
```

LLM이 생성한 텍스트 응답을 출력합니다.

---

## 8. Execution

실행 명령어:

```bash
python app/main.py
```

실행 예시:

```text
질문을 입력하세요:

RAG와 Fine-tuning의 차이를 설명해줘


답변:

RAG는 외부 데이터를 검색하여...
```

---

## 9. Learned Concepts

### HTTP API

API 통신 구조를 이해했습니다.

```text
Client

↓

Request

↓

Server

↓

Response

↓

Client
```

학습 내용:

* HTTP Request / Response
* Status Code
* API 통신 구조

---

### JSON Response 처리

API 응답 데이터는 JSON 형태로 전달됩니다.

```text
JSON

↓

Python Object

↓

필요한 데이터 추출
```

LLM API 또한 JSON 기반으로 요청과 응답이 이루어집니다.

---

### LLM API 구조

LLM 모델을 직접 학습하지 않고 API 형태로 제공되는 모델을 활용하는 방법을 학습했습니다.

```text
Application

↓

LLM API

↓

Pre-trained Model

↓

Generated Response
```

---

### Prompt

사용자의 입력 문장은 모델에 전달되는 Prompt입니다.

Prompt의 구성 방식에 따라 LLM 응답 품질이 달라집니다.

---

## 10. Troubleshooting

### API Rate Limit Error (429)

발생 오류:

```text
openai.RateLimitError:
You exceeded your current quota
```

원인:

* API Billing 설정 필요
* API 사용량 제한 초과

해결:

* OpenAI API Billing 설정 확인
* API Usage 확인

---

## 11. Future Improvements

향후 다음 기능을 추가할 예정입니다.

* Prompt Template 적용
* System Prompt 활용
* 대화 기록 관리
* Streaming Response 구현
* Embedding 기반 검색 구현
* RAG Pipeline 구축

---

## 12. References

* OpenAI API Documentation
* Python dotenv Documentation
* HTTP API Fundamentals
