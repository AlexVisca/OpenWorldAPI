import logging

def config():
    logging.basicConfig(
        filename="logs/server.log", 
        filemode='w', 
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s]:\t%(message)s")
    # --
    logger = logging.getLogger(__name__)
    return logger
