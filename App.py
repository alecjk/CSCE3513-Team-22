import tkinter as tk
from tkinter import ttk


class AppState:
    splash = 0
    playerScreen = 1
    gameScreen = 2

    def __init__(self, state=None):
        self.state = self.splash

    def setState(self, state):
        if state >= self.splash and state <= self.gameScreen:
            self.state = state
            return True
        else:
            return False

    def getState(self):
        return self.state


class AppObject(tk.Frame):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.root = tkRoot
        self.setDefaults()

    # Size control - prevent widget from over-expanding outside grid cell
    # This should be applied to most widgets
    def propagateWidget(self, widget):
        widget.pack_propagate(False)
        widget.grid_propagate(False)

    def setDefaults(self):
        self.strDefaultFont = "Arial"
        self["bg"] = "#000000"

    def hideSelf(self):
        self.grid_remove()

    def showSelf(self):
        self.grid()
        self.tkraise()
