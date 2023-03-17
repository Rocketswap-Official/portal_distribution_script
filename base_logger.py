import logging

logger = logging
logger.basicConfig(
    # filename="log.txt",
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)