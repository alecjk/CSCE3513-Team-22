class AppState:
    S_SPLASH = 0
    S_EDITGAME = 1

    def __init__(self, state=None):
        self.state = self.S_SPLASH

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state