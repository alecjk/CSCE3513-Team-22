from MVC.model.database.DB import *
from MVC.app.ApplicationObj import *
from MVC.view.display_EntryBox import *
from MVC.model.entryTerminal.addPlayerName import *
from MVC.model.entryTerminal.addPlayerCodename import *
from MVC.view.entryTerminal.teamBox import *

class entryTerminalController(AppObject):
    INDEX_PLAYER_ID = 0
    INDEX_PLAYER_FIRST_NAME = 1
    INDEX_PLAYER_LAST_NAME = 2
    INDEX_PLAYER_CODE = 3
    PLAYERSELECT = 0
    PLAYERNAME = 1
    PLAYERCODENAME = 2
    PLAYERID = 3

    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.intDisplay = self.PLAYERSELECT
        self.listPlayerInfo = [0, "", "", ""]

    def setDatabase(self, db):
        self.database = db

    def setTeamBoxes(self, frameTeamBoxes):
        self.frameTeamBoxes = frameTeamBoxes

    def createSelf(self):
        self.createAddPlayerIDDisplay()
        self.createAddPlayerDisplay()
        self.createAddCodenameDisplay()

    def createAddPlayerIDDisplay(self):
        self.displayAddPlayerID = Display_SingleEntryBox(self)
        self.displayAddPlayerID.setTitle("Enter Player ID")
        self.displayAddPlayerID.setInputTitleText("Player ID: ")
        self.displayAddPlayerID.bindSubmit(self.submit_PlayerID)
        self.displayAddPlayerID.closeSelf()

    def createAddPlayerDisplay(self):
        self.displayAddPlayerName = Display_AddPlayerName(self, self.submitPlayerName)
        self.displayAddPlayerName.closeSelf()

    def createAddCodenameDisplay(self):
        self.displayAddCodename = Display_AddCodename(self, self.submitCodeName)
        self.displayAddCodename.closeSelf()

    def gridify(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.displayAddPlayerID.grid(column=0, row=0, sticky="NSEW")
        self.displayAddPlayerID.gridify()
        self.displayAddPlayerName.grid(column=0, row=0, sticky="NSEW")
        self.displayAddPlayerName.gridify()
        self.displayAddCodename.grid(column=0, row=0, sticky="NSEW")
        self.displayAddCodename.gridify()


    def openAddPlayerID(self):
        self.show()
        self.intDisplay = self.PLAYERID
        self.displayAddPlayerID.openSelf()
        self.displayAddPlayerID.setInputEntryText(self.frameTeamBoxes.getPlayerIDAtArrow())
        self.root.update()

    def openAddPlayerName(self):
        self.show()
        self.intDisplay = self.PLAYERNAME
        listPlayerAtArrow = self.getPlayerAtArrow()
        self.displayAddPlayerName.setPlayerName(listPlayerAtArrow[0],
                                                listPlaayerAtArrow[1])
        self.displayAddPlayerName.openSelf()
        self.root.update()

    def openAddCodename(self):
        self.intDisplay = self.PLAYERCODENAME
        self.displayAddCodename.openSelf()
        self.root.update()


    def switchToMainDisplay(self):
        self.intDisplay = self.PLAYERSELECT
        self.frameTeamBoxes.tkraise()
        self.root.update()

    def closeAllMenus(self):
        self.displayAddPlayerID.closeSelf()
        self.displayAddPlayerName.closeSelf()
        self.displayAddCodename.closeSelf()
        self.switchToMainDisplay()


    def closeAllDisplays(self):
        self.displayAddPlayerID.closeSelf()
        self.displayAddPlayerName.closeSelf()
        self.displayAddCodename.closeSelf()
        self.switchToMainDisplay()

    def closeAddPlayerID(self):
        self.displayAddPlayerID.closeSelf()
        self.switchToMainDisplay()

    def closeAddCodename(self):
        self.displayAddCodename.closeSelf()
        self.switchToMainDisplay()

    def closeAddPlayerName(self):
        self.displayAddPlayerName.closeSelf()
        self.switchToMainDisplay()

    def closeInsPlayerWithoutSave(self):
        self.displayAddPlayerName.closeSelf()
        self.displayAddCodename.closeSelf()
        self.switchToMainDisplay()


    def getDisplayState(self):
        return self.intDisplay

    def submit_PlayerID(self):
        strID = self.displayAddPlayerID.getInputEntryText()
        try:
            intID = 0
            if strID.isdigit():
                intID = int(strID)
            strPlayerIDAtArrow = self.frameTeamBoxes.getPlayerIDAtArrow()
            if not strID.isdigit():
                self.displayAddPlayerID.setError(
                    "ID needs to be positive integer\n and less than 100,000",
                    boolOverwrite=True)
            elif intID >= 100000:
                self.displayAddPlayerID.setError("ID must be less than 100,000!", boolOverwrite=True)
            elif not self.frameTeamBoxes.isIDAlreadyEntered(intID) or strPlayerIDAtArrow == strID:
                self.displayAddPlayerID.closeSelf()
                self.listPlayerInfo[self.INDEX_PLAYER_ID] = intID
                # Check DB for ID
                playerRow = self.database.findId(self.listPlayerInfo[self.INDEX_PLAYER_ID])
                print(playerRow)
                if len(playerRow) < 1:
                    print("Player not found")
                    self.intDisplay = self.PLAYERCODENAME
                    self.listPlayerInfo[self.INDEX_PLAYER_ID] = intID
                    self.displayAddPlayerName.openSelf()
                else:
                    player = playerRow[0]
                    self.listPlayerInfo[self.INDEX_PLAYER_ID] = player[self.INDEX_PLAYER_ID]
                    self.listPlayerInfo[self.INDEX_PLAYER_FIRST_NAME] = player[self.INDEX_PLAYER_FIRST_NAME]
                    self.listPlayerInfo[self.INDEX_PLAYER_LAST_NAME] = player[self.INDEX_PLAYER_LAST_NAME]
                    self.listPlayerInfo[self.INDEX_PLAYER_CODE] = player[self.INDEX_PLAYER_CODE]
            else:
                self.displayAddPlayerID.setError("ID already entered for this game",
                                                 boolOverwrite=True)
        except (Exception) as error:
            print(error)
            self.closeAllDisplays()

    def submitPlayerName(self, strFirstName, strLastName):
        self.displayAddPlayerName.closeSelf()
        self.listPlayerInfo[self.INDEX_PLAYER_FIRST_NAME] = strFirstName
        self.listPlayerInfo[self.INDEX_PLAYER_LAST_NAME] = strLastName
        # Check DB for name
        playerRow = self.database.findPlayerByName(strFirstName, strLastName)
        if len(playerRow) < 1:
            print("Player not found")
            self.intDisplay = self.PLAYERCODENAME
            self.displayAddCodename.openSelf()
        else:
            player = playerRow[0]
            print(player)
            self.listPlayerInfo[self.INDEX_PLAYER_ID] = player[self.INDEX_PLAYER_ID]
            self.listPlayerInfo[self.INDEX_PLAYER_CODE] = player[self.INDEX_PLAYER_CODE]

    def submitCodeName(self, strCodeName):
        self.listPlayerInfo[3] = strCodeName
        self.displayAddCodename.closeSelf()
        print(self.listPlayerInfo)
        if self.listPlayerInfo[self.INDEX_PLAYER_ID] == -1:
            row = self.database.getLastId()
            id = 0
            if len(row) == 0:
                id = 1
            else:
                id = row[0][self.INDEX_PLAYER_ID] + 1
            self.listPlayerInfo[self.INDEX_PLAYER_ID] = id
            if self.database.findId(id) == []:
                self.database.insertPlayer(self.listPlayerInfo)
                self.database.commit()
        else:
            id = self.listPlayerInfo[self.INDEX_PLAYER_ID]
            if self.database.findId(id) != []:
                self.database.updateUsingId(self.listPlayerInfo)
                self.database.commit()
            else:
                self.database.insertPlayer(self.listPlayerInfo)
                self.database.commit()
        rows = self.database.getAllRows()

        strPlayerName = self.listPlayerInfo[self.INDEX_PLAYER_FIRST_NAME] + " " + self.listPlayerInfo[self.INDEX_PLAYER_LAST_NAME]
        if len(strPlayerName) <= 1:
            strPlayerName = "(Left blank)"
        self.addPlayer(self.listPlayerInfo[self.INDEX_PLAYER_ID],
                       strPlayerName,
                       self.listPlayerInfo[self.INDEX_PLAYER_CODE])
        self.switchToMainDisplay()

    def getPlayerAtArrow(self):
        return self.frameTeamBoxes.getPlayerAtArrow()

    def addPlayer(self, intID, strPlayer, strCode):
        self.frameTeamBoxes.addPlayer(intID, strPlayer, strCode)
        self.listPlayerInfo = [0, "", "", ""]
        self.root.update()

    def deletePlayer(self, event=None):
        self.frameTeamBoxes.deletePlayer()
        self.root.update()

    def debug_AddOrUpdatePlayer(self, intID, strPlayerCodename, boolCommit=True):
        tupleDBEntry = self.database.findId(intID)
        if tupleDBEntry is None or len(tupleDBEntry) == 0:
            listNewPlayerEntry = [intID, "(blank)", "(blank)", str(strPlayerCodename)]
            self.database.insertPlayer(listNewPlayerEntry)
            if boolCommit:
                self.database.commit()
            return listNewPlayerEntry[0]
        else:
            listUpdatedEntry = [tupleDBEntry[0][0], tupleDBEntry[0][1], tupleDBEntry[0][2], tupleDBEntry[0][3]]
            listUpdatedEntry[3] = strPlayerCodename
            self.database.updateUsingId(listUpdatedEntry)
            if boolCommit:
                self.database.commit()
            return listUpdatedEntry[0]

