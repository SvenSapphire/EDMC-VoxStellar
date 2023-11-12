import logging
from os import path

from config import appname


class Debug:
    logger = None

    def __init__(self, voxstellar):
        Debug.logger = logging.getLogger(f'{appname}.{path.basename(voxstellar.plugin_dir)}')

        if not Debug.logger.hasHandlers():
            level = logging.INFO

            Debug.logger.setLevel(level)
            logger_channel = logging.StreamHandler()
            logger_formatter = logging.Formatter(
                f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
            logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
            logger_formatter.default_msec_format = '%s.%03d'
            logger_channel.setFormatter(logger_formatter)
            Debug.logger.addHandler(logger_channel)
