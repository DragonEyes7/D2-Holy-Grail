from tkinter import *
from PIL import ImageTk

import GlobalWindowSettings as GlobalWindowSettingsClass

class ItemView:
    def _MoveToOtherCharacter(self):
        pass

    def _UpdateImage(self):
        pass
    
    def _DeleteItem(self, item, win=None):
        self.currentCharacter.GetInventory().RemoveItemFromInventory(item)
        item.Delete()
        self.hGH.ItemListView.ShowItemList(self.currentCharacter.GetInventory().GetList())
        if win:
            win.destroy()

    def ShowItemWindow(self, item):
        win = GlobalWindowSettingsClass.GlobalWindowSettings().InitNewWindow()

        Label(win, text=item.GetData().GetName()).pack(side=TOP)

        win.itemImage = ImageTk.PhotoImage(file=item.GetFullPath())

        buttonsFrame = Frame(win)

        Label(win, image=win.itemImage).pack()

        Button(buttonsFrame, text='(U)pdate Image', width=30,  command= lambda: self._UpdateImage()).grid(row=0, column=0, sticky=W, pady=4)
        win.bind('u', lambda e: self._UpdateImage())

        Button(buttonsFrame, text='(M)ove to other Character', width=30,  command= lambda: self._MoveToOtherCharacter()).grid(row=0, column=0, sticky=W, pady=4)
        win.bind('m', lambda e: self._MoveToOtherCharacter())

        Button(buttonsFrame, text='(D)elete', width=30,  command= lambda: self._DeleteItem(item, win)).grid(row=0, column=1, sticky=W, pady=4)
        win.bind('d', lambda e: self._DeleteItem(item, win))

        Button(buttonsFrame, text='(C)lose', width=30,  command= lambda: win.destroy()).grid(row=0, column=2, sticky=W, pady=4)
        win.bind('c', lambda e: win.destroy())

        buttonsFrame.pack()

    def __init__(self):
        pass