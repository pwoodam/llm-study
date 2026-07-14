from pathlib import Path

from chatbot import Chatbot


def load_system_prompt():
    prompt_path = (
        Path(__file__).parent
        / "prompts"
        / "system.txt"
    )

    with open(
        prompt_path,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()
    
def load_summary_prompt():
    prompt_path = (
        Path(__file__).parent
        / "prompts"
        / "summary.txt"
    )

    with open(
        prompt_path,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def main():

    system_prompt = load_system_prompt()
    summary_prompt = load_summary_prompt()
    chatbot = Chatbot(
        system_prompt,
        summary_prompt
    )


    print(
        "AI Chatbot 시작 (exit 입력 시 종료)"
    )


    while True:

        user_input = input(
            "\nUser: "
        )


        if user_input.lower() == "exit":
            break


        print("\nAssistant:", end=" ")

        for chunk in chatbot.chat_stream(user_input):
            print(chunk, end="", flush=True)
        
        print()  # 줄바꿈

# 프로그램의 시작점일 때만 아래 코드 실행
if __name__ == "__main__":
    main()