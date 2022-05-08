import os
import Character as CharacterClass
import Inventory as InventoryClass
import Item as ItemClass

class CharacterList:
    def GetCharacterList(self, settings):
        result = []
        for character in self.characters:
            if settings.GameType == 'Online' and not character.GetIsOnline() \
                or settings.GameType == 'Offline' and character.GetIsOnline():
                continue

            if settings.IsHardcore and not character.GetIsHardcore() \
                or not settings.IsHardcore and character.GetIsHardcore():
                continue

            if settings.GameType == 'Ladder' and not character.GetIsLadder():
                continue
            
            result.append(character)

        return result

    def CreateCharacter(self, characterName, gameType, isHardcore):
        onlinePath = os.path.join(gameType, ('Hardcore' if isHardcore else 'Softcore'))
        path = os.path.join("Characters", onlinePath)
        fullpath = os.path.join(path, characterName)
        List = None

        if not os.path.isdir(fullpath):
            os.mkdir(fullpath)
            character = self._CreateCharacter(fullpath, characterName)
            self.characters.append(character)
            self.characters.sort(key=lambda char: char.GetName().lower())
        else:
            return (List, "Character already Exist")

        if self.settingsRef.GameType == gameType and self.settingsRef.IsHardcore == isHardcore:
            #We are looking at this list of character refresh!
            List = self.GetCharacterList(self.settingsRef)

        return (List, "Character Created Successfully")

    def DeleteCharacter(self, character):
        #warning Character Inventory is not empty are you sure you want to delete?
        if len(character.GetInventory().GetList()) > 0:
            #open a warning popup
            return ("Character Inventory is not empty are you sure you want to delete?", None)

        fullpath = os.path.join(character.GetPath(), character.GetName())
        if os.path.isdir(fullpath):
            os.rmdir(fullpath)
            self.characters.remove(character)
            return ("Character Deleted Successfully", self.GetCharacterList(self.settingsRef))

        return ("Strange behaviour, please give peanuts to plants", None)

    def __init__(self, settingsRef, itemList):
        self.characters = []
        self.settingsRef = settingsRef
        
        rootPath = 'Characters'
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
                            itemPath = os.path.join(currentPath, Character.name)
                            with os.scandir(itemPath) as Items:
                                for itemFile in Items:
                                    #find item Data and fill it
                                    itemData = itemList.GetItemFromName(itemFile.name.split('.')[0], None)
                                    item = ItemClass.Item(itemFile, itemPath, itemData)
                                    character.GetInventory().AddItemToInventory(item)

    def _CreateCharacter(self, dirpath, dirName):
        characterInv = InventoryClass.Inventory()
        character = CharacterClass.Character(dirpath, dirName, characterInv) 
        return character
