import json


def parse_response(response_text: str):
    """
    JSON 문자열을 Python Dictionary로 변환
    """

    return json.loads(response_text)