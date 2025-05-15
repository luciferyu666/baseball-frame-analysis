import os
from loguru import logger logger.add("logs/{time}.log", rotation="12 MB", retention="10 days")
