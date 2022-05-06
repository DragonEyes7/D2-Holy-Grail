import os
import Character as CharacterClass
import Inventory as InventoryClass
import Item as ItemClass

class CharacterList:
    def __init__(self, itemList):
        self.characters = []
        
        rootPath = 'Characters\\'
        gamePath = ''
        currentPath = ''

        with os.scandir(rootPath) as GameTypes:
            for GameType in GameTypes:
                gamePath = os.path.join(rootPath, GameType.name)
                with os.scandir(gamePath) as Hardcores:
                    for Hardcore in Hardcores:
                        currentPath = os.path.join(gamePath, Hardcore.name)
                    with os.scandir(currentPath) as Characters:
                        for Character in Characters:
                            character = self._CreateCharacter(currentPath, Character.name)
                            self.characters.append(character)
                            itemPath = os.path.join(currentPath + Character.name)
                            with os.scandir(itemPath) as Items:
                                for itemFile in Items:
                                    #find item Data and fill it
                                    itemData = itemList.GetItemFromName(itemFile.split('.')[0], None)
                                    item = ItemClass.Item(itemFile, itemPath, itemData)
                                    character.GetInventory().AddItemToInventory(item)

    def _CreateCharacter(self, dirpath, dirName):
        characterInv = InventoryClass.Inventory()
        character = CharacterClass.Character(dirpath, dirName, characterInv) 
        return character
