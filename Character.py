import os

class Character:
    def GetPath(self):
        return os.join('Characters', self.imageFile)

    def GetName(self):
        return self.name
    
    def GetInventory(self):
        return self.inventory

    def __init__(self, characterName, inventory):
        self.name = characterName
        self.inventory = inventory