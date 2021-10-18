import os
from os import walk
from tkinter import *

import CharacterList as CharacterListClass
import ItemList as ItemListClass
import ScreenCapture as ScreenCaptureClass
import ItemListView as ItemListViewClass

class HolyGrailHelper:
    def _InitData(self):
        self.ItemList = ItemListClass.ItemList()

    def _InitVisual(self, root):
        self.root = root
        self.root.focus_force()

        root.geometry('750x750')
        self.root.resizable()

        self.root.title("Holy Grail Helper")

        icon = PhotoImage(file='Icons\\holygrailicon.png')
        self.root.iconphoto(True, icon)

        self.root.config(bg="#232b25")

        self.MainFrame = Frame(self.root)

    def _InitModules(self):
        self.ScreenCapture = ScreenCaptureClass.ScreenCapture(self.root, self)
        self.ItemListView = ItemListViewClass.ItemListView(self)

    def _InitFrames(self):
        self.CharacterListFrame = Frame(self.root)
        self.CurrentViewFrame = Frame(self.root)

    def ClearCharacterListFrame(self):
        self.CharacterListFrame.destroy()
        self.CharacterListFrame = Frame(self.root)
        self.CharacterListFrame.grid(row=0, column=0)

    def MainMenu(self):
        self.characterList = CharacterListClass.CharacterList(self, self.root, self.ItemList)

        self.CharacterListFrame.grid(row=0, column=0)
        self.CurrentViewFrame.grid(row=0, column=1)
        
        self.characterList.ShowCharacterButtons()
        self.ItemListView.ShowAllItemList()
        
        Button(self.MainFrame, text='Create Character', width=30,  command=self.characterList.CreateCharacterWindow).pack()

        Button(self.MainFrame, text='(Q)uit', width=30, command=lambda: self.root.destroy()).pack()
        self.MainFrame.bind('q', lambda e: self.root.destroy())

    def Main(self):
        self.MainMenu()

        self.MainFrame.grid(row=2, columnspan=2)

        self.root.mainloop()

    def __init__(self):
        self._InitData()
        self._InitVisual(Tk())
        self._InitFrames()
        self._InitModules()

holyGrailHelper = HolyGrailHelper()

holyGrailHelper.Main()
