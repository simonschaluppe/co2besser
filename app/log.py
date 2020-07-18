import logging


##########
### LOGGING
##########

def configure_logger(LOG_FORMAT='%(levelname)-8s | %(asctime)s | %(filename)-12s | %(message)s',
                     LOG_TO_CONSOLE=False,
                     LOG_TO_FILE=False,
                     LOG_FILE_PATH="logs\db_utils.log"):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT,
                                  datefmt='%d-%m %H:%M')
    if LOG_TO_FILE:
        handler = logging.FileHandler(filename=LOG_FILE_PATH,
                                      mode='a',
                                      encoding="utf-8")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    if LOG_TO_CONSOLE:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger
