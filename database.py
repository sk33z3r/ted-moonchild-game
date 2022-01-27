import pymongo, os, json, re
from shutil import rmtree
from bson.json_util import dumps
import engine as eng

# setup saves path
savesPath = "./save-states"
if not os.path.exists(savesPath):
    os.makedirs(savesPath)

# Setup database connection
client = pymongo.MongoClient("mongodb://root:kjZbFF5jMQL2sPS4vyRYgbW#CEt#2cDA@172.200.0.121:27017/")

# define empty variables
equippedInstrument = None
equippedHead = None
addedFX = None

# define function to remove a save slot
def deleteSave(n, rm):

    # try to delete the db
    try:
        client.drop_database(n)

    # if the drop failed, return False
    except:
        return False

    # otherwise setup the dblist
    dbList = list(client.list_database_names())

    # check if the database is still there or not, and raise an exception if it is
    if n in dbList:
        raise Exception("MongoDB Error: '{0}' didn't get dropped.".format(n))

    # if the local folders should be removed, do it
    if rm == True:
        path = "{0}/{1}".format(savesPath, n)
        if os.path.exists(path):
            rmtree(path)

    # return true if all is successful
    return True

# function to set a new location
def setLocation(n):

    # define globals
    global locationInfo
    global ROOM
    global SECTOR
    global PLANET

    # set the new location in payer's db
    player.update_one( { "SECTION": "location" }, { "$set": { "NAME": n } } )

    # if the new location is a sector, set the space db only
    if n.endswith("Sector"):
        locationInfo = locations.find_one( { "$and": { { "NAME": "space" }, { "SECTOR": SECTOR } } } )

    # otherwise, if this is the winnibego, set the sector and load the winnie location
    elif n.lower() == "winnibego":
        locations.update_one( { "NAME": "Winnibego" }, { "$set": { "SECTOR": SECTOR } } )
        locationInfo = locations.find_one( { "NAME": n } )

    # otherwise just load the location
    else:
        locationInfo = locations.find_one( { "NAME": n } )

    # set easy to reference vars
    ROOM = locationInfo["NAME"]
    SECTOR = locationInfo["SECTOR"]
    PLANET = locationInfo["PLANET"]

# function to define a new location in Space
def setSpaceLocation(sector):

    # define globals
    global locationInfo
    global ROOM
    global SECTOR
    global PLANET

    # first set the player's new location
    player.update_one( { "SECTION": "location" }, { "$set": { "NAME": "Space" } } )
    locationInfo = locations.find_one( { "NAME": "Space" } )

    # set the current sector
    locations.update_one( { "NAME": "Winnibego" }, { "$set": { "SECTOR": sector } } )
    locations.update_one( { "NAME": "Space" }, { "$set": { "SECTOR": sector } } )

    # setup easy to reference vars from new info
    ROOM = locationInfo["NAME"]
    SECTOR = locationInfo["SECTOR"]
    PLANET = locationInfo["PLANET"]

# function to refresh the current location in memory
def getLocation():

    # define globals
    global locationInfo
    global ROOM
    global SECTOR
    global PLANET

    # define info var with current values
    locationInfo = locations.find_one( { "NAME": ROOM } )

    # setup easy to reference vars from the info
    ROOM = locationInfo["NAME"]
    SECTOR = locationInfo["SECTOR"]
    PLANET = locationInfo["PLANET"]

# function to load a new location into memory
def loadLocation(n):

    # define globals
    global locationInfo
    global ROOM
    global SECTOR
    global PLANET

    # get the location from player's db
    locationInfo = locations.find_one( { "NAME": n } )

    # setup easy to reference vars from the new info
    ROOM = locationInfo["NAME"]
    SECTOR = locationInfo["SECTOR"]
    PLANET = locationInfo["PLANET"]

