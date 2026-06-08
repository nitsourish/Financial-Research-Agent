#src/utils/logger.py
import logging
from config import Config

LOG_LEVEL = Config.LOG_LEVEL

def set_logger():
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(filename='finance_reacherch.log'),
            logging.StreamHandler()
        ]
        
    )
    return logging.getLogger('finance_reacherch')