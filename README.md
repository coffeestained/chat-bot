# Twitch Chat Bot

## Goal

Develop a Twitch chat bot that interacts dynamically with users. The bot processes messages, generates responses, integrates with Twitch OAuth, logs activity, and stores data using Redis and MongoDB.

## Features

- Dynamic response generation
- Twitch OAuth integration
- Logging with rotation every 4 months
- Data storage with Redis and MongoDB
- Firewall setup to secure the server 

## Project Structure

```
chat_app.py # Main bot service
services/
├── generative_service.py # Generates responses
├── custom_model_service.py # Custom model for predictions
├── integration_service.py # Integrates various services
utils/
├── logging.py # Logging configuration  
├── message_memory.py # Handles message memory  
lib/
├── bot.py # Bot class
├── mongodb.py # MongoDB client
├── redis.py # Redis client
logs/
├── ...*.log # Bot logs
.github/workflows/
├── ...*.yml # GitHub Actions workflows
.env # Environment variables    
.gitignore # Git ignore
requirements.txt # Project dependencies
README.md # This file
LICENSE # License
sample-env # Sample environment variables
docker-compose.yml # Docker compose file
Dockerfile-Bot
```


## Technologies Used

- **Language**: Python
- **Libraries**: `discord.py`, `aiohttp`, `scikit-learn`, `numpy`, `requests`, `pymongo`, `redis`, `flask`
- **Database**: MongoDB
- **Caching**: Redis
- **Containerization**: Docker

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/twitch_bot.git
    cd twitch_bot
    ```

2. **Build and run with Docker**:
    ```bash
    docker build -t twitch_bot .
    docker run -d -p 5000:5000 --name twitch_bot twitch_bot
    ```

3. **Environment Variables**:
    Set the following environment variables:
    - DISCORD_TOKEN: Your Discord bot token
    - TWITCH_CLIENT_ID: Your Twitch client ID
    - TWITCH_CLIENT_SECRET: Your Twitch client secret
    - TWITCH_REDIRECT_URI: Your Twitch redirect URI
    - ACCESS_TOKEN: Your Twitch access token
    - MESSAGE_INTERVAL_IN_MINUTES: How often to send messages   
    - MODE = llm || markov -- use llm to generate responses requires LLM_URI and LLM_API_KEY. Use markov to generate responses from markov chains.
    - STOP_WORDS_URL: URL to the stop words text file. Must be a text file with one word per line.
    - LLM_URI: Your LLM URI 
    - LLM_API_KEY: Your LLM API key
    - LLM_MESSAGE_PREFIX: Your LLM message prefix
    - LLM_MESSAGE_SUFFIX: Your LLM message suffix
    - CHANNEL: Desired channel to join
    - MONGO_URI: MongoDB URL
    - REDIS_URI: Redis URL
    - LOG_LEVEL: Log level (e.g., DEBUG, INFO, ERROR) 
    - STD_OUT: True or False - if true, logs will be printed to the console
    - SHOW_MESSAGES: True or False - if true, messages will be printed to the console

## Usage

1. **Start the bot**:
    ```bash
    docker start twitch_bot
    ```

## Contributions

Open issues or submit pull requests for improvements or new features.

## License

This project is licensed under the MIT License.
