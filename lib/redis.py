import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URI')
redis_client = redis.StrictRedis.from_url(REDIS_URL)

def get_redis():
    return redis_client
