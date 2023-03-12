import tkinter as tk
from tkinter import ttk
from MVC.app.ApplicationObj import *
from MVC.view.playAction.Display_TeamScore import *

class Frame_Scoreboard(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        
        self.createSelf()
        
    def createSelf(self):
        self.frameTeamRed = Frame_TeamScore(self)
        self.frameTeamRed.setMaxTopPlayers(15)
        self.frameTeamRed.setTeamName("TEAM RED")
        self.frameTeamRed.setTeamColor("#ff6666")
        self.frameTeamRed.setTopTeamColor("#ff0000")
        self.frameTeamRed.setTeamScoreFlashingColor("#ff0000")
        self.frameTeamRed.createSelf()
        self.propagateWidget(self.frameTeamRed)
        self.frameTeamGreen = Frame_TeamScore(self)
        self.frameTeamGreen.setMaxTopPlayers(15)
        self.frameTeamGreen.setTeamName("TEAM GREEN")
        self.frameTeamGreen.setTeamColor("#66ff66")
        self.frameTeamGreen.setTopTeamColor("#00ff00")
        self.frameTeamGreen.setTeamScoreFlashingColor("#00ffc0")
        self.frameTeamGreen.createSelf()
        self.propagateWidget(self.frameTeamGreen)
        
    def gridify(self):
        intCols = 2
        intRows = 1
    
        for i in range(intCols):
            self.columnconfigure(i,weight=1, uniform="gridUniform")
        for i in range(intRows):
            self.rowconfigure(i,weight=1, uniform="gridUniform")
        
        self.frameTeamRed.grid(column=0, row=0, padx=(10,20), sticky="NSEW")
        self.frameTeamRed.gridify()
        self.frameTeamGreen.grid(column=1, row=0, padx=(20,10), sticky="NSEW")
        self.frameTeamGreen.gridify()
        
    def getCodenameFromID(self, intID, charTeam):
        if charTeam.upper() == "R":
            return self.frameTeamRed.getCodenameFromID(intID)
        else:
            return self.frameTeamGreen.getCodenameFromID(intID)
            
    def getValidListIntID(self):
        listIntRed = self.frameTeamRed.getValidListIntID()
        listIntGreen = self.frameTeamGreen.getValidListIntID()
        return [listIntRed, listIntGreen]
        
    def setPlayersUsingList(self, listPlayers, listIntID=None):
        if listIntID is not None:
            self.frameTeamRed.setPlayersUsingList(listPlayers[0], listIntID[0])
            self.frameTeamGreen.setPlayersUsingList(listPlayers[1], listIntID[1])
        else:
            self.frameTeamRed.setPlayersUsingList(listPlayers[0])
            self.frameTeamGreen.setPlayersUsingList(listPlayers[1])
    
    # Returns list: [charTeamLetter ex:"R","G","B"(both), intScore]
    def getListHighestTeamScore(self):
        intGreenScore = self.frameTeamGreen.getTeamScore()
        intRedScore = self.frameTeamRed.getTeamScore()
        if intRedScore > intGreenScore:
            return ["R",intRedScore]
        elif intGreenScore > intRedScore:
            return ["G",intGreenScore]
        else:
            return ["B",intRedScore] # "B" Both
            
    def flashTeamScore(self, charTeam):
        if charTeam.upper() == "R":
            self.frameTeamGreen.setTeamScoreColorToDefault()
            self.frameTeamRed.alternateTeamScoreColor()
        elif charTeam.upper() == "G":
            self.frameTeamRed.setTeamScoreColorToDefault()
            self.frameTeamGreen.alternateTeamScoreColor()
        else:
            self.frameTeamRed.setTeamScoreColorToDefault()
            self.frameTeamGreen.setTeamScoreColorToDefault()
    
    # Returns list of list valid ID's: [listValidRedIDs, listValidGreenIDs]
    def getValidIDList_RedTeam(self):
        return self.frameTeamRed.getValidListIntID()
        
    def getValidIDList_GreenTeam(self):
        return self.frameTeamGreen.getValidListIntID()
            
    def resetScores(self):
        self.frameTeamRed.resetScores()
        self.frameTeamGreen.resetScores()