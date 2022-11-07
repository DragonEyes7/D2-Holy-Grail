from logging import root
import os
import Character as CharacterClass
import Inventory as InventoryClass
import Item as ItemClass

import Settings as SettingsClass
import StashTabList as StashTabListClass

class CharacterList:
    def GetCharacterList(self, settings, filterName=''):
        result = []
        for character in self.characters:
            if filterName != '' and filterName not in character.GetName():
                continue

            if settings.IsHardcore and not character.GetIsHardcore() \
                or not settings.IsHardcore and character.GetIsHardcore():
                continue

            if character.GetIsLadder() and not settings.GameType == 'Ladder' \
                or not character.GetIsLadder() and settings.GameType == 'Ladder':
                continue
            elif not character.GetIsLadder():
                if character.GetIsOnline() and not settings.GameType == 'Online':
                   continue

                if not character.GetIsOnline() and not settings.GameType == 'Offline':
                    continue
                
            result.append(character)

        result.sort(key=lambda x: x.GetName().lower())
        return result

    def InitStashTabs(self):
        self.StashTabs = []

        settings = SettingsClass.Settings('Online', False)
        self.StashTabs.append(StashTabListClass.StashTabList(self.GetCharacterList(settings, '_StashTab'), settings))

        settings = SettingsClass.Settings('Online', True)
        self.StashTabs.append(StashTabListClass.StashTabList(self.GetCharacterList(settings, '_StashTab'), settings))

        settings = SettingsClass.Settings('Offline', False)
        self.StashTabs.append(StashTabListClass.StashTabList(self.GetCharacterList(settings, '_StashTab'), settings))

        settings = SettingsClass.Settings('Offline', True)
        self.StashTabs.append(StashTabListClass.StashTabList(self.GetCharacterList(settings, '_StashTab'), settings))

        settings = SettingsClass.Settings('Ladder', False)
        self.StashTabs.append(StashTabListClass.StashTabList(self.GetCharacterList(settings, '_StashTab'), settings))

        settings = SettingsClass.Settings('Ladder', True)
        self.StashTabs.append(StashTabListClass.StashTabList(self.GetCharacterList(settings, '_StashTab'), settings))

    def MinStashTabs(self):
        return min(len(self.StashTabs[0].Tabs), len(self.StashTabs[1].Tabs), len(self.StashTabs[2].Tabs), len(self.StashTabs[3].Tabs), len(self.StashTabs[4].Tabs), len(self.StashTabs[5].Tabs))

    def UpdateStashTabs(self, number):
        for tab in self.StashTabs:
            for count in range(len(tab.Tabs), number):
                self.CreateCharacter(('_StashTab_' + str(count + 1)), tab.Settings.GameType, tab.Settings.IsHardcore)

    def CreateCharacter(self, characterName, gameType, isHardcore):
        onlinePath = os.path.join(gameType, ('Hardcore' if isHardcore else 'Softcore'))
        path = os.path.join("Characters", onlinePath)
        fullpath = os.path.join(path, characterName)
        List = None

        if not os.path.isdir(fullpath):
            os.makedirs(fullpath)
            character = self._CreateCharacter(path, characterName)
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

        self.InitStashTabs()

        if os.path.exists(rootPath):
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
                                            item = ItemClass.Item(itemFile.name, itemPath, itemData)
                                            character.GetInventory().AddItemToInventory(item)
        else:
            #Todo change Modes everwhere to be in a global config
            self._CreateCharacterFolder(rootPath, ['Ladder', 'Online', 'Offline'])
            self.UpdateStashTabs(3)
        
    def _CreateCharacterFolder(self, rootPath, GameTypes):
        os.makedirs(rootPath)

        for GameType in GameTypes:
            gamePath = os.path.join(rootPath, GameType)
            os.makedirs(gamePath)
            self._CreateCharacterSubFolders(gamePath)

    def _CreateCharacterSubFolders(self, path):
        path1 = os.path.join(path, 'Hardcore')
        os.makedirs(path1)
        path2 = os.path.join(path, 'Softcore')
        os.makedirs(path2)

    def _CreateCharacter(self, dirpath, dirName):
        characterInv = InventoryClass.Inventory()
        character = CharacterClass.Character(dirpath, dirName, characterInv) 
        return character
