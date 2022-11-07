import os

class Item:
    def GetData(self):
        return self.itemData

    def GetPath(self):
        return self.path

    def SetPath(self, path):
        self.path = path

    def GetFullPath(self):
        return self.fullPath

    def SetFullPath(self, newFullPath):
        self.fullPath = newFullPath

    def Delete(self):
        os.remove('./' + self.GetFullPath())

    def Size(self):
        return 0

    def __init__(self, imageFile, imagePath, itemData):
        self.imageFile = imageFile
        self.path = imagePath
        self.fullPath = os.path.join(imagePath, imageFile)
        self.itemData = itemData