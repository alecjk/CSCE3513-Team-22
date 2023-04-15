import tkinter as tk
from MVC.view.display import *


class Display_SingleEntryBox(Display):
    def __init__(self, tkRoot, methodSubmit=None):
        super().__init__(tkRoot)

        if methodSubmit is not None:
            self.bindSubmit(methodSubmit)
        self.createSelf()
        self.gridify()

    def bindSubmit(self, methodSubmit):
        self.methodSubmit = methodSubmit

    def setTitle(self, strInput):
        self.labelTitle["text"] = strInput

    def setInputEntryText(self, strInput):
        self.entryInputEntry.delete(0, tk.END)
        self.entryInputEntry.insert(0, strInput)

    def getInputEntryText(self):
        return self.entryInputEntry.get()

    def setInputTitleText(self, strInput):
        self.labelInputTitle["text"] = strInput

    def setHintText(self, strInput):
        self.labelHint["text"] = strInput

    def enableSelf(self):
        self.tkraise()
        self.entryInputEntry["state"] = "normal"
        self.entryInputEntry.focus_set()
        self.entryInputEntry.bind("<Return>", self.submit)
        self.buttonSubmit["state"] = "normal"
        self.buttonSubmit.bind("<Return>", self.submit)

    def disableSelf(self):
        self.entryInputEntry.delete(0, tk.END)
        self.entryInputEntry["state"] = "disabled"
        self.entryInputEntry.unbind("<Return>")
        self.buttonSubmit["state"] = "disabled"
        self.buttonSubmit.unbind("<Return>")
        self.clearError()

    def setError(self, text, boolOverwrite=False):
        if len(self.labelError["text"]) > 0 and not boolOverwrite:
            self.labelError["text"] = self.labelError["text"] + "\nError: " + text
        else:
            self.labelError["text"] = "Error: " + text

    def clearError(self):
        self.labelError["text"] = ""

    def submit(self, event=None):
        self.methodSubmit()

    def createSelf(self):
        strBGColor = "#000000"
        strTextcolorError = "#FF0000"
        strTextcolorMain = "#FFFFFF"
        strFont = self.strDefaultFont
        intTextsizeHead = 20
        intTextsizeError = 14
        intTextsizeHint = 15
        intTextsizeMain = 16

        self.propagateWidget(self)
        self.frameInterior = tk.Frame(self, bg=strBGColor)
        self.labelTitle = tk.Label(self.frameInterior,
                                   text="This is a Title",
                                   fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeHead))
        self.labelError = tk.Label(self.frameInterior,
                                   text="",
                                   fg=strTextcolorError, bg=strBGColor, font=(strFont, intTextsizeError))
        self.labelInputTitle = tk.Label(self.frameInterior,
                                        text="Input Title:",
                                        fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))
        self.entryInputEntry = tk.Entry(self.frameInterior,
                                        state="disabled", font=(strFont, intTextsizeMain))
        self.labelHint = tk.Label(self.frameInterior,
                                  text="This is\na hint box.\nThis is\n a hint box.",
                                  fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeHint))
        self.buttonSubmit = tk.Button(self.frameInterior,
                                      text="Submit",
                                      command=self.submit,
                                      state="disabled",
                                      fg=strTextcolorMain, bg=strBGColor, font=(strFont, intTextsizeMain))

    def gridify(self):
        intBorderSize = 10
        self.frameInterior.pack(side="top", fill="both", expand=True,
                                padx=intBorderSize, pady=intBorderSize)
        intFrameInsPCols = 12
        intFrameInsPRows = 12

        for i in range(intFrameInsPCols):
            self.frameInterior.columnconfigure(i, weight=1, uniform="uniformIns")
        for i in range(intFrameInsPRows):
            self.frameInterior.rowconfigure(i, weight=1, uniform="uniformIns")
        self.labelTitle.grid(column=0, row=0, columnspan=10, rowspan=2, sticky="NSEW")
        self.labelError.grid(column=0, row=2, columnspan=10, rowspan=2, sticky="NEW")
        self.labelInputTitle.grid(column=0, row=4, columnspan=4, rowspan=2, sticky="SEW")
        self.entryInputEntry.grid(column=4, row=4, columnspan=6, rowspan=2, sticky="SEW")
        self.buttonSubmit.grid(column=7, row=9, rowspan=2, columnspan=2, sticky="NSEW")