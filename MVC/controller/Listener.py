from pynput import keyboard
from MVC.app.ApplicationState import *
from MVC.view.entryTerminal.screenEntryTerminal import *
from MVC.view.splash.splash import *


def on_release(key):
    return True


class Listener:
    def __init__(self):
        self.appState = None
        self.screenPlayAction = None
        self.screenPlayerEntry = None
        self.screenSplash = None
        self.listener = None

    def combiningAppWithScreens(self, splash, playerEntry, playAction ,appState):
        self.screenSplash = splash
        self.screenPlayerEntry = playerEntry
        self.screenPlayAction = playAction
        self.appState = appState



    def start(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=on_release)
        self.listener.start()

    def playerIns(self, key):
        if key == keyboard.Key.esc:
            self.screenPlayerEntry.closeAllDisplays()

    def on_press(self, key):
        if self.appState.getState() == AppState.entryTerminal:
            if self.screenPlayerEntry.getDisplayState() == self.screenPlayerEntry.PLAYERSELECT:
                self.playerSelect(key)
            elif self.screenPlayerEntry.getDisplayState() != self.screenPlayerEntry.PLAYERSELECT:
                self.playerIns(key)

    def playerSelect(self, key):
        if key == keyboard.Key.up:
            self.screenPlayerEntry.moveArrow(0, -1)
        elif key == keyboard.Key.down:
            self.screenPlayerEntry.moveArrow(0, 1)
        if key == keyboard.Key.left:
            self.screenPlayerEntry.moveArrow(-1, 0)
        elif key == keyboard.Key.right:
            self.screenPlayerEntry.moveArrow(1, 0)
        if key == keyboard.Key.insert:
            self.screenPlayerEntry.openAddPlayerID()
        if key == keyboard.Key.delete:
            self.screenPlayerEntry.deletePlayer()











