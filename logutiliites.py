import logging

class LogUtilities:
    LOG_NAME = "unhinged".upper()
    LOG_FILE = "unhinged.log"
    log = logging.getLogger(LOG_NAME)
    log.setLevel(logging.DEBUG)

    def __init__(self):
        formatter = logging.Formatter("%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

        # Log to file
        filehandler = logging.FileHandler(self.LOG_FILE, "w")
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        self.log.addHandler(filehandler)

        # Log to stdout too
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.INFO)
        streamhandler.setFormatter(formatter)
        self.log.addHandler(streamhandler)