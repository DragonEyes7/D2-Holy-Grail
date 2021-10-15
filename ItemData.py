class ItemData:
    def GetName(self):
        return self.name

    def GetType(self):
        return self.type

    def GetDescription(self):
        return self.description

    def Size(self):
        return 0

    def __init__(self, name, type, description):
        self.name = name
        self.type = type
        self.description = description