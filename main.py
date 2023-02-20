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
        self.root.title("Entry Terminal")
        self.root.geometry("1200x800+0+0") 
        self.root.minsize(1000, 700)

        print("Platform: {}".format(platform))
        if platform == "win32" or platform == "win64" or platform == "win82":
            self.root.state("zoomed")
        else:
            self.root.wm_attributes('-zoomed', 1)
        self.propagateWidget(self.root)

        self.gridConfigure()


        self.appMembers()

        self.appState.setState(AppState.splash)
        self.screen = self.screen_Splash
        self.changeScreens(AppState.splash)
        self.startInputListener()
        self.root.update()
        print("Showing Splash Screen for 3 seconds...")
        self.idRootAfter = self.root.after(3000, self.SplashFor3Secs)

    def appMembers(self):
        self.screen_Splash = Screen_Splash(self)
        self.screen_Splash.grid(column=0, row=0, sticky="NSEW")
        self.screen_EntryTerminal = ScreenEntryTerminal(self)
        self.screen_EntryTerminal.grid(column=0, row=0, sticky="NSEW")


        self.appState = AppState()
        self.appState.setState(AppState.splash)
        self.inputListener = Listener()
        self.inputListener.combiningAppWithScreens(self.screen_Splash, self.screen_EntryTerminal, self.appState)

    def gridConfigure(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self["bg"] = "#000000"
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky="NSEW")

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
            print("Switching from unknown screen")

    def loadScreen(self, nextScreen):
        if nextScreen == AppState.splash:
            print("Loading Splash...")
            self.appState.setState(AppState.splash)
            self.loadScreen_Splash()
        elif nextScreen == AppState.entryTerminal:
            print("Loading Entry Terminal...")
            self.appState.setState(AppState.entryTerminal)
            self.loadScreen_EditGame()
        else:
            print("No Screen")

    def loadScreen_Splash(self):
        self.screen = self.screen_Splash
        self.screen.show()

    def unloadScreen_Splash(self):
        self.screen.hide()

    def loadScreen_EditGame(self):
        self.screen = self.screen_EntryTerminal
        self.screen.show()
        self.screen.tkraise()


    def SplashFor3Secs(self):
        self.root.after_cancel(self.idRootAfter)
        self.changeScreens(AppState.entryTerminal)

    def closeDB(self):
        if self.screen_EntryTerminal == None:
            print("Closing DB...")
            self.database.closeDB_NoCommit()
        else:
            self.screen_EntryTerminal.closeDB()

    def startInputListener(self):
        self.inputListener.start()


def driver_TK():
    tkRoot = tk.Tk()
    app = App(tkRoot)
    app.mainloop()
    app.closeDB()


if __name__ == "__main__":
    driver_TK()
