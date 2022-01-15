import pymongo, json, os, shutil, re, time
from bson.json_util import dumps
import engine as eng

# setup saves path
savesPath = "./save-states"
if not os.path.exists(savesPath):
    os.makedirs(savesPath)

# Setup database connection
client = pymongo.MongoClient("mongodb://root:kjZbFF5jMQL2sPS4vyRYgbW#CEt#2cDA@172.200.0.121:27017/")

# get and store the collection list
collections = []
for o in os.listdir("./json"):
    f = o.replace(".json", "")
    collections.append(f)

# define empty variables
equippedWeapon = None
addedFX = None

# TODO make CRIT value based on PLAYERLVL

# define function to remove a save slot
def deleteSave(n, rm):
    try:
        client.drop_database(n)
    except:
        print("Database doesn't exist")
        return
    dbList = list(client.list_database_names())
    if n in dbList:
        raise Exception("MongoDB Error: '" + n + "' didn't get dropped.")
        return
    if eng.DEBUG == 1:
        print("Dropped '" + n + "' database from MongoDB.")
        time.sleep(1)
    if rm == True:
        path = savesPath + "/" + n
        if os.path.exists(path):
            shutil.rmtree(path)
        if not os.path.exists(path) and eng.DEBUG == 1:
            print("Removed '" + path + "' from filesystem.")
            time.sleep(1)

# set a new location
def setLocation(n):
    global location
    global locationInfo
    player.update_one( { "SECTION": "location" }, { "$set": { "NAME": n } } )
    locationInfo = rooms.find_one( { "NAME": n } )
    location = locationInfo["NAME"]
    if eng.DEBUG == 1:
        print("New location name: " + location)
        print(locationInfo)
        time.sleep(1)

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
    if eng.DEBUG == 1:
        print("New weapon name: " + equippedWeapon)
        print(weaponInfo)
        time.sleep(1)

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
    if eng.DEBUG == 1:
        print("New FX name: " + addedFX)
        print(fxInfo)
        time.sleep(1)

def getPrefs():
    global playerPrefs
    playerPrefs = player.find_one( { "SECTION": "prefs" } )

def getInventory():
    global playerInv
    playerInv = player.find_one( { "SECTION": "inventory" } )

def getStats():
    global playerStats
    playerStats = player.find_one( { "SECTION": "stats" } )

def updateGround(item, action):
    if action == "del":
        # remove item from ground
        rooms.update_one( { "NAME": location }, { "$pull": { "GROUND": item } } )
        groundList = list(rooms.find_one( { "NAME": location } )["GROUND"])
        if item in groundList:
            raise Exception("'" + item + "' still exists on the ground.")
            return
        if eng.DEBUG == 1:
            print("Item to be removed: " + item)
            print("New GROUND list:")
            print(groundList)
    elif action == "add":
        # add item to the ground
        groundTemp = list(locationInfo["GROUND"])
        groundTemp.append(item)
        rooms.update_one( { "NAME": location }, { "$set": { "GROUND": groundTemp } } )
        groundList = list(rooms.find_one( { "NAME": location } )["GROUND"])
        if item not in groundList:
            raise Exception("'" + item + "' doesn't exist on the ground.")
            return
        if eng.DEBUG == 1:
            print("Item to be added: " + item)
            print("New GROUND list:")
            print(groundList)
    else:
        print("FUNCTION CALL BUG: Someone forgot to specify an action for updateGround()")
        time.sleep(3)
        return
    setLocation(location)

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
            return
        getInventory()
    elif action == "add":
        # add item
        if items.find_one( { "NAME": item } )["TYPE"] == "key":
            player.update_one( { "SECTION": "inventory" }, { "$push": { "KEY_ITEMS": item } } )
            getInventory()
            if item not in list(playerInv["KEY_ITEMS"]):
                raise Exception("'" + item + "' is not in Ted's inventory.")
                return
        else:
            player.update_one( { "SECTION": "inventory" }, { "$push": { "ITEMS": item } } )
            getInventory()
            if item not in list(playerInv["ITEMS"]):
                raise Exception("'" + item + "' is not in Ted's inventory.")
                return
    else:
        print("FUNCTION CALL BUG: Someone forgot to specify an action for updateInv()")
        time.sleep(3)
        return
    if eng.DEBUG == 1:
        print("New inventory list:")
        print("Items: " + str(playerInv["ITEMS"]))
        print("Key Items: " + str(playerInv["KEY_ITEMS"]))
        print("Equipped Items: " + str(playerInv["EQUIPPED"]))
        time.sleep(1)

def updateStat(stat, num, action):
    global playerStats
    getStats()
    if eng.DEBUG == 1:
        print("Updating stat '" + stat + "'")
    temp = int(playerStats[stat])
    if action == "inc":
        # increase the stat
        temp += int(num)
    elif action == "dec":
        # decrease the stat
        temp -= int(num)
    else:
        print("FUNCTION CALL BUG: Someone forgot to specify an action for updateStat()")
        time.sleep(3)
        return
    player.update_one( { "SECTION": "stats" }, { "$set": { stat : temp } } )
    getStats()
    if eng.DEBUG == 1:
        print("New value for " + stat + ": " + str(playerStats[stat]))

