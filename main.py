from tkinter import *
from ButtonBar import ButtonBar

import Settings as SettingsClass

import CharacterList as CharacterListClass
import CharacterListView as CharacterListViewClass

import ScreenCapture as ScreenCaptureClass

import ItemList as ItemListClass
import ItemListView as ItemListViewClass

class HolyGrailHelper:
    def UpdateBarSelect(self, pickName):
        self.Settings.GameType = pickName
        
        self.CharacterListView.ShowCharacterButtons(self.CharacterListData.GetCharacterList(self.Settings), True)

    def UpdateBarSelectHarcore(self, boolvar):
        self.Settings.IsHardcore = boolvar.get()

        self.CharacterListView.ShowCharacterButtons(self.CharacterListData.GetCharacterList(self.Settings), True)
        
    def __init__(self):
        self._InitData()
        self._InitVisual(Tk())
        self._InitFrames()
        self._InitModules()

    def _InitData(self):
        self.ItemList = ItemListClass.ItemList()
        self.Settings = SettingsClass.Settings('Online', False)
        self.CharacterListData = CharacterListClass.CharacterList(self.Settings, self.ItemList)

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
        self.TopFrame = Frame(self.root)
        self.BottomFrame = Frame(self.root)

    def _InitFrames(self):
        self.CharacterListFrame = Frame(self.MainFrame)
        self.CurrentViewFrame = Frame(self.MainFrame)

    def _InitModules(self):
        self.ScreenCapture = ScreenCaptureClass.ScreenCapture(self, self.root)
        self.ItemListView = ItemListViewClass.ItemListView(self, self.ItemList)
        self.CharacterListView = CharacterListViewClass.CharacterListView(self, self.MainFrame, self.CharacterListFrame)

    def _TopMenu(self):
        bar = ButtonBar(self, self.TopFrame, ['Online', 'Offline', 'Ladder'])
        bar.pack(side=LEFT)
        bar.config(relief=GROOVE, bd=2)

        boolvar = BooleanVar()
        Checkbutton(self.TopFrame, text="Hardcore", width=10, variable=boolvar, command=lambda b=boolvar: self.UpdateBarSelectHarcore(b)).pack(side=LEFT)

        Button(self.TopFrame, text='(Q)uit', width=10, command=lambda: self.root.destroy()).pack(side=RIGHT)
        self.TopFrame.bind('q', lambda e: self.root.destroy())

    def _MainMenu(self):
        self._LoadCharacters()
        self._LoadItems()
        
    def _LoadCharacters(self):
        self.CharacterListView.ShowCharacterButtons(self.CharacterListData.GetCharacterList(self.Settings))

        self.CharacterListFrame.pack(side=LEFT, fill='y')


    def _LoadItems(self):
        #Button(self.MainFrame, text='(A)dd Item', width=30,  command=lambda: self.ScreenCapture.AreaSelect()).pack()
        self.CurrentViewFrame.pack(side=RIGHT, fill='y') #grid(row=1, column=1)
        
        self.ItemListView.ShowAllItemList()

    def Main(self):
        self._TopMenu()
        self._MainMenu()

        self.TopFrame.pack(side=TOP, fill='x') #.grid(row=0, column=0, columnspan=2, sticky=N)
        self.MainFrame.pack(fill='both') #grid(row=2, columnspan=2)

        self.root.mainloop()

holyGrailHelper = HolyGrailHelper()

holyGrailHelper.Main()
