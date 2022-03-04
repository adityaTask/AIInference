import inspect
import logging

def customLogger(log_level=logging.DEBUG):
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("automation.log",mode='a')
    file_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s: -%(name)s - %(levelname)s: %(message)s',
                                        datefmt='%m/%d/%Y %I:%M:%S %p')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
