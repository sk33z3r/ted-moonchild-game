import curses, sys
from os import system
from time import sleep
from natsort import natsorted
import database as dbs
import art

# define border styles so they're easier to change later
lb, rb = 0, 0
tb, bb = 0, 0
tl, tr, ll, lr = 0, 0, 0, 0

# available command definitions
BASE_COMMANDS = [ "save", "shop", "look", "take", "drop", "sell", "buy", "equip", "unequip", "quit", "exit", "help", "use" ]
USE_CMDS = [ "use", "try" ]
EAT_CMDS = [ "eat", "gobble", "consume" ]
DRINK_CMDS = [ "swallow", "gulp", "slurp", "drink" ]
SMOKE_CMDS = [ "smoke", "toke", "inhale" ]
DRUG_CMDS = [ "swallow", "snort", "lick" ]
BATTLE_COMMANDS = [ "attack", "mojo", "magic", "hit" ]
MOVE_CMDS = [ "move", "walk", "run", "shimmy", "slide" ]
ALL_COMMANDS = BASE_COMMANDS + EAT_CMDS + DRINK_CMDS + SMOKE_CMDS + DRUG_CMDS
LONG_DIRS = [ "north", "south", "east", "west", "up", "down" ]
SHORT_DIRS = [ "n", "s", "e", "w", "u", "d" ]
ROOM_WORDS = [ "here", "room", "around", "ground", "floor", "area" ]

### Setup Window Dimensions

# define max size
max_x = 110
max_y = 40

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
    global helpDims
    global mainDims
    global mainInputDims

    # determine where curses needs to start the windows to be centered in the terminal
    initBegin_y = round((height - max_y) / 2)
    initBegin_x = round((width - max_x) / 2)

    ### all tuples (height, width, begin_y, begin_x)
    ### input border tuple (uly, ulx, lry, lrx)

    # main menu section dimension map
    menuSectionDims = {
        "main": {
            "border": [ 9, 109, (initBegin_y + 16), (initBegin_x + 1) ],
            "content": [ 7, 105, (initBegin_y + 17), (initBegin_x + 3) ],
            "logo": [ 16, 109, initBegin_y, (initBegin_x + 1) ]
        },
        "input": {
            "border": [ (initBegin_y + 25), (initBegin_x + 1), (initBegin_y + 27), (initBegin_x + 109) ],
            "content": [ 1, 100, (initBegin_y + 26), (initBegin_x + len(PROMPT) + 3) ],
            "prompt": [ (initBegin_y + 26), (initBegin_x + 3) ]
        }
    }

    # world section dimension map
    worldSectionDims = {
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
            "border": [35, 55, (initBegin_y + 17), (initBegin_x + 27)],
            "content": [33, 51, (initBegin_y + 18), (initBegin_x + 29)]
        }
    }

    # battle section dimension map
    battleSectionDims = {
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
            "border": [35, 55, (initBegin_y + 17), (initBegin_x + 27)],
            "content": [33, 51, (initBegin_y + 18), (initBegin_x + 29)]
        }
    }

    # main menu section references
    mainDims = menuSectionDims["main"]
    mainInputDims = menuSectionDims["input"]

    # world section references
    worldTitleDims = worldSectionDims["title"]
    worldGroundDims = worldSectionDims["ground"]
    worldExitDims = worldSectionDims["exits"]
    worldEventDims = worldSectionDims["events"]
    worldInputDims = worldSectionDims["input"]
    worldMsgDims = worldSectionDims["msg"]
    worldStatDims = worldSectionDims["stats"]
    worldInvDims = worldSectionDims["inventory"]
    worldHelpDims = worldSectionDims["help"]

    # world section references
    battleTitleDims = battleSectionDims["title"]
    battleGroundDims = battleSectionDims["ground"]
    battleExitDims = battleSectionDims["exits"]
    battleEventDims = battleSectionDims["events"]
    battleInputDims = battleSectionDims["input"]
    battleMsgDims = battleSectionDims["msg"]
    battleStatDims = battleSectionDims["stats"]
    battleInvDims = battleSectionDims["inventory"]
    battleHelpDims = battleSectionDims["help"]

# define the PROMPT design
PROMPT = "\m/: "

# identify the OS
def identify_os():

    # setup the clear function
    system = sys.platform
    if system == "win32":
        return "cls"
    else:
        return "clear"

# clear the terminal
def clear():
    system(identify_os())

