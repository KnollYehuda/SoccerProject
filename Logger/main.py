import logging
import sys
import os
import datetime

# this function will handle writing to log file,in specific format
# format: DATE, TIME, log.LEVEL, message


def loggerHandler(log_filename):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(log_filename, mode='a', encoding=None, delay=False)
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    ret_val_logger = logging.getLogger('Logger')
    ret_val_logger.setLevel(logging.DEBUG)
    ret_val_logger.addHandler(handler)
    ret_val_logger.addHandler(screen_handler)
    return ret_val_logger


# main function: setup_logger
# function get log name FIXME("create constant string for log name")
# function returning log object that will write to log
# Example : logger = setup_logger(log_filename)
# logger.info("Hello World")
# The logic: create log file at the current directory if log file doesn't exist.
#            else write the log to current directory and move old log to history


def setup_logger(name):
    if not os.path.exists(name):    # checking whether there is a log file already
        return loggerHandler(name)

    else:
        directory = "history"
        old_name = name + datetime.datetime.now().strftime('%m%d-%H%M%S')
        abs_dir = os.getcwd() + os.sep + directory   # os.getcwd() --> current root dir
        if not os.path.exists(abs_dir):
            os.makedirs(directory)

        os.rename(os.getcwd() + os.sep + name, os.getcwd() + os.sep + directory + os.sep + old_name)
        return loggerHandler(name)


# logger = setup_logger("logger.log")
# logger.debug(datetime.datetime.now().strftime('%m%d-%H%M%S'))
# logger.info(datetime.datetime.now().strftime('%m%d-%H%M%S'))


# log level information
# DEBUG: Detailed information, typically of interest only when diagnosing problems.

# INFO: Confirmation that things are working as expected.

# WARNING: An indication that something unexpected happened,
#          or indicative of some problem in the near future (e.g. ‘disk space low’).
#          The software is still working as expected.

# ERROR: Due to a more serious problem, the software has not been able to perform some function.

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
