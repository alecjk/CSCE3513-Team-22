import tkinter as tk
from tkinter import ttk
from MVC.model.database.DB import *
from MVC.app.ApplicationObj import *
from MVC.view.entryTerminal.teamBox import *
from MVC.controller.entryTerminalController import *
import pygame
import random



class ScreenEntryTerminal(AppObject):
    INDEX_PINFO_ID = 0
    INDEX_PINFO_FNAME = 1
    INDEX_PINFO_LNAME = 2
    INDEX_PINFO_CODE = 3
    PLAYERSELECT = 0
    PLAYERNAME = 1
    PLAYERCODENAME = 2


    def __init__(self, tkRoot, f):
        super().__init__(tkRoot)
        self.database = Database()
        self.createScreen()
        self.gridify()
        self.switchToPlayAction = f
        self.switchToDisplay()
        self.hide()

    def createScreen(self):
        self["bg"] = "#063459"

        self.createTeamBoxes()
        self.createLabelFooter()
        self.createDisplayManager()
        self.creatStartGameButton()


    def bind_StartGame(self):
        self.switchToPlayAction()
        pygame.mixer.init()
        trackChar = str(random.getrandbits(3) + 1)
        print("Playing Track " + trackChar)
        pygame.mixer.music.load("resources\photon_tracks\Track0" + trackChar + ".mp3")
        pygame.mixer.music.play()
        
        

    def creatStartGameButton(self):
        strBGColor = "#28CA00"
        strTextcolorMain = "#FFFFFF"
        strFont = self.strDefaultFont
        intTextsizeMain = 48

        self.buttonSubmit = tk.Button(self,
                                      text="Start Game",
                                      command=self.bind_StartGame,
                                      state="normal",
                                      fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.buttonSubmit.bind("<Return>", self.bind_StartGame)

    def createPageHeader(self):
        strTextColor = "#5b5bc3"
        strBGColor = "#000000"
        strFontStyle = self.strDefaultFont
        intFontSize = 25

        self.labelEditGame = tk.Label(self, text="Edit Current Game", fg=strTextColor, bg=strBGColor,
                                      font=(strFontStyle, intFontSize))
        self.propagateWidget(self.labelEditGame)

    def createTeamBoxes(self):
        self.frameTeamBoxes = Frame_TeamBoxes(self)
        self.propagateWidget(self.frameTeamBoxes)

    def createLabelFooter(self):
        strTextColor = "#000000"
        strBGColor = "#d9d9d9"
        strFontStyle = self.strDefaultFont
        strFontSize = 14

        self.labelFooter = tk.Label(self, text="<Ins> Insert Player or Edit <Del> Delete player", fg=strTextColor, bg=strBGColor, font=(strFontStyle, strFontSize))
        self.propagateWidget(self.labelFooter)

    def createDisplayManager(self):
        self.displayManager = entryTerminalController(self)
        self.displayManager.setDatabase(self.database)
        self.displayManager.setTeamBoxes(self.frameTeamBoxes)
        self.displayManager.createSelf()

    def gridify(self):
        intMainFrameCols = 24
        intMainFrameRows = 42

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky="NSEW")
        self.displayManager.grid(column=6, row=8, columnspan=12, rowspan=20, sticky="NSEW")
        self.displayManager.gridify()

        for i in range(intMainFrameCols):
            self.columnconfigure(i, weight=1, uniform="gridUniform")
        for i in range(intMainFrameRows):
            self.rowconfigure(i, weight=1, uniform="gridUniform")



        self.frameTeamBoxes.grid(column=2, row=2, columnspan=20, rowspan=31, sticky="NSEW")
        self.frameTeamBoxes.gridify()
        self.frameTeamBoxes.show()
        self.buttonSubmit.grid(column=10, row=35, columnspan=5, rowspan=4, sticky="NSEW")
        self.labelFooter.grid(column=0, row=41, columnspan=24, rowspan=1, sticky="NSEW")

    def getDisplayState(self):
        return self.displayManager.getDisplayState()

    def getPlayerIDList(self):
        return self.frameTeamBoxes.getPlayerIDList()

    def getPlayerList(self):
        return self.frameTeamBoxes.getPlayerList()

    def closeDB(self):
        print("Closing DB...")
        self.database.deleteAllRows()
        self.database.closeDB_NoCommit()

    def moveArrow(self, intOffsetX, intOffsetY):
        if self.frameTeamBoxes.isValidArrowOffset(intOffsetX, intOffsetY):
            self.frameTeamBoxes.moveArrow(intOffsetX, intOffsetY)
            self.root.update()

    def getPlayerAtArrow(self):
        return self.frameTeamBoxes.getPlayerAtArrow()

    def openAddPlayerID(self):
        self.displayManager.openAddPlayerID()

    def openAddPlayerName(self):
        self.displayManager.openAddPlayerName()

    def closeAllMenus(self):
        self.displayManager.closeAllMenus()

    def closeAllDisplays(self):
        self.displayManager.closeAllDisplays()

    def openAddCodename(self):
        self.displayManager.openAddCodename()

    def switchToDisplay(self):
        self.displayManager.switchToMainDisplay()

    def addPlayer(self, strPlayer, strCode):
        self.frameTeamBoxes.addPlayer(strPlayer, strCode)
        self.root.update()

    def deletePlayer(self, event=None):
        self.frameTeamBoxes.deletePlayer()
        self.root.update()





