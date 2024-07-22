import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from twitchio.ext import commands
import redis
import pymongo
from datetime import datetime, timedelta
from services.generative_service import generate_response
from services.custom_model_service import custom_model
from utils.logging import logger

# Load environment variables from .env file
load_dotenv()

# Read environment variables for MongoDB and Redis
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:your_password@localhost:27017/')
REDIS_URI = os.getenv('REDIS_URI', 'redis://localhost:6379')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

TWITCH_CHANNEL = os.getenv('CHANNEL', '')

# Connect to Redis and MongoDB
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["chatbot"]
messages_collection = db["messages"]
state_collection = db["state"]

executor = ThreadPoolExecutor()

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix='!', initial_channels=[CHANNEL])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.author.name.lower() == self.nick.lower():
            return

        response = await process_message(message.content)
        # await message.channel.send(response)

async def process_message(message):
    loop = asyncio.get_event_loop()

    # Fire and forget model update
    loop.run_in_executor(executor, update_model, message)

    # Get cached response
    cached_response = redis_client.get("latest_response")
    if cached_response:
        return cached_response.decode("utf-8")
    else:
        # If no cached response, generate a custom response
        generative_future = loop.run_in_executor(executor, generate_response, message)
        generative_response = await generative_future

        # Cache the new response
        redis_client.set("latest_response", generative_response)
        return generative_response

def update_model(message):
    # Save message to MongoDB for auditing
    response = generate_response(message)
    messages_collection.insert_one({
        "message": message,
        "response": response,
        "timestamp": datetime.utcnow(),
        "feedback_score": random.randint(0, 100)  # Simulated feedback score
    })

    # Update the model
    custom_model.update_model([message], [response])

    # Save the state to MongoDB
    state_collection.replace_one({}, {"state": custom_model}, upsert=True)

    # Update the highest feedback response if needed
    feedback_scores = [doc["feedback_score"] for doc in messages_collection.find()]
    highest_feedback_score = max(feedback_scores, default=0)
    if feedback_scores[-1] == highest_feedback_score:
        redis_client.set("latest_response", response)

# Set the interval for updating the model (in minutes)
UPDATE_INTERVAL = 10

async def scheduled_updates():
    while True:
        await asyncio.sleep(UPDATE_INTERVAL * 60)
        # Update the highest feedback score response
        update_highest_feedback_response()

def update_highest_feedback_response():
    ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
    recent_messages = messages_collection.find({"timestamp": {"$gte": ten_minutes_ago}})
    best_response = max(recent_messages, key=lambda msg: msg.get("feedback_score", 0), default=None)
    if best_response:
        redis_client.set("latest_response", best_response["response"])

if __name__ == "__main__":
    bot = Bot()
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_updates())
    loo
