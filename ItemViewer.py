import os
import shutil

from tkinter import *
from PIL import ImageTk, Image

import GlobalWindowSettings as GlobalWindowSettingsClass

class ItemViewer:
    def _MoveToOtherCharacter(self, item):
        win = GlobalWindowSettingsClass.GlobalWindowSettings().InitNewWindow()

        i = 0
        for character in self.HGH.CharacterListData.GetCharacterList(self.HGH.Settings):
            i += 1
            if character != self.HGH.CharacterListView.GetCurrentCharacter():
                Button(win, text=character.GetName(), width=30,  command= lambda win=win, c=character, i=item: self._SelectCharacter(win, c, i)).grid(row=i, column=0)

    def _UpdateImage(self):
        #take an other screenshot to update te picture
        pass

    def _SelectCharacter(self, win, destinationCharacter, item):
        itemName = item.GetData().GetName()

        #Make sure the destination character doesn't have a copy of this item
        if os.path.isfile(os.path.join(destinationCharacter.GetFullPath(), itemName + ".jpg")):
            i = 0
            while True:
                i = i + 1
                if not os.path.isfile(os.path.join(destinationCharacter.GetFullPath(), (itemName + '_' + str(i) + ".jpg"))):
                    itemName = itemName + '_' + str(i)
                    break

        shutil.move('.\\' + item.GetFullPath(), os.path.join(destinationCharacter.GetFullPath(), itemName + ".jpg"))
        win.destroy()
    
    def _DeleteItem(self, item, win=None):
        self.HGH.CharacterListView.GetCurrentCharacter().GetInventory().RemoveItemFromInventory(item)
        item.Delete()
        self.HGH.ItemListView.ShowItemList(self.HGH.CharacterListView.GetCurrentCharacter().GetInventory().GetList())
        self.HGH.ClearItemViewFrame()

    def ShowItem(self, item):
        self.HGH.ClearItemViewFrame()
      
        self.ItemName = Label(self.HGH.ItemViewFrame, text=item.GetData().GetName())
        self.ItemName.pack(side=TOP)

        itemImage = Image.open(item.GetFullPath())
        self.ItemImage = ImageTk.PhotoImage(itemImage)

        print(item.GetData().GetName())
        self.ItemImageDisplay = Label(self.HGH.ItemViewFrame, image=self.ItemImage)
        self.ItemImageDisplay.pack()

        buttonFrame = Frame(self.HGH.ItemViewFrame)

        self.UpdateImage = Button(buttonFrame, text='(U)pdate Image', width=30,  command= lambda: self.HGH.ScreenCapture.AreaSelect()).grid(row=0, column=0, sticky=W, pady=4)
        self.MoveToChar = Button(buttonFrame, text='(M)ove to other Character', width=30,  command= lambda i=item: self._MoveToOtherCharacter(i)).grid(row=0, column=1, sticky=W, pady=4)
        self.DeleteItem = Button(buttonFrame, text='(D)elete', width=30,  command= lambda: self._DeleteItem(item, self.HGH.ItemViewerWindow)).grid(row=0, column=2, sticky=W, pady=4)
        #self.HGH.ItemViewerWindow.bind('d', lambda e: self._DeleteItem(item, self.HGH.ItemViewFrame))

        buttonFrame.pack()

    def __init__(self, hgh):
        self.HGH = hgh
        self.Frame = None
        self.ItemName = None
        self.ItemImage = None
        self.ItemImageDisplay = None
        self.UpdateImage = None
        self.MoveToChar = None
        self.DeleteItem = None
        self.CloseWindow = None