# define styles for curses
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
        "BLINK_DIM": curses.A_DIM + curses.A_BLINK,
        "RED": curses.color_pair(1),
        "DIM_RED": curses.A_DIM + curses.color_pair(1),
        "BRIGHT_RED": curses.A_BOLD + curses.color_pair(1),
        "BLINK_RED": curses.A_BLINK + curses.color_pair(1),
        "BLINK_BRIGHT_RED": curses.A_BLINK + curses.A_BOLD + curses.color_pair(1),
        "BLINK_DIM_RED": curses.A_BLINK + curses.A_DIM + curses.color_pair(1),
        "GREEN": curses.color_pair(2),
        "DIM_GREEN": curses.A_DIM + curses.color_pair(2),
        "BRIGHT_GREEN": curses.A_BOLD + curses.color_pair(2),
        "BLINK_GREEN": curses.A_BLINK + curses.color_pair(2),
        "BLINK_BRIGHT_GREEN": curses.A_BLINK + curses.A_BOLD + curses.color_pair(2),
        "BLINK_DIM_GREEN": curses.A_BLINK + curses.A_DIM + curses.color_pair(2),
        "YELLOW": curses.color_pair(3),
        "DIM_YELLOW": curses.A_DIM + curses.color_pair(3),
        "BRIGHT_YELLOW": curses.A_BOLD + curses.color_pair(3),
        "BLINK_YELLOW": curses.A_BLINK + curses.color_pair(3),
        "BLINK_BRIGHT_YELLOW": curses.A_BLINK + curses.A_BOLD + curses.color_pair(3),
        "BLINK_DIM_YELLOW": curses.A_BLINK + curses.A_DIM + curses.color_pair(3),
        "BLUE": curses.color_pair(4),
        "DIM_BLUE": curses.A_DIM + curses.color_pair(4),
        "BRIGHT_BLUE": curses.A_BOLD + curses.color_pair(4),
        "BLINK_BLUE": curses.A_BLINK + curses.color_pair(4),
        "BLINK_BRIGHT_BLUE": curses.A_BLINK + curses.A_BOLD + curses.color_pair(4),
        "BLINK_DIM_BLUE": curses.A_BLINK + curses.A_DIM + curses.color_pair(4),
        "MAGENTA": curses.color_pair(5),
        "DIM_MAGENTA": curses.A_DIM + curses.color_pair(5),
        "BRIGHT_MAGENTA": curses.A_BOLD + curses.color_pair(5),
        "BLINK_MAGENTA": curses.A_BLINK + curses.color_pair(5),
        "BLINK_BRIGHT_MAGENTA": curses.A_BLINK + curses.A_BOLD + curses.color_pair(5),
        "BLINK_DIM_MAGENTA": curses.A_BLINK + curses.A_DIM + curses.color_pair(5),
        "CYAN": curses.color_pair(6),
        "DIM_CYAN": curses.A_DIM + curses.color_pair(6),
        "BRIGHT_CYAN": curses.A_BOLD + curses.color_pair(6),
        "BLINK_CYAN": curses.A_BLINK + curses.color_pair(6),
        "BLINK_BRIGHT_CYAN": curses.A_BLINK + curses.A_BOLD + curses.color_pair(6),
        "BLINK_DIM_CYAN": curses.A_BLINK + curses.A_DIM + curses.color_pair(6)
    }

# function to refresh info in memory
def refreshInfo():
    dbs.getInventory()
    dbs.getStats()
    dbs.getLocation()

# get the effects string for inventory and shop printouts
def getEffectString(item):

    # get the name of the item
    itemInfo = dbs.items.find_one( { "NAME": item } )
    effectList = ""

    # check if the item has EFFECTs
    try:
        effectList = itemInfo["EFFECT"]

    # if not, build string based on TYPE
    except KeyError:
        if itemInfo["TYPE"] in [ "weapon", "fx" ]:
            effectString = "[+{0}]".format(str(itemInfo["ATKBNS"]))
        else:
            effectString = ""

    # otherwise build the string based on the EFFECT
    else:
        if effectList[0] in [ "DEF", "ATK", "MAG" ]:
            effectString = "[{0}{1}]".format(effectList[0], effectList[1])
        elif effectList[0] in [ "HP", "MP", "XP" ]:
            effectString = "[{0} {1}{2}]".format(effectList[0], effectList[2], str(effectList[1]))

    # return the whole string
    return effectString

# get the first item that matches a descword
def getFirstItemMatchingDesc(desc, itemList):

    # make itemList unique
    itemList = list(set(itemList))

    # iterate through each item in the given list
    for item in itemList:

        # when the first one is found, return the name
        if desc in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
            return item

    # if none are found, return None
    return None

# get an item's grounddesc
def getGroundDesc(item):
    desc = dbs.items.find_one( { "NAME": item } )["GROUNDDESC"]
    return desc

# function to get a full list of the current player inventory
def tempInv():

    # get the latest info
    dbs.getInventory()

    # build temp inv list from all types
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

    # return the list
    return inv

