import ItemView as ItemViewClass

from tkinter import *

class ItemListView:
    def SearchBar(self):
        Label(self.hGH.CurrentViewFrame, text='Search: ').grid(row=0, column=0)
        search = Entry(self.hGH.CurrentViewFrame, text='Search: ').grid(row=0, column=0)


    def ShowItemListFromInventory(self, list):
        self.ClearItemList()

        i = 0
        for item in list:
            i += 1
            self.listBox.insert(i, item.GetData().GetName())
        
        self.listBox.bind('<<ListboxSelect>>', lambda _: self.OnItemSelectedFromInventory(list))

    def ShowItemList(self, list, filter=''):
        self.ClearItemList()
        i = 0
        for item in list:
            if filter.lower() in item.GetName().lower():
                i += 1
                self.listBox.insert(i, item.GetName())

        self.listBox.bind('<<ListboxSelect>>', self.OnItemSelected)

    def RefreshItemList(self):
        pass

    def ClearItemList(self):
        self.listBox.delete(0, END)

    def OnItemSelected(self, event):
        itemName = self.listBox.get(ANCHOR)
        #show item
        #itemView = ItemViewClass.ItemView()
        #itemView.ShowItemWindow(event[0])

    def OnItemSelectedFromInventory(self, event):
        itemName = self.listBox.get(ANCHOR)
        #show item
        itemView = ItemViewClass.ItemView()
        itemView.ShowItemWindow(event[0])
        #Open window with character owning this item
        #Add this item
            #Select a character
            #take a screenshot
            #save

    def Search(self, var):
        self.ShowItemList(self.hGH.ItemList.UniqueList, var.get())

    def __init__(self, hgh):
        self.hGH = hgh
        self.ItemListOptions = Frame(self.hGH.CurrentViewFrame)
        self.ItemListFrame = Frame(self.hGH.CurrentViewFrame)

        sv = StringVar()
        sv.trace_variable("w", lambda var, index, mode, sv=sv: self.Search(sv))

        self.ItemListOptions.pack(side=TOP)
        Label(self.ItemListOptions, text='Search:').grid(row=0, column=0)
        Entry(self.ItemListOptions, textvariable=sv).grid(row=0, column=1)
        Label(self.ItemListOptions, text='Item List:').grid(row=1, column=0)

        self.ItemListFrame.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.listBox = Listbox(self.ItemListFrame)
        self.listBox.pack(side = LEFT, fill = BOTH)
        self.scrollbar = Scrollbar(self.ItemListFrame)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.listBox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listBox.yview)
        self.ItemListFrame.pack()