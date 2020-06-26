import logging
import os

from Config import Conf
from logging.handlers import TimedRotatingFileHandler

'''
@author Asiri Hewage
date : 31 May 2020
Class : Logger
Objective : Manage log rotation and log levels
'''


class Logger:

    def __init__(self):
        # initiating ConfigParser
        self.config = Conf()

        try:
            if not os.path.exists(self.config.get_configs('LOGGER', 'logger_path')):
                os.mkdir(self.config.get_configs('LOGGER', 'logger_path'))
        except Exception as er:
            pass

        self.path = self.config.get_configs('LOGGER', 'logger_path')

        self.logger = logging.getLogger("Migrator")
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(funcName)s | %(message)s')

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        handler = TimedRotatingFileHandler(self.path, when="d", interval=1, backupCount=5)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

        aps_logger = logging.getLogger('apscheduler.scheduler')
        aps_logger.addHandler(handler)
        aps_logger.addHandler(ch)
        aps_logger.setLevel(logging.DEBUG)

    def info(self, logstr):
        self.logger.info(logstr)

    def log(self, logstr):
        self.logger.log(logstr)

    def debug(self, logstr):
        self.logger.debug(logstr)

    def error(self, logstr):
        self.logger.error(logstr)




