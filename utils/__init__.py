import logging.handlers

def getlogger(mod_name:str, filepath:str, level=logging.INFO, propagate=False, maxBytes=10*1024*1024):
    logger = logging.getLogger(mod_name)
    logger.setLevel(level)
    logger.propagate = propagate # 阻止传递到父logger

    handler = logging.handlers.RotatingFileHandler(filepath, maxBytes=maxBytes, backupCount=5)
    handler.setLevel(level)

    formater = logging.Formatter(fmt='%(asctime)s %(levelname)s [%(name)s %(funcName)s] %(message)s')
    handler.setFormatter(formater)
    logger.addHandler(handler)

    return logger

if __name__ == '__main__':
    logger = getlogger('hello', 'text.log', maxBytes=10*1024)
    import time
    for i in range(1000):
        time.sleep(0.001)
        logger.info("i={}".format(i))

