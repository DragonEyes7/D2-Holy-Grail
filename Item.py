import os

class Item:
    def GetName(self):
        return self.name

    def GetPath(self):
        return self.fileName

    def GetFullPath(self):
        return os.join(self.fileName, self.imageFile)

    def Delete(self):
        os.remove(self.GetFullPath())

    def Size(self):
        return 0

    def __init__(self, imageFile, imagePath):
        self.imageFile = imageFile
        self.name = imageFile.split('.')[0]
        self.fileName = imagePath