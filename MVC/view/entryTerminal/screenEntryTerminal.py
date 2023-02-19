import tkinter as tk
from MVC.model.database.DB import *
from MVC.app.ApplicationObj import *
from MVC.view.entryTerminal.teamBox import *
from MVC.controller.entryTerminalController import *


class Screen_EditGame(AppObject):
    INDEX_PINFO_ID = 0
    INDEX_PINFO_FNAME = 1
    INDEX_PINFO_LNAME = 2
    INDEX_PINFO_CODE = 3
    PLAYERSELECT = 0
    PLAYERNAME = 1
    ASKUSEPREVCODE = 2
    PLAYERCODENAME = 3
    DELETEDBCONFIRM = 4
    MOVETOPLAYCONFIRM = 5

    def __init__(self, tkRoot):
        super().__init__(tkRoot)

        self.database = Database()
        self.database.openConnection()

        self.createScreen()
        self.gridify()
        self.switchToMainMenu()
        self.hide()

    def createScreen(self):
        self["bg"] = "#000000"
        self.createPageHeader()
        self.createTeamBoxes()
        self.createLabelFooter()
        self.createMenuManager()

    def createPageHeader(self):
        strTextColor = "#5b5bc3"  # Light, purplish blue
        strBGColor = "#000000"  # Black
        strFontStyle = self.strDefaultFont
        intFontSize = 25

        self.labelEditGame = tk.Label(self, text="Edit Current Game", fg=strTextColor, bg=strBGColor,
                                      font=(strFontStyle, intFontSize))
        self.proWidget(self.labelEditGame)

    def createTeamBoxes(self):
        self.frameTeamBoxes = Frame_TeamBoxes(self)
        self.proWidget(self.frameTeamBoxes)

    def createLabelFooter(self):
        strTextColor = "#000000"  # Black
        strBGColor = "#d9d9d9"  # Very light gray, almost white
        strFontStyle = self.strDefaultFont
        strFontSize = 14

        self.labelFooter = tk.Label(self,
                                    text="<Del> to delete player, <Ins> to Manually Insert, or edit codename",
                                    fg=strTextColor, bg=strBGColor, font=(strFontStyle, strFontSize))
        self.proWidget(self.labelFooter)

    def createMenuManager(self):
        self.menuManager = entryTerminalController(self)
        self.menuManager.setDatabase(self.database)
        self.menuManager.setTeamBoxes(self.frameTeamBoxes)
        self.menuManager.createSelf()

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
        self.menuManager.grid(column=6, row=8, columnspan=12, rowspan=20, sticky="NSEW")
        self.menuManager.gridify()

        for i in range(intMainFrameCols):
            self.columnconfigure(i, weight=1, uniform="gridUniform")
        for i in range(intMainFrameRows):
            self.rowconfigure(i, weight=1, uniform="gridUniform")

        self.labelEditGame.grid(column=0, row=0, columnspan=24, rowspan=2, sticky="SEW")

        self.frameTeamBoxes.grid(column=2, row=2, columnspan=20, rowspan=31, sticky="NSEW")
        self.frameTeamBoxes.gridify()
        self.frameTeamBoxes.show()

        self.labelFooter.grid(column=0, row=41, columnspan=24, rowspan=1, sticky="NSEW")

    def getMenuState(self):
        return self.menuManager.getMenuState()

    def getPlayerIDList(self):
        return self.frameTeamBoxes.getPlayerIDList()

    def getPlayerList(self):
        return self.frameTeamBoxes.getPlayerList()

    def closeDB(self):
        print("Closing DB...")
        self.database.closeDB_NoCommit()

    def moveArrow(self, intOffsetX, intOffsetY):
        if self.frameTeamBoxes.isValidArrowOffset(intOffsetX, intOffsetY):
            self.frameTeamBoxes.moveArrow(intOffsetX, intOffsetY)
            self.root.update()

    def getPlayerAtArrow(self):
        return self.frameTeamBoxes.getPlayerAtArrow()

    def openDeleteDBConfirmMenu(self):
        self.menuManager.show()
        self.menuManager.openDeleteDBConfirmMenu()

    def bind_ChangeToPlay(self, mFunc):
        self.menuManager.bind_ChangeToPlay(mFunc)

    def openAddPlayerID(self):
        self.menuManager.openAddPlayerID()

    def openAddPlayerName(self):
        self.menuManager.openAddPlayerName()

    def closeAllMenus(self):
        self.menuManager.closeAllMenus()

    def openAddCodename(self):
        self.menuManager.openAddCodename()

    def openMoveToPlayConfirm(self):
        self.menuManager.show()
        self.menuManager.openMoveToPlayConfirm()

    def openDebugFillPlayers(self):
        self.menuManager.show()
        self.menuManager.openDebugFillPlayers()

    def switchToMainMenu(self):
        self.menuManager.switchToMainMenu()

    def addPlayer(self, strPlayer, strCode):
        self.frameTeamBoxes.addPlayer(strPlayer, strCode)
        self.root.update()

    def deletePlayer(self, event=None):
        self.frameTeamBoxes.deletePlayer()
        self.root.update()

    def clearAllPlayers(self):
        self.frameTeamBoxes.deleteAllPlayers()
        self.root.update()
