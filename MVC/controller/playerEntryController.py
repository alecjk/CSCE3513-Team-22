from MVC.model.database.DB import *
from MVC.app.ApplicationObj import *
from MVC.view.display_EntryBox import *
from MVC.model.playerEntry.addPlayerName import *
from MVC.model.playerEntry.addPlayerCodename import *
from MVC.view.playerEntry.teamBox import *

class MenuManager_EditGame(AppObject):
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
    ERRORNEEDPLAYERS = 6
    DEBUGFILLPLAYERS = 7
    PLAYERID = 8

    def __init__(self, tkRoot):
        super().__init__(tkRoot)

        self.intMenu = self.PLAYERSELECT
        self.listPlayerInfo = [0, "", "", ""]

    def setDatabase(self, db):
        self.database = db

    def setTeamBoxes(self, frameTeamBoxes):
        self.frameTeamBoxes = frameTeamBoxes

    def createSelf(self):
        self.createAddPlayerIDMenu()
        self.createAddPlayerMenu()
        self.createAddCodenameMenu()

    def createAddPlayerIDMenu(self):
        self.menuAddPlayerID = Menu_SingleEntryBox(self)
        self.menuAddPlayerID.setTitle("Enter Player ID")
        self.menuAddPlayerID.setInputTitleText("Player ID: ")
        self.menuAddPlayerID.setHintText(
            "Enter an ID to search/retrieve or\nto create a new player if not\nfound in database.")
        self.menuAddPlayerID.bindSubmit(self.submit_PlayerID)
        self.menuAddPlayerID.closeSelf()

    def createAddPlayerMenu(self):
        self.menuAddPlayerName = Menu_AddPlayerName(self, self.submitPlayerName)
        self.menuAddPlayerName.closeSelf()

    def createAddCodenameMenu(self):
        self.menuAddCodename = Menu_AddCodename(self, self.submitCodeName)
        self.menuAddCodename.closeSelf()

    def gridify(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.menuAddPlayerID.grid(column=0, row=0, sticky="NSEW")
        self.menuAddPlayerID.gridify()
        self.menuAddPlayerName.grid(column=0, row=0, sticky="NSEW")
        self.menuAddPlayerName.gridify()
        self.menuAddCodename.grid(column=0, row=0, sticky="NSEW")
        self.menuAddCodename.gridify()

    def openDeleteDBConfirmMenu(self):
        self.intMenu = self.DELETEDBCONFIRM
        self.menuDeleteDBConfirm.openSelf()

    def openAddPlayerID(self):
        self.showSelf()
        self.intMenu = self.PLAYERID
        self.menuAddPlayerID.openSelf()
        self.menuAddPlayerID.setInputEntryText(self.frameTeamBoxes.getPlayerIDAtArrow())
        self.root.update()  # keep

    def openAddPlayerName(self):
        self.showSelf()
        self.intMenu = self.PLAYERNAME  # keep
        listPlayerAtArrow = self.getPlayerAtArrow()  # keep
        self.menuAddPlayerName.setPlayerName(listPlayerAtArrow[0],
                                             listPlayerAtArrow[1])
        self.menuAddPlayerName.openSelf()
        self.root.update()  # keep

    def openAddCodename(self):
        self.intMenu = self.PLAYERCODENAME  # keep
        self.menuAddCodename.openSelf()
        self.root.update()  # keep

    def openMoveToPlayConfirm(self):
        self.showSelf()
        self.intMenu = self.MOVETOPLAYCONFIRM
        self.menuMoveToPlayConfirm.openSelf()
        self.root.update()

    def openErrorNeedPlayers(self):
        self.intMenu = self.ERRORNEEDPLAYERS
        self.menuErrorNeedPlayers.openSelf()
        self.root.update()

    def openDebugFillPlayers(self):
        self.intMenu = self.DEBUGFILLPLAYERS
        self.menuDebugFillPlayers.openSelf()
        self.root.update()

    def switchToMainMenu(self):
        self.intMenu = self.PLAYERSELECT  # keep
        self.frameTeamBoxes.tkraise()
        self.root.update()  # keep

    def closeAllMenus(self):
        self.menuAddPlayerID.closeSelf()
        self.menuAddPlayerName.closeSelf()
        self.menuAddCodename.closeSelf()
        self.switchToMainMenu()

    def closeAddPlayerID(self):
        self.menuAddPlayerID.closeSelf()
        self.switchToMainMenu()

    def closeAddCodename(self):
        self.menuAddCodename.closeSelf()
        self.switchToMainMenu()

    def closeUsePrevCodename(self):
        self.menuUsePrevCodename.closeSelf()
        self.switchToMainMenu()

    def closeAddPlayerName(self):
        self.menuAddPlayerName.closeSelf()
        self.switchToMainMenu()

    def closeInsPlayerWithoutSave(self):
        self.menuAddPlayerName.closeSelf()
        self.menuAddCodename.closeSelf()
        self.switchToMainMenu()

    def closeDebugFillPlayers(self):
        self.menuDebugFillPlayers.closeSelf()
        self.switchToMainMenu()

    def getMenuState(self):
        return self.intMenu

    def bind_ChangeToPlay(self, mFunc):
        self.methodChangeToPlay = mFunc

    def submitYes_UsePrevCodename(self):
        self.menuUsePrevCodename.closeSelf()
        strPlayerName = self.listPlayerInfo[self.INDEX_PINFO_FNAME] + " " + self.listPlayerInfo[self.INDEX_PINFO_LNAME]
        if len(strPlayerName) <= 1:
            strPlayerName = "(Left blank)"
        self.addPlayer(self.listPlayerInfo[self.INDEX_PINFO_ID],
                       strPlayerName,
                       self.listPlayerInfo[self.INDEX_PINFO_CODE])
        self.switchToMainMenu()

    def submitNo_UsePrevCodename(self):
        self.intMenu = self.PLAYERCODENAME
        self.menuUsePrevCodename.closeSelf()
        self.menuAddCodename.openSelf()
        self.menuAddCodename.setInputEntryText(self.listPlayerInfo[self.INDEX_PINFO_CODE])

    def submitYes_DeleteDB(self):
        self.menuDeleteDBConfirm.closeSelf()
        print("Deleting all rows in DB...")
        self.database.deleteAllRows()
        self.database.commit()
        rows = self.database.getAllRows()
        print(rows)
        self.clearAllPlayers()
        self.switchToMainMenu()

    def submitNo_DeleteDB(self):
        self.menuDeleteDBConfirm.closeSelf()
        self.switchToMainMenu()

    def submitYes_MoveToPlay(self):
        listPlayerCount = self.frameTeamBoxes.getPlayerCount()
        if listPlayerCount[0] >= 1 and listPlayerCount[1] >= 1:
            self.intMenu = self.PLAYERSELECT
            self.menuMoveToPlayConfirm.closeSelf()
            self.methodChangeToPlay()
        else:
            self.menuMoveToPlayConfirm.closeSelf()
            self.openErrorNeedPlayers()

    def submitNo_MoveToPlay(self):
        self.menuMoveToPlayConfirm.closeSelf()
        self.switchToMainMenu()

    def submitOk_NeedPlayers(self):
        self.menuErrorNeedPlayers.closeSelf()
        self.switchToMainMenu()

    def submitYes_FillPlayers(self):
        self.closeDebugFillPlayers()
        self.debug_FillAllPlayers()

    def submitNo_FillPlayers(self):
        self.closeDebugFillPlayers()

    def submit_PlayerID(self):
        strID = self.menuAddPlayerID.getInputEntryText()
        try:
            intID = 0
            if strID.isdigit():
                intID = int(strID)
            strPlayerIDAtArrow = self.frameTeamBoxes.getPlayerIDAtArrow()
            if not strID.isdigit():
                self.menuAddPlayerID.setError(
                    "ID is not a positive integer\n and less than 100,000!\nPlease enter a valid positive integer.",
                    boolOverwrite=True)
            elif intID >= 100000:
                self.menuAddPlayerID.setError("ID must be less than 100,000!", boolOverwrite=True)
            elif not self.frameTeamBoxes.isIDAlreadyEntered(intID) or strPlayerIDAtArrow == strID:
                self.menuAddPlayerID.closeSelf()
                self.listPlayerInfo[self.INDEX_PINFO_ID] = intID
                # Check DB for ID
                playerRow = self.database.findId(self.listPlayerInfo[self.INDEX_PINFO_ID])
                print(playerRow)
                if len(playerRow) < 1:
                    print("Player not found")
                    self.intMenu = self.PLAYERCODENAME
                    self.listPlayerInfo[self.INDEX_PINFO_ID] = intID
                    self.listPlayerInfo[self.INDEX_PINFO_FNAME] = "(blank)"
                    self.listPlayerInfo[self.INDEX_PINFO_LNAME] = "(blank)"
                    self.menuAddCodename.openSelf()
                else:
                    player = playerRow[0]  # First occurrence, if somehow multiple entries
                    self.intMenu = self.ASKUSEPREVCODE
                    self.menuUsePrevCodename.setCodename(player[self.INDEX_PINFO_CODE])
                    self.menuUsePrevCodename.openSelf()
                    self.listPlayerInfo[self.INDEX_PINFO_ID] = player[self.INDEX_PINFO_ID]
                    self.listPlayerInfo[self.INDEX_PINFO_FNAME] = player[self.INDEX_PINFO_FNAME]
                    self.listPlayerInfo[self.INDEX_PINFO_LNAME] = player[self.INDEX_PINFO_LNAME]
                    self.listPlayerInfo[self.INDEX_PINFO_CODE] = player[self.INDEX_PINFO_CODE]
            else:
                self.menuAddPlayerID.setError("ID already entered for this game!\nPlease enter another ID instead.",
                                              boolOverwrite=True)
        except (Exception) as error:
            print(error)
            self.closeAllMenus()

    def submitPlayerName(self, strFirstName, strLastName):
        self.menuAddPlayerName.closeSelf()
        self.listPlayerInfo[self.INDEX_PINFO_FNAME] = strFirstName
        self.listPlayerInfo[self.INDEX_PINFO_LNAME] = strLastName
        # Check DB for name
        playerRow = self.database.findPlayerByName(strFirstName, strLastName)
        if len(playerRow) < 1:
            print("Player not found")
            self.intMenu = self.PLAYERCODENAME
            self.menuAddCodename.openSelf()
        else:
            player = playerRow[0]  # First occurrence, if somehow multiple entries
            print(player)
            self.intMenu = self.ASKUSEPREVCODE
            self.menuUsePrevCodename.setCodename(player[self.INDEX_PINFO_CODE])
            self.menuUsePrevCodename.openSelf()
            self.listPlayerInfo[self.INDEX_PINFO_ID] = player[self.INDEX_PINFO_ID]
            self.listPlayerInfo[self.INDEX_PINFO_CODE] = player[self.INDEX_PINFO_CODE]

    def submitCodeName(self, strCodeName):
        self.listPlayerInfo[3] = strCodeName
        self.menuAddCodename.closeSelf()
        print(self.listPlayerInfo)
        if self.listPlayerInfo[self.INDEX_PINFO_ID] == -1:  # should never occur - quick-change to remove functionality
            row = self.database.getLastId()
            id = 0
            if len(row) == 0:
                id = 1
            else:
                id = row[0][self.INDEX_PINFO_ID] + 1
            self.listPlayerInfo[self.INDEX_PINFO_ID] = id
            if self.database.findId(id) == []:
                self.database.insertPlayer(self.listPlayerInfo)
                self.database.commit()
        else:
            id = self.listPlayerInfo[self.INDEX_PINFO_ID]
            if self.database.findId(id) != []:
                self.database.updateUsingId(self.listPlayerInfo)
                self.database.commit()
            else:
                self.database.insertPlayer(self.listPlayerInfo)
                self.database.commit()
        rows = self.database.getAllRows()
        # print(rows)
        strPlayerName = self.listPlayerInfo[self.INDEX_PINFO_FNAME] + " " + self.listPlayerInfo[self.INDEX_PINFO_LNAME]
        if len(strPlayerName) <= 1:
            strPlayerName = "(Left blank)"
        self.addPlayer(self.listPlayerInfo[self.INDEX_PINFO_ID],
                       strPlayerName,
                       self.listPlayerInfo[self.INDEX_PINFO_CODE])
        self.switchToMainMenu()

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

