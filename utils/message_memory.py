from collections import Counter, deque
from datetime import UTC, datetime, timedelta, timezone
import os
import requests
from utils.logging import logger 
from dotenv import load_dotenv

load_dotenv()

MAX_AGE=30
MAX_MEMORY_SIZE = 2000
MAX_POPULAR_KEYWORDS = 30

STOP_WORD_CSV_URL = os.getenv('STOP_WORDS_URL', 'https://raw.githubusercontent.com/4troDev/profanity.csv/refs/heads/main/English.csv')

# DOwnloads CSV to List
def download_csv_to_list(url):
    response = requests.get(url)
    return response.text.splitlines()

STOP_WORDS = download_csv_to_list(STOP_WORD_CSV_URL)

class Message:
    def __init__(self, item):
        self.message = item.content
        self.timestamp = item.timestamp
        self.author = item.author.name
        self.channel = item.channel.name
        self.keywords = self.get_keywords()
        self.markov_chains = self.get_markov_chains()

    def __str__(self):
        return f"{self.timestamp}: {self.message}"
    
    def get_keywords(self):
        cleaned = self.message.split()
        filtered = [word for word in cleaned if word not in STOP_WORDS]
        return filtered
    
    def get_markov_chains(self):
        tuple_list = []
        for i in range(len(self.keywords) - 1):
            tuple_list.append((self.keywords[i], [self.keywords[i + 1]]))
        return tuple_list
    
class MemoryDeque:
    def __init__(self, max_size=MAX_MEMORY_SIZE):
        self.max_size = max_size
        self.queue = deque(maxlen=max_size)
        self.markov_chains = {}

    def enqueue(self, item):
        logger.debug(f'Enqueuing message: {item}')
        self.queue.append(Message(item))

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None  # or raise an exception

    def peek(self):
        return self.queue[-1] if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return len(self.queue) == self.max_size

    def get_popular_keywords(self):
        keywords = []
        for message in self.queue:
            keywords.extend(message.keywords)
        popular = Counter(keywords).most_common(MAX_POPULAR_KEYWORDS)
        logger.debug(f'Popular keywords: {popular}')
        return popular
    
    def combine_markov_chains(self):
        for message in self.queue:
            for keyword, next_words in message.markov_chains:
                if keyword in self.markov_chains:
                    self.markov_chains[keyword].extend(next_words)
                else:
                    self.markov_chains[keyword] = next_words
        return self.markov_chains

    def trim_old_messages(self):
        self.queue = deque(
            message for message in self.queue if not self.trim_condition(message)
        )

    def trim_condition(self, message):
        message_time = message.timestamp.replace(tzinfo=timezone.utc)
        if message_time < datetime.now(UTC) - timedelta(minutes=MAX_AGE):
            logger.debug(f'Trimming message: {message}')
            return True
        return False

    def __len__(self):
        return len(self.queue)

    def __iter__(self):
        return iter(self.queue)

