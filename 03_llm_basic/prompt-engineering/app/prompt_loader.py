from pathlib import Path


def load_prompt(prompt_name: str, **kwargs):
    """
    Prompt 파일을 읽고 변수를 치환한다.
    **kwargs는 함수 호출 시 전달되는 키워드 인자(keyword arguments)를 dictionary 형태로 받아 저장하는 매개변수
    Prompt Template에서는 전달받은 key와 value를 이용해 템플릿 내부의 변수를 치환
    """

    prompt_path = Path(__file__).parent / "prompts" / prompt_name

    with open(prompt_path, "r", encoding="utf-8") as file:
        template = file.read()

    return template.format(**kwargs)