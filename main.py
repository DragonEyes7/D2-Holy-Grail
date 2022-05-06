from tkinter import *
from ButtonBar import ButtonBar

import Settings as SettingsClass
import CharacterList as CharacterListClass
import ItemList as ItemListClass
import ScreenCapture as ScreenCaptureClass
import ItemListView as ItemListViewClass

class HolyGrailHelper:
    def _InitData(self):
        self.ItemList = ItemListClass.ItemList()
        self.Settings = SettingsClass.Settings('Online', False)

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
        bar = ButtonBar(self, self.TopFrame, ['Online', 'Offline', 'Ladder'])
        bar.pack(side=LEFT)
        bar.config(relief=GROOVE, bd=2)

        boolvar = BooleanVar()
        Checkbutton(self.TopFrame, text="Hardcore", width=30, variable=boolvar).pack(side=LEFT)
        self.Settings.IsHardcore = boolvar.get()

        Button(self.TopFrame, text='(Q)uit', width=30, command=lambda: self.root.destroy()).pack(side=RIGHT)
        self.TopFrame.bind('q', lambda e: self.root.destroy())
        
    def LoadCharacters(self, type):
        self.Settings.GameType = type
        self.Character()

    def Character(self):
        self.CharacterList = CharacterListClass.CharacterList(self.Settings, self.ItemList)

        self.CharacterListFrame.grid(row=1, column=0)
        self.CurrentViewFrame.grid(row=1, column=1)
        
        self.CharacterList.ShowCharacterButtons()
        self.ItemListView.ShowAllItemList()
        
        if not hasattr(self, '_createButton'):
            self._createButton = Button(self.MainFrame, text='Create Character', width=30,  command=self.CharacterList.CreateCharacterWindow).pack()

    def Main(self):
        self.MainMenu()

        self.TopFrame.grid(row=0, column=0, columnspan=2)
        self.MainFrame.grid(row=2, columnspan=2)

        self.root.mainloop()

    def __init__(self):
        self._InitData()
        self._InitVisual(Tk())
        self._InitFrames()
        self._InitModules()

holyGrailHelper = HolyGrailHelper()

holyGrailHelper.Main()
