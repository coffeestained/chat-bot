import os
from flask import Flask
from dotenv import load_dotenv
from lib.mongodb import get_db
from lib.redis import get_redis
from utils.logging import logger 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize MongoDB and Redis
db = get_db()
redis_client = get_redis()

@app.route('/')
def index():
    logger.info('Management ping.')
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)