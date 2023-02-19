class AppState:
    splash = 0
    entryTerminal = 1

    def __init__(self, state=None):
        self.state = self.splash

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state