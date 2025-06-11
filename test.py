from openai import OpenAI

client = OpenAI(
    api_key="YOUR GEMINI API KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def main():
    print("Welcome to the chatbot!")
    system_prompt = input("Enter the system prompt: ")
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Exiting chat. Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=messages
        )
        assistant_reply = response.choices[0].message.content
        print(f"Assistant: {assistant_reply}")
        messages.append({"role": "assistant", "content": assistant_reply})

if __name__ == "__main__":
    main()
