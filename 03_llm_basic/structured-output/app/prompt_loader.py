from pathlib import Path


def load_prompt(prompt_name: str, **kwargs):

    prompt_path = Path(__file__).parent / "prompts" / prompt_name

    with open(prompt_path, "r", encoding="utf-8") as file:
        template = file.read()

    return template.format(**kwargs)