### WARS CLI v001, 12-29-23
###
### Goals:
### - create Factions
###     - handle Goal
###     - handle Tag
###     - handle Asset (maybe Flag system?)
### - create Assets
###     - handle Ownership
###     - handle Attack
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
        # stat-data interations
        ## health
        self.AssetMaxHealth = self.AssetData["MaxHealth"]
        self.AssetCurrentHealth = self.AssetMaxHealth
        ## purchase requirements
        self.AssetStatType = self.AssetData["AssetType"]
        self.AssetStatRequirement = self.AssetData["AssetLevel"]
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
        self.CurrentHealth = MaximumHealth      # The faction's current Health as an int()
        self.MaximumHealth = MaximumHealth      # The faction's maximum Health as an int()
        self.OwnedAssets = []
        pass

    # Data Interactions...
    ### Stats setters
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

    ### Complex Object setters
    def setGoal(self, GoalID):
        self.FacGoal = FacGoalObject(self.FacID, GoalID)
        return 
    
    def setTag(self, TagID):
        self.FacTag = FacTagObject(self.FacID, TagID)
        return 
    
    # Asset Interactions...
    ### CreateAsset will .append() an AssetObject into the FactionObject's OwnedObjects list().
    def CreateAsset(self, AssetID):
        self.AssetToCreate = FacAsset(self, AssetID)
        self.OwnedAssets.append(self.AssetToCreate)
        pass
