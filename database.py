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
equippedWeapon = None
addedFX = None

# define function to remove a save slot
def deleteSave(n, rm):
    try:
        client.drop_database(n)
    except:
        print("Database doesn't exist")
        return
    dbList = list(client.list_database_names())
    if n in dbList:
        raise Exception("MongoDB Error: '{0}' didn't get dropped.".format(n))
    if rm == True:
        path = "{0}/{1}".format(savesPath, n)
        if os.path.exists(path):
            rmtree(path)

# set a new location
def setLocation(n):
    global locationInfo
    global ROOM
    global SECTOR
    global PLANET
    player.update_one( { "SECTION": "location" }, { "$set": { "NAME": n } } )
    if n.endswith("Sector"):
        locationInfo = locations.find_one( { "$and": { { "NAME": "space" }, { "SECTOR": SECTOR } } } )
    elif n.lower() == "winnibego":
        locations.update_one( { "NAME": "Winnibego" }, { "$set": { "SECTOR": SECTOR } } )
        locationInfo = locations.find_one( { "NAME": n } )
    else:
        locationInfo = locations.find_one( { "NAME": n } )
    ROOM = locationInfo["NAME"]
    SECTOR = locationInfo["SECTOR"]
    PLANET = locationInfo["PLANET"]

# set a new space location
def setSpaceLocation(sector):
    global locationInfo
    global ROOM
    global SECTOR
    global PLANET
    player.update_one( { "SECTION": "location" }, { "$set": { "NAME": "Space" } } )
    locationInfo = locations.find_one( { "NAME": "Space" } )
    locations.update_one( { "NAME": "Winnibego" }, { "$set": { "SECTOR": sector } } )
    locations.update_one( { "NAME": "Space" }, { "$set": { "SECTOR": sector } } )
    ROOM = locationInfo["NAME"]
    SECTOR = locationInfo["SECTOR"]
    PLANET = locationInfo["PLANET"]

def getLocation():
    global locationInfo
    global ROOM
    global SECTOR
    global PLANET
    locationInfo = locations.find_one( { "NAME": ROOM } )
    ROOM = locationInfo["NAME"]
    SECTOR = locationInfo["SECTOR"]
    PLANET = locationInfo["PLANET"]

def loadLocation(n):
    global locationInfo
    global ROOM
    global SECTOR
    global PLANET
    locationInfo = locations.find_one( { "NAME": n } )
    ROOM = locationInfo["NAME"]
    SECTOR = locationInfo["SECTOR"]
    PLANET = locationInfo["PLANET"]

# equip a new weapon
def setWeapon(n):
    global equippedWeapon
    global weaponInfo
    if equippedWeapon is None:
        equippedWeapon = "Fists"
    if equippedWeapon != "Fists":
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "EQUIPPED": equippedWeapon } } )
        player.update_one( { "SECTION": "inventory" }, { "$push": { "ITEMS": equippedWeapon } } )
    player.update_one( { "SECTION": "equipped" }, { "$set": { "WEAPON": n } } )
    if n != "Fists":
        player.update_one( { "SECTION": "inventory" }, { "$push": { "EQUIPPED": n } } )
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "ITEMS": n } } )
    equippedWeapon = player.find_one( { "SECTION": "equipped" } )["WEAPON"]
    weaponInfo = items.find_one( {"NAME": equippedWeapon } )

# equip a new FX pedal
def setFX(n):
    global addedFX
    global fxInfo
    if addedFX is None:
        addedFX = "noFX"
    if addedFX != "noFX":
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "EQUIPPED": addedFX } } )
        player.update_one( { "SECTION": "inventory" }, { "$push": { "ITEMS": addedFX } } )
    player.update_one( { "SECTION": "equipped" }, { "$set": { "FX": n } } )
    if n != "noFX":
        player.update_one( { "SECTION": "inventory" }, { "$push": { "EQUIPPED": n } } )
        player.update_one( { "SECTION": "inventory" }, { "$pull": { "ITEMS": n } } )
    addedFX = player.find_one( { "SECTION": "equipped" } )["FX"]
    fxInfo = items.find_one( {"NAME": addedFX } )

def getInventory():
    global playerInv
    playerInv = player.find_one( { "SECTION": "inventory" } )

def getStats():
    global playerStats
    global levelStats
    playerStats = player.find_one( { "SECTION": "stats" } )
    levelStats = levels.find_one( { "LEVEL": playerStats["LVL"] } )

def updateGround(item, action):
    if action == "del":
        # remove item from ground
        groundList = list(locations.find_one( { "NAME": ROOM } )["GROUND"])
        if item in groundList:
            groundList.remove(item)
            locations.update_one( { "NAME": ROOM }, { "$set": { "GROUND": groundList } } )
    elif action == "add":
        # add item to the ground
        groundTemp = list(locationInfo["GROUND"])
        groundTemp.append(item)
        locations.update_one( { "NAME": ROOM }, { "$set": { "GROUND": groundTemp } } )
        groundList = list(locations.find_one( { "NAME": ROOM } )["GROUND"])
        if item not in groundList:
            raise Exception("'{0}' doesn't exist on the ground.".format(item))
            return
    else:
        raise Exception("FUNCTION CALL BUG: Someone forgot to specify an action for updateGround()")
    setLocation(ROOM)

