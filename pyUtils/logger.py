import logging
import sys


def get_module_logger(mod_name):
  logger = logging.getLogger(mod_name)
  handler = logging.StreamHandler(stream=sys.stdout)
  formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)
  return logger
