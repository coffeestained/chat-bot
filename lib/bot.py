import os
import asyncio
from dotenv import load_dotenv
from twitchio.ext import commands
from datetime import datetime, timedelta, UTC
from services.generative_service import generate_llm_response
from utils.logging import logger 
import random
from utils.message_memory import MemoryDeque

# Load environment variables from .env file
load_dotenv()

# Set the interval for updating the model (in minutes)
UPDATE_MODEL_INTERVAL = 10

# minutes between responses
MAX_RESPONSE_RATE = int(os.getenv('MESSAGE_INTERVAL_IN_MINUTES', 10))

class Bot():
    def __init__(self, db, redis, executor):
        self.messages_collection = db["messages"]
        self.state_collection = db["state"]
        self.redis_client = redis
        self.executor = executor
        self.last_response_time = datetime.now(UTC)
        self.memory_deque = MemoryDeque()
        self.twitch_bot = TwitchBot(self)

        # Response loop
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.do_response())

    async def process_message(self, message):
        self.memory_deque.trim_old_messages()
        # Add message to FIFO queue
        self.memory_deque.enqueue(message)

    async def do_response(self):
        interval = 5
        while True:
            if False:    
                peek = self.memory_deque.peek()
                if peek:
                    logger.info(f'Memory deque peek: {self.memory_deque.get_popular_keywords()}')
            valid = True
            
            # Check if we need to generate a response
            if self.memory_deque.is_empty():
                valid = False

            if self.last_response_time > datetime.now(UTC) - timedelta(minutes=MAX_RESPONSE_RATE):
                valid = False
            
            if valid:
                # Generate response
                logger.info(f'Generating response.')
                # await message.channel.send(response)
                self.last_response_time = datetime.now(UTC)
                response = None
                if os.getenv('MODE') == 'llm':
                    response = generate_llm_response(self.memory_deque.get_popular_keywords())
                if response:
                    logger.info(f'Response: {response}')    
                    channel = self.twitch_bot.get_channel(os.getenv('CHANNEL', ''))
                    await channel.send(response)

            await asyncio.sleep(interval)
            continue  

class TwitchBot(commands.Bot):
    def __init__(self, bot):
        super().__init__(token=os.getenv('ACCESS_TOKEN', 'default_access_token'), prefix='!', initial_channels=[os.getenv('CHANNEL', ''), os.getenv('MY_CHANNEL', '')])
        self.bot = bot
        logger.info('Bot initialized.')

    async def event_ready(self):
        logger.info(f'Logged in as | {self.nick}')
        logger.info(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if not message.author or message.author.name.lower() == self.nick.lower():
            return

        if os.getenv('SHOW_MESSAGES') == 'True':
            logger.info(f'Received message from {message.author.name}: {message.content}')

        await self.bot.process_message(message)
