import os
import asyncio
import uvicorn
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from flask import Flask
from lib.redis import get_redis
from lib.mongodb import get_db
from lib.bot import Bot

# Load environment variables from .env file
load_dotenv()

# Initialize Redis and MongoDB connections
redis_client = get_redis()
db = get_db()
messages_collection = db["messages"]
state_collection = db["state"]

# Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Thread pool executor
executor = ThreadPoolExecutor()

async def run_flask():
    config = uvicorn.Config(app, host="0.0.0.0", port=3000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    bot = Bot(db, redis_client, executor)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        bot.twitch_bot.start(),
        run_flask()
    ))
    