from tkinter import *
from turtle import left
from ButtonBar import ButtonBar

import Settings as SettingsClass

import CharacterList as CharacterListClass
import CharacterListView as CharacterListViewClass

import ScreenCapture as ScreenCaptureClass

import ItemList as ItemListClass
import ItemListView as ItemListViewClass
import ItemViewer as ItemViewerClass

class HolyGrailHelper:
    def UpdateBarSelect(self, pickName):
        self.Settings.GameType = pickName
        
        self.CharacterListView.ShowCharacterButtons(self.CharacterListData.GetCharacterList(self.Settings), True)

    def UpdateBarSelectHarcore(self, boolvar):
        self.Settings.IsHardcore = boolvar.get()

        self.CharacterListView.ShowCharacterButtons(self.CharacterListData.GetCharacterList(self.Settings), True)

    def ErrorMessage(self, errorMessage):
        self.ClearItemViewFrame()
        Label(self.ItemViewFrame, text=errorMessage).pack()

    def ClearItemViewFrame(self):
        self.ItemViewFrame.destroy()
        self.ItemViewFrame = Frame(self.MainFrame)
        self.ItemViewFrame.pack(side=LEFT, fill='y')

    def Main(self):
        self._TopMenu()
        self._MainMenu()
        self._BottomMenu()

        self.TopFrame.pack(side=TOP, fill=X)
        self.MainFrame.pack(fill=BOTH, expand=True)
        self.BottomFrame.pack(side=BOTTOM, fill=X)

        self.root.mainloop()
        
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
        self.root.resizable()

        self.root.title("D2 Inventory Manager")

        icon = PhotoImage(file='Icons\\ChestIcon.png')
        self.root.iconphoto(True, icon)

        self.root.config(bg="#232b25")

        self.MainFrame = Frame(self.root)
        self.TopFrame = Frame(self.root)
        self.BottomFrame = Frame(self.root)
        self.ItemViewerWindow = None
        self.ItemViewer = ItemViewerClass.ItemViewer(self)

    def _InitFrames(self):
        self.CharacterListFrame = Frame(self.MainFrame)
        self.ItemListViewFrame = Frame(self.MainFrame)
        self.ItemViewFrame = Frame(self.MainFrame)

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

        value = self.CharacterListData.MinStashTabs()
        if value <= 0:
            value = 3

        nbStashTabs = StringVar(value=value)
        self.NbStashTabs = nbStashTabs.get()
        Label(self.TopFrame, text='NB of stash tabs:').pack(side=LEFT)
        vcmd = (self.TopFrame.register(self._Validate), '%i')
        Entry(self.TopFrame, width=5, textvariable=nbStashTabs, validatecommand = vcmd).pack(side=LEFT)
        nbStashTabs.trace_variable("w", lambda var, index, mode, sv=nbStashTabs: self._UpdateStashNumber(sv.get()))

        Button(self.TopFrame, text='(Q)uit', width=10, command=lambda: self.root.destroy()).pack(side=RIGHT)
        self.TopFrame.bind('q', lambda e: self.root.destroy())

    def _Validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                return int(value_if_allowed)
            except ValueError:
                return prior_value
        else:
            return prior_value

    def _UpdateStashNumber(self, number):
        number = self._Validate(None, None, number, self.NbStashTabs, None, None, None, None)
        if self.NbStashTabs == number:
            return
            
        if number > self.CharacterListData.MinStashTabs():
            self.CharacterListData.UpdateStashTabs(number)

    def _MainMenu(self):
        self._LoadCharacters()
        self._LoadItems()
        self._LoadItem()

    def _BottomMenu(self):
        Label(self.BottomFrame, text="Made by Frédéric Carrier").pack()
        
    def _LoadCharacters(self):
        self.CharacterListView.ShowCharacterButtons(self.CharacterListData.GetCharacterList(self.Settings))

        self.CharacterListFrame.pack(side=LEFT, fill='y')

    def _LoadItems(self):
        self.ItemListViewFrame.pack(side=LEFT, fill='y')
        
        self.ItemListView.ShowAllItemList()
    
    def _LoadItem(self):
        self.ItemViewFrame.pack(side=LEFT, fill='y')