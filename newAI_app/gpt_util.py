import os
import openai
import requests

API_ENDPOINT = "https://icd-finetuned-api.vercel.app/AI/chat"

def get_response(prompt):
    data = {"q": prompt}
    headers = {"Content-Type": "application/json"}
    print (data)
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    print(response.text)
    if response.status_code == 200:
        return response.text
    else:
        return "Error in API request."


# # API_KEY = os.environ['OPENAI_API_KEY']
# API_KEY = '943OVjNXFK7RJMVPklo7T3BlbkFJnx1YersHJf8G86vLM5s-H'
# openai.api_key = API_KEY


# def get_response(prompt, model="gpt-3.5-turbo"):
#     messages = [
#         {"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0.8,
#     )
#     return response.choices[0].message['content']
