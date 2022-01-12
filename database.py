import pymongo, json, os
from bson.json_util import dumps

# setup saves path
savesPath = "./save-states"
if not os.path.exists(savesPath):
    os.makedirs(savesPath)

# Setup database connection
client = pymongo.MongoClient("mongodb://root:example@172.100.0.121:27017/")

# get and store the collection list
collections = []
for o in os.listdir("./json"):
    f = o.replace(".json", "")
    collections.append(f)

# TODO make CRIT value based on PLAYERLVL

# set a new location
def setLocation(n):
    global location
    global locationInfo
    player.update_one( { "SECTION": "location" }, { "$set": { "NAME": n } } )
    locationInfo = rooms.find_one( { "NAME": n } )
    location = locationInfo["NAME"]

# equip a new weapon
def setWeapon(n):
    global equippedWeapon
    global weaponInfo
    player.update_one( { "SECTION": "equipped" }, { "$set": { "WEAPON": n } } )
    equippedWeapon = player.find_one( { "SECTION": "equipped" } )["WEAPON"]
    weaponInfo = items.find_one( {"NAME": equippedWeapon } )

# equip a new FX pedal
def setFX(n):
    global addedFX
    global fxInfo
    player.update_one( { "SECTION": "equipped" }, { "$set": { "FX": n } } )
    addedFX = player.find_one( { "SECTION": "equipped" } )["FX"]
    fxInfo = items.find_one( {"NAME": addedFX } )

# function to set paths and collections
def define(n):
    # Define collection variables
    global db
    global abilities
    global challenge_ratings
    global enemies
    global engine
    global items
    global rooms
    global player
    global playerPath
    # setup new save directory
    playerPath = savesPath + "/" + n
    if not os.path.exists(playerPath):
        os.makedirs(playerPath)
    else:
        pass
    # define collections
    db = client[n]
    abilities = db['abilities']
    challenge_ratings = db['challenge_ratings']
    enemies = db['enemies']
    engine = db['engine']
    items = db['items']
    rooms = db['rooms']
    player = db['player']

# save current game state to the database
def saveGame():
    # iterate through collections to dump the current db state
    for n in collections:
        col = db[n]
        # save to a new state file set
        newFile = playerPath + "/" + n + ".json"
        if os.path.exists(newFile):
            os.remove(newFile)
        else:
            pass
        cursor = col.find({})
        with open(newFile, 'w') as file:
            json.dump(json.loads(dumps(cursor)), file)

# load game state from database
def loadGame(name):
    global equipment
    define(name)
    # remove documents from all collections just in case they exists
    try:
        abilities.delete_many({})
        challenge_ratings.delete_many({})
        enemies.delete_many({})
        engine.delete_many({})
        items.delete_many({})
        rooms.delete_many({})
        player.delete_many({})
    except:
        print("No documents found.")
        pass
    # iterate through collections to insert documents
    for n in collections:
        col = db[n]
        # load the json
        initFile = playerPath + '/' + n + '.json'
        with open(initFile) as file:
            file_data = json.load(file)
        # use _many or _one based on docs in the json
        if isinstance(file_data, list):
            col.insert_many(file_data)
            print("inserted init document to " + n)
        else:
            col.insert_one(file_data)
            print("inserted init documents to " + n)
    equipment = player.find_one( { "SECTION": "equipped" } )
    setWeapon(equipment["WEAPON"])
    setFX(equipment["FX"])
    locationName = player.find_one( { "SECTION": "location" } )["NAME"]
    setLocation(locationName)

# create new database and set initial values
def newGame(name):
    global equipment
    define(name)
    # remove documents from all collections just in case they exists
    try:
        abilities.delete_many({})
        challenge_ratings.delete_many({})
        enemies.delete_many({})
        engine.delete_many({})
        items.delete_many({})
        rooms.delete_many({})
        player.delete_many({})
    except:
        print("No documents found.")
        pass
    # iterate through collections to insert and dump a new save
    for n in collections:
        col = db[n]
        # load the json
        initFile = './json/' + n + '.json'
        with open(initFile) as file:
            file_data = json.load(file)
        # use _many or _one based on docs in the json
        if isinstance(file_data, list):
            col.insert_many(file_data)
            print("inserted init document to " + n)
        else:
            col.insert_one(file_data)
            print("inserted init documents to " + n)
        # save to a new state file set
        newFile = playerPath + "/" + n + ".json"
        if os.path.exists(newFile):
            os.remove(newFile)
        else:
            pass
        cursor = col.find({})
        with open(newFile, 'w') as file:
            json.dump(json.loads(dumps(cursor)), file)
    equipment = player.find_one( { "SECTION": "equipped" } )
    setWeapon(equipment["WEAPON"])
    setFX(equipment["FX"])
    locationName = player.find_one( { "SECTION": "location" } )["NAME"]
    setLocation(locationName)