# equip a new instrument
def setInstrument(n):

    # define globals
    global equippedInstrument
    global instrumentInfo

    # if the current value is empty, set it to Fists
    if equippedInstrument is None:
        equippedInstrument = "Fists"

    # if the current value isn't Fists, then remove the new item from equipped and add to reg inventory
    if equippedInstrument != "Fists":
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "EQUIPPED": equippedInstrument } } )
        player.update_one( { "SECTION": "inventory" }, { "$push": { "ITEMS": equippedInstrument } } )

    # setup new item as equipped
    player.update_one( { "SECTION": "equipped" }, { "$set": { "INSTRUMENT": n } } )

    # if the new value isn't Fists, then add the new item to equipped and remove from reg inventory
    if n != "Fists":
        player.update_one( { "SECTION": "inventory" }, { "$push": { "EQUIPPED": n } } )
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "ITEMS": n } } )

    # setup global vars with new info
    equippedInstrument = player.find_one( { "SECTION": "equipped" } )["INSTRUMENT"]
    instrumentInfo = items.find_one( {"NAME": equippedInstrument } )

# equip a new head piece
def setHead(n):

    # define globals
    global equippedHead
    global headInfo

    # if the current value is empty, set noFX
    if equippedHead is None:
        equippedHead = "Hair"

    # if the current value is not noFX, pull the old item from the player's equipped section and put it in reg inventory
    if equippedHead != "Hair":
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "EQUIPPED": equippedHead } } )
        player.update_one( { "SECTION": "inventory" }, { "$push": { "ITEMS": equippedHead } } )

    # add the new item to the player's equipped section
    player.update_one( { "SECTION": "equipped" }, { "$set": { "HEAD": n } } )

    # if the new item isn't noFX, then add it to the equipped section and remove from reg inventory
    if n != "Hair":
        player.update_one( { "SECTION": "inventory" }, { "$push": { "EQUIPPED": n } } )
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "ITEMS": n } } )

    # set global vars with new info
    equippedHead = player.find_one( { "SECTION": "equipped" } )["HEAD"]
    headInfo = items.find_one( {"NAME": equippedHead } )

# equip a new FX pedal
def setFX(n):

    # define globals
    global addedFX
    global fxInfo

    # if the current value is empty, set noFX
    if addedFX is None:
        addedFX = "noFX"

    # if the current value is not noFX, pull the old item from the player's equipped section and put it in reg inventory
    if addedFX != "noFX":
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "EQUIPPED": addedFX } } )
        player.update_one( { "SECTION": "inventory" }, { "$push": { "ITEMS": addedFX } } )

    # add the new item to the player's equipped section
    player.update_one( { "SECTION": "equipped" }, { "$set": { "FX": n } } )

    # if the new item isn't noFX, then add it to the equipped section and remove from reg inventory
    if n != "noFX":
        player.update_one( { "SECTION": "inventory" }, { "$push": { "EQUIPPED": n } } )
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "ITEMS": n } } )

    # set gobal vars with new info
    addedFX = player.find_one( { "SECTION": "equipped" } )["FX"]
    fxInfo = items.find_one( {"NAME": addedFX } )

# function to store current inventory in memory
def getInventory():

    global playerInv
    playerInv = player.find_one( { "SECTION": "inventory" } )

# function to store latest player info to memory
def getStats():

    # define globals
    global playerStats
    global levelStats

    # setup vars
    playerStats = player.find_one( { "SECTION": "stats" } )
    levelStats = levels.find_one( { "LEVEL": playerStats["LVL"] } )

# function to store the enemy's info into memory
def getEnemyInfo(name):

    # define globals
    global enemyStats
    global challengeRatingStats

    # setup vars
    enemyStats = enemies.find_one( { "NAME": name } )
    challengeRatingStats = challenge_ratings.find_one( { "RATING": enemyStats["CR"] } )

