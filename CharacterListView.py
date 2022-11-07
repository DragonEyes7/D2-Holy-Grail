from tkinter import *
from ButtonBar import ButtonBar

import GlobalWindowSettings as GlobalWindowSettingsClass

class CharacterListView:
    def GetCurrentCharacter(self):
        return self.currentCharacter if hasattr(self, 'currentCharacter') else None

    def ShowCharacterWithCurrentItem(self, itemName):
        self.HGH.ClearItemViewFrame()

        found = False
        i = 0
        for character in self.HGH.CharacterListData.GetCharacterList(self.HGH.Settings):
            i += 1
            for item in character.GetInventory().GetList():
                if itemName == item.GetData().GetName():
                    Button(self.HGH.ItemViewFrame, text=character.GetName(), width=30,  command= lambda c=character: self._SelectCharacter(c)).grid(row=i, column=0)
                    Button(self.HGH.ItemViewFrame, text='Show Item', width=9, command= lambda c=character, i=itemName: self._ShowItem(c, i)).grid(row=i, column=1)
                    found = True

        if not found:
            Label(self.HGH.ItemViewFrame, text='No Character found with this item').grid()

    def CreateCharacterWindow(self):
        win = GlobalWindowSettingsClass.GlobalWindowSettings().InitNewWindow()

        Label(win, text="Character Name").grid(row=0)
        
        sv = StringVar()
        sv.trace_variable("w", lambda var, index, mode, sv=sv: self._CharacterNameEntryChanged(ErrorLabel, sv))

        characterNameInput = Entry(win, textvariable=sv)
        characterNameInput.grid(row=0, column=1)

        bar = ButtonBar(self, win, ['Online', 'Offline', 'Ladder'])
        bar.grid(row=1)
        bar.config(relief=GROOVE, bd=2)

        boolvar = BooleanVar()
        Checkbutton(win, text="Hardcore", width=30, variable=boolvar).grid(row=1, column=1)

        ErrorLabel = Label(win, text='')
        ErrorLabel.grid(row=2)

        Button(win, text='Create', width=30,  command=lambda: self._CreateCharacterFolder(characterNameInput.get(), ErrorLabel, bar.GetSelected(), boolvar.get())).grid(row=3, column=0, sticky=W, pady=4)
        win.bind('<Return>', lambda e: self._CreateCharacterFolder(characterNameInput.get(), ErrorLabel, bar.GetSelected(), boolvar.get()))

        Button(win, text='Close', width=30,  command= lambda: win.destroy()).grid(row=3, column=1, sticky=W, pady=4)

    def ClearList(self):
        if hasattr(self, 'Label'):
            self.Label.destroy()
        
        if hasattr(self, '_Unselected'):
            self._Unselected.destroy()
            self._Unselected = None

        for button in self.CharacterButtons:
            button[0].destroy()
            button[1].destroy()

        self.CharacterButtons = []

        self._UnselectCharacter()

    def ShowCharacterButtons(self, characterList, clear = False):
        if clear:
            self.ClearList()
        else:
            Label(self.TKContainer, text='Character List:').grid(row=0)
            Button(self.TKContainer, text='Create Character', width=30,  command=self.HGH.CharacterListView.CreateCharacterWindow).grid(row=1)
            self.CharacterButtons = []

        #Maybe change the delete by an icon
        #self.hGH.CharacterListFrame.deleteIcon = ImageTk.PhotoImage(file='Icons\\delete-folder.png')
        
        i = 2
        for character in characterList:
            color = 'white'
            if hasattr(self, 'currentCharacter') and character == self.currentCharacter:
                color = 'green'

            btn = Button(self.TKContainer, bg=color, text=character.GetName(), width=30,  command= lambda c=character: self._SelectCharacter(c))
            btn.grid(row=i, column=0);
            btn2 = Button(self.TKContainer, text='Delete', width=5, command= lambda c=character: self._DeleteCharacter(c))
            btn2.grid(row=i, column=1)
            self.CharacterButtons.append((btn, btn2))
            i += 1

        if not hasattr(self, '_Unselected') or self._Unselected == None:
           self._Unselected = Button(self.TKContainer, text='Unselect Character', width=30,  command= lambda: self._UnselectCharacter())
           self._Unselected.grid(row=i, column=0)
        
        if len(characterList) <= 0:
            self.Label = Label(self.TKContainer, text='No Character')
            self.Label.grid(row=1)

    def _ShowItem(self, character, itemName):
        item = character.GetInventory().GetItemFromName(itemName)
        if item:
            self.HGH.ItemViewer.ShowItem(item)
        
    def _CharacterNameEntryChanged(self, ErrorLabel, sv):
        ErrorLabel['text'] = ''

    def _CreateCharacterFolder(self, characterName, ErrorLabel, gameType, isHardcore):
        result = self.HGH.CharacterListData.CreateCharacter(characterName, gameType, isHardcore)
        ErrorLabel['text'] = result[1]

        if result[0] != None:
            self.ShowCharacterButtons(result[0],True)

    def _DeleteCharacter(self, character):
        result = self.HGH.CharacterListData.DeleteCharacter(character)
        self.HGH.ErrorMessage(result[0])
        if result[1] != None:
            self.ShowCharacterButtons(result[1], True)

    def _SelectCharacter(self, character):
        if not hasattr(self, 'currentCharacter'):
            #self.main.MainFrame = Frame(self.root)

            #Button(self.main.MainFrame, text='(A)dd Item', width=30,  command=lambda: self.main.ScreenCapture.AreaSelect()).pack()
            #self.root.bind('a', lambda e: self.main.ScreenCapture.AreaSelect())

            #self.main.MainFrame.pack()
            pass

        self.currentCharacter = character
        self.HGH.ItemListView.ShowItemListFromInventory(self.currentCharacter.GetInventory().GetList())
        self._UpdateSelectedCharacter()

    def _UnselectCharacter(self):
        self.currentCharacter = None
        self._UpdateSelectedCharacter()
        self.HGH.ItemListView.ShowAllItemList()
    
    def _UpdateSelectedCharacter(self):
        for btn in self.CharacterButtons:
            if self.currentCharacter is not None and btn[0]['text'] == self.currentCharacter.GetName():
                btn[0].configure(bg='green')
            else:
                btn[0].configure(bg='white')
    
    def __init__(self, hgh, root, tkContainer):
        self.root = root
        self.HGH = hgh
        self.TKContainer = tkContainer