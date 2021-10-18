from tkinter import *

class GlobalWindowSettings:
    def InitNewWindow(self):
        win = Toplevel()
        win.config(bg="#232b25")
        win.focus_force()
        return win

    def __init__(self) -> None:
        pass