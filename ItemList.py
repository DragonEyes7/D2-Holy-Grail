import DataFeeder as DataFeederClass

from difflib import SequenceMatcher

class ItemList:
    def FindBestMatch(self, list, itemName, itemType, bestMatchItem, bestMatchRatio):
        for item in list:
            currentRatio = SequenceMatcher(None, itemName.lower(), item.GetName().lower()).ratio()
            if  currentRatio > bestMatchRatio:
                bestMatchRatio = currentRatio
                bestMatchItem = item

        return bestMatchItem, bestMatchRatio

    def GetItemFromName(self, itemName, itemType):
        bestMatchItem = None
        bestMatchRatio = 0

        bestMatchItem, bestMatchRatio = self.FindBestMatch(self.UniqueList, itemName, itemType, bestMatchItem, bestMatchRatio)
        bestMatchItem, bestMatchRatio = self.FindBestMatch(self.SetList, itemName, itemType, bestMatchItem, bestMatchRatio)
        bestMatchItem, bestMatchRatio = self.FindBestMatch(self.RuneList, itemName, itemType, bestMatchItem, bestMatchRatio)

        return bestMatchItem

    def __init__(self):
        self.UniqueList = DataFeederClass.DataFeeder().FillItemList('Data\\CSV\\UniqueList.csv')
        self.SetList = DataFeederClass.DataFeeder().FillItemList('Data\\CSV\\SetList.csv')
        self.RuneList = DataFeederClass.DataFeeder().FillItemList('Data\\CSV\\RuneList.csv')