# function to get a dict from the player's stats
def getPlayerDict():

    # refresh player info
    getStats()
    getInventory()

    # setup the player dict
    calcs = {
        "ATK": {
            "BASE": 0,
            "BONUS": 0
        },
        "DEF": {
            "BASE": 0,
            "BONUS": 0
        },
        "MOJO": {
            "BASE": 0,
            "BONUS": 0
        },
        "LUK": {
            "BASE": 0,
            "BONUS": 0
        },
        "ACC": {
            "BASE": 0,
            "BONUS": 0
        }
    }

    # run through each stat
    for s in eng.STATS:

        # get the base value
        val = playerStats[s]

        # add all equipment bonuses together
        bonuses = instrumentInfo["BONUS"][s] + fxInfo["BONUS"][s] + headInfo["BONUS"][s]

        # add the values to the dict
        calcs[s]["BASE"] = val
        calcs[s]["BONUS"] = bonuses

    # return the dict object
    return calcs

# function to get a dict from the enemy's stats
def getEnemyDict():

    # run through each stat, setup dict for later
    calcs = { "ATK": 0, "DEF": 0, "MOJO": 0, "LUK": 0, "ACC": 0 }
    for s in eng.STATS:

        # if the stat has a bonus value in the enemy's document, add it
        if s in enemyStats:
            c = challengeRatingStats[s] + enemyStats[s]

        # otherwise just set the base CR stat
        else:
            c = challengeRatingStats[s]

        # add the calc to the list
        calcs[s] = c

    # return the dict object
    return calcs

# function to update ground items in a room
def updateGround(item, action):

    # if asked to delete, remove item from ground
    if action == "del":

        # set the groundList
        groundList = list(locations.find_one( { "NAME": ROOM } )["GROUND"])

        # if the item is in the ground list, remove it
        if item in groundList:
            groundList.remove(item)

            # set the update list as the new value
            locations.update_one( { "NAME": ROOM }, { "$set": { "GROUND": groundList } } )

    # if asked to add, add the item to the ground
    elif action == "add":

        # set a temp ground list and add the item
        groundTemp = list(locationInfo["GROUND"])
        groundTemp.append(item)

        # set the new value as the list
        locations.update_one( { "NAME": ROOM }, { "$set": { "GROUND": groundTemp } } )

        # set a new list from the database
        groundList = list(locations.find_one( { "NAME": ROOM } )["GROUND"])

        # if the item doesn't exist for some reason, raise an exception
        if item not in groundList:
            raise Exception("'{0}' doesn't exist on the ground.".format(item))
            return

    # otherwise let the player know I messed up somewhere when calling this function
    else:
        raise Exception("FUNCTION CALL BUG: Someone forgot to specify an action for updateGround()")

    # run a function to rewrite the room
    setLocation(ROOM)

# function to update the player's inventory
def updateInv(item, action):

    # define globals
    global playerInv

    # refresh inventory info
    getInventory()

    # if asked to delete
    if action == "del":

        # setup temp inventory lists
        i = list(playerInv["ITEMS"])
        k = list(playerInv["KEY_ITEMS"])
        e = list(playerInv["EQUIPPED"])

        # if the item is in the regular list
        if item in i:

            # remove the item
            i.remove(item)

            # update the db
            player.update_one( { "SECTION": "inventory" }, { "$set": { "ITEMS": i } } )

        # if the item is in the key item list
        elif item in k:

            # remove the item
            k.remove(item)

            # update the db
            player.update_one( { "SECTION": "inventory" }, { "$set": { "KEY_ITEMS": k } } )

        # if the item is in the equipped slot
        elif item in e:

            # remove the item
            e.remove(item)

            # update the db
            player.update_one( { "SECTION": "inventory" }, { "$set": { "EQUIPPED": e } } )

        # otherwise, let the player know I messed something up when calling this function
        else:
            raise NameError("Cannot find item in any list.")

        # refresh inventory info again
        getInventory()

    # if asked to add
    elif action == "add":

        # if the item is a key item
        if items.find_one( { "NAME": item } )["TYPE"] == "key":

            # add it to the key item list in player db
            player.update_one( { "SECTION": "inventory" }, { "$push": { "KEY_ITEMS": item } } )

            # refresh inventory info
            getInventory()

            # if for some reason the item doesn't appear in the key list in player db, raise an exception
            if item not in list(playerInv["KEY_ITEMS"]):
                raise Exception("'{0}' is not in Ted's inventory.".format(item))

        # otherwise just add the item to the regular inventory list
        else:
            player.update_one( { "SECTION": "inventory" }, { "$push": { "ITEMS": item } } )

            # refresh inventory info
            getInventory()

            # if for some reason the item doesn't appear in the key list in player db, raise an exception
            if item not in list(playerInv["ITEMS"]):
                raise Exception("'{0}' is not in Ted's inventory.".format(item))

    # otherwise let the player know I forgot to specify an action
    else:
        raise Exception("FUNCTION CALL BUG: Someone forgot to specify an action for updateInv()")

