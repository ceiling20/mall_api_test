import logging
import sys
def get_logger(name = "api_test"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        fmt = "%(asctime)s | %(levelname)s | %(message)s"
        handler.setFormatter(logging.Formatter(fmt,datefmt = "%H:%M:%S"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger