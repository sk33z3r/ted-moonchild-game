import curses, sys
from os import system
from time import sleep
from natsort import natsorted
import database as dbs
from world import worldUI
import art
import main

# define border styles so they're easier to change later
lb, rb = 0, 0
tb, bb = 0, 0
tl, tr, ll, lr = 0, 0, 0, 0

### Setup Window Dimensions

# define max size
max_x = 110
max_y = 70

# function to calculate section dimensions and starting points based on terminal size
def calculateWindows(height, width):

    # define globals
    global initHeight
    global initWidth
    global initBegin_y
    global initBegin_x
    global sectionDims
    global titleDims
    global groundDims
    global exitDims
    global eventDims
    global inputDims
    global msgDims
    global statDims
    global invDims

    # TODO set initial height, width, begin_y, begin_x from terminal size
    initHeight = 0
    initWidth = 0
    initBegin_y = round((height - max_y) / 2)
    initBegin_x = round((width - max_x) / 2)

    # section dimension map
    ### all tuples (height, width, begin_y, begin_x)
    ### input border tuple (uly, ulx, lry, lrx)
    sectionDims = {
        "title": {
            "border": [ 3, 80, initBegin_y, (initBegin_x + 1) ],
            "content": [ 1, 76, (initBegin_y + 1), (initBegin_x + 3) ]
        },
        "ground": {
            "border": [ 8, 50, (initBegin_y + 25), (initBegin_x + 1) ],
            "content": [ 6, 46, (initBegin_y + 26), (initBegin_x + 3) ]
        },
        "exits": {
            "border": [ 8, 29, (initBegin_y + 25), (initBegin_x + 52) ],
            "content": [ 6, 25, (initBegin_y + 26), (initBegin_x + 53) ]
        },
        "events": {
            "border": [ 22, 80, (initBegin_y + 3), (initBegin_x + 1) ],
            "content": [ 20, 76, (initBegin_y + 4), (initBegin_x + 3) ]
        },
        "input": {
            "border": [ (initBegin_y + 33), (initBegin_x + 1), (initBegin_y + 35), (initBegin_x + 80) ],
            "content": [ 1, 72, (initBegin_y + 34), (initBegin_x + len(PROMPT) + 3) ],
            "prompt": [ (initBegin_y + 34), (initBegin_x + 3) ]
        },
        "msg": {
            "border": [ 4, 109, (initBegin_y + 36), (initBegin_x + 1) ],
            "content": [ 2, 105, (initBegin_y + 37), (initBegin_x + 3) ]
        },
        "stats": {
            "border": [ 9, 28, initBegin_y, (initBegin_x + 82) ],
            "content": [ 7, 24, (initBegin_y + 1), (initBegin_x + 84) ]
        },
        "inventory": {
            "border": [ 27, 28, (initBegin_y + 9), (initBegin_x + 82) ],
            "content": [ 25, 24, (initBegin_y + 10), (initBegin_x + 84) ]
        },
        "help": {
            "border": [],
            "content": []
        }
    }

    # section references
    titleDims = sectionDims["title"]
    groundDims = sectionDims["ground"]
    exitDims = sectionDims["exits"]
    eventDims = sectionDims["events"]
    inputDims = sectionDims["input"]
    msgDims = sectionDims["msg"]
    statDims = sectionDims["stats"]
    invDims = sectionDims["inventory"]

# define the PROMPT design
PROMPT = "\m/: "

# identify the OS
def identify_os():
    system = sys.platform
    if system == "win32":
        return "cls"
    else:
        return "clear"

# clear the terminal
def clear():
    system(identify_os())

