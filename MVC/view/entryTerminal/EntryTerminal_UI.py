import tkinter as tk
from tkinter import ttk
from MVC.model.database.DB import *
from MVC.app.ApplicationObj import *
from MVC.view.entryTerminal.teamBox import *
from MVC.controller.entryTerminalController import *


class UI_EditGame(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)

        self.createScreen()
        self.gridify()
        self.switchToMainMenu()
        self.hide()

    def createScreen(self):
        self["bg"] = "#000000"
        self.createHeader()
        self.createTeamBoxes()
        self.createFKeys()
        self.createLabelFooter()

    def createHeader(self):
        TextColor = "#5b5bc3"
        BGColor = "#000000"
        self.labelEditGame = tk.Label(self, text="Edit Current Game", fg=TextColor, bg=BGColor,
                                      font=(self.strDefaultFont, 25))
        self.proWidget(self.labelEditGame)

    def createTeamBoxes(self):
        self.frameTeamBoxes = Frame_TeamBoxes(self)
        self.proWidget(self.frameTeamBoxes)


    def createLabelFooter(self):
        TextColor = "#000000"
        BGColor = "#d9d9d9"

        self.labelFooter = tk.Label(self,
                                    text="<Ins> Insert Player or Edit <Del> Delete player,",
                                    fg=TextColor, bg=BGColor, font=(self.strDefaultFont, 14))
        self.proWidget(self.labelFooter)


    def gridify(self):
        intMainFrameCols = 24
        intMainFrameRows = 42

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky="NSEW")

        for i in range(intMainFrameCols):
            self.columnconfigure(i, weight=1, uniform="gridUniform")
        for i in range(intMainFrameRows):
            self.rowconfigure(i, weight=1, uniform="gridUniform")

        self.labelEditGame.grid(column=0, row=0, columnspan=24, rowspan=2, sticky="SEW")
        self.frameTeamBoxes.grid(column=2, row=2, columnspan=20, rowspan=31, sticky="NSEW")
        self.frameTeamBoxes.gridify()
        self.frameTeamBoxes.show()
        self.labelFooter.grid(column=0, row=41, columnspan=24, rowspan=1, sticky="NSEW")

    def getPlayerList(self):
        return self.frameTeamBoxes.getPlayerList()

    def moveArrow(self, intOffsetX, intOffsetY):
        if self.frameTeamBoxes.isValidArrowOffset(intOffsetX, intOffsetY):
            self.frameTeamBoxes.moveArrow(intOffsetX, intOffsetY)
            self.root.update()

    def getPlayerAtArrow(self):
        return self.frameTeamBoxes.getPlayerAtArrow()

    def addPlayer(self, Player, Code):
        self.frameTeamBoxes.addPlayer(Player, Code)
        self.root.update()

    def deletePlayer(self, event=None):
        self.frameTeamBoxes.deletePlayer()
        self.root.update()
