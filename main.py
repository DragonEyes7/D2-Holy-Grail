import cv2
import pytesseract
import numpy as nm
import PIL.Image
import os
import CharacterList as CharacterListClass

from PIL import ImageGrab, Image, ImageTk, ImageEnhance
from tkinter import *
from os import walk

class HolyGrailHelper:
    def ShowImage(self, image):
        win = self.InitNewWindow()

        win.image = ImageTk.PhotoImage(image)

        top = Frame(win)
        bottom = Frame(win)
        top.pack(side=TOP)
        bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

        Label(win, image=win.image).pack(in_=top)

        imgpil = ImageTk.getimage(win.image)
        rgbImg = imgpil.convert('RGB')
        
        itemName = self.ReadImageToString(rgbImg).splitlines()[0]
        itemNameInputValue = StringVar(win, value=itemName)

        typeName = self.ReadImageToString(rgbImg).splitlines()[1]
        itemTypeInputValue = StringVar(win, value=typeName)
        
        nameFrame = Frame(win)

        Label(nameFrame, text='Item Name').grid(row=0)
        itemNameInput = Entry(nameFrame, textvariable=itemNameInputValue)
        itemNameInput.grid(row=0, column=1)

        Label(nameFrame, text='Item Type').grid(row=1)
        itemTypeInput = Entry(nameFrame, textvariable=itemTypeInputValue)
        itemTypeInput.grid(row=1, column=1)

        nameFrame.pack()
        
        Button(win, text='(S)ave', width=30, command=lambda: self.SaveImage(win, rgbImg, itemNameInput.get())).pack(in_=bottom, side=LEFT)
        #Don't save when typing in the entry
        #win.bind('s', lambda e: self.SaveImage(win, rgbImg, itemNameInput.get()))

        Button(win, text='(C)lose', width=30, command= lambda: win.destroy()).pack(in_=bottom, side=LEFT)
        #Don't close when typing in the entry
        #win.bind('c', lambda e: win.destroy())

        win.grab_set()
        win.wait_window(win)

    def ReadImageToString(self, image):
        pytesseract.pytesseract.tesseract_cmd = r'I:\\Apps\\Tesseract-OCR\\tesseract.exe'

        return pytesseract.image_to_string(cv2.cvtColor(nm.array(image), cv2.COLOR_BGR2GRAY), lang ='eng')

    def SaveImage(self, win, rgbImg, itemName):
        fileName = itemName + ".jpg"
        rgbImg.save(os.path.join(self.characters.currentCharacter.GetPath(), fileName), "JPEG")
        rgbImg.close()

        win.destroy()

    def AreaSelect(self):
        x1 = y1 = x2 = y2 = 0
        roi_image = None

        def on_mouse_down(event):
            nonlocal x1, y1
            x1, y1 = event.x, event.y
            canvas.create_rectangle(x1, y1, x1, y1, outline='red', tag='roi')

        def on_mouse_move(event):
            nonlocal roi_image, x2, y2
            x2, y2 = event.x, event.y
            canvas.delete('roi-image') # remove old overlay image
            roi_image = image.crop((x1, y1, x2, y2)) # get the image of selected region
            canvas.image = ImageTk.PhotoImage(roi_image)
            canvas.create_image(x1, y1, image=canvas.image, tag=('roi-image'), anchor='nw')
            canvas.coords('roi', x1, y1, x2, y2)
            # make sure the select rectangle is on top of the overlay image
            canvas.lift('roi') 

        self.root.withdraw()  # hide the root window
        image = ImageGrab.grab()  # grab the fullscreen as select region background
        bgimage = ImageEnhance.Brightness(image).enhance(0.3)  # darken the capture image
        # create a fullscreen window to perform the select region action
        win = Toplevel()
        win.attributes('-fullscreen', 1)
        win.attributes('-topmost', 1)
        canvas = Canvas(win, highlightthickness=0)
        canvas.pack(fill='both', expand=1)
        tkimage = ImageTk.PhotoImage(bgimage)
        canvas.create_image(0, 0, image=tkimage, anchor='nw', tag='images')
        # bind the mouse events for selecting region
        win.bind('<ButtonPress-1>', on_mouse_down)
        win.bind('<B1-Motion>', on_mouse_move)
        win.bind('<ButtonRelease-1>', lambda e: win.destroy())
        # use Esc key to abort the capture
        win.bind('<Escape>', lambda e: win.destroy())
        # make the capture window modal
        win.focus_force()
        win.grab_set()
        win.wait_window(win)
        self.root.deiconify()  # restore root window
        # show the capture image
        if roi_image:
            self.ShowImage(roi_image)

    def Init(self, root):
        self.root = root
        self.root.focus_force()

        root.geometry('420x420')
        self.root.resizable()

        self.root.title("Holy Grail Helper")

        icon = PhotoImage(file='Icons\\holygrailicon.png')
        self.root.iconphoto(True, icon)

        self.root.config(bg="#232b25")

        self.MainFrame = Frame(root) 

    def InitNewWindow(self):
        win = Toplevel()
        win.config(bg="#232b25")
        win.focus_force()
        return win

    def MainMenu(self):
        self.characterList = CharacterListClass.CharacterList(self, self.root)

        self.CharacterListFrame = Frame(self.root)
        self.CurrentViewFrame = Frame(self.root)

        self.CharacterListFrame.grid(row=0, column=0)
        self.CurrentViewFrame.grid(row=0, column=1)
        
        self.characterList.ShowCharacterButtons()
        
        Button(self.MainFrame, text='Create Character', width=30,  command=self.characterList.CreateCharacterWindow).pack()

        Button(self.MainFrame, text='(Q)uit', width=30, command=lambda: self.root.destroy()).pack()
        self.MainFrame.bind('q', lambda e: self.root.destroy())

    def Main(self):
        self.Init(Tk())

        self.MainMenu()

        self.MainFrame.grid(row=2, columnspan=2)

        self.root.mainloop()

    def __init__(self):
        pass

holyGrailHelper = HolyGrailHelper()

holyGrailHelper.Main()