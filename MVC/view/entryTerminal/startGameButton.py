import tkinter as tk
from tkinter import ttk
from MVC.view.display import *

class Display_startGameButton(Display):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)

        strBGColor = "#FFFFFF"
        strTextcolorError = "#FF0000"
        strTextcolorMain = "#FFFFFF"
        strDefaultFont = "Serif"
        intTextsizeHead = 20
        intTextsizeError = 14
        intTextsizeHint = 15
        intTextsizeMain = 16
        self.frameInsPInterior = tk.Frame(self, bg=strBGColor)

        buttonStartGame = tk.Button(self.frameInsPInterior,
                                            text="Start Game",
                                            command=self.switchDisplay,
                                            state="disabled",
                                            fg=strTextcolorMain, bg=strBGColor, font=(self.strDefaultFont, intTextsizeMain)
                                            )
                                            
        #self.buttonStartGame.bind("<Return>", self.addPlayerFromMenu)

        def gridify(self):

            intBorderSize = 10
            self.frameInsPInterior.pack(side="top", fill="both", expand=True,
                                        padx=intBorderSize, pady=intBorderSize)
        
            self.buttonStartGame.grid(column=1, row=50, rowspan=2, columnspan=2, sticky="NSEW")
        
    def switchDisplay(self, event=None):
        print("YOURE PRESSING THE BUTTON")