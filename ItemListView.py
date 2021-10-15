from tkinter import *

class ItemListView:
    def ShowItemListFromInventory(self, list):
        Label(self.hGH.CurrentViewFrame, text='Item List:').grid(row=0)

        i = 0
        for item in list:
            i += 1
            
            Button(self.hGH.CurrentViewFrame, text=item.GetData().GetName(), width=30,  command= lambda i=item: self._SelectItem(i)).grid(row=i, column=0)
            Button(self.hGH.CurrentViewFrame, text='Delete', width=5, command= lambda i=item: self._DeleteItem(i)).grid(row=i, column=1)

    def ShowItemList(self, list):
        Label(self.ItemListOptions, text='Item List:').pack(side=TOP)

        i = 0
        for item in list:
            i += 1
            self.listBox.insert(i, item.GetName())
            #Button(self.hGH.CurrentViewFrame, text=item.GetName(), width=30,  command= lambda i=item: self._SelectItem(i))

        self.listBox.bind('<<ListboxSelect>>', self.changecolor)

    def RefreshItemList(self):
        pass

    def changecolor(self, event):
        # configure color to the window
        print(self.listBox.get(ANCHOR))

    def SearchBar(self):
        pass

    def __init__(self, hgh):
        self.hGH = hgh
        self.ItemListOptions = Frame(self.hGH.CurrentViewFrame)
        self.ItemListFrame = Frame(self.hGH.CurrentViewFrame)

        self.ItemListOptions.pack(side=TOP)
        self.ItemListFrame.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.listBox = Listbox(self.ItemListFrame)
        self.listBox.pack(side = LEFT, fill = BOTH)
        self.scrollbar = Scrollbar(self.ItemListFrame)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.listBox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listBox.yview)
        self.ItemListFrame.pack()