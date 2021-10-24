import os
import shutil

from tkinter import *
from PIL import ImageTk

import GlobalWindowSettings as GlobalWindowSettingsClass

class ItemView:
    def _MoveToOtherCharacter(self, item):
        win = GlobalWindowSettingsClass.GlobalWindowSettings().InitNewWindow()

        i = 0
        for character in self.hGH.CharacterList.characters:
            i += 1
            if character != self.hGH.CharacterList.GetCurrentCharacter():
                Button(win, text=character.GetName(), width=30,  command= lambda win=win, c=character, i=item: self._SelectCharacter(win, c, i)).grid(row=i, column=0)

    def _UpdateImage(self):
        pass

    def _SelectCharacter(self, win, character, item):
        name = item.GetData().GetName()

        if os.path.isfile(os.path.join('.\\Characters\\' + character.GetName(), name + ".jpg")):
            i = 0
            while True:
                i = i + 1
                if not os.path.isfile(os.path.join('.\\Characters\\' + character.GetName(), (name + '_' + str(i) + ".jpg"))):
                    name = name + '_' + str(i)
                    break

        shutil.move('.\\' + item.GetFullPath(), os.path.join('.\\Characters\\' + character.GetName(), name + ".jpg"))
        win.destroy()
    
    def _DeleteItem(self, item, win=None):
        self.hGH.CharacterList.GetCurrentCharacter().GetInventory().RemoveItemFromInventory(item)
        item.Delete()
        self.hGH.ItemListView.ShowItemList(self.hGH.CharacterList.GetCurrentCharacter().GetInventory().GetList())
        if win:
            win.destroy()

    def ShowItemWindow(self, item):
        win = GlobalWindowSettingsClass.GlobalWindowSettings().InitNewWindow()

        Label(win, text=item.GetData().GetName()).pack(side=TOP)

        win.itemImage = ImageTk.PhotoImage(file=item.GetFullPath())

        buttonsFrame = Frame(win)

        Label(win, image=win.itemImage).pack()

        Button(buttonsFrame, text='(U)pdate Image', width=30,  command= lambda: self.hGH.ScreenCapture.AreaSelect()).grid(row=0, column=0, sticky=W, pady=4)
        win.bind('u', lambda e: self.hGH.ScreenCapture.AreaSelect())

        Button(buttonsFrame, text='(M)ove to other Character', width=30,  command= lambda i=item: self._MoveToOtherCharacter(i)).grid(row=0, column=0, sticky=W, pady=4)
        win.bind('m', lambda e: self._MoveToOtherCharacter())

        Button(buttonsFrame, text='(D)elete', width=30,  command= lambda: self._DeleteItem(item, win)).grid(row=0, column=1, sticky=W, pady=4)
        win.bind('d', lambda e: self._DeleteItem(item, win))

        Button(buttonsFrame, text='(C)lose', width=30,  command= lambda: win.destroy()).grid(row=0, column=2, sticky=W, pady=4)
        win.bind('c', lambda e: win.destroy())

        buttonsFrame.pack()

    def __init__(self, HGH):
        self.hGH = HGH