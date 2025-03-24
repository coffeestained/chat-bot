
import random
import requests
import os

# LLM Response Generator
def generate_llm_response(message):
    if message:
        url = os.getenv('LLM_URI') 
        headers = {
            "Authorization": f"Bearer {os.getenv('LLM_API_KEY')}"
        }
        data = {
            "model": "gpt-4o-mini",
            "input": os.getenv('LLM_MESSAGE_PREFIX', '') + ", ".join(word for word, count in message) + os.getenv('LLM_MESSAGE_SUFFIX', ''),
            "max_output_tokens": 16
        }
        response = requests.post(url, headers=headers, json=data)
        json = response.json()
        print(json['output'][0])
        if json and json['output'] and json['output'][0] and json['output'][0]['content'] and json['output'][0]['content'][0] and json['output'][0]['content'][0]['text']:
            return json['output'][0]['content'][0]['text']
        else:
            return None
