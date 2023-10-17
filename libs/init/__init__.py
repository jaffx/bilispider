import logging
import urllib3

urllib3.disable_warnings()

DEFAULT_LOG_FORMAT = "[%(levelname)s] <%(asctime)s> %(message)s (%(pathname)s %(lineno)d)"
fileHandler = logging.FileHandler("./log/biliSpider.log")
fileHandler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
fileHandler.setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=DEFAULT_LOG_FORMAT, handlers=[fileHandler])
