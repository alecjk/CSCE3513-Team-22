from MVC.app.ApplicationObj import *


class Menu(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)

    def destroyMain(self):
        self.destroy()

    def openSelf(self):
        self.show()
        self.enableSelf()

    def closeSelf(self):
        self.hide()
        self.disableSelf()
