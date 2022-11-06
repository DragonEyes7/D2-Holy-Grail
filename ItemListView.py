from numpy import character
from ButtonBar import ButtonBar

from tkinter import *

class ItemListView:
    def SearchBar(self):
        self.SearchValue = StringVar()
        self.SearchValue.trace_variable("w", lambda var, index, mode, sv=self.SearchValue: self.Search(self.hGH.ItemList.UniqueList, sv.get()))

        Label(self.ItemListOptions, text='Search:').grid(row=0, column=0)
        Entry(self.ItemListOptions, textvariable=self.SearchValue).grid(row=0, column=1)

    def Search(self, list, var):
        self.ShowItemList(list, var)

    def UpdateBarSelect(self, pickName):
        sv = StringVar()

        if self.SearchValue:
            sv = self.SearchValue

        iList = []
        if pickName == 'Unique':
            iList = self.hGH.ItemList.UniqueList
        elif pickName == 'Sets':
            iList = self.hGH.ItemList.SetList
        elif pickName == 'Runes':
            iList = self.hGH.ItemList.RuneList
        elif pickName == 'Rares':
            iList = []
        elif pickName == 'Crafted':
            iList = []
        else:
            self.ShowAllItemList(sv.get())
            return
        
        self.Search(iList, sv.get())

    def FilterBar(self):
        bar = ButtonBar(self, self.ItemListOptions, ['All', 'Uniques', 'Sets', 'Runes', 'Rares', 'Crafted'])
        bar.grid(row=1, columnspan=6)

    def ShowItemListFromInventory(self, list):
        self.ClearItemList()

        i = 0
        for item in list:
            i += 1
            self.listBox.insert(i, item.GetData().GetName())
        
        self.listBox.bind('<<ListboxSelect>>', lambda _: self.OnItemSelectedFromInventory(list))

    def ShowAllItemList(self, var=''):
        self.ClearItemList()

        self.fullList.sort(key=lambda i: i.GetName())

        self.ShowItemList(self.fullList, var)

    def ShowItemList(self, list, filter=''):
        self.ClearItemList()
        
        i = 0
        for item in list:
            name = item.GetName() if hasattr(item,'GetName') else item.GetData().GetName()
            if filter.lower() in name.lower():
                i += 1
                self.listBox.insert(i, name)

        self.listBox.bind('<<ListboxSelect>>', self.OnItemSelected)

    def ClearItemList(self):
        self.listBox.delete(0, END)

    def OnItemSelected(self, event):
        itemName = self.listBox.get(ANCHOR)
        self.hGH.CharacterListView.ShowCharacterWithCurrentItem(itemName)

    def OnItemSelectedFromInventory(self, event):
        itemName = self.listBox.get(ANCHOR)
        if len(event) > 0:
            for e in event:
                if e.GetData().GetName() == itemName:
                    self.hGH.ItemViewer.ShowItem(e)
                    return

    def __init__(self, hgh, itemList):
        self.fullList = itemList.UniqueList + itemList.SetList + itemList.RuneList

        self.hGH = hgh
        self.ItemListOptions = Frame(self.hGH.ItemListViewFrame)
        self.ItemListFrame = Frame(self.hGH.ItemListViewFrame)

        self.SearchBar()
        self.FilterBar()
        self.ItemListOptions.pack(side=TOP, fill = BOTH)

        Button(self.ItemListOptions, text='(A)dd Item', width=30, command=lambda: self.hGH.ScreenCapture.AreaSelect()).grid(row=2, columnspan=6)
        self.ItemListOptions.bind('a', lambda e: self.main.ScreenCapture.AreaSelect())

        Label(self.ItemListOptions, text='Item List:').grid(row=3, column=0, columnspan=6)

        self.listBox = Listbox(self.ItemListFrame)
        self.listBox.pack(side = LEFT, fill = BOTH)
        self.scrollbar = Scrollbar(self.ItemListFrame)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.listBox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listBox.yview)
        self.ItemListFrame.pack(side=LEFT, fill=BOTH, expand=True)