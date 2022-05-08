from tkinter import *

class ButtonBar(Frame):
    def GetSelected(self):
        return self._Selected

    def __init__(self, script, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)

        self.UnselectedColor = 'White'
        self.SelectedColor = 'Green'

        self.buttons = []

        self._Selected = picks[0]

        for pick in picks:
            color = self.UnselectedColor
            if pick == picks[0]:
                color = self.SelectedColor
                
            btn = Button(self, bg=color, text=pick, command=lambda p=pick, s=script: self._Clicked(p, s))
            btn.pack(side=side, anchor=anchor, expand=YES)
            self.buttons.append(btn)

    def _Clicked(self, pickName, script):
        self._Selected = pickName

        for btn in self.buttons:
            if btn['text'] == pickName:
                btn.configure(bg=self.SelectedColor)
            else:
                btn.configure(bg=self.UnselectedColor)

        script.UpdateBarSelect(pickName)