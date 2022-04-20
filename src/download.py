import gdown
import logging


def download(url):
    logger = logging.getLogger("medshot")
    logger.info("Downloading model: " + url)
    output = 'resources/model.h5'
    gdown.download(url, output, quiet=False)
    logger.info("Downloaded model: " + output)
