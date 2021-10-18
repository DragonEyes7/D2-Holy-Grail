import os
import Character as CharacterClass
import Inventory as InventoryClass
import Item as ItemClass

from tkinter import *
from os import walk

import GlobalWindowSettings as GlobalWindowSettingsClass

class CharacterList:
    def GetCurrentCharacter(self):
        return self.currentCharacter

    def CreateCharacterWindow(self):
        win = GlobalWindowSettingsClass.GlobalWindowSettings().InitNewWindow()

        Label(win, text="Character Name").grid(row=0)
        
        sv = StringVar()
        sv.trace_variable("w", lambda var, index, mode, sv=sv: self._CharacterNameEntryChanged(ErrorLabel, sv))

        characterNameInput = Entry(win, textvariable=sv)
        characterNameInput.grid(row=0, column=1)

        ErrorLabel = Label(win, text='')
        ErrorLabel.grid(row=2)

        Button(win, text='Create', width=30,  command= lambda: self._CreateCharacterFolder(win, characterNameInput.get(), ErrorLabel)).grid(row=3, column=0, sticky=W, pady=4)
        win.bind('<Return>', lambda e: self._CreateCharacterFolder(win, characterNameInput.get(), ErrorLabel))

        Button(win, text='Cancel', width=30,  command= lambda: win.destroy()).grid(row=3, column=1, sticky=W, pady=4)
        
    def _CharacterNameEntryChanged(self, ErrorLabel, sv):
        ErrorLabel['text'] = ''

    def _CreateCharacter(self, dirName):
        characterInv = InventoryClass.Inventory()
        character = CharacterClass.Character(dirName, characterInv) 
        return character

    def _CreateCharacterFolder(self, win, characterName, ErrorLabel):
        if not os.path.isdir("Characters\\" + characterName):
            os.mkdir("Characters\\" + characterName)
            win.destroy()
            character = self._CreateCharacter(characterName)
            self.characters.append(character)
            self.characters.sort(key=lambda char: char.GetName().lower())
            self.ShowCharacterButtons(True)
        else:
            ErrorLabel['text'] = "Character already Exist" 

    def _DeleteCharacter(self, character):
        #warning Character Inventory is not empty are you sure you want to delete?
        if len(character.GetInventory().GetList()) > 0:
            #open a warning popup
            Label(self.root, text="Character Inventory is not empty are you sure you want to delete?").pack(side=TOP)
        else:
            if os.path.isdir(character.GetPath()):
                os.rmdir(character.GetPath())
                self.characters.remove(character)

        self.ShowCharacterButtons(True)

    def _SelectCharacter(self, character):
        if not hasattr(self, 'currentCharacter'):
            self.hGH.MainFrame = Frame(self.root)

            Button(self.hGH.MainFrame, text='(A)dd Item', width=30,  command=lambda: self.hGH.ScreenCapture.AreaSelect()).pack()
            self.hGH.MainFrame.bind('a', lambda e: self.hGH.ScreenCapture.AreaSelect())

            self.hGH.MainFrame.grid()

        self.currentCharacter = character
        self.hGH.ItemListView.ShowItemListFromInventory(self.currentCharacter.GetInventory().GetList())

    def ShowCharacterButtons(self, clear = False):
        if clear:
            self.hGH.ClearCharacterListFrame()

        Label(self.hGH.CharacterListFrame, text='Character List:').grid(row=0)
        
        #Maybe change the delete by an icon
        #self.hGH.CharacterListFrame.deleteIcon = ImageTk.PhotoImage(file='Icons\\delete-folder.png')
        
        i = 0
        for character in self.characters:
            i += 1

            Button(self.hGH.CharacterListFrame, text=character.GetName(), width=30,  command= lambda c=character: self._SelectCharacter(c)).grid(row=i, column=0)
            Button(self.hGH.CharacterListFrame, text='Delete', width=5, command= lambda c=character: self._DeleteCharacter(c)).grid(row=i, column=1)
    
    def __init__(self, hGH, root, itemList):
        self.root = root
        self.hGH = hGH
        
        self.characters = []

        path = 'Characters'

        for (dirpath, dirnames, filenames) in walk(path):
            for dirname in dirnames:
                character = self._CreateCharacter(dirname)
                self.characters.append(character)
                for (dirpath, dirnames, filenames) in walk(path + '\\' + dirname):
                    for file in filenames:
                        #find item Data and fill it
                        itemData = itemList.GetItemFromName(file.split('.')[0], None)
                        item = ItemClass.Item(file, dirpath, itemData)
                        character.GetInventory().AddItemToInventory(item)