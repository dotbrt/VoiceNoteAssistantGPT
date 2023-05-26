import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def model_call(text):
    print(text)
    instructions = "You're an experienced copywriter. I give you transcription of my voice memos and you fix grammar and improve wording."
    reply = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": text},
        ]
    )
    return reply.choices[0].message.content.strip()


if __name__ == "__main__":
    text = input("Enter text to be fixed: ")
    print(model_call(text))
