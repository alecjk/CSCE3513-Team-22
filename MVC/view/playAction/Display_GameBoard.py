import tkinter as tk
from tkinter import ttk
from MVC.app.ApplicationObj import *
from MVC.view.playAction.Display_Scoreboard import *
from MVC.view.playAction.Display_GameAction import *
from MVC.view.playAction.Display_GameTimer import *

class Display_GameBoard(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)

        self.createSelf()
        
    def createSelf(self):
        strBorderColor = "#FFFFFF"
    
        self["bg"] = strBorderColor
        
        self.frameScoreboard = Display_Scoreboard(self)
        self.propagateWidget(self.frameScoreboard)
        self.frameGameAction = Display_GameAction(self)
        self.propagateWidget(self.frameGameAction)
        self.frameGameTimer = Display_GameTimer(self)
        self.propagateWidget(self.frameGameTimer)
        
    def setPlayersUsingList(self, listPlayers, listIntID=None):
        self.frameScoreboard.setPlayersUsingList(listPlayers, listIntID)
        
    def getCodenameFromID(self, intID, charTeam):
        return self.frameScoreboard.getCodenameFromID(intID, charTeam)
        
    def getValidListIntID(self):
        return self.frameScoreboard.getValidListIntID()
        
    def clearGameAction(self):
        self.frameGameAction.clearEvents()
        
    def resetScoreboard(self):
        self.frameScoreboard.resetScores()
        
    def gridify(self):
        intBackgroundCols = 10
        intBackgroundRows = 10
        
        for i in range(intBackgroundCols):
            self.columnconfigure(i,weight=1, uniform="gridUniform")
        for i in range(intBackgroundRows):
            self.rowconfigure(i,weight=1, uniform="gridUniform")
            
        self.frameGameAction.grid(column=0, row=0, columnspan=10, rowspan=3, padx=2, pady=2, sticky="NSEW")
        self.frameGameAction.gridify()
        self.frameScoreboard.grid(column=0, row=3, columnspan=10, rowspan=6, padx=2, pady=2, sticky="NSEW")
        self.frameScoreboard.gridify()
        self.frameGameTimer.grid(column=0, row=9, columnspan=10, rowspan=1, padx=2, pady=2, sticky="NSEW")
        self.frameGameTimer.gridify()