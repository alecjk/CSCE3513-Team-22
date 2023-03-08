from MVC.app.ApplicationObj import *
from MVC.view.entryTerminal.teamBoxEntry import *


class Frame_TeamBoxes(AppObject):
    INDEX_TEAM = 0
    INDEX_ENTRY = 1
    REDARROWPOS = 0
    GREENARROWPOS = 1

    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.intDefaultTextsize = 12
        self.intPlayerEntries = 15
        self.listArrowPos = [0, 0]
        self.createSelf()

    def createSelf(self):
        strRedTeamColor = "#330000"
        strGreenTeamColor = "#003300"

        self.frameTeamRed = Frame_EditTeam(self)
        self.frameTeamRed["bg"] = strRedTeamColor
        self.frameTeamGreen = Frame_EditTeam(self)
        self.frameTeamGreen["bg"] = strGreenTeamColor
        self.proWidget(self.frameTeamRed)
        self.proWidget(self.frameTeamGreen)

        self.createRedTeamBox()
        self.createGreenTeamBox()
        self.setArrowPos(self.REDARROWPOS, 0)

    def createRedTeamBox(self):
        strTeamName = "TEAM RED"
        strTeamColor = "#330000"

        self.frameTeamRed.setTeamName(strTeamName)
        self.frameTeamRed.setTeamColor(strTeamColor)
        self.frameTeamRed.setPlayerEntries(self.intPlayerEntries)
        self.frameTeamRed.createSelf()

    def createGreenTeamBox(self):
        strTeamName = "TEAM GREEN"
        strTeamColor = "#003300"

        self.frameTeamGreen.setTeamName(strTeamName)
        self.frameTeamGreen.setTeamColor(strTeamColor)
        self.frameTeamGreen.setPlayerEntries(self.intPlayerEntries)
        self.frameTeamGreen.createSelf()

    def createStartGameButton(self):
        strText = "START"

        self.frameStartGameButton.set

    def gridify(self):
        intFrameCols = 2
        intFrameRows = 1

        for i in range(intFrameCols):
            self.columnconfigure(i, weight=1)
        for i in range(intFrameRows):
            self.rowconfigure(i, weight=1)

        self.frameTeamRed.grid(column=0, row=0, sticky="NSEW")
        self.frameTeamRed.gridify()

        self.frameTeamGreen.grid(column=1, row=0, sticky="NSEW")
        self.frameTeamGreen.gridify()

    def getArrowPos(self):
        return self.listArrowPos

    def isValidArrowPos(self, intTeam, intEntry):
        return ((intTeam == self.REDARROWPOS or intTeam == self.GREENARROWPOS)
                and (intEntry >= 0 and intEntry < self.intPlayerEntries))

    def isValidArrowOffset(self, intOffsetX, intOffsetY):
        newPosX = intOffsetX + self.listArrowPos[self.INDEX_TEAM]
        newPosY = intOffsetY + self.listArrowPos[self.INDEX_ENTRY]
        return self.isValidArrowPos(newPosX, newPosY)

    def removeArrowAtPos(self):
        if self.listArrowPos[self.INDEX_TEAM] == self.REDARROWPOS:
            self.frameTeamRed.removeArrow()
        else:
            self.frameTeamGreen.removeArrow()

    def placeArrowAtPos(self):
        if self.listArrowPos[self.INDEX_TEAM] == self.REDARROWPOS:
            self.frameTeamRed.setArrowPos(self.listArrowPos[self.INDEX_ENTRY])
        else:
            self.frameTeamGreen.setArrowPos(self.listArrowPos[self.INDEX_ENTRY])

    def setArrowPos(self, intTeam, intEntry):
        if intTeam != self.REDARROWPOS and intTeam != self.GREENARROWPOS:
            print("Frame_TeamBoxes: Invalid intTeam passed to setArrowPos!")
        else:
            if intEntry < 0 or intEntry >= self.intPlayerEntries:
                print("Frame_TeamBoxes: Invalid intEntry passed to setArrowPos!")
            else:
                self.removeArrowAtPos()
                self.listArrowPos[self.INDEX_TEAM] = intTeam
                self.listArrowPos[self.INDEX_ENTRY] = intEntry
                self.placeArrowAtPos()

    def moveArrow(self, intOffsetX, intOffsetY):
        newPosX = intOffsetX + self.listArrowPos[self.INDEX_TEAM]
        newPosY = intOffsetY + self.listArrowPos[self.INDEX_ENTRY]
        if newPosX == self.REDARROWPOS or newPosX == self.GREENARROWPOS:
            if newPosY >= 0 and newPosY < self.intPlayerEntries:
                self.setArrowPos(newPosX, newPosY)
            else:
                print("Frame_TeamBoxes: Invalid intOffsetY passed to moveArrow!")
        else:
            print("Frame_TeamBoxes: Invalid intOffsetX passed to moveArrow!")

    def getPlayerIDAtArrow(self):
        if self.listArrowPos[self.INDEX_TEAM] == self.REDARROWPOS:
            return self.frameTeamRed.getPlayerIDAtArrow()
        else:
            return self.frameTeamGreen.getPlayerIDAtArrow()

    def getPlayerAtArrow(self):
        if self.listArrowPos[self.INDEX_TEAM] == self.REDARROWPOS:
            return self.frameTeamRed.getPlayerAtArrow()
        else:
            return self.frameTeamGreen.getPlayerAtArrow()

    def getPlayerIDList(self):
        return [self.frameTeamRed.getPlayerIDList(), self.frameTeamGreen.getPlayerIDList()]

    def getPlayerList(self):
        return [self.frameTeamRed.getPlayerList(), self.frameTeamGreen.getPlayerList()]

    def getPlayerCount(self):
        return [self.frameTeamRed.getPlayerCount(), self.frameTeamGreen.getPlayerCount()]

    def addPlayer(self, intID, strPlayer, strCode):
        if self.listArrowPos[self.INDEX_TEAM] == self.REDARROWPOS:
            self.frameTeamRed.addPlayerAtArrow(intID, strPlayer, strCode)
        else:
            self.frameTeamGreen.addPlayerAtArrow(intID, strPlayer, strCode)

    def isIDAlreadyEntered(self, intID):
        return (self.frameTeamRed.isIDAlreadyEntered(intID) or self.frameTeamGreen.isIDAlreadyEntered(intID))

    def deletePlayer(self):
        if self.listArrowPos[self.INDEX_TEAM] == self.REDARROWPOS:
            self.frameTeamRed.deletePlayerAtArrow()
        else:
            self.frameTeamGreen.deletePlayerAtArrow()
