import DataFeeder as DataFeederClass
from difflib import SequenceMatcher

class ItemList:
    def CurrentItemInView(self):
        #print(self.UniqueList)
        pass

    def Search(self, item):
        pass

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