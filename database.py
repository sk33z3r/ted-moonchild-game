import pymongo

# Setup database connection
client = pymongo.MongoClient("mongodb://root:example@172.100.0.121:27017/")
db = client['moonchild']

# Define collection variables
abilities = db['abilities']
rating = db['challenge_ratings']
enemies = db['enemies']
engine = db['engine']
items = db['items']
rooms = db['rooms']
