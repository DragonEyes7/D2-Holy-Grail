import ItemView as ItemViewClass

from tkinter import *

class ItemListView:
    def SearchBar(self):
        self.SearchValue = StringVar()
        self.SearchValue.trace_variable("w", lambda var, index, mode, sv=self.SearchValue: self.Search(self.hGH.ItemList.UniqueList, sv.get()))
        Label(self.ItemListOptions, text='Search:').grid(row=0, column=0)
        Entry(self.ItemListOptions, textvariable=self.SearchValue).grid(row=0, column=1)

    def Search(self, list, var):
        self.ShowItemList(list, var)

    def FilterBar(self):
        sv = StringVar()

        if self.SearchValue:
            sv = self.SearchValue

        Button(self.ItemListOptions, text='All', width=10,  command= lambda: self.ShowAllItemList(sv.get())).grid(row=1, column=0)
        Button(self.ItemListOptions, text='Uniques', width=10,  command= lambda: self.Search(self.hGH.ItemList.UniqueList, sv.get())).grid(row=1, column=1)
        Button(self.ItemListOptions, text='Sets', width=10,  command= lambda: self.Search(self.hGH.ItemList.SetList, sv.get())).grid(row=1, column=2)
        Button(self.ItemListOptions, text='Runes', width=10,  command= lambda: self.Search(self.hGH.ItemList.RuneList, sv.get())).grid(row=1, column=3)
        #Button(self.ItemListOptions, text='Runewords', width=10,  command= lambda: self.Search(self.hGH.ItemList.UniqueList, sv.get())).grid(row=1, column=4)
        #Look on Characters and find the rares to fill a list
        Button(self.ItemListOptions, text='Rares', width=10,  command= lambda: self.Search(self.hGH.ItemList.UniqueList, sv.get())).grid(row=1, column=5)
        #Look on Characters and find the crafted to fill a list
        Button(self.ItemListOptions, text='Crafted', width=10,  command= lambda: self.Search(self.hGH.ItemList.UniqueList, sv.get())).grid(row=1, column=6)

    def ShowItemListFromInventory(self, list):
        self.ClearItemList()

        i = 0
        for item in list:
            i += 1
            self.listBox.insert(i, item.GetData().GetName())
        
        self.listBox.bind('<<ListboxSelect>>', lambda _: self.OnItemSelectedFromInventory(list))

    def ShowAllItemList(self, var=''):
        self.ClearItemList()

        fullList = self.hGH.ItemList.UniqueList + self.hGH.ItemList.SetList + self.hGH.ItemList.RuneList

        fullList.sort(key=lambda i: i.GetName())

        self.ShowItemList(fullList, var)

    def ShowItemList(self, list, filter=''):
        self.ClearItemList()
        
        i = 0
        for item in list:
            if filter.lower() in item.GetName().lower():
                i += 1
                self.listBox.insert(i, item.GetName())

        self.listBox.bind('<<ListboxSelect>>', self.OnItemSelected)

    def ClearItemList(self):
        self.listBox.delete(0, END)

    def OnItemSelected(self, event):
        itemName = self.listBox.get(ANCHOR)
        self.hGH.CharacterList.ShowCharacterWindowWithCurrentItem(itemName)

    def OnItemSelectedFromInventory(self, event):
        itemView = ItemViewClass.ItemView()
        itemView.ShowItemWindow(event[0])

    def __init__(self, hgh):
        self.hGH = hgh
        self.ItemListOptions = Frame(self.hGH.CurrentViewFrame)
        self.ItemListFrame = Frame(self.hGH.CurrentViewFrame)

        self.SearchBar()
        self.FilterBar()
        self.ItemListOptions.pack(side=TOP)
        Label(self.ItemListOptions, text='Item List:').grid(row=2, column=0)

        self.ItemListFrame.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.listBox = Listbox(self.ItemListFrame)
        self.listBox.pack(side = LEFT, fill = BOTH)
        self.scrollbar = Scrollbar(self.ItemListFrame)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.listBox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listBox.yview)
        self.ItemListFrame.pack()