def setStyles():
    # define globals
    global c
    # initialize color pairs
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    # color map
    c = {
        "WHITE": curses.color_pair(0),
        "DIM": curses.A_DIM,
        "BRIGHT": curses.A_BOLD,
        "BLINK": curses.A_BLINK,
        "BLINK_BRIGHT": curses.A_BOLD + curses.A_BLINK,
        "RED": curses.color_pair(1),
        "DIM_RED": curses.A_DIM + curses.color_pair(1),
        "BRIGHT_RED": curses.A_BOLD + curses.color_pair(1),
        "BLINK_RED": curses.A_BLINK + curses.color_pair(1),
        "BLINK_BRIGHT_RED": curses.A_BLINK + curses.A_BOLD + curses.color_pair(1),
        "GREEN": curses.color_pair(2),
        "DIM_GREEN": curses.A_DIM + curses.color_pair(2),
        "BRIGHT_GREEN": curses.A_BOLD + curses.color_pair(2),
        "BLINK_GREEN": curses.A_BLINK + curses.color_pair(2),
        "BLINK_BRIGHT_GREEN": curses.A_BLINK + curses.A_BOLD + curses.color_pair(2),
        "YELLOW": curses.color_pair(3),
        "DIM_YELLOW": curses.A_DIM + curses.color_pair(3),
        "BRIGHT_YELLOW": curses.A_BOLD + curses.color_pair(3),
        "BLINK_YELLOW": curses.A_BLINK + curses.color_pair(3),
        "BLINK_BRIGHT_YELLOW": curses.A_BLINK + curses.A_BOLD + curses.color_pair(3),
        "BLUE": curses.color_pair(4),
        "DIM_BLUE": curses.A_DIM + curses.color_pair(4),
        "BRIGHT_BLUE": curses.A_BOLD + curses.color_pair(4),
        "BLINK_BLUE": curses.A_BLINK + curses.color_pair(4),
        "BLINK_BRIGHT_BLUE": curses.A_BLINK + curses.A_BOLD + curses.color_pair(4),
        "MAGENTA": curses.color_pair(5),
        "DIM_MAGENTA": curses.A_DIM + curses.color_pair(5),
        "BRIGHT_MAGENTA": curses.A_BOLD + curses.color_pair(5),
        "BLINK_MAGENTA": curses.A_BLINK + curses.color_pair(5),
        "BLINK_BRIGHT_MAGENTA": curses.A_BLINK + curses.A_BOLD + curses.color_pair(5),
        "CYAN": curses.color_pair(6),
        "DIM_CYAN": curses.A_DIM + curses.color_pair(6),
        "BRIGHT_CYAN": curses.A_BOLD + curses.color_pair(6),
        "BLINK_CYAN": curses.A_BLINK + curses.color_pair(6),
        "BLINK_BRIGHT_CYAN": curses.A_BLINK + curses.A_BOLD + curses.color_pair(6)
    }

def refreshInfo():
    dbs.getInventory()
    dbs.getStats()
    dbs.getLocation()

def getEffectString(item):
    # get the name of the item
    itemInfo = dbs.items.find_one( { "NAME": item } )
    effectList = ""
    # check if the item has EFFECTs
    try:
        effectList = itemInfo["EFFECT"]
    except KeyError:
        # if not, build string based on TYPE
        if itemInfo["TYPE"] in [ "weapon", "fx" ]:
            effectString = "[+{0}]".format(str(itemInfo["ATKBNS"]))
        else:
            effectString = ""
    else:
        # build the string based on the EFFECT
        if effectList[0] in [ "DEF", "ATK", "MAG" ]:
            effectString = "[{0}{1}]".format(effectList[0], effectList[1])
        elif effectList[0] in [ "HP", "MP", "XP" ]:
            effectString = "[{0} {1}{2}]".format(effectList[0], effectList[2], str(effectList[1]))
    return effectString

def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    for item in itemList:
        if desc in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
            return item
    return None

def getRandDescWords(item):
    # Returns a list of "description words" for each item named in itemList.
    descWords = []
    descWords.extend(dbs.items.find_one( { "NAME": item } )["DESCWORDS"])
    desc = random.randomchoice(descWords)
    return desc

def getGroundDesc(item):
    desc = dbs.items.find_one( { "NAME": item } )["GROUNDDESC"]
    return desc

# function to get a full list of the current player inventory
def tempInv():
    dbs.getInventory()
    # build temp inv list
    inv = []
    n = 0
    for i in dbs.playerInv["ITEMS"]:
        inv.append(dbs.playerInv["ITEMS"][n])
        n += 1
    n = 0
    for i in dbs.playerInv["KEY_ITEMS"]:
        inv.append(dbs.playerInv["KEY_ITEMS"][n])
        n += 1
    n = 0
    for i in dbs.playerInv["EQUIPPED"]:
        inv.append(dbs.playerInv["EQUIPPED"][n])
        n += 1
    inv = natsorted(inv)
    return inv

