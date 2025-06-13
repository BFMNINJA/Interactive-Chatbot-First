from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import mimetypes
from urllib.parse import urlparse

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

        def is_image_url(url):
            parsed = urlparse(url)
            if not parsed.scheme.startswith("http"):
                return False
            ext = os.path.splitext(parsed.path)[1].lower()
            return ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]

        if is_image_url(user_input.strip()):
            image_url = user_input.strip()
            try:
                img_response = requests.get(image_url)
                img_response.raise_for_status()
                img_bytes = img_response.content
                mime_type, _ = mimetypes.guess_type(image_url)
                if mime_type is None:
                    mime_type = "image/jpeg"
                # Gemini/OpenAI vision API expects images as bytes or base64, depending on client
                # Here, we use OpenAI's vision API style
                response = client.chat.completions.create(
                    model="gemini-2.0-flash", # Replace with your vision-capable model if needed
                    messages=messages + [
                        {"role": "user", "content": [
                            {"type": "text", "text": "Describe this image."},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]}
                    ],
                    stream=True
                )
                for chunk in response:
                    print(chunk.choices[0].delta.content, end="")
                    response_text += chunk.choices[0].delta.content
                messages.append({"role": "user", "content": image_url})
                messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                print(f"Failed to process image: {e}")
        else:
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
