"""Module dedicated to bot initiation variables that are usable in other modules."""
import logging
from os import environ
import random

from telegram.ext import Updater


__author__ = "Vlad Chitic"
__copyright__ = "Copyright 2019, Vlad Chitic"
__credits__ = ["Vlad Chitic"]
__license__ = "MIT License"
__version__ = "1.0 stable"
__maintainer__ = "Vlad Chitic"
__email__ = "feorache@protonmail.com"
__status__ = "Production"

# Setup logging
logging.basicConfig(
    filename='logs.log',
    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

LOGGER.info('-----------------------------------------------')
LOGGER.info('Initializing the bot and creating database tables if needed...')

# Bot initialization
updater = Updater(token=environ.get("TG_BOT_TOKEN"),
                  use_context=True, workers=32)
dispatcher = updater.dispatcher

# Create a randomizer
randomizer = random.SystemRandom()
