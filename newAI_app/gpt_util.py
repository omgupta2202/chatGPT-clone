import os
import openai

# API_KEY = os.environ['OPENAI_API_KEY']
API_KEY = 'k-F7GoHJFQaTqad5DyADsDT3BlbkFJxvVKt3LzVUg0XkTu8pcT'
openai.api_key = API_KEY


def get_response(prompt, model="gpt-3.5-turbo"):
    messages = [
        {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.4,
    )
    return response.choices[0].message['content']
