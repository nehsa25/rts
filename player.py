class Player:
    selected_race = None
    army = []
    logutils = None

    def __init__(self, logutils):
        self.logutils = logutils
        self.logutils.log.debug("Initializing Player() class")
        
