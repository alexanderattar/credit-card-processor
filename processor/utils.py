
import sys
import logging

LOGGER_DISABLED = False  # convenience for testing

loggers = {}


def setup_logger(name):
    global loggers
    if loggers.get(name):
        return loggers.get(name)
    else:
        log = logging.getLogger(name)
        out_hdlr = logging.StreamHandler(sys.stdout)
        out_hdlr.setFormatter(logging.Formatter('%(asctime)s - %(levelname)7s - %(message)s', '%Y-%m-%d %H:%M'))
        out_hdlr.setLevel(logging.INFO)
        log.addHandler(out_hdlr)
        log.setLevel(logging.INFO)
        log.disabled = LOGGER_DISABLED
        loggers.update(dict(logger=log))
    return log
