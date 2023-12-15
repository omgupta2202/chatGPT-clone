import os
import openai

# API_KEY = os.environ['OPENAI_API_KEY']
API_KEY = '-kfSWjicWEpivb9y2UFJnT3BlbkFJX2FUculBXLEZ0kjU2iHc'
openai.api_key = API_KEY


def get_response(prompt, model="gpt-3.5-turbo"):
    messages = [
        {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.8,
    )
    return response.choices[0].message['content']
