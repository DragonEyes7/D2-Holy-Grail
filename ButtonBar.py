from tkinter import *

class ButtonBar(Frame):
    def __init__(self, main, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)

        self.buttons = []

        self.main = main

        for pick in picks:            
            color = 'white'
            btn = Button(self, bg=color, text=pick, command=lambda p=pick: self._Clicked(p))
            btn.pack(side=side, anchor=anchor, expand=YES)
            self.buttons.append(btn)

    def _Clicked(self, pickName):
        for btn in self.buttons:
            if btn['text'] == pickName:
                btn.configure(bg='green')
            else:
                btn.configure(bg='white')

        self.main.LoadCharacters(pickName)