import tkinter as tk
from MVC.view.display import *



class Menu_AddCodename(Menu):
    def __init__(self, tkRoot, mSubmitCodename):
        super().__init__(tkRoot)

        self.methodSubmitCodename = mSubmitCodename
        self.createSelf()
        self.gridify()

    def enableSelf(self):
        self.entryPlayerCodeName["state"] = "normal"
        self.entryPlayerCodeName.insert(0, "")
        self.entryPlayerCodeName.focus_set()
        self.entryPlayerCodeName.bind("<Return>", self.addPlayerFromMenu)
        self.buttonSubmit["state"] = "normal"
        self.buttonSubmit.bind("<Return>", self.addPlayerFromMenu)

    def disableSelf(self):
        self.entryPlayerCodeName.delete(0, tk.END)
        self.entryPlayerCodeName["state"] = "disabled"
        self.entryPlayerCodeName.unbind("<Return>")
        self.buttonSubmit["state"] = "disabled"
        self.buttonSubmit.unbind("<Return>")
        self.clearInsertMenuError()

    def setInputEntryText(self, strInput):
        self.entryPlayerCodeName.delete(0, tk.END)
        self.entryPlayerCodeName.insert(0, strInput)

    def showInsertMenuError(self, text):
        if len(self.labelInsPError["text"]) > 0:
            self.labelInsPError["text"] = self.labelInsPError["text"] + "\nError: " + text
        else:
            self.labelInsPError["text"] = "Error: " + text

    def clearInsertMenuError(self):
        self.labelInsPError["text"] = ""

    def addPlayerFromMenu(self, event=None):
        intMinCNameLen = 2  # Code Name
        intMaxCNameLen = 30  # Code Name

        self.clearInsertMenuError()
        intLenCodeName = len(self.entryPlayerCodeName.get())
        boolCodeNameInvalid = intLenCodeName < intMinCNameLen or intLenCodeName > intMaxCNameLen or " " in self.entryPlayerCodeName.get() or not self.entryPlayerCodeName.get().isalnum()
        if boolCodeNameInvalid:
            self.showInsertMenuError(
                "Codename name must be \n between 2 - 30 alphanumeric characters \n and no spaces!")
        if not boolCodeNameInvalid:
            print("Can add player!")
            self.clearInsertMenuError()
            self.methodSubmitCodename(self.entryPlayerCodeName.get())

    def createSelf(self):
        strBorderColor = "#5b5bc3"
        strBGColor = "#000000"
        strTextcolorError = "#FF0000"  # True Red
        strTextcolorMain = "#FFFFFF"  # Full White
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
        self.labelPlayerCodeName = tk.Label(self.frameInsPInterior,
                                            text="Player Code Name:",
                                            fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.entryPlayerCodeName = tk.Entry(self.frameInsPInterior,
                                            state="disabled", font=(strFont, intTextsizeMain))
        self.labelHint = tk.Label(self.frameInsPInterior,
                                  text="Tab or click to switch between boxes\nClick submit to insert player\nPress Esc to cancel",
                                  fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeHint))
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
        self.labelPlayerCodeName.grid(column=0, row=6, columnspan=4, rowspan=2, sticky="SEW")
        self.entryPlayerCodeName.grid(column=4, row=6, columnspan=6, rowspan=2, sticky="SEW")
        self.labelHint.grid(column=0, row=9, rowspan=3, columnspan=8, padx=10, sticky="NSW")
        self.buttonSubmit.grid(column=7, row=9, rowspan=2, columnspan=2, sticky="NSEW")