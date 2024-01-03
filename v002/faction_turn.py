### WARS CLI v001, 01-03-24
###
### Goals:
### - create Factions
###     - handle Goal
###     - handle Tag
###     - handle Asset (maybe Flag system?)
### - create Assets
###     - handle Ownership
###     - handle Attack
###         - handle SpecialAttackEffects
###     - handle Location
###     - handle ActivatedAbility

import json
import math

# EXAMINATION: FileInterpreter
# FileInterpreter is built to handle - ideally - both the reading and writing of a JSON file.
# Initializaion will take a FileName in both str() and list() and copy it's contents into FileContents
# FileInterpreter.append() takes any input and append()s it to the FileContents.
# FileInterpreter.save() will overwrite the current written contents of the file with the current contents of FileContents

class FileInterpreter:
    # Initialize object variables...
    def __init__(self, FileName):
        self.FileName = FileName
        self.FileContents = []
        try:
            ## Read FileName into FileContents as json data
            ## Correctly interpret FileName as both str() and list()
            if type(FileName) is list:
                for item in FileName:
                    opened_FileName = open(item, "r")
                    self.FileContents.append(json.load(opened_FileName))
                    opened_FileName.close()
            if type(FileName) is str:
                opened_FileName = open(self.FileName, "r")
                self.FileContents.append(json.load(opened_FileName))
                opened_FileName.close()
        except FileNotFoundError:
            print("File not found; execution failed. Please retry.")
    
    def append(self, input):
        self.FileContents.append(input)

    def lookup(self, input):
        return self.FileContents[input]

    def save(self):
        try:
            opened_FileName = open(self.FileName, "w")
            opened_FileName.write(json.dump(self.FileContents))     # json.dump() passes a str() for proper writing
            opened_FileName.close()
        except FileNotFoundError:
            print("File not found; execution failed. Please retry.")

# EXAMINATION: Logger
# Logger is built to create a file that is human-readable for debugging and "process examination".
# See FileInterpreter...
# Logger.log() is a preset str() that marks it's readable contents with a numerical value.
class Logger(FileInterpreter):
    def __init__(self, FileName):
        try:
            super().__init__(FileName)
        except FileNotFoundError:
            print("File not found; execution failed. Please retry.")

    def log(self, LogMessage, LogLevel=10):
        self.append(f"{LogLevel}: {LogMessage}\n")

# EXAMINATION: MenuHandler()
# MenuHandler is built to build an array of options and keys, and options to manipulate and examine them

class MenuHandler():
    def __init__(self, optionList):
        self.menuContents = {}
        self.iterableSymbol = "a"
        self.interationCounter = self.iterableSymbol
        for item in optionList:
            self.menuContents.append(f"{self.iterableSymbol}:{item}")
            self.interationCounter += 1
        pass

    def examineContents(self):
        return self.menuContents
    
    def lookup(self, symbolToLookup):
        return self.menuContents[str(symbolToLookup)]

# EXAMINTION: FacGoalObject
# Initializaion will take two str()s; an OwnerFac for reference and a GoalID to FileInterpreter.lookup().
# FacGoalObject.setID() will take a new ID, reset the current GoalProgress, and set the new GoalMaxProgress.
# FacGoalObject.increment() will increase GoalProgress and compare it to the GoalMaxProgress, requesting a new GoalID if the two are equal.
#   - should be greater than or equal to
class FacGoalObject:
    # Initialize object variables...
    def __init__(self, OwnerFac, GoalID):
        self.GoalData = FileInterpreter("goals.json")
        self.OwnerFac = OwnerFac
        self.GoalID = GoalID
        self.GoalPreset = self.GoalData.lookup(GoalID)
        self.GoalProgress = 0
        self.GoalMaxProgress = self.GoalPreset["MaxProgress"]

    def setID(self, newID):
        self.GoalID = newID
        self.GoalPreset = self.GoalData.lookup(newID)
        self.GoalProgress = 0
        self.GoalMaxProgress = self.GoalPreset["MaxProgress"]

    def increment(self):
        self.GoalProgress += 1
        if self.GoalProgress == self.GoalMaxProgress:
            self.setID(input("Please enter a new GoalID."))
            pass # send experience to owner
                 # exception for "Expand Influence" to gain 1 or 2 xp

# EXAMINTION: FacTagObject
# Initializaion will take two str()s; an OwnerFac for reference and a TagID to FileInterpreter.lookup().
class FacTagObject:
    # Initialize object variables...
    def __init__(self, OwnerFac, TagID):
        self.TagData = FileInterpreter("tags.json")
        self.OwnerFac = OwnerFac
        self.TagID = TagID
        self.TagEffect = self.TagData.lookup(TagID)
        pass

