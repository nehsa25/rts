class Player(object):
    selected_race = None
    army = []
    log_utils = None

    def __init__(self, log_utils):
        self.log_utils = log_utils
        self.log_utils.log.debug("Initializing Player() class")
