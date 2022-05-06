class Character:
    def GetIsLadder(self):
        return self.IsLadder

    def GetIsOnline(self):
        return self.IsOnline

    def GetIsHardcore(self):
        return self.IsHardcore

    def GetPath(self):
        return self.path

    def GetName(self):
        return self.name
    
    def GetInventory(self):
        return self.inventory

    def __init__(self, path, characterName, inventory):
        self.path = path

        self.IsHardcore = False
        if 'Hardcore' in path:
            self.IsHardcore = True

        self.Online = False
        if 'Online' in path:
            self.Online = True

        self.Ladder = False
        if 'Ladder' in path:
            self.Ladder = True

        print("Character " + characterName + " Path: " + path)
        self.name = characterName
        self.inventory = inventory