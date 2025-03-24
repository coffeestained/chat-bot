import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

# Log level constant and STD flag from environment
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
STD = os.getenv('STD_OUT', 'False').lower() == 'true'

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
logger.setLevel(log_levels.get(LOG_LEVEL, logging.DEBUG))

# Create a file handler with log rotation every 4 months
file_handler = TimedRotatingFileHandler(
    os.path.join(log_directory, 'chat-bot.log'),
    when='M',
    interval=4,
    backupCount=6
)
file_handler.setLevel(log_levels.get(LOG_LEVEL, logging.DEBUG))

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add file handler
logger.addHandler(file_handler)

# If STD mode is enabled, add stdout handler
if STD:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)  # Always output everything to stdout
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

# Example usage
logger.debug('Debug message')
logger.info('Info message')
logger.error('Error message')
