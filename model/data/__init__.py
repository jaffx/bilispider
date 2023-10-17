import logging
from libs.init import *


class dataLayerBase:
    logger = logging.getLogger("data logger")

    def __init__(self):
        pass


fileHandler = logging.FileHandler("log/data.log")
fileHandler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
fileHandler.setLevel(logging.WARNING)
dataLayerBase.logger.addHandler(fileHandler)
