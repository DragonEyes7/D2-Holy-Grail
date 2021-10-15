import csv
from re import template
import ItemData as ItemDataClass

class DataFeeder:
    def FillItemList(self, csvPath):
        itemList = []

        with open(csvPath, newline='') as csvFile:
                    spamreader = csv.reader(csvFile, delimiter=',')

                    for item in spamreader:
                        type = item[0]
                        name = item[1]
                        description = None
                        itemList.append(ItemDataClass.ItemData(name, type, description))

        return itemList

    def __init__(self):
        pass
