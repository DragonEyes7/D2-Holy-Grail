import os
import Character as CharacterClass
import Inventory as InventoryClass
import Item as ItemClass

from tkinter import *
from os import walk
from PIL import ImageTk

class CharacterList:
    def GetCurrentCharacter(self):
        return self.currentCharacter

    def CreateCharacterWindow(self):
        win = self.hGH.InitNewWindow()

        Label(win, text="Character Name").grid(row=0)
        
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self._CharacterNameEntryChanged(ErrorLabel, sv))

        characterNameInput = Entry(win)
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
            self.ShowCharacterButtons()
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

        self.ShowCharacterButtons()

    def _SelectCharacter(self, character):
        self.currentCharacter = character

        #self.hGH.MainFrame.destroy()

        self._ShowItemList()

        self.hGH.MainFrame = Frame(self.root)

        Button(self.hGH.MainFrame, text='(A)dd Item', width=30,  command=lambda: self.hGH.AreaSelect()).pack()
        #self.MainFrame.bind('a', lambda e: self.hGH.AreaSelect())

        Button(self.hGH.MainFrame, text='Delete Item', width=30).pack()  #command=lambda: self.hGH.AreaSelect()).pack()

        self.hGH.MainFrame.pack()

    def _ShowItemList(self):
        Label(self.hGH.CurrentViewFrame, text='Item List:').grid(row=0)

        i = 0
        for item in self.currentCharacter.GetInventory().GetList():
            i += 1
            
            Button(self.hGH.CurrentViewFrame, text=item.GetName(), width=30,  command= lambda i=item: self._SelectItem(i)).grid(row=i, column=0)
            Button(self.hGH.CurrentViewFrame, text='Delete', width=5, command= lambda i=item: self._DeleteItem(i)).grid(row=i, column=1)

    def _SelectItem(self, item):
        win = self.hGH.InitNewWindow()

        Label(win, text=item.GetName()).pack(side=TOP)

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

    def _DeleteItem(self, item, win=None):
        self.currentCharacter.GetInventory().RemoveItemFromInventory(item)
        item.Delete()
        self._ShowItemList()
        if win:
            win.destroy()

    def _MoveToOtherCharacter(self):
        pass

    def ShowCharacterButtons(self):
        Label(self.hGH.CharacterListFrame, text='Character List:').grid(row=0)
        
        #Maybe change the delete by an icon
        #self.hGH.CharacterListFrame.deleteIcon = ImageTk.PhotoImage(file='Icons\\delete-folder.png')
        
        i = 0
        for character in self.characters:
            i += 1

            Button(self.hGH.CharacterListFrame, text=character.GetName(), width=30,  command= lambda c=character: self._SelectCharacter(c)).grid(row=i, column=0)
            Button(self.hGH.CharacterListFrame, text='Delete', width=5, command= lambda c=character: self._DeleteCharacter(c)).grid(row=i, column=1)
    
    def __init__(self, hGH, root):
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
                        item = ItemClass.Item(file, dirpath)
                        character.GetInventory().AddItemToInventory(item)