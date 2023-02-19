import tkinter as tk
from MVC.app.ApplicationObj import *


class Screen_Splash(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.root = tkRoot

        self.createScreen()
        self.gridify()

    def createScreen(self):
        '''create splash screen'''
        strBGColor = "#000000"

        self.mainFrame = tk.Frame(self,
                                  bg=strBGColor)
        self.proWidget(self.mainFrame)
        self.imgSplash = tk.PhotoImage(file="resources/logo.png")
        self.labelSplash = tk.Label(self.mainFrame,
                                    image=self.imgSplash)

    def gridify(self):
        '''Expands image'''
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainFrame.grid(column=0, row=0, sticky="NSEW")
        self.labelSplash.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

