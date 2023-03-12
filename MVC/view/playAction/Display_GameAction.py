import tkinter as tk
from tkinter import ttk
from MVC.app.ApplicationObj import *

class Frame_GameAction(AppObject):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.intMaxGARecords = 6
        
        self.createListColors()
        self.createSelf()
        
    def createListColors(self):
        self.listStrColorRed = [None] * self.intMaxGARecords
        self.listStrColorGreen = [None] * self.intMaxGARecords
        self.listStrColorWhite = [None] * self.intMaxGARecords
        for i in range(self.intMaxGARecords - 3):
            self.listStrColorRed[i] = "#ff0000"
            self.listStrColorGreen[i] = "#00ff00"
            self.listStrColorWhite[i] = "#FFFFFF"
        self.listStrColorRed[self.intMaxGARecords - 3] = "#bd206e"
        self.listStrColorGreen[self.intMaxGARecords - 3] = "#1bbe6e"
        self.listStrColorWhite[self.intMaxGARecords - 3] = "#bdbed4"
        self.listStrColorRed[self.intMaxGARecords - 2] = "#8d2885"
        self.listStrColorGreen[self.intMaxGARecords - 2] = "#238e85"
        self.listStrColorWhite[self.intMaxGARecords - 2] = "#8d8eb9"
        self.listStrColorRed[self.intMaxGARecords - 1] = "#612c91"
        self.listStrColorGreen[self.intMaxGARecords - 1] = "#276391"
        self.listStrColorWhite[self.intMaxGARecords - 1] = "#616386"
        
    def createSelf(self):
        strBGColor = "#731C36"
        strGAColor = "#FFFFFF"
        strFontGA = self.strDefaultFont
        intTextsizeGA = 20
        intTextsizePlayers = 14
        
        self["bg"] = strBGColor
        
        self.labelGameAction = tk.Label(self,
            text="Current Game Action",
            fg = strGAColor, bg = strBGColor, font=(strFontGA, intTextsizeGA))
        self.propagateWidget(self.labelGameAction)
        
        self.midBGFrameAction = [None] * self.intMaxGARecords
        self.labelGAPlayerFrom = [None] * self.intMaxGARecords
        self.labelGAHit = [None] * self.intMaxGARecords
        self.labelGAPlayerTo = [None] * self.intMaxGARecords
        self.listTuplesStrFromTo = [None] * self.intMaxGARecords
        for i in range(self.intMaxGARecords):
            self.midBGFrameAction[i] = tk.Frame(self, 
                bg=strBGColor)
            self.labelGAPlayerFrom[i] = tk.Label(self.midBGFrameAction[i],
                text="",
                fg = self.listStrColorRed[i], bg=strBGColor, font=(strFontGA, intTextsizePlayers))
            self.labelGAHit[i] = tk.Label(self.midBGFrameAction[i],
                text="",
                fg = self.listStrColorWhite[i], bg=strBGColor, font=(strFontGA, intTextsizePlayers))
            self.labelGAPlayerTo[i] = tk.Label(self.midBGFrameAction[i],
                text="",
                fg = self.listStrColorGreen[i], bg=strBGColor, font=(strFontGA, intTextsizePlayers))
            self.listTuplesStrFromTo[i] = ("r", "g")
                
    def gridify(self):
        intCols = 1
        intRows = 8
    
        for i in range(intCols):
            self.columnconfigure(i,weight=1, uniform="uniformMid")
        for i in range(intRows):
            self.rowconfigure(i,weight=1, uniform="uniformMid")
            
        self.labelGameAction.grid(row=0,column=0,columnspan=4,rowspan=2,sticky="NSEW")
        
        intRecordRowspan = 1
        for i in range(self.intMaxGARecords):
            self.midBGFrameAction[i].grid(row=i*intRecordRowspan+2,column=0,columnspan=1,rowspan=intRecordRowspan)
            self.labelGAPlayerFrom[i].pack(side=tk.LEFT, padx=(10,0))
            self.labelGAHit[i].pack(side=tk.LEFT,padx=4)
            self.labelGAPlayerTo[i].pack(side=tk.LEFT, padx=(0,10))
            
    def clearEvents(self):
        for i in range(self.intMaxGARecords):
            self.labelGAPlayerFrom[i]["text"] = ""
            self.labelGAPlayerTo[i]["text"] = ""
            self.labelGAHit[i]["text"] = ""
            
    def writeEvent(self, index, strColorFrom, strPlayerFrom, strColorTo, strPlayerTo, strHit="hit"):
        self.listTuplesStrFromTo[index] = (strColorFrom, strColorTo)
        self.labelGAPlayerFrom[index]["text"] = strPlayerFrom
        self.labelGAPlayerTo[index]["text"] = strPlayerTo
        self.labelGAHit[index]["text"] = strHit
        if strColorFrom == "r" or strColorFrom == "R":
            self.labelGAPlayerFrom[index]["fg"] = self.listStrColorRed[index]
        else:
            self.labelGAPlayerFrom[index]["fg"] = self.listStrColorGreen[index]
        if strColorTo == "r" or strColorTo == "R":
            self.labelGAPlayerTo[index]["fg"] = self.listStrColorRed[index]
        else:
            self.labelGAPlayerTo[index]["fg"] = self.listStrColorGreen[index]
            
    def pushEvent(self, strColorFrom, strPlayerFrom, strColorTo, strPlayerTo):
        for i in range(self.intMaxGARecords - 1):
            indexWrite = self.intMaxGARecords - (i+1)
            indexRead = self.intMaxGARecords - (i+2)
            tupleReadToFrom = self.listTuplesStrFromTo[indexRead]
            self.writeEvent(indexWrite, 
                            tupleReadToFrom[0], self.labelGAPlayerFrom[indexRead]["text"],
                            tupleReadToFrom[1], self.labelGAPlayerTo[indexRead]["text"],
                            self.labelGAHit[indexRead]["text"])
        self.writeEvent(0, strColorFrom, strPlayerFrom, strColorTo, strPlayerTo)
            
            