import pymongo, json

# Setup database connection
client = pymongo.MongoClient("mongodb://root:example@172.100.0.121:27017/")
db = client['moonchild']

# collection list for later use
collections = [ "abilities", "challenge_ratings", "enemies", "engine", "items", "rooms" ]

# Define collection variables
abilities = db['abilities']
challenge_ratings = db['challenge_ratings']
enemies = db['enemies']
engine = db['engine']
items = db['items']
rooms = db['rooms']

# reset all documents to initial state
def initDB():
    # remove documents from all collections
    abilities.delete_many({})
    challenge_ratings.delete_many({})
    enemies.delete_many({})
    engine.delete_many({})
    items.delete_many({})
    rooms.delete_many({})
    # iterate through collections list and insert from json
    for name in collections:
        col = db[name]
        # load the json
        jsonFile = './json/' + name + '.json'
        with open(jsonFile) as file:
            file_data = json.load(file)
        # insert_many if there are multiple documents in the json
        if isinstance(file_data, list):
            col.insert_many(file_data)
            print("inserted init document to" + name)
        else:
            col.insert_one(file_data)
            print("inserted init documents to" + name)
