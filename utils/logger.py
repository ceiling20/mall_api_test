import logging
import sys
from pathlib import Path
LOG_DIR = Path(__file__).parent.parent/"logs"
LOG_DIR.mkdir(exist_ok=True)
def get_logger(name = "api_test"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        #控制台 handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_fmt = "%(asctime)s | %(levelname)s | %(message)s"
        console_handler.setFormatter(logging.Formatter(console_fmt,datefmt = "%H:%M:%S"))
        logger.addHandler(console_handler)

        #文件handler
        file_handler = logging.FileHandler(LOG_DIR / "test.log" , encoding="utf-8")
        file_fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        file_handler.setFormatter(logging.Formatter(file_fmt))
        logger.addHandler(file_handler)
    return logger