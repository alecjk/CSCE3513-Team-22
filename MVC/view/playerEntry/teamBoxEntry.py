import tkinter as tk
from MVC.app.ApplicationObj import *


class Frame_EditTeam(AppObject):
    NO_ARROW = -1

    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.intDefaultTextsize = 12
        self.strTeamColor = "#330000"
        self.strTeamName = "DEFAULT"
        self.intPlayerEntries = 15
        self.intArrowPos = self.NO_ARROW
        # self.createSelf()

    def createSelf(self):
        strTeamName = self.strTeamName
        strTeamHeadBG = "#444444"  # Mid gray
        intTeamHFontSize = 14
        strTeamColor = self.strTeamColor
        strTextColor = "#FFFFFF"  # White
        strFontStyle = self.strDefaultFont
        intArrowFontSize = 18
        intCBoxFontSize = 14
        intEntryFontSize = 12

        self.labelTeamName = tk.Label(self, text=strTeamName, fg=strTextColor, bg=strTeamHeadBG,
                                      font=(strFontStyle, intTeamHFontSize), borderwidth=2, relief="groove")
        self.propagateWidget(self.labelTeamName)

        self.labelID = [None] * self.intPlayerEntries
        self.labelPlayerName = [None] * self.intPlayerEntries
        self.labelCodeName = [None] * self.intPlayerEntries
        self.checkboxC = [None] * self.intPlayerEntries
        self.checkboxVar = [None] * self.intPlayerEntries
        self.labelArrow = [None] * self.intPlayerEntries

        for i in range(self.intPlayerEntries):
            self.labelArrow[i] = tk.Label(self, text="", fg=strTextColor, bg=strTeamColor,
                                          font=(strFontStyle, intArrowFontSize))
            self.checkboxVar[i] = tk.BooleanVar(value=False)
            self.checkboxC[i] = tk.Checkbutton(self,
                                               text=str(i + 1),
                                               highlightthickness=0, bd=0,
                                               fg=strTextColor, bg=strTeamColor, font=(strFontStyle, intCBoxFontSize),
                                               onvalue=1, offvalue=0,
                                               state="disabled", variable=self.checkboxVar[i])
            self.labelID[i] = tk.Label(self, bd=2, font=(strFontStyle, intEntryFontSize), anchor="w")
            self.labelPlayerName[i] = tk.Label(self, bd=2, font=(strFontStyle, intEntryFontSize), anchor="w")
            self.labelCodeName[i] = tk.Label(self, bd=2, font=(strFontStyle, intEntryFontSize), anchor="w")

            self.propagateWidget(self.checkboxC[i])
            self.propagateWidget(self.labelPlayerName[i])
            self.propagateWidget(self.labelCodeName[i])
            self.propagateWidget(self.labelArrow[i])

    def gridify(self):
        intFrameCols = 10
        intFrameRows = 15

        for i in range(intFrameCols):
            self.columnconfigure(i, weight=1, uniform="uniformTeam")
        for i in range(intFrameRows):
            self.rowconfigure(i, weight=1, uniform="uniformTeam")

        self.labelTeamName.grid(column=1, row=0, columnspan=11)

        for i in range(self.intPlayerEntries):
            self.labelArrow[i].grid(column=0, row=i + 1, sticky="E")
            self.checkboxC[i].grid(column=1, row=i + 1)
            self.labelID[i].grid(column=2, row=i + 1, columnspan=2, padx=2, sticky="EW")
            # self.labelPlayerName[i].grid(column=3, row=i+1,columnspan=3,padx=2,sticky="EW")
            self.labelCodeName[i].grid(column=4, row=i + 1, columnspan=7, padx=(2, 10), sticky="EW")

    def setTeamColor(self, strColor):
        self.strTeamColor = strColor

    def setTeamName(self, strName):
        self.strTeamName = strName

    def setPlayerEntries(self, intNum):
        self.intPlayerEntries = intNum

    def isIDAlreadyEntered(self, intID):
        for i in range(self.intPlayerEntries):
            strRawPlayerID = self.labelID[i]["text"]
            if strRawPlayerID != "":
                if int(strRawPlayerID) == intID:
                    return True
        return False

    def getPlayerIDAtArrow(self):
        if self.intArrowPos == self.NO_ARROW:
            return ""
        else:
            strRawPlayerID = self.labelID[self.intArrowPos]["text"]
            return strRawPlayerID

    def getPlayerAtArrow(self):
        if self.intArrowPos == self.NO_ARROW:
            return ["", ""]
        else:
            listStrPlayerName = self.labelPlayerName[self.intArrowPos]["text"].split()
            if listStrPlayerName == [] or listStrPlayerName == None:
                listStrPlayerName = ["", ""]
            return [listStrPlayerName[0], listStrPlayerName[1]]

    def getPlayerIDList(self):
        listPlayerIDs = [None] * self.intPlayerEntries
        for i in range(self.intPlayerEntries):
            listPlayerIDs[i] = self.labelID[i]["text"]
            if listPlayerIDs[i] != "":
                listPlayerIDs[i] = int(listPlayerIDs[i])
        return listPlayerIDs

    def getPlayerList(self):
        listPlayers = [None] * self.intPlayerEntries
        for i in range(self.intPlayerEntries):
            listPlayers[i] = [self.labelPlayerName[i]["text"], self.labelCodeName[i]["text"]]
        return listPlayers

    def getPlayerCount(self):
        intCount = 0
        for i in range(self.intPlayerEntries):
            strPlayerName = self.labelPlayerName[i]["text"]
            if strPlayerName != "" and strPlayerName != None:
                intCount += 1
        return intCount

    def addPlayer(self, intArrowPos, intID, strPlayer, strCode):
        self.labelID[intArrowPos]["text"] = str(intID)
        self.labelPlayerName[intArrowPos]["text"] = strPlayer
        self.labelCodeName[intArrowPos]["text"] = strCode
        self.checkboxVar[intArrowPos].set(True)
        self.checkboxC[intArrowPos].select()

    def addPlayerAtArrow(self, intID, strPlayer, strCode):
        if self.intArrowPos != self.NO_ARROW:
            self.addPlayer(self.intArrowPos, intID, strPlayer, strCode)

    def deletePlayer(self, intArrowPos):
        self.labelID[intArrowPos]["text"] = ""
        self.labelPlayerName[intArrowPos]["text"] = ""
        self.labelCodeName[intArrowPos]["text"] = ""
        self.checkboxVar[intArrowPos].set(False)
        self.checkboxC[intArrowPos].deselect()

    def deletePlayerAtArrow(self):
        if self.intArrowPos != self.NO_ARROW:
            self.deletePlayer(self.intArrowPos)

    def deleteAllPlayers(self):
        for i in range(self.intPlayerEntries):
            self.deletePlayer(i)

    def setArrowPos(self, intPos):
        if intPos < 0 or intPos >= self.intPlayerEntries:
            raise Exception("Frame_EditTeam: Arrow Pos exceeds number of PlayerEntries!")
        else:
            if self.intArrowPos != self.NO_ARROW:
                self.removeArrow()
            self.labelArrow[intPos]["text"] = ">>"
            self.intArrowPos = intPos

    def removeArrow(self):
        if self.intArrowPos != self.NO_ARROW:
            self.labelArrow[self.intArrowPos]["text"] = ""
            self.intArrowPos = self.NO_ARROW