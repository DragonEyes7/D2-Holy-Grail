import DataFeeder as DataFeederClass

from difflib import SequenceMatcher

class ItemList:
    def CurrentItemInView(self):
        #print(self.UniqueList)
        pass

    def Search(self, string):
        itemList = []

        for item in self.UniqueList:
            if string in item.GetName():
                itemList.append(item)

        return itemList

    def GetItemFromName(self, itemName, itemType):
        bestMatchItem = None
        bestMatchRatio = 0

        for item in self.UniqueList:
            currentRatio = SequenceMatcher(None, itemName.lower(), item.GetName().lower()).ratio()
            if  currentRatio > bestMatchRatio:
                bestMatchRatio = currentRatio
                bestMatchItem = item

        return bestMatchItem

    def __init__(self):
        self.UniqueList = DataFeederClass.DataFeeder().FillItemList('Data\\CSV\\UniqueList.csv')