import logging
import logging.handlers

def getLogger(logger_name, use_syslog):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    cf = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(cf)
    logger.addHandler(ch)

    if use_syslog:
        # Address is /dev/log on Ubuntu, might be different on others
        sh = logging.handlers.SysLogHandler(address="/dev/log", facility="local0")
        sh.setLevel(logging.DEBUG)
        sf = logging.Formatter("%(name)s[%(process)d] - %(levelname)s - %(message)s")
        sh.setFormatter(sf)
        logger.debug("configured writing to syslog")
        logger.addHandler(sh)

    return logger

