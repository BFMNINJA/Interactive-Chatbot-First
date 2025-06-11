from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def main():
    print("Welcome to the chatbot!")
    system_prompt = input("Enter the system prompt: ")
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    while True:
        response_text = ""
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Exiting chat. Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=messages,
            stream=True
        )
        for chunk in response:
            print(chunk.choices[0].delta.content, end="")
            response_text += chunk.choices[0].delta.content
        messages.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main()