# EXAMINATION: FacAsset
# Initialization 
class FacAsset:
    # Initialize object variables...
    def __init__(self, OwnerFac, AssetID):
        # metadata interactions
        self.OwnerFac = OwnerFac
        self.AssetID = AssetID
        self.AssetData = FileInterpreter("assets.json")
        self.AssetData = self.AssetData.lookup(self.AssetID)
        self.DisplayName = self.AssetData["AssetName"]
        # stat-data interations
        ## health
        self.AssetMaxHealth = self.AssetData["MaxHealth"]
        self.AssetCurrentHealth = self.AssetMaxHealth
        ## purchase requirements
        self.AssetStatType = self.AssetData["AssetType"]
        self.AssetStatLevel = self.AssetData["AssetLevel"]
        self.AssetCost = self.AssetData["TreasureCost"]
        ## attack & counterattack
        self.AssetAttackAs = self.AssetData["AttackAs"]
        self.AssetAttackVs = self.AssetData["AttackVs"]
        self.AssetMinimumAttack = self.AssetData["MinAttack"]
        self.AssetMaximumAttack = self.AssetData["MaxAttack"]
        self.AssetMinimumCounter = self.AssetData["MinCounter"]
        self.AssetMaximumCounter = self.AssetData["MaxCounter"]
        pass

    # Data Interactions...
    ## Metadata setters

    def setOwnerFac(self, newOwner):
        self.OwnerFac = newOwner
        pass

    def setAssetID(self, newAsset):         # likely will not be used and will *most likely cause major issues* if implemented improporly
        self.AssetID = newAsset
        pass

    ## Stat-data setters

    def setMaxHP(self, n):
        self.AssetMaxHealth = n
        pass

    def setCurHP(self, n):
        self.AssetCurrentHealth = n
        pass

    ## Data tellers
    def tellCost(self):
        return self.AssetCost
    
    def tellType(self):
        return self.AssetStatType
    
    def tellLevel(self):
        return self.AssetStatLevel

    # Intra Asset Handling

