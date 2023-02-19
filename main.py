from sys import platform
from MVC.view.entryTerminal.screenEntryTerminal import *
from MVC.view.splash.splash import *
from MVC.app.ApplicationState import *
from MVC.controller.Listener import *


class App(tk.Frame):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.root = tkRoot
        self.root.configure(background="#000000")

        # Root Window
        self.root.title("Entry Terminal")
        self.root.geometry("1200x800+0+0") 
        self.root.minsize(1000, 700)  # Minimum size of window is 1200x700 before scrunching
        # self.root.resizable(False, False)

        print("Running for platform: {}".format(platform))
        if platform == "win32" or platform == "win64" or platform == "win82":
            self.root.state("zoomed")
        else:
            self.root.wm_attributes('-zoomed', 1)
        self.propagateWidget(self.root)

        self.gridConfigure()

        # Needed for bug with F10 key.
        self.inputSim = keyboard.Controller()

        self.appMembers()

        self.appState.setState(AppState.splash)
        self.screen = self.screen_Splash
        self.changeScreens(AppState.splash)
        self.startInputListener()
        self.root.update()
        print("Waiting 3 seconds...")
        self.idRootAfter = self.root.after(3000, self.showSplashFor3Sec)

    def appMembers(self):
        # App members
        # I moved this into it's own function just for the sake of separating things and clarity. -Mason Woodward
        self.screen_Splash = Screen_Splash(self)
        self.screen_Splash.grid(column=0, row=0, sticky="NSEW")
        self.screen_EditGame = Screen_EditGame(self)
        self.screen_EditGame.grid(column=0, row=0, sticky="NSEW")


        self.appState = AppState()
        self.appState.setState(AppState.splash)
        self.inputListener = Listener()
        self.inputListener.combiningAppWithScreens(self.screen_Splash, self.screen_EditGame, self.appState)

    def gridConfigure(self):
        # Using grid instead of pack to allow frame-on-frame for
        #    inserting player menu, and other similar menus
        # Put this into it's own function for the sake of separation and clarity
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self["bg"] = "#000000"
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky="NSEW")

    # Size control - prevent widget from over-expanding outside grid cell
    # This should be applied to most widgets
    def propagateWidget(self, widget):
        widget.pack_propagate(0)
        widget.grid_propagate(0)

    def changeScreens(self, nextScreen):
        self.unloadCurrentScreen()
        self.loadScreen(nextScreen)
        self.root.update()




    def unloadCurrentScreen(self):
        if self.appState.getState() == AppState.splash:
            self.unloadScreen_Splash()
        elif self.appState.getState() == AppState.entryTerminal:
            self.unloadScreen_EditGame()
        elif self.appState.getState() == AppState.S_PLAYGAME:
            self.unloadScreen_PlayGame()
        else:
            print("Changing from unknown screen")

    def loadScreen(self, nextScreen):
        if nextScreen == AppState.splash:
            print("Loading Splash...")
            self.appState.setState(AppState.splash)
            self.loadScreen_Splash()
        elif nextScreen == AppState.entryTerminal:
            print("Loading Edit Game...")
            self.appState.setState(AppState.entryTerminal)
            self.loadScreen_EditGame()
        else:
            print("Not a valid screen!")

    def loadScreen_Splash(self):
        self.screen = self.screen_Splash
        self.screen.show()

    def unloadScreen_Splash(self):
        self.screen.hide()

    def loadScreen_EditGame(self):
        self.screen = self.screen_EditGame
        self.screen.show()
        self.screen.tkraise()


    def showSplashFor3Sec(self):
        print("3 seconds finished.")
        self.root.after_cancel(self.idRootAfter)
        self.changeScreens(AppState.entryTerminal)

    def closeDB(self):
        if self.screen_EditGame == None:
            print("Closing DB...")
            self.database.closeDB_NoCommit()
        else:
            self.screen_EditGame.closeDB()

    def startInputListener(self):
        self.inputListener.start()


def driver_TK():
    tkRoot = tk.Tk()
    app = App(tkRoot)
    app.mainloop()
    app.closeDB()


if __name__ == "__main__":
    driver_TK()
