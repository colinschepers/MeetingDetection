import os
from database import mockdata
from logger import logger


mockdata.create_mockdata()

logger.debug('hello world')
