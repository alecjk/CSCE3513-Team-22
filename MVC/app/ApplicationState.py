class AppState:
    splash = 0
    entryTerminal = 1
    playAction = 2

    def __init__(self, state=None):
        self.state = self.splash

    def setState(self, state):
        if state >= self.splash and state <= self.playAction:
            self.state = state
            return True
        else:
            return False
    def getState(self):
        return self.state