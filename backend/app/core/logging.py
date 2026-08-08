import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging():
    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    logHandler.setFormatter(formatter)
    
    logger = logging.getLogger("swibit")
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    
    return logger


logger = setup_logging()