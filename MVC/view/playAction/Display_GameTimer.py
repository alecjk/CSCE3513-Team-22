import tkinter as tk
from tkinter import ttk
import time
from MVC.app.ApplicationObj import *

class Display_GameTimer(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.boolIsTimerActive = False
        self.boolHasTimerFinished = True
        self.boolIsTimerPaused = False
        self.floatTimeUntil = 0.0
        self.floatLastUpdatedTime = 0.0
        self.floatTimePausedRemaining = 0.0
        self.createSelf()


    def createSelf(self):
        strBGColor = "#000000"
        strTextColor = "#FFFFFF"
        strFont = self.strDefaultFont
        strTextsizeTime = 24
    
        self["bg"] = strBGColor        
        
        self.labelTimeRemaining = tk.Label(self, 
            text="Time Remaining: 6:00",
            fg=strTextColor, bg=strBGColor, font=(self.strDefaultFont, strTextsizeTime))
        self.propagateWidget(self.labelTimeRemaining)
        
    def gridify(self):
        intCols = 1
        intRows = 1
        for i in range(intCols):
            self.columnconfigure(i,weight=1, uniform="gridUniform")
        for i in range(intRows):
            self.rowconfigure(0,weight=1, uniform="gridUniform")
        self.labelTimeRemaining.grid(column=0, row=0, sticky="E")
        
    def updateTimerStrLabel(self, strTime):
        self.labelTimeRemaining["text"] = "Time Remaining: " + strTime
        self.root.update()
         
    def updateTimer(self):
        if self.boolIsTimerActive:
            floatTimeRemaining = self.floatTimeUntil - time.time()
            if floatTimeRemaining <= 1.0: # Does not reach below 0.0 - not sure why. Should still function correctly though
                self.stopTimer()
            elif int(floatTimeRemaining) != int(self.floatLastUpdatedTime):
                strTimeRemaining = self.getFormattedTimeStr(floatTimeRemaining)
                self.updateTimerStrLabel(strTimeRemaining)
                
    def getTimeRemaining(self):
        if self.boolIsTimerPaused:
            return self.floatTimePausedRemaining
        else:
            return self.floatTimeUntil - time.time()
            
    def getFormattedTimeRemaining(self):
        if self.boolIsTimerPaused:
            return self.getFormattedTimeStr(self.floatTimePausedRemaining)
        else:
            return self.getFormattedTimeStr(self.floatTimeUntil - time.time())
            
    def getFormattedTimeStr(self, floatTimeRemaining):
        intMinRemaining = int(floatTimeRemaining / 60.0)
        intSecRemaining = int(floatTimeRemaining - intMinRemaining*60.0)
        strSecRemaining = str(intSecRemaining)
        if intSecRemaining < 10:
            strSecRemaining = "0" + strSecRemaining
        return str(intMinRemaining) + ":" + strSecRemaining
                
    def pauseTimer(self):
        self.floatTimePausedRemaining = self.floatTimeUntil - time.time()
        self.boolIsTimerPaused = True
        self.boolIsTimerActive = False
        
    def unpauseTimer(self):
        self.boolIsTimerPaused = False
        self.startTimer(self.floatTimePausedRemaining)
        
    def isTimerPaused(self):
        return self.boolIsTimerPaused
        
    def isTimerActive(self):
        return self.boolIsTimerActive
        
    def hasTimerFinished(self):
        return self.hasTimerFinished
        
    def startTimer(self, starttime=361.0):
        if not self.boolIsTimerActive:
            self.floatTimeUntil = time.time() + starttime
            self.boolIsTimerActive = True
            self.boolHasTimerFinished = False
            
    def stopTimer(self):
        if self.boolIsTimerActive:
            self.updateTimerStrLabel("0:00")
            self.boolHasTimerFinished = True
            self.boolIsTimerActive = False