# function to buy and sell items
def itemTransaction(item, dowhat):
    if dowhat == "sell":
        val = round(dbs.items.find_one( { "NAME": item } )["VALUE"] * 0.75)
        message = [ "Ted sold {0} for {1} FLOYDS.".format(item, str(val)), "GREEN" ]
        dbs.updateStat("FLOYDS", val, "inc")
        dbs.updateInv(item, "del")
    if dowhat == "buy":
        val = dbs.items.find_one( { "NAME": item } )["VALUE"]
        if val > dbs.playerStats["FLOYDS"]:
            message = [ "Ted doesn't have enough FLOYDS to pay for that!", "RED" ]
        else:
            message = [ "Ted bought {0} for {1} FLOYDS.".format(item, str(val)), "GREEN" ]
            dbs.updateStat("FLOYDS", val, "dec")
            dbs.updateInv(item, "add")
    return message

def gainXP(val):
    dbs.updateStat("XP", val, "inc")
    if dbs.playerStats["XP"] >= dbs.levels.find_one( { "LEVEL": dbs.playerStats["LVL"] + 1 } )["XPREQ"]:
        # if XP went above the requirement for the next level, do the level increase
        dbs.updateStat("LVL", 1, "inc")
        dbs.getStats()
        dbs.updateStat("HPMAX", dbs.levelStats["HPMAX"], "set")
        dbs.updateStat("MPMAX", dbs.levelStats["MPMAX"], "set")
        dbs.updateStat("HP", dbs.levelStats["HPMAX"], "set")
        dbs.updateStat("MP", dbs.levelStats["MPMAX"], "set")
        dbs.getStats()
        lvlMsg = "Ted gained a level! {0}".format(" ".join(dbs.levels.find_one( { "LEVEL": dbs.playerStats["LVL"] } )["MSG"]))
    else:
        lvlMsg = ""
    return lvlMsg

# function to use items
def useItem(name):
    # get item info
    itemInfo = dbs.items.find_one( { "NAME": name } )
    # figure out what the item is, and do the thing
    if itemInfo["TYPE"] in [ "drug", "food", "smoke", "drink" ]:
        # store some vars for later
        lvlMsg = ""
        stat = itemInfo["EFFECT"][0]
        op = itemInfo["EFFECT"][1]
        try:
            val = itemInfo["EFFECT"][2]
        except IndexError:
            val = ""
        maxHP = dbs.playerStats["HPMAX"]
        hp = dbs.playerStats["HP"]
        maxMP = dbs.playerStats["MPMAX"]
        mp = dbs.playerStats["MP"]
        # if the stat is HP or MP, we need to check that the new value isn't above or below the max/min parameters
        if stat == "HP" and op == "+":
            hp = hp + val
            if hp >= maxHP:
                dbs.updateStat(stat, maxHP, "set")
            else:
                dbs.updateStat(stat, val, "inc")
        elif stat == "HP" and op == "-":
            hp = hp - val
            if hp <= 0:
                message = [ "Don't do it! That would kill you, Ted!", "RED" ]
                return message
            else:
                dbs.updateStat(stat, val, "dec")
        elif stat == "MP" and op == "+":
            mp = mp + val
            if mp >= maxMP:
                dbs.updateStat(stat, maxMP, "set")
            else:
                dbs.updateStat(stat, val, "inc")
        elif stat == "MP" and op == "-":
            mp = mp - val
            if mp <= 0:
                dbs.updateStat(stat, 0, "set")
            else:
                dbs.updateStat(stat, val, "dec")
        elif stat == "XP" and op == "+":
            lvlMsg = gainXP(val)
        elif stat in [ "MAG", "ATK", "DEF" ]:
            message = [ "TODO: use the item during battle", "MAGENTA" ]
            return message
        else:
            raise Exception("ITEM ERROR: The item effect combo shouldn't exist")
        message = [ "Ted consumes the {0}! Effect: {1} {2}{3}\n{4}".format(name, stat, op, str(val), lvlMsg), "GREEN" ]
        # remove the item from inventory and write the new information to screen
        dbs.updateInv(name, "del")
        dbs.getStats()
        dbs.getInventory()
    # TODO try something with key items
    # otherwise, let the user know it can't be used
    else:
        message = [ "Ted, you can't use this item'!", "RED" ]
    return message

def endGame():
    sys.exit()
