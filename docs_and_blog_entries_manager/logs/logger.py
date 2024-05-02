import logging

logging.basicConfig(format='%(asctime)s - %(name)s [%(levelname)s] %(message)s', level=logging.DEBUG)


class Logger:
    @staticmethod
    def debug(message):
        logging.debug(message)

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def warn(message):
        logging.warning(message)

    @staticmethod
    def error(message):
        logging.error(message)
