def get_module_logger(LOG_NAME = '', LOG_FILE_INFO  = 'file.log', LOG_FILE_ERROR = 'file.err'):
  
    LOG_FORMAT     = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    log           = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)

    # comment this to suppress console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    log.addHandler(stream_handler)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.DEBUG)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.DEBUG)

    return log

def main():

    my_logger = get_logger()

    my_logger.info('This is an INFO message')
    my_logger.warning('This is a WARNING message')
    my_logger.error('This is an ERROR message')


if __name__ == '__main__':
    main()