# EXAMINTION: FactionObject
# Initializaion will take many simple int()s as it's numerical stats.
# FactionObject.setGoal will take a str() and create this FactionObject's FacGoalObject.
# FactionObject.setTag will take a str() and create this FactionObject's FacTagObject.
class FactionObject:
    # Initialize object variables...
    def __init__(self, FacID, ForceStat, CunningStat, WealthStat, CurrentExperience, CurrentTreasure, MaximumHealth):
        self.FacID = FacID              # The faction's identifier / name as a str()
        self.ForceStat = ForceStat      # The faction's Force stat as an int()
        self.CunningStat = CunningStat  # The faction's Cunning stat as an int()
        self.WealthStat = WealthStat    # The faction's Wealth stat as an int()
        self.CurrentExperience = CurrentExperience  # The faction's current Experience (to be spent to gain Stats) as an int()
        self.CurrentTreasure = CurrentTreasure      # The faction's current Treasure (to be spent to gain / manipulate Assets) as an int()
        self.CurrentHealth = MaximumHealth          # The faction's current Health as an int()
        self.MaximumHealth = MaximumHealth          # The faction's maximum Health as an int()
        self.OwnedAssets = []                       # The faction's Owned Assets in a list()
        self.TookTurnAction = False                 # The faction's action Flag as a bool()

        # File loading
        self.AssetsFile = FileInterpreter("assets.json")
        self.GoalsFile = FileInterpreter("goals.json")
        self.TagsFile = FileInterpreter("tags.json")

        pass

    # Data Interactions...
    ## Stats setters
    def setForceStat(self, n):
        self.ForceStat = n
        return
    
    def setCunningStat(self, n):
        self.CunningStat = n
        return

    def setWealthStat(self, n):
        self.WealthStat = n
        return

    def setExperience(self, n):
        self.CurrentExperience = n
        return
    
    def setTreasure(self, n):
        self.CurrentTreasure = n
        return
    
    def setCurrentHealth(self, n):
        self.CurrentHealth = n
        return
    
    def setMaximumHealth(self, n):
        self.MaximumHealth = n
        return

    ## Complex Object setters
    def setGoal(self, GoalID):
        self.FacGoal = FacGoalObject(self.FacID, GoalID)
        return 
    
    def setTag(self, TagID):
        self.FacTag = FacTagObject(self.FacID, TagID)
        return 
    
    ## Data tellers
    def tellCurrentTreasure(self):
        return self.CurrentTreasure
    
    def tellCurrentHealth(self):
        return self.CurrentHealth
    
    def tellMaximumHealth(self):
        return self.MaximumHealth
    
    def lookupStat(self, StatToLookup):
        if StatToLookup == "Force":
            return self.ForceStat
        if StatToLookup == "Cunning":
            return self.CunningStat
        if StatToLookup == "Wealth":
            return self.WealthStat
        else:
            return 0

    # Asset Interactions...
    ## Generic Interactions, used in other functions
    ### lookupOwnedAssetsOfType() takes a type str(), and examines each asset owned by the Faction, returns list of assets of that type
    def lookupOwnedAssetsOfType(self, TypeToLookup):
        AssetsOfType = []
        for item in self.OwnedAssets:
            if item["AssetType"] == TypeToLookup:
                AssetsOfType.append(item)
        return AssetsOfType

    ### findOwnedAssetPositionInList() takes a str() that is a copy taken from OwnedAssets list(), which is what we're searching so hopefully no funny business
    def findOwnedAssetPositionInList(self, CopyOfAssetToFind):
        positionInList = 0
        for item in self.OwnedAssets:
            if item == CopyOfAssetToFind:
                self.OwnedAssets.pop(positionInList)
                pass
            positionInList += 1
            pass


    ## *Create Asset*
    ### findLegalPurchases() returns a list of Assets the Faction could currently buy based on their stats.
    def findLegalPurchases(self):
        ListOfLegalAssets = []      # list to return
        statsLegal = False          # flag as bool
        treasureLegal = False       # flag as bool

        for item in self.AssetsFile:            # for all assets in file:
            ItemAssetType = item["AssetType"]               # check asset type
            ItemAssetLevel = item["AssetLevel"]             # check asset cost
            FacTypeStat = self.lookupStat(ItemAssetType)    # check faction stat
            if FacTypeStat >= ItemAssetLevel:               # compare ^
                statsLegal = True
            ItemTreasureCost = item["TreasureCost"]         
            if ItemTreasureCost <= self.tellCurrentTreasure():  # check faction treasure
                treasureLegal = True                            # compare ^
            if statsLegal and treasureLegal:                    # if both compare good:
                ListOfLegalAssets.append(item)                  # add to list
            else:
                pass

        return ListOfLegalAssets                # send back good assets
    
    ### presentLegalPurchases() prints a good list of options, then calls executePurchase()
    def presentLegalPurchases(self, ListOfLegalAssets):
        purchaseMenu = MenuHandler(ListOfLegalAssets)       # create a MenuHandler object with the legal assets
        selectedOption = input(purchaseMenu.examineContents())  # get input
        return purchaseMenu.lookup(selectedOption)          # handle input and send back selected asset  
        
    ### executePurchase() handles subtracting treasure and creating and adding AssetObjects
    def executePurchase(self, OptionToPurchase):
        AssetToPurchase = self.AssetsFile.lookup(str(OptionToPurchase))     # gather asset data structure
        PurchasedAsset = FacAsset(self, AssetToPurchase["AssetID"])         # create a FacAsset owned by this FacObject
        self.OwnedAssets.append(PurchasedAsset)                         # append the new asset to the FacObject.OwnedAssets list
        pass

    ## *Sell Assets*
    def executeSale(self, AssetToSell):
        realAssetPosition = self.findOwnedAssetPositionInList(AssetToSell)
        self.OwnedAssets.pop(realAssetPosition)
        pass

    ### MakeSellMenu() creates both the first sell menu (where a user chooses an Asset Type or the Finish option), and the second sell menu (where the Assets are selected and sold)
    def MakeSellMenu(self):
        FLAG_StillSelling = True                            # flag for while looping
        firstHalfMenu = MenuHandler(["Force", "Cunning", "Wealth", "Done"]) # menu for type selection
        while FLAG_StillSelling:                            # while loop to handle multiple asset sales
            print(firstHalfMenu.examineContents())          # display to user
            FHSelection = input()                           # input from user
            if FHSelection == "d":                          # notice user wants to escape while loop & end sales
                FLAG_StillSelling = False                   # set escape flag to true
                self.TookTurnAction = True                  # set TookTurnAction flag to True as "Selling Assets" is a main action
                pass                                        # try to leave the while loop
            else:                                           #
                FHSelection = firstHalfMenu.lookup(FHSelection) # manage user input as key to dict() to find desired Type
                secondHalfContents = self.lookupOwnedAssetsOfType(FHSelection)  # find Assets of that Type
                secondHalfNames = []                            # create empty name list
                for item in secondHalfContents:                 # 
                    secondHalfNames.append(item["AssetName"])   # append display names of Assets in Type
                secondHalfMenu = MenuHandler(secondHalfNames)   # menu that list
                print(secondHalfMenu.examineContents())         # present the menu to the user
                SHSelection = input()                           # gather user input
                if SHSelection == "z":                          # notice user wants to escape Asset selection and return to Type selection
                    pass                                        # return to while
                else:                                           #
                    selectedAsset = secondHalfMenu.lookup(SHSelection)  # turn input character into Asset selected in menu
                    self.executeSale(selectedAsset)                     # execute sale of asset - note we are passing a copy, but this will be handled appropriately
                    pass                                                # return to while            
        pass    ## finished selling, get out of here
        