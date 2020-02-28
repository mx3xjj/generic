import logging
import traceback

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logger = logging.getLogger("test")
logger_formatter = logging.Formatter(LOG_FORMAT)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logger_formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

# log error with traceback
try:
    raise ValueError('test error')
except Exception as err:
    t = err

# with native logger funcs
logger.exception(t)     # exception allows log all the traceback
logger.info(t)
logger.info(t, exc_info=True)    # other log level could hace traceback logged with exec_info=True)

# with custom logging info
def format_error_msg(err, with_traceback=False):
    error_msg = traceback.format_exception_only(err.__class__, err)
    if with_traceback:
        error_msg = traceback.format_exception(err.__class__, err, err.__traceback__)
    return "".join(error_msg).strip()
logger.debug('runing failed with error: {}'.format(format_error_msg(t)))
logger.debug('runing failed with error: {}'.format(format_error_msg(t, with_traceback=True)))
