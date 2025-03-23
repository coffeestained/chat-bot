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
twitch_bot/
│
├── chat_app.py # Main bot service
├── services/
│ ├── generative_service.py # Generates responses
│ ├── custom_model_service.py # Custom model for predictions
│ ├── integration_service.py # Integrates various services
│ ├── auth_app.py # Handles Twitch OAuth
├── utils/
│ ├── logging.py # Logging configuration
├── logs/ # Directory for log files
├── firewall_setup.sh # Firewall configuration script
├── requirements.txt # Project dependencies
├── Dockerfile # Docker configuration for containerization
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
    docker run -d -p 3000:3000 --name twitch_bot twitch_bot
    ```

3. **Environment Variables**:
    Set the following environment variables:
    - DISCORD_TOKEN: Your Discord bot token
    - TWITCH_CLIENT_ID: Your Twitch client ID
    - TWITCH_CLIENT_SECRET: Your Twitch client secret
    - TWITCH_REDIRECT_URI: Your Twitch redirect URI
    - ACCESS_TOKEN: Your Twitch access token
    - CHANNEL: Desired channel to join
    - MONGO_URI: MongoDB URL
    - REDIS_URI: Redis URL
    - LOG_LEVEL: Log level (e.g., DEBUG, INFO, ERROR) 

## Usage

1. **Start the bot**:
    ```bash
    docker start twitch_bot
    ```

2. **Access the authentication URL**:
    Visit `http://yourserver.com/login` to authenticate with Twitch.

## Contributions

Open issues or submit pull requests for improvements or new features.

## License

This project is licensed under the MIT License.
