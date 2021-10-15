class Inventory:
    def GetList(self):
        return self.inventory

    def AddItemToInventory(self, item):
        self.inventory.append(item)
        self.capacity = self.capacity - item.Size()

    def RemoveItemFromInventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.capacity = self.capacity + item.Size()

    def GetInventoryMaxCapacity(self):
        return 100 + 40

    def GetCurrentCapacity(self):
        return self.capacity

    def __init__(self):
        self.inventory = []
        self.capacity = 100 + 40