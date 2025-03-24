from collections import Counter, deque
from datetime import UTC, datetime, timedelta, timezone
from utils.logging import logger 
import re

MAX_AGE=1
MAX_MEMORY_SIZE = 2000
MAX_POPULAR_KEYWORDS = 100
STOP_WORDS = []

class Message:
    def __init__(self, item):
        self.message = item.content
        self.timestamp = item.timestamp
        self.author = item.author.name
        self.channel = item.channel.name
        self.keywords = self.get_keywords()

    def __str__(self):
        return f"{self.timestamp}: {self.message}"
    
    def get_keywords(self):
        cleaned = self.message.split()
        filtered = [word for word in cleaned if word not in STOP_WORDS]
        return filtered

class MemoryDeque:
    def __init__(self, max_size=MAX_MEMORY_SIZE):
        self.max_size = max_size
        self.queue = deque(maxlen=max_size)

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

