import logging
def get_logger(name = "api_test"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%(asctime)s | %(levelname) | %(message)s"
        handler.setFormatter(logging.Formatter(fmt,datefmt = "%H:%M:%S"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger