import tkinter as tk


class AppObject(tk.Frame):
    def __init__(self, tkRoot):
        super().__init__(tkRoot)
        self.root = tkRoot
        self.setDefaults()

    def propagateWidget(self, widget):
        widget.pack_propagate(False)
        widget.grid_propagate(False)

    def setDefaults(self):
        self.strDefaultFont = "Arial"
        self["bg"] = "#000000"

    def hideSelf(self):
        self.grid_remove()

    def showSelf(self):
        self.grid()
        self.tkraise()