# function to set paths and collections
def define(n):
    # Define collection variables
    global db
    global abilities
    global challenge_ratings
    global enemies
    global items
    global rooms
    global player
    global playerPath
    global playerInv
    # setup new save directory
    playerPath = savesPath + "/" + n
    if eng.DEBUG == 1:
        print("Local saves path: " + playerPath)
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
    rooms = db['rooms']
    player = db['player']
    # set SLOT_NAME variable
    eng.SLOT_NAME = n
    if eng.DEBUG == 1:
        print("Defined all database paths for '" + n + "'")

# save current game state to the database
def saveGame():
    # iterate through collections to dump the current db state
    print("Saving game to file...")
    for n in collections:
        col = db[n]
        # save to a new state file set
        newFile = playerPath + "/" + n + ".json"
        if eng.DEBUG == 1:
            print("JSON file path: " + newFile)
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
            if eng.DEBUG == 1:
                print("Converted BSON to JSON")
        with open(newFile, 'w') as f:
            f.close()
            if eng.DEBUG == 1:
                print("Emptied file")
        with open(newFile, 'w') as f:
            f.write(content_new)
            f.close()
            if eng.DEBUG == 1:
                print("Saved new JSON to file")
                time.sleep(1)
    print("        ...done.")

# load game state from database
def loadGame(name):
    global equipment
    global playerInv
    # remove old save db if it exists
    client.drop_database(name)
    # setup new save data
    define(name)
    print("Loading game '" + name + "'...")
    # iterate through collections to insert documents
    for n in collections:
        col = db[n]
        # load the json
        initFile = playerPath + '/' + n + '.json'
        if eng.DEBUG == 1:
            print("Initialized JSON path: " + initFile)
        with open(initFile) as f:
            file_data = json.load(f)
            f.close()
        # use _many or _one based on docs in the json
        if isinstance(file_data, list):
            col.insert_many(file_data)
            if eng.DEBUG == 1:
                print("inserted saved document to " + n)
        else:
            col.insert_one(file_data)
            if eng.DEBUG == 1:
                print("inserted saved documents to " + n)
    if eng.DEBUG == 1:
        print("Setting up player environment...")
    getInventory()
    getPrefs()
    equipment = player.find_one( { "SECTION": "equipped" } )
    setWeapon(equipment["WEAPON"])
    setFX(equipment["FX"])
    locationName = player.find_one( { "SECTION": "location" } )["NAME"]
    setLocation(locationName)
    if eng.DEBUG == 1:
        print("Save game loaded: '" + name + "'")
        time.sleep(1)
    print("        ...done.")

# create new database and set initial values
def newGame(name):
    global equipment
    # remove old save data
    deleteSave(name, True)
    # setup new save data
    define(name)
    print("Creating new game '" + name + "'...")
    # iterate through collections to insert and dump a new save
    for n in collections:
        col = db[n]
        # load the json
        initFile = './json/' + n + '.json'
        if eng.DEBUG == 1:
            print("Old JSON path: " + initFile)
        with open(initFile) as f:
            file_data = json.load(f)
            f.close()
        # use _many or _one based on docs in the json
        if isinstance(file_data, list):
            col.insert_many(file_data)
            if eng.DEBUG == 1:
                print("Inserted init document to '" + n + "'")
        else:
            col.insert_one(file_data)
            if eng.DEBUG == 1:
                print("Inserted init documents to '" + n + "'")
        # save to a new state file set
        newFile = playerPath + "/" + n + ".json"
        if eng.DEBUG == 1:
            print("New JSON file path: " + newFile)
        if os.path.exists(newFile):
            if eng.DEBUG == 1:
                print("Removing old save game files...")
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
            if eng.DEBUG == 1:
                print("Converting BSON to JSON...")
            content = f.read()
            content_new = re.sub('(\{"\$oid": )("[A-Za-z0-9]{24}")(\})', r'\2', content, flags = re.M)
            f.close()
        with open(newFile, 'w') as f:
            if eng.DEBUG == 1:
                print("Emptying old file...")
            f.close()
        with open(newFile, 'w') as f:
            if eng.DEBUG == 1:
                print("Saving to new JSON to file...")
            f.write(content_new)
            f.close()
    if eng.DEBUG == 1:
        print("Setting up player environment...")
    getInventory()
    getPrefs()
    equipment = player.find_one( { "SECTION": "equipped" } )
    setWeapon(equipment["WEAPON"])
    setFX(equipment["FX"])
    locationName = player.find_one( { "SECTION": "location" } )["NAME"]
    setLocation(locationName)
    if eng.DEBUG == 1:
        print("New game created: '" + name + "'")
        time.sleep(1)
    print("        ...done.")
