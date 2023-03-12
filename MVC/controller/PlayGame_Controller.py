import time
import tkinter as tk
from tkinter import ttk
from MVC.app.ApplicationObj import *
from lib.playgame.PlayGame_UI import *
from lib.playgame.PlayGame_MenuManager import *
from lib.playgame.TrafficGenerator import *
from lib.Network import *

class Screen_PlayGame(AppObject):
	MENU_MAIN = 0
	MENU_WAITSTART = 1
	MENU_BACKTOEDIT = 2

	def __init__(self, tkRoot):
		super().__init__(tkRoot)
		
		self.intMenu = self.MENU_MAIN
		self.methodMoveToEdit = None
		self.intIDAfter = 0
		self.floatHighScoreFlashLastTime = 0.0
		
		self.listValidRedIDs = []
		self.listValidGreenIDs = []
		
		self.network = Network()
		self.trafficGenerator = TrafficGenerator()
		self.trafficGenerator.bindBroadcastingSocket(self.network.getReceivingSocket())
		
		self.network.startThread()
		
		self.menuManager = PlayGame_MenuManager()
		self.createScreen()
		self.gridify()
		self.showSelf()
		self.hideSelf()
		
	def createScreen(self):
		self["bg"] = "#000000"
		self.playGameUI = PlayGame_UI()
		
	def gridify(self):
		FrameCols = 24
		FrameRows = 40

		# Position F Key - Row
		intPosFKeyRow = 35
		intFKeyRowSpan = 5
		intFKeyColSpan = 2
		
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(0, weight = 1)
		self.grid(column = 0, row = 0, sticky = "NSEW")
		for i in range(FrameCols):
			self.columnconfigure(i, weight = 1, uniform = "gridUniform")
		for i in range(FrameRows):
			self.rowconfigure(i, weight = 1, uniform = "gridUniform")
			
		self.menuManager.grid(column = 6, row = 8, columnspan = 12, rowspan = 20, sticky = "NSEW")
		self.menuManager.gridify()
		self.menuManager.closeSelf()
		
		self.playGameUI.grid(column = 0, row = 0, columnspan = FrameCols, rowspan = FrameRows, sticky = "NSEW")
		self.playGameUI.gridify()
		self.playGameUI.closeSelf()
	

	# Menu Functions	
	def getMenuState(self):
		return self.menuManager.getMenuState()
		
	def closeAllMenus(self):
		self.menuManager.closeAllMenus()
		
	def closeMoveToEditMenu(self):
		self.menuManager.closeMoveToEditMenu()
			
	def openMoveToEditMenu(self):
		self.menuManager.openMoveToEditMenu()


	# Update Game Functions     
	def updateHitEventByLastTrans(self):
		if self.network.hasNewTransmission():
			lastTransmission = self.network.getLastTransmission()
			listID = lastTransmission.split(":")
			self.updateHitEvent(int(listID[0]), int(listID[1]))
		
	def updateScreen(self):
		if self.frameGameboard.frameGameTimer.isTimerActive() and not self.frameGameboard.frameGameTimer.isTimerPaused():
			self.updateHitEventByLastTrans()
			self.frameGameboard.frameGameTimer.updateTimer()
			if abs(time.time() - self.floatHighScoreFlashLastTime) >= 0.25:
				self.flashTeamScore()
				self.floatHighScoreFlashLastTime = time.time()
			self.intIDAfter = self.root.after(1, self.updateScreen)
		elif self.frameWaitUntilPlay.isCountActive() and not self.frameWaitUntilPlay.isPaused():
			self.frameWaitUntilPlay.updateCount()
			self.intIDAfter = self.root.after(1, self.updateScreen)
			
	def updateHitEvent(self, intIDFrom, intIDTo):
		charFromColor = 'r'
		if intIDFrom in self.listOfListIntPlayerIDs[1]:
			charFromColor = 'g'
		charToColor = 'r'
		if intIDTo in self.listOfListIntPlayerIDs[1]:
			charToColor = 'g'
		if charFromColor == charToColor:
			print("Both IDs from same color! Ignoring...")
		elif self.isValidID(charFromColor, intIDFrom) == False or self.isValidID(charToColor, intIDTo) == False:
			print("updateHitEvent: Error - One or more invalid IDs given!")
			if self.isValidID(charFromColor, intIDFrom) == False:
				print("\tID: {} is invalid for given team color!".format(intIDFrom))
			if self.isValidID(charToColor, intIDTo) == False:
				print("\tID: {} is invalid for given team color!".format(intIDTo))
		else:
			strPlayerFrom = self.frameGameboard.getCodenameFromID(intIDFrom, charFromColor)
			#print("strPlayerFrom: {}".format(strPlayerFrom))
			strPlayerTo = self.frameGameboard.getCodenameFromID(intIDTo, charToColor)
			#print("strPlayerTo: {}".format(strPlayerTo))
			self.frameGameboard.frameGameAction.pushEvent(
										charFromColor, strPlayerFrom,
										charToColor, strPlayerTo)
			if intIDFrom in self.listOfListIntPlayerIDs[0]:
				self.frameGameboard.frameScoreboard.frameTeamRed.updatePlayerScore(intIDFrom,10)
			else:
				self.frameGameboard.frameScoreboard.frameTeamGreen.updatePlayerScore(intIDFrom,10)
  

   # Score Functions         
	def flashTeamScore(self):
		charHighestTeam = self.frameGameboard.frameScoreboard.getListHighestTeamScore()[0]
		self.frameGameboard.frameScoreboard.flashTeamScore(charHighestTeam)
		
	def setPlayersUsingList(self, listPlayers, listIDs):
		self.playGameUI.setPlayersUsingList(listPlayers, listIDs)
		
	def setValidIDsFromScoreboard(self):
		self.listValidRedIDs = self.frameGameboard.frameScoreboard.getValidIDList_RedTeam()
		self.listValidGreenIDs = self.frameGameboard.frameScoreboard.getValidIDList_GreenTeam()
		
	def isValidID(self, charTeam, intID):
		if charTeam.upper() == "R":
			return (intID in self.listValidRedIDs)
		elif charTeam.upper() == "G":
			return (intID in self.listValidGreenIDs)
		else:
			return False


	# Traffic Generators    
	def isTrafficGeneratorRunning(self):
		return self.trafficGenerator.isRunning()

	def startTrafficGenerator(self):
		self.trafficGenerator.startThread()
		
	def resetScoreboard(self):
		self.frameGameboard.resetScoreboard()

	def endTrafficGenerator(self):
		self.trafficGenerator.stopThread()

	def clearGameAction(self):
		self.frameGameboard.clearGameAction()

