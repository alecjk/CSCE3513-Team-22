import tkinter as tk
from tkinter import ttk
from MVC.view.display import *


class Display_AddPlayerName(Display):
    def __init__(self, tkRoot, mSubmitPlayerName):
        super().__init__(tkRoot)

        self.methodSubmitPlayerName = mSubmitPlayerName
        self.createSelf()
        self.gridify()

    def setPlayerName(self, strFirstName, strLastName):
        self.entryPlayerFirstName.insert(0, strFirstName)
        self.entryPlayerLastName.insert(0, strLastName)

    def enableSelf(self):
        self.tkraise()
        self.entryPlayerFirstName["state"] = "normal"
        self.entryPlayerFirstName.focus_set()
        self.entryPlayerLastName["state"] = "normal"
        self.buttonSubmit["state"] = "normal"
        self.buttonSubmit.bind("<Return>", self.addPlayerFromMenu)

    def disableSelf(self):
        self.entryPlayerFirstName.delete(0, tk.END)
        self.entryPlayerFirstName["state"] = "disabled"
        self.entryPlayerLastName.delete(0, tk.END)
        self.entryPlayerLastName["state"] = "disabled"
        self.buttonSubmit["state"] = "disabled"
        self.buttonSubmit.unbind("<Return>")
        self.clearInsertMenuError()

    def showInsertMenuError(self, text):
        if len(self.labelInsPError["text"]) > 0:
            self.labelInsPError["text"] = self.labelInsPError["text"] + "\nError: " + text
        else:
            self.labelInsPError["text"] = "Error: " + text

    def clearInsertMenuError(self):
        self.labelInsPError["text"] = ""

    def addPlayerFromMenu(self, event=None):
        intMinPFNameLen = 2
        intMaxPFNameLen = 30
        intMinPLNameLen = 2
        intMaxPLNameLen = 30

        self.clearInsertMenuError()
        intLenPlayerFirstName = len(self.entryPlayerFirstName.get())
        intLenPlayerLastName = len(self.entryPlayerLastName.get())
        boolFirstNameInvalid = intLenPlayerFirstName < intMinPFNameLen or intLenPlayerFirstName > intMaxPFNameLen or " " in self.entryPlayerFirstName.get() or not self.entryPlayerFirstName.get().isalnum()
        boolLastNameInvalid = intLenPlayerLastName < intMinPLNameLen or intLenPlayerLastName > intMaxPLNameLen or " " in self.entryPlayerLastName.get() or not self.entryPlayerLastName.get().isalnum()
        if boolFirstNameInvalid:
            self.showInsertMenuError("First name must be between \n4 - 48 characters")
        if boolLastNameInvalid:
            self.showInsertMenuError("First name must be between \n4 - 48 characters")
        if not boolFirstNameInvalid and not boolLastNameInvalid:
            self.clearInsertMenuError()
            self.methodSubmitPlayerName(self.entryPlayerFirstName.get(), self.entryPlayerLastName.get())

    def createSelf(self):
        strBGColor = "#000000"
        strTextcolorError = "#FF0000"
        strTextcolorMain = "#FFFFFF"
        strFont = self.strDefaultFont
        intTextsizeHead = 20
        intTextsizeError = 14
        intTextsizeHint = 15
        intTextsizeMain = 16

        self.proWidget(self)
        self.frameInsPInterior = tk.Frame(self, bg=strBGColor)
        self.labelInsPHead = tk.Label(self.frameInsPInterior,
                                      text="Insert Player",
                                      fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeHead))
        self.labelInsPError = tk.Label(self.frameInsPInterior,
                                       text="",
                                       fg=strTextcolorError, bg=strBGColor, font=(strFont, intTextsizeError))
        self.labelPlayerFirstName = tk.Label(self.frameInsPInterior,
                                             text="Player First Name:",
                                             fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.entryPlayerFirstName = tk.Entry(self.frameInsPInterior,
                                             state="disabled", font=(strFont, intTextsizeMain))
        self.labelPlayerLastName = tk.Label(self.frameInsPInterior,
                                            text="Player Last Name:",
                                            fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.entryPlayerLastName = tk.Entry(self.frameInsPInterior,
                                            state="disabled", font=(strFont, intTextsizeMain))
        self.buttonSubmit = tk.Button(self.frameInsPInterior,
                                      text="Submit",
                                      command=self.addPlayerFromMenu,
                                      state="disabled",
                                      fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.buttonSubmit.bind("<Return>", self.addPlayerFromMenu)

    def gridify(self):
        intBorderSize = 10
        self.frameInsPInterior.pack(side="top", fill="both", expand=True,
                                    padx=intBorderSize, pady=intBorderSize)

        intFrameInsPCols = 12
        intFrameInsPRows = 12

        for i in range(intFrameInsPCols):
            self.frameInsPInterior.columnconfigure(i, weight=1, uniform="uniformIns")
        for i in range(intFrameInsPRows):
            self.frameInsPInterior.rowconfigure(i, weight=1, uniform="uniformIns")
        self.labelInsPHead.grid(column=0, row=0, columnspan=10, rowspan=2, sticky="NSEW")
        self.labelInsPError.grid(column=0, row=2, columnspan=10, rowspan=2, sticky="NEW")
        self.labelPlayerFirstName.grid(column=0, row=4, columnspan=4, rowspan=2, sticky="SEW")
        self.entryPlayerFirstName.grid(column=4, row=4, columnspan=6, rowspan=2, sticky="SEW")
        self.labelPlayerLastName.grid(column=0, row=6, columnspan=4, rowspan=2, sticky="SEW")
        self.entryPlayerLastName.grid(column=4, row=6, columnspan=6, rowspan=2, sticky="SEW")
        self.buttonSubmit.grid(column=7, row=9, rowspan=2, columnspan=2, sticky="NSEW")