# function to update a player's stat
def updateStat(stat, num, action):

    # define globals
    global playerStats

    # refresh stat info
    getStats()

    # set a temp var of the current stat value
    temp = int(playerStats[stat])

    # if asked to increase
    if action == "inc":

        # increase the stat
        temp += int(num)

        # set the new value
        player.update_one( { "SECTION": "stats" }, { "$set": { stat : temp } } )

    # if asked to decrease
    elif action == "dec":

        # decrease the stat
        temp -= int(num)

        # set the new value
        player.update_one( { "SECTION": "stats" }, { "$set": { stat : temp } } )

    # if asked to set
    elif action == "set":

        # set the new value with no calculation
        player.update_one( { "SECTION": "stats" }, { "$set": { stat : num } } )

    # otherwise let the player know I forgot to define an action
    else:
        raise Exception("FUNCTION CALL BUG: Someone forgot to specify an action for updateStat()")

    # refresh stat info
    getStats()

# function specifically for money transactions
def floydsTransaction(num, action):

    # define globals
    global playerStats

    # refresh stat info
    getStats()

    # set the current amount of floyds
    floyds = int(playerStats["FLOYDS"])

    # if asked to increase, add the new value
    if action == "inc":
        floyds += num

    # if asked to decrease
    elif action == "dec":

        # and the player has enough floyds, decrease the stat
        if floyds >= num:
            floyds -= num

        # and the player doesn't have enough floyds, return False
        elif floyds < num:
            return False

    # if asked to set
    elif action == "set":

        # set the new value
        floyds = num

    # update the player db
    player.update_one( { "SECTION": "stats" }, { "$set": { "FLOYDS": floyds } } )

    # refresh stat info
    getStats()

    # return True if all is successful
    return True

# function to set paths and collections
def define(n):

    # define globals
    global db
    global abilities
    global challenge_ratings
    global enemies
    global items
    global locations
    global player
    global levels
    global playerPath
    global playerInv

    # setup new save directory
    playerPath = "{0}/{1}".format(savesPath, n)
    if not os.path.exists(playerPath):
        os.makedirs(playerPath)
    else:
        pass

    # define collections
    db = client[n]
    abilities = db['abilities']
    challenge_ratings = db['challenge_ratings']
    enemies = db['enemies']
    items = db['items']
    locations = db['locations']
    player = db['player']
    levels = db["levels"]

    # set SLOT_NAME variable
    eng.SLOT_NAME = n

# save current game state to the database
def saveGame():

    # iterate through collections to dump the current db state
    # get and store the collection list
    collections = []
    for o in os.listdir(playerPath):
        f = o.replace(".json", "")
        collections.append(f)

    # try to run the save function
    try:

        # for each collection found
        for n in collections:

            # set the collection up
            col = db[n]

            # define the new file, and remove if it already exists
            newFile = "{0}/{1}.json".format(playerPath, n)
            if os.path.exists(newFile):
                os.remove(newFile)
            else:
                pass

            # get all docs in the collection
            cursor = col.find({})

            # wait for the file operation to finish
            with open(newFile, 'w') as f:

                # dump all the docs to file
                json.dump(json.loads(dumps(cursor)), f)
                f.close()

            # reset the variable in case it was set already
            content_new = ""

            # wait for file to operation to finish
            with open(newFile, 'r') as f:

                # get the current contents
                content = f.read()

                # regex to replace the mongo $oid method in the dumped json to just their IDs so mongo will be able to import this later
                content_new = re.sub('(\{"\$oid": )("[A-Za-z0-9]{24}")(\})', r'\2', content, flags = re.M)
                f.close()

            # empty the current file
            with open(newFile, 'w') as f:
                f.close()

            # write the new edited text to the file
            with open(newFile, 'w') as f:
                f.write(content_new)
                f.close()

        # set a success message for the player
        message = [ "Game data was saved!", "GREEN" ]

    # if anything goes wrong, set a failure message for the player
    except:
        message = [ "Something went wrong when trying to save.", "RED" ]

    # return the message
    return message

