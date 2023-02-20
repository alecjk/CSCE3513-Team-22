import tkinter as tk
from MVC.view.display import *


class Display_AddCodename(Display):
    def __init__(self, tkRoot, dSubmitCodename):
        super().__init__(tkRoot)

        self.methodSubmitCodename = dSubmitCodename
        self.createSelf()
        self.gridify()

    def enableSelf(self):
        self.entryCodeName["state"] = "normal"
        self.entryCodeName.insert(0, "")
        self.entryCodeName.focus_set()
        self.entryCodeName.bind("<Return>", self.addPlayerFromDisplay)
        self.submitButton["state"] = "normal"
        self.submitButton.bind("<Return>", self.addPlayerFromDisplay)

    def disableSelf(self):
        self.entryCodeName.delete(0, tk.END)
        self.entryCodeName["state"] = "disabled"
        self.entryCodeName.unbind("<Return>")
        self.submitButton["state"] = "disabled"
        self.submitButton.unbind("<Return>")
        self.clearInsertDisplayError()

    def setInputEntryText(self, strInput):
        self.entryCodeName.delete(0, tk.END)
        self.entryCodeName.insert(0, strInput)

    def showInsertDisplayError(self, text):
        if len(self.labelInsPError["text"]) > 0:
            self.labelInsPError["text"] = self.labelInsPError["text"] + "\nError: " + text
        else:
            self.labelInsPError["text"] = "Error: " + text

    def clearInsertDisplayError(self):
        self.labelInsPError["text"] = ""

    def addPlayerFromDisplay(self, event=None):
        intMinCNameLen = 4
        intMaxCNameLen = 48

        self.clearInsertDisplayError()
        intLenCodeName = len(self.entryCodeName.get())
        boolCodeNameInvalid = intLenCodeName < intMinCNameLen or intLenCodeName > intMaxCNameLen or " " in self.entryCodeName.get() or not self.entryCodeName.get().isalnum()
        if boolCodeNameInvalid:
            self.showInsertDisplayError(
                "Codename cannot be longer \n than 4 - 48 characters")
        if not boolCodeNameInvalid:
            print("Can add player!")
            self.clearInsertDisplayError()
            self.methodSubmitCodename(self.entryCodeName.get())

    def createSelf(self):
        strBGColor = "#000000"
        strTextcolorError = "#FF0000"
        strTextcolorMain = "#FFFFFF"
        strFont = self.strDefaultFont
        intTextsizeHead = 20
        intTextsizeError = 14
        intTextsizeMain = 16

        self.proWidget(self)
        self.frameInsPInterior = tk.Frame(self, bg=strBGColor)
        self.labelInsPHead = tk.Label(self.frameInsPInterior,
                                      text="Insert Player",
                                      fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeHead))
        self.labelInsPError = tk.Label(self.frameInsPInterior,
                                       text="",
                                       fg=strTextcolorError, bg=strBGColor, font=(strFont, intTextsizeError))
        self.labelPlayerCodeName = tk.Label(self.frameInsPInterior,
                                            text="Player Code Name:",
                                            fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.entryCodeName = tk.Entry(self.frameInsPInterior,
                                      state="disabled", font=(strFont, intTextsizeMain))
        self.submitButton = tk.Button(self.frameInsPInterior,
                                      text="Submit",
                                      command=self.addPlayerFromDisplay,
                                      state="disabled",
                                      fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.submitButton.bind("<Return>", self.addPlayerFromDisplay)

    def gridify(self):
        intBorderSize = 6
        self.frameInsPInterior.pack(side="top", fill="both", expand=True, padx=intBorderSize, pady=intBorderSize)

        intFrameInsPCols = 15
        intFrameInsPRows = 15

        for i in range(intFrameInsPCols):
            self.frameInsPInterior.columnconfigure(i, weight=1, uniform="uniformIns")
        for i in range(intFrameInsPRows):
            self.frameInsPInterior.rowconfigure(i, weight=1, uniform="uniformIns")
        self.labelInsPHead.grid(column=0, row=0, columnspan=10, rowspan=2, sticky="NSEW")
        self.labelInsPError.grid(column=0, row=2, columnspan=10, rowspan=2, sticky="NEW")
        self.labelPlayerCodeName.grid(column=0, row=6, columnspan=4, rowspan=2, sticky="SEW")
        self.entryCodeName.grid(column=4, row=6, columnspan=6, rowspan=2, sticky="SEW")
        self.submitButton.grid(column=7, row=9, rowspan=2, columnspan=2, sticky="NSEW")