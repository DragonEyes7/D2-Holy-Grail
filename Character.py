class Character:
    def GetGameType(self):
        return 'Ladder' if self.IsLadder else 'Online' if self.IsOnline else 'Offline'

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

        self.IsHardcore = 'Hardcore' in path

        self.IsOnline = 'Online' in path

        self.IsLadder = 'Ladder' in path

        self.name = characterName
        self.inventory = inventory