# function to load game state from database
def loadGame(name):

    # define globals
    global equipment
    global playerInv

    # remove old save db if it exists
    client.drop_database(name)

    # setup new save data
    define(name)

    # get and store the collection list
    collections = []
    for o in os.listdir(playerPath):
        f = o.replace(".json", "")
        collections.append(f)

    # for each collection found
    for n in collections:

        # define the collection
        col = db[n]

        # set the file path
        initFile = "{0}/{1}.json".format(playerPath, n)

        # wait on file operations to finish
        with open(initFile) as f:

            # load the file
            file_data = json.load(f)
            f.close()

        # use _many or _one based on amount of docs in the json
        if isinstance(file_data, list):
            col.insert_many(file_data)
        else:
            col.insert_one(file_data)

    # load inv into memory
    getInventory()

    # load player's equipment to memory
    equipment = player.find_one( { "SECTION": "equipped" } )
    setInstrument(equipment["INSTRUMENT"])
    setFX(equipment["FX"])
    setHead(equipment["HEAD"])

    # load player's location to memory
    locationName = player.find_one( { "SECTION": "location" } )["NAME"]
    loadLocation(locationName)

# function to create new database and set initial values
def newGame(name):

    # define globals
    global equipment

    # remove old save data
    deleteSave(name, True)

    # setup new save data
    define(name)

    # get and store the new collection names
    collections = []
    for o in os.listdir("./json"):
        f = o.replace(".json", "")
        collections.append(f)

    # for each json file found
    for n in collections:

        # if the name is a location, we need to consolidate the docs into one collection called locations
        if n.startswith("locations_"):
            col = db['locations']
            newName = "locations"

        # otherwise use the filename as the collection name
        else:
            col = db[n]
            newName = n

        # set the init files' path
        initFile = "./json/{0}.json".format(n)

        # wait for file operations to complete
        with open(initFile) as f:

            # load the json file
            file_data = json.load(f)
            f.close()

        # use _many or _one based on number of docs in the json
        if isinstance(file_data, list):
            col.insert_many(file_data)
        else:
            col.insert_one(file_data)

        # define new player filepath
        newFile = "{0}/{1}.json".format(playerPath, newName)
        if os.path.exists(newFile):
            os.remove(newFile)
        else:
            pass

        # get a list of all the docs in the new collection
        cursor = col.find({})

        # wait for file operations to complete
        with open(newFile, 'w') as f:

            # dump the new collection into the player's file
            json.dump(json.loads(dumps(cursor)), f)
            f.close()

        # reset the variable in case it was already set
        content_new = ""

        # wait for file operations to complete
        with open(newFile, 'r') as f:

            # load the current content into memory
            content = f.read()
            # replace mongo's $oid method with just the _id so mongo can load this later
            content_new = re.sub('(\{"\$oid": )("[A-Za-z0-9]{24}")(\})', r'\2', content, flags = re.M)
            f.close()

        # empty the file
        with open(newFile, 'w') as f:
            f.close()

        # write the edited text to the file
        with open(newFile, 'w') as f:
            f.write(content_new)
            f.close()

    # set player's inventory
    getInventory()

    # set player's equipment
    equipment = player.find_one( { "SECTION": "equipped" } )
    setInstrument(equipment["INSTRUMENT"])
    setFX(equipment["FX"])
    setHead(equipment["HEAD"])

    # set player's location
    locationName = player.find_one( { "SECTION": "location" } )["NAME"]
    loadLocation(locationName)