def updateInv(item, action):
    global playerInv
    getInventory()
    if action == "del":
        # remove item
        i = list(playerInv["ITEMS"])
        k = list(playerInv["KEY_ITEMS"])
        e = list(playerInv["EQUIPPED"])
        if item in i:
            i.remove(item)
            player.update_one( { "SECTION": "inventory" }, { "$set": { "ITEMS": i } } )
        elif item in k:
            k.remove(item)
            player.update_one( { "SECTION": "inventory" }, { "$set": { "KEY_ITEMS": k } } )
        elif item in e:
            e.remove(item)
            player.update_one( { "SECTION": "inventory" }, { "$set": { "EQUIPPED": e } } )
        else:
            raise NameError("Cannot find item in any list.")
        getInventory()
    elif action == "add":
        # add item
        if items.find_one( { "NAME": item } )["TYPE"] == "key":
            player.update_one( { "SECTION": "inventory" }, { "$push": { "KEY_ITEMS": item } } )
            getInventory()
            if item not in list(playerInv["KEY_ITEMS"]):
                raise Exception("'{0}' is not in Ted's inventory.".format(item))
        else:
            player.update_one( { "SECTION": "inventory" }, { "$push": { "ITEMS": item } } )
            getInventory()
            if item not in list(playerInv["ITEMS"]):
                raise Exception("'{0}' is not in Ted's inventory.".format(item))
    else:
        raise Exception("FUNCTION CALL BUG: Someone forgot to specify an action for updateInv()")

def updateStat(stat, num, action):
    global playerStats
    getStats()
    temp = int(playerStats[stat])
    if action == "inc":
        # increase the stat
        temp += int(num)
        player.update_one( { "SECTION": "stats" }, { "$set": { stat : temp } } )
    elif action == "dec":
        # decrease the stat
        temp -= int(num)
        player.update_one( { "SECTION": "stats" }, { "$set": { stat : temp } } )
    elif action == "set":
        player.update_one( { "SECTION": "stats" }, { "$set": { stat : num } } )
    else:
        raise Exception("FUNCTION CALL BUG: Someone forgot to specify an action for updateStat()")
    getStats()

# function specifically for money transactions
def floydsTransaction(num, action):
    global playerStats
    getStats()
    floyds = int(playerStats["FLOYDS"])
    if action == "inc":
        floyds += num
    elif action == "dec":
        if floyds >= num:
            floyds -= num
        elif floyds < num:
            return False
    elif action == "set":
        floyds = num
    player.update_one( { "SECTION": "stats" }, { "$set": { "FLOYDS": floyds } } )
    getStats()
    return True

# function to set paths and collections
def define(n):
    # Define collection variables
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
    try:
        for n in collections:
            col = db[n]
            # save to a new state file set
            newFile = "{0}/{1}.json".format(playerPath, n)
            if os.path.exists(newFile):
                os.remove(newFile)
            else:
                pass
            cursor = col.find({})
            with open(newFile, 'w') as f:
                json.dump(json.loads(dumps(cursor)), f)
                f.close()
            # convert json dump so it can be inserted to mongo later
            content_new = ""
            with open(newFile, 'r') as f:
                content = f.read()
                content_new = re.sub('(\{"\$oid": )("[A-Za-z0-9]{24}")(\})', r'\2', content, flags = re.M)
                f.close()
            with open(newFile, 'w') as f:
                f.close()
            with open(newFile, 'w') as f:
                f.write(content_new)
                f.close()
        message = [ "Game data was saved!", "GREEN" ]
    except:
        message = [ "Something went wrong when trying to save.", "RED" ]
    return message

# load game state from database
def loadGame(name):
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
    # iterate through collections to insert documents
    for n in collections:
        col = db[n]
        # load the json
        initFile = "{0}/{1}.json".format(playerPath, n)
        with open(initFile) as f:
            file_data = json.load(f)
            f.close()
        # use _many or _one based on docs in the json
        if isinstance(file_data, list):
            col.insert_many(file_data)
        else:
            col.insert_one(file_data)
    getInventory()
    equipment = player.find_one( { "SECTION": "equipped" } )
    setWeapon(equipment["WEAPON"])
    setFX(equipment["FX"])
    locationName = player.find_one( { "SECTION": "location" } )["NAME"]
    loadLocation(locationName)

# create new database and set initial values
def newGame(name):
    global equipment
    # remove old save data
    deleteSave(name, True)
    # setup new save data
    define(name)
    # get and store the collection list
    collections = []
    for o in os.listdir("./json"):
        f = o.replace(".json", "")
        collections.append(f)
    # iterate through collections to insert and dump a new save
    for n in collections:
        if n.startswith("locations_"):
            col = db['locations']
            newName = "locations"
        else:
            col = db[n]
            newName = n
        # load the json
        initFile = "./json/{0}.json".format(n)
        with open(initFile) as f:
            file_data = json.load(f)
            f.close()
        # use _many or _one based on docs in the json
        if isinstance(file_data, list):
            col.insert_many(file_data)
        else:
            col.insert_one(file_data)
        # save to a new state file set
        newFile = "{0}/{1}.json".format(playerPath, newName)
        if os.path.exists(newFile):
            os.remove(newFile)
        else:
            pass
        cursor = col.find({})
        with open(newFile, 'w') as f:
            json.dump(json.loads(dumps(cursor)), f)
            f.close()
        # convert json dump so it can be inserted to mongo later
        content_new = ""
        with open(newFile, 'r') as f:
            content = f.read()
            content_new = re.sub('(\{"\$oid": )("[A-Za-z0-9]{24}")(\})', r'\2', content, flags = re.M)
            f.close()
        with open(newFile, 'w') as f:
            f.close()
        with open(newFile, 'w') as f:
            f.write(content_new)
            f.close()
    getInventory()
    equipment = player.find_one( { "SECTION": "equipped" } )
    setWeapon(equipment["WEAPON"])
    setFX(equipment["FX"])
    locationName = player.find_one( { "SECTION": "location" } )["NAME"]
    loadLocation(locationName)
