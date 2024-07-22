import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Log level constant
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

# Create logs directory if it doesn't exist
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Map log level constant to logging levels
log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'ERROR': logging.ERROR
}

# Create a logger
logger = logging.getLogger('TwitchBotLogger')
logger.setLevel(log_levels[LOG_LEVEL])

# Create a file handler with log rotation every 4 months
handler = TimedRotatingFileHandler(os.path.join(log_directory, 'chat-bot.log'), when='M', interval=4, backupCount=6)
handler.setLevel(log_levels[LOG_LEVEL])

# Create a log formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Set log level based on the constant
if LOG_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
elif LOG_LEVEL == 'INFO':
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.ERROR)
