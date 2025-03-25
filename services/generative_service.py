
import random
import re
import requests
import os

MAX_MARKOV_CHAIN_LENGTH = 10

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
        if json and json['output'] and json['output'][0] and json['output'][0]['content'] and json['output'][0]['content'][0] and json['output'][0]['content'][0]['text']:
            return re.sub(r'\n', '', json['output'][0]['content'][0]['text'])
        else:
            return None
        

def generate_markov_chain_response(deque):
    if deque:
        # Starts with the most popular keyword
        random_word = deque.get_popular_keywords()[0][0]
        response = random_word + " "
        # Generates a response of MAX_MARKOV_CHAIN_LENGTH - random.randint(0, 5) words
        for i in range(MAX_MARKOV_CHAIN_LENGTH - random.randint(0, 5)):
            try:
                # Chooses possible next words from the Markov Chain from the current word
                next_word = random.choice(deque.markov_chains[random_word])
                if next_word:
                    response += next_word + " "
                else:
                    # If no next word, chooses a random word from the Markov Chain
                    next_word = random.choice(deque.markov_chains.keys())
                    response += next_word + " "
                random_word = next_word
            except KeyError:
                random_word = random.choice(deque.get_popular_keywords())[0]
        return response

