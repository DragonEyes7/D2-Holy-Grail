from tkinter import *
from PIL import ImageTk

class ItemView:
    def ShowItemWindow(self, item):
        win = self.hGH.InitNewWindow()

        Label(win, text=item.GetData().GetName()).pack(side=TOP)

        win.itemImage = ImageTk.PhotoImage(file=item.GetFullPath())

        buttonsFrame = Frame(win)

        Label(win, image=win.itemImage).pack()

        Button(buttonsFrame, text='(M)ove to other Character', width=30,  command= lambda: self._MoveToOtherCharacter()).grid(row=0, column=0, sticky=W, pady=4)
        win.bind('m', lambda e: self._MoveToOtherCharacter())

        Button(buttonsFrame, text='(D)elete', width=30,  command= lambda: self._DeleteItem(item, win)).grid(row=0, column=1, sticky=W, pady=4)
        win.bind('d', lambda e: self._DeleteItem(item, win))

        Button(buttonsFrame, text='(C)lose', width=30,  command= lambda: win.destroy()).grid(row=0, column=2, sticky=W, pady=4)
        win.bind('c', lambda e: win.destroy())

        buttonsFrame.pack()

    def __init__(self):
        pass