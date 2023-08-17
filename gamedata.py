
class GameData:
    logutils = None
    selected_units = []

    Player = None
    def __init__(self, logutils):

        self.Player = GameData.Player(logutils)

    class Player:
        selected_race = None
        army = []
        logutils = None

        def __init__(self, logutils):
            self.logutils = logutils
            self.logutils.log.debug("Initializing Player() class")
            
