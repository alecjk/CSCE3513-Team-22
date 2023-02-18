import tkinter as tk
from tkinter import ttk
from MVC.model.database.DB import *
from MVC.app.ApplicationObj import *
from MVC.view.playerEntry.teamBox import *
from MVC.controller.playerEntryController import *


class UI_EditGame(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)

        self.createScreen()
        self.gridify()
        self.switchToMainMenu()
        self.hideSelf()

    def createScreen(self):
        self["bg"] = "#000000"
        self.createHeader()
        self.createTeamBoxes()
        self.createFKeys()
        self.createLabelFooter()

    def createHeader(self):
        TextColor = "#5b5bc3"  # Light, purplish blue
        BGColor = "#000000"  # Black
        self.labelEditGame = tk.Label(self, text="Edit Current Game", fg=TextColor, bg=BGColor,
                                      font=(self.strDefaultFont, 25))
        self.propagateWidget(self.labelEditGame)

    def createTeamBoxes(self):
        self.frameTeamBoxes = Frame_TeamBoxes(self)
        self.propagateWidget(self.frameTeamBoxes)

    def createFKeys(self):
        self.frameFKeys = Frame_FKeys(self)
        self.frameFKeys.clearAllKeyText()
        self.frameFKeys.setKeyText(5, "F5 \nMove to \nPlay")
        self.frameFKeys.setKeyText(7, "F7 \nDelete DB \nEntries")
        self.frameFKeys.setKeyText(12, "F12 \nClear \nGame")
        self.frameFKeys.setKeyText(10, "10 \nFlick \nSync")

    def createLabelFooter(self):
        TextColor = "#000000"  # Black
        BGColor = "#d9d9d9"  # Very light gray, almost white

        self.labelFooter = tk.Label(self,
                                    text="<Del> to delete player, <Ins> to Manually Insert, or edit codename",
                                    fg=TextColor, bg=BGColor, font=(self.strDefaultFont, 14))
        self.propagateWidget(self.labelFooter)

    # Intended to be used after gridify()
    def setMenuManagerOntoGrid(self, menuManagerFrame):
        self.menuManager.grid(column=6, row=8, columnspan=12, rowspan=20, sticky="NSEW")
        self.menuManager.gridify()

    def gridify(self):
        # If either of below are edited, all widgets will need to be repositioned
        # i.e: All calls to grid with row/column updated
        intMainFrameCols = 24
        intMainFrameRows = 42
        # Position F Key - Row
        intPosFKeyRow = 35
        intFKeyRowSpan = 6
        intFKeyColSpan = 2

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
        self.frameTeamBoxes.showSelf()

        self.frameFKeys.grid(column=0, row=intPosFKeyRow, rowspan=intFKeyRowSpan, columnspan=intMainFrameCols,
                             sticky="NSEW")
        self.frameFKeys.gridify()

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

    def clearAllPlayers(self):
        self.frameTeamBoxes.deleteAllPlayers()
        self.root.update()