import random
from pynput import keyboard
from MVC.app.ApplicationState import *
from MVC.view.playerEntry.screenPlayerEntry import *
from MVC.view.splash.splash import *


class InputListener:
    def __init__(self):
        self.listener = None
        # Needed for bug with F10 key.
        self.inputSim = keyboard.Controller()

    def bindAllScreensAndAppState(self, splash, edit, appState):
        self.screen_Splash = splash
        self.screen_EditGame = edit
        self.appState = appState

    def start(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()

    def isRunning(self):
        return self.listener != None

    def on_release(self, key):
        return True

    def on_press(self, key):
        if self.appState.getState() == AppState.S_EDITGAME:
            if self.screen_EditGame.getMenuState() == self.screen_EditGame.PLAYERSELECT:
                self.editgame_PlayerSelect(key)
            elif self.screen_EditGame.getMenuState() != self.screen_EditGame.PLAYERSELECT:
                self.editgame_PlayerIns(key)
        elif self.appState.getState() == AppState.S_SPLASH:
            pass

    def editgame_PlayerSelect(self, key):
        if key == keyboard.Key.up:
            self.screen_EditGame.moveArrow(0, -1)
        elif key == keyboard.Key.down:
            self.screen_EditGame.moveArrow(0, 1)
        if key == keyboard.Key.left:
            self.screen_EditGame.moveArrow(-1, 0)
        elif key == keyboard.Key.right:
            self.screen_EditGame.moveArrow(1, 0)

        if key == keyboard.Key.insert:
            self.screen_EditGame.openAddPlayerID()
        if key == keyboard.Key.delete:
            self.screen_EditGame.deletePlayer()

        if key == keyboard.Key.f4:
            self.screen_EditGame.openDebugFillPlayers()
        if key == keyboard.Key.f5:
            self.screen_EditGame.openMoveToPlayConfirm()

        if key == keyboard.Key.f7:
            self.screen_EditGame.openDeleteDBConfirmMenu()

    def editgame_PlayerIns(self, key):
        if key == keyboard.Key.esc:
            self.screen_EditGame.closeAllMenus()




