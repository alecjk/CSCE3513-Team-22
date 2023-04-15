import tkinter as tk
from tkinter import ttk
from MVC.app.ApplicationObj import *

class Display_TeamScore(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.intMaxTopPlayers = 15
        self.listStrPlayerNames = [None]*15
        self.listIntPlayerID = [None]*15
        self.strTeamName = "RED TEAM"
        self.strTeamColor = "#ff6666" # Light Red
        self.strTopTeamColor = "#ff0000"
        self.boolIsFlashing = False
        self.strTeamScoreFlashingColor = "#ff0000"
        
    def setMaxTopPlayers(self, intMax):
        self.intMaxTopPlayers = intMax
        
    def setTeamName(self, strName):
        self.strTeamName = strName
        
    def setTeamColor(self, strColor):
        self.strTeamColor = strColor
        
    def setTopTeamColor(self, strColor):
        self.strTopTeamColor = strColor
        
    def setTeamScoreFlashingColor(self, strColor):
        self.strTeamScoreFlashingColor = strColor
        
    def createSelf(self):
        strBGColor = "#000000"
        strTeamHeadColor = "#FFFFFF" # White
        strPlayerColor = self.strTeamColor
        strTeamName = self.strTeamName
        strFont = self.strDefaultFont
        intTextsizeTeamHead = 20
        intTextsizePlayer = 14
        intTextsizeTeamScore = 20
        
        self["bg"] = strBGColor
        # self.propagateWidget(self.frameRedTeam)
        
        self.labelTeamHead = tk.Label(self, 
            text=strTeamName,
            bg=strBGColor, fg=strTeamHeadColor, font=(strFont, intTextsizeTeamHead,"bold"))
        self.propagateWidget(self.labelTeamHead)
        
        self.labelTopPlayers = [None] * self.intMaxTopPlayers
        self.labelTopScore = [None] * self.intMaxTopPlayers
        for i in range(self.intMaxTopPlayers):
            self.labelTopPlayers[i] = tk.Label(self, 
                text="Player "+str(i+1), 
                fg=strPlayerColor, bg=strBGColor, font=(strFont,intTextsizePlayer))
            self.labelTopScore[i] = tk.Label(self, 
                text=str((self.intMaxTopPlayers-i)*1000), 
                fg=strPlayerColor, bg=strBGColor, font=(strFont,intTextsizePlayer))
            if i < 3:
                self.labelTopPlayers[i]["font"]=(strFont,intTextsizePlayer,"bold")
                self.labelTopPlayers[i]["fg"]=self.strTopTeamColor
                self.labelTopScore[i]["font"]=(strFont,intTextsizePlayer,"bold")
                self.labelTopScore[i]["fg"]=self.strTopTeamColor
            self.propagateWidget(self.labelTopPlayers[i])
            self.propagateWidget(self.labelTopScore[i])
            
        self.labelTeamScoreHead = tk.Label(self,
            text="TEAM SCORE", 
            fg=strPlayerColor, bg=strBGColor, font=(strFont,intTextsizeTeamScore))
        self.labelTeamScoreAmount = tk.Label(self,
            text="0",
            fg=strPlayerColor, bg=strBGColor, font=(strFont,intTextsizeTeamScore))
        self.propagateWidget(self.labelTeamScoreHead)
        self.propagateWidget(self.labelTeamScoreAmount)
        
    def gridify(self):
        intCols = 4
        intRows = 20
    
        for i in range(intCols):
            self.columnconfigure(i,weight=1, uniform="gridUniformTeam")
        for i in range(intRows):
            self.rowconfigure(i,weight=1, uniform="gridUniformTeam")
            
        self.labelTeamHead.grid(column=0,row=0,columnspan=4,rowspan=2, sticky="NEW")
            
        for i in range(self.intMaxTopPlayers):
            self.labelTopPlayers[i].grid(column=0,row=i+2, rowspan=1,columnspan=3,sticky="NSW")
            self.labelTopScore[i].grid(column=3,row=i+2,rowspan=1,sticky="NSE")
        
        self.labelTeamScoreHead.grid(column=0,row=18,rowspan=2,columnspan=3,sticky="SW", pady=(0,10))
        self.labelTeamScoreAmount.grid(column=3,row=18,rowspan=2,sticky="SE", pady=(0,10))
        
    def setPlayer(self, intIndex, strPlayer, intScore, intID=None):
        if intID is not None:
            self.labelTopPlayers[intIndex]["text"] = str(intIndex+1) + ". " + strPlayer + " (ID: " + str(intID) + ")"
            self.listIntPlayerID[intIndex] = intID
        else:
            self.labelTopPlayers[intIndex]["text"] = str(intIndex+1) + ". " + strPlayer
        self.listStrPlayerNames[intIndex] = strPlayer
        self.labelTopScore[intIndex]["text"] = str(intScore)
        
    def swapPlayers(self, intIndex1, intIndex2):
        strTempPlayer = self.listStrPlayerNames[intIndex1]
        intTempScore = int(self.labelTopScore[intIndex1]["text"])
        intTempID = self.listIntPlayerID[intIndex1]
        self.setPlayer(intIndex1, self.listStrPlayerNames[intIndex2],
                                self.labelTopScore[intIndex2]["text"],
                                self.listIntPlayerID[intIndex2])
        self.setPlayer(intIndex2, strTempPlayer, intTempScore, intTempID)
        
    def getValidListIntID(self):
        if None in self.listIntPlayerID:
            return self.listIntPlayerID[0:self.listIntPlayerID.index(None)]
        else:
            return self.listIntPlayerID[0:15]
                                
    def setPlayersUsingList(self, listPlayers, listIntID=None):
        self.clearAllPlayers()
        intCurrentLabel=0
        for i in range(len(listPlayers)):
            if listPlayers[i][0] != "":
                if listIntID is not None:
                    self.setPlayer(intCurrentLabel, listPlayers[i][1], 0, listIntID[i])
                else:
                    self.setPlayer(intCurrentLabel, listPlayers[i][1], 0)
                intCurrentLabel += 1
        print(listIntID)
                
    def alternateTeamScoreColor(self):
        if self.boolIsFlashing == True:
            self.setTeamScoreColorToDefault()
        else:
            self.setTeamScoreColorToFlashing()
        
    def setTeamScoreColorToDefault(self):
        self.boolIsFlashing = False
        self.labelTeamScoreHead["fg"] = self.strTeamColor
        self.labelTeamScoreAmount["fg"] = self.strTeamColor
        
    def setTeamScoreColorToFlashing(self):
        self.boolIsFlashing = True
        self.labelTeamScoreHead["fg"] = self.strTeamScoreFlashingColor
        self.labelTeamScoreAmount["fg"] = self.strTeamScoreFlashingColor   
    
    def getIndexOfID(self, intID):
        return self.listIntPlayerID.index(intID)
        
    def getCodenameFromID(self, intID):
        return self.listStrPlayerNames[self.listIntPlayerID.index(intID)]
        
    def getTeamScore(self):
        return int(self.labelTeamScoreAmount["text"])
    
    def updatePlayerScore(self, intID, scoreAdd):
        intIndexGivenID = self.getIndexOfID(intID)
        intNewScore = int(self.labelTopScore[intIndexGivenID]["text"])+scoreAdd
        self.labelTopScore[intIndexGivenID]["text"] = str(intNewScore)
        
        intIndexNewPos = 0
        for i in range(intIndexGivenID-1, -1, -1):
            if intNewScore <= int(self.labelTopScore[i]["text"]):
                intIndexNewPos = i+1
                break
                
        for i in range(intIndexGivenID, intIndexNewPos,-1):
            self.swapPlayers(i, i-1)
        #print("(intIndexGivenID, intIndexNewPos): {}, {}".format(intIndexGivenID, intIndexNewPos))
        self.labelTeamScoreAmount["text"] = str(int(self.labelTeamScoreAmount["text"])+scoreAdd)
                
    def clearAllPlayers(self):
        for i in range(self.intMaxTopPlayers):
            self.labelTopPlayers[i]["text"] = ""
            self.labelTopScore[i]["text"] = ""
            
    def resetScores(self):
        self.clearAllPlayers()
        self.listStrPlayerNames = [None]*15
        self.listIntPlayerID = [None]*15
        self.labelTeamScoreAmount["text"] = "0"