# function to buy and sell items
def itemTransaction(item, dowhat):

    # if sell is specified
    if dowhat == "sell":

        # reduce the value by 25%
        val = round(dbs.items.find_one( { "NAME": item } )["VALUE"] * 0.75)

        # set message text
        message = [ "Ted sold {0} for {1} FLOYDS.".format(item, str(val)), "GREEN" ]

        # updateplayer's FLOYDS and inventory
        dbs.updateStat("FLOYDS", val, "inc")
        dbs.updateInv(item, "del")

    # if buy is specified
    if dowhat == "buy":

        # get the raw value
        val = dbs.items.find_one( { "NAME": item } )["VALUE"]

        # if the item costs more than player has floyds, set a failure message
        if val > dbs.playerStats["FLOYDS"]:
            message = [ "Ted doesn't have enough FLOYDS to pay for that!", "RED" ]

        # otherwise set a success message
        else:
            message = [ "Ted bought {0} for {1} FLOYDS.".format(item, str(val)), "GREEN" ]

            # update player's FLOYDS and inventory
            dbs.updateStat("FLOYDS", val, "dec")
            dbs.updateInv(item, "add")

    # return set message
    return message

# function to gain XP and check if a level was gained
def gainXP(val):

    # update the stat in db
    dbs.updateStat("XP", val, "inc")

    # if XP went above the requirement for the next level, do the level increase
    if dbs.playerStats["XP"] >= dbs.levels.find_one( { "LEVEL": dbs.playerStats["LVL"] + 1 } )["XPREQ"]:

        # increase LVL
        dbs.updateStat("LVL", 1, "inc")

        # update memory
        dbs.getStats()

        # update remaining stats from the level db
        dbs.updateStat("HPMAX", dbs.levelStats["HPMAX"], "set")
        dbs.updateStat("MPMAX", dbs.levelStats["MPMAX"], "set")
        dbs.updateStat("HP", dbs.levelStats["HPMAX"], "set")
        dbs.updateStat("MP", dbs.levelStats["MPMAX"], "set")

        # reload memory again
        dbs.getStats()

        # set a message
        lvlMsg = "Ted gained a level! {0}".format(" ".join(dbs.levels.find_one( { "LEVEL": dbs.playerStats["LVL"] } )["MSG"]))

    # if no level gain, set blank message
    else:
        lvlMsg = ""

    # return message
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

        # if the item has a 3rd effect, then store it
        try:
            val = itemInfo["EFFECT"][2]

        # otherwise make it blank
        except IndexError:
            val = ""

        # set remaining vars
        maxHP = dbs.playerStats["HPMAX"]
        hp = dbs.playerStats["HP"]
        maxMP = dbs.playerStats["MPMAX"]
        mp = dbs.playerStats["MP"]

        # if the effect increases HP, make sure it doesn't go above max
        if stat == "HP" and op == "+":
            hp = hp + val
            if hp >= maxHP:
                dbs.updateStat(stat, maxHP, "set")
            else:
                dbs.updateStat(stat, val, "inc")

        # if the effect wants to decrease HP, make sure it won't go below 0
        elif stat == "HP" and op == "-":
            hp = hp - val
            if hp <= 0:
                message = [ "Don't do it! That would kill you, Ted!", "RED" ]
                return message
            else:
                dbs.updateStat(stat, val, "dec")

        # if the effect increases MP, make sure it won't go above the max
        elif stat == "MP" and op == "+":
            mp = mp + val
            if mp >= maxMP:
                dbs.updateStat(stat, maxMP, "set")
            else:
                dbs.updateStat(stat, val, "inc")

        # if the effect decreases MP, make sure it doesn't go past 0
        elif stat == "MP" and op == "-":
            mp = mp - val
            if mp <= 0:
                dbs.updateStat(stat, 0, "set")
            else:
                dbs.updateStat(stat, val, "dec")

        # if the effect increases XP, run the gainXP() function
        elif stat == "XP" and op == "+":
            lvlMsg = gainXP(val)

        # otherwise, the effect should buff a stat in battle
        elif stat in [ "MAG", "ATK", "DEF" ]:
            message = [ "TODO: use the item during battle", "MAGENTA" ]
            return message

        # catch exceptions
        else:
            raise Exception("ITEM ERROR: The item effect combo shouldn't exist")

        # setup the message
        message = [ "Ted consumes the {0}! Effect: {1} {2}{3}\n{4}".format(name, stat, op, str(val), lvlMsg), "GREEN" ]

        # remove the item from inventory and write the new information to screen
        dbs.updateInv(name, "del")
        dbs.getStats()
        dbs.getInventory()

    # otherwise, let the user know it can't be used
    else:
        message = [ "Ted, you can't use this item'!", "RED" ]

    # return the message
    return message
