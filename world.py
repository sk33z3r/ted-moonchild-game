import curses
from textwrap import wrap
from time import sleep
from natsort import natsorted
from curses.textpad import Textbox, rectangle
from random import randrange, choice
import engine as eng
import database as dbs

class worldUI():

    # available command definitions
    BASE_COMMANDS = [ "save", "shop", "look", "take", "drop", "sell", "buy", "equip", "unequip", "quit", "exit", "help", "use" ]
    USE_CMDS = [ "use", "try" ]
    EAT_CMDS = [ "eat", "gobble", "consume" ]
    DRINK_CMDS = [ "swallow", "gulp", "slurp", "drink" ]
    SMOKE_CMDS = [ "smoke", "toke", "inhale" ]
    DRUG_CMDS = [ "swallow", "snort", "lick" ]
    ALL_COMMANDS = BASE_COMMANDS + EAT_CMDS + DRINK_CMDS + SMOKE_CMDS + DRUG_CMDS
    LONG_DIRS = [ "north", "south", "east", "west", "up", "down" ]
    SHORT_DIRS = [ "n", "s", "e", "w", "u", "d" ]
    ROOM_WORDS = [ "here", "room", "around", "ground", "there", "floor", "area" ]

    # updates room visited and solved status
    def updateRoomStatus(what):

        # set the VISITED value
        if what == "VISITED":
            status = dbs.locationInfo["VISITED"]
            dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$set": { "VISITED": 1 } } )

        # set the SOLVED value
        elif what == "SOLVED":
            status = dbs.locationInfo["SOLVED"]
            dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$set": { "SOLVED": 1 } } )

            # add an item to the ground if specified
            if "ADD_GROUND" in dbs.locationInfo:
                for item in dbs.locationInfo["ADD_GROUND"]:
                    dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$push": { "GROUND" : item } } )

            # remove an item from the ground if specified
            if "DEL_GROUND" in dbs.locationInfo:
                for item in dbs.locationInfo["DEL_GROUND"]:
                    dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$pull": { "GROUND" : item } } )

            # add a direction to the room if specified
            if "ADD_DIRS" in dbs.locationInfo:
                d = 0
                while d < len(dbs.locationInfo["ADD_DIRS"]):
                    dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$set": { dbs.locationInfo["ADD_DIRS"][str(d)][0] : dbs.locationInfo["ADD_DIRS"][str(d)][1] } } )
                    d += 1

            # remove a direction from the room if specified
            if "DEL_DIRS" in dbs.locationInfo:
                d = 0
                while d < len(dbs.locationInfo["DEL_DIRS"]):
                    dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$unset": { dbs.locationInfo["DEL_DIRS"][str(d)][0] : "" } } )
                    d += 1

            # remove item from player's inventory
            for item in dbs.locationInfo["EVENT_KEYS"]:
                if item != "FLOYDS" and not type(item) == int:
                    dbs.updateInv(item, "del")

        # refresh data
        eng.refreshInfo()

    # updates sector visited status
    def updateSectorStatus(sector):

        # get sector's short name
        sectorShort = sector.replace(" Sector", "")

        # update the db entry
        dbs.locations.update_one( { "NAME": "Space" }, { "$set": { sectorShort.upper() : 1 } } )

        # refresh data
        eng.refreshInfo()

    # function to write Space events
    def writeSpaceEvents(speed, sector):

        # setup initial line and position
        y, l = 1, 0

        # define the sector's short name and get info
        sectorShort = sector.replace(" Sector", "").upper()
        spaceInfo = dbs.locations.find_one( { "NAME": "Space" } )

        # if this sector hasn't been visited before, run the special events
        if spaceInfo[sectorShort] == 0:
            sectorEvents = "{0}_EVENTS".format(sectorShort)
            events = dbs.locations.find_one( { "NAME": "Space" } )[sectorEvents]

        # otherwise run the default events
        else:
            events = dbs.locations.find_one( { "NAME": "Space" } )["DEFAULT_EVENTS"]

        # display each line with a specified delay
        while l < len(events):

            # if the dialogue is taking up the whole window, we need to clear it and start writing at the beginning again
            if y >= 15:
                eventWin.addstr(18, 4, ">>>>>", eng.c["BLINK_BRIGHT_YELLOW"])
                sleep(speed)
                y = 1
                eventWin.clear()
                sleep(0.5)

            # get event text and wrap the text to fit inside the window
            eventString = '\n'.join(wrap(events[str(l)][1], 75))

            # get event's text style
            stringStyle = events[str(l)][0]

            # display the text
            eventWin.addstr(y, 0, eventString, eng.c[stringStyle])

            # move to new position
            l += 1

            # add more newlines if text will be wrapped multiple times in the window
            if len(eventString) < 75:
                y += 2
                sleep(speed)
            if len(eventString) > 75 and len(eventString) < 150:
                y += 3
                sleep((speed + 1))
            elif len(eventString) > 150 and len(eventString) < 225:
                y += 4
                sleep((speed + 2))
            elif len(eventString) > 225 and len(eventString) < 300:
                y += 5
                sleep((speed + 3))

    # display FIRST and KEY events to the EVENTS section
    def writeTimedEvents(speed, what):

        # setup initial line and position
        y, l = 1, 0

        # set FIRST_EVENTS as the list
        if what == "first":
            events = dbs.locationInfo["FIRST_EVENTS"]

        # set KEY_EVENTS as the list
        elif what == "key":
            events = dbs.locationInfo["KEY_EVENTS"]

        # catch unknown exceptions
        else:
            raise Exception("BUG: 'what' arg for writeTimedEvents() not specified")

        # print each line to the EVENTS section with a specified delay
        while l < len(events):

            # if the dialogue is taking up the whole window, we need to clear it and start writing at the beginning again
            if y >= 15:
                eventWin.addstr(18, 4, ">>>>>", eng.c["BLINK_BRIGHT_YELLOW"])
                sleep(speed)
                y = 1
                eventWin.clear()
                sleep(0.5)

            # get event text and wrap the text to fit inside the window
            eventString = '\n'.join(wrap(events[str(l)][1], 75))

            # get event's text style
            stringStyle = events[str(l)][0]

            # display the text
            eventWin.addstr(y, 0, eventString, eng.c[stringStyle])

            # move to new position
            l += 1

            # add more newlines if text will be wrapped multiple times in the window
            if len(eventString) < 75:
                y += 2
                sleep(speed)
            if len(eventString) > 75 and len(eventString) < 150:
                y += 3
                sleep((speed + 1))
            elif len(eventString) > 150 and len(eventString) < 225:
                y += 4
                sleep((speed + 2))
            elif len(eventString) > 225 and len(eventString) < 300:
                y += 5
                sleep((speed + 3))

    # display SOLVED and UNSOLVED events
    def writeStaticEvents(what):

        # set starting line and position
        y, l = 1, 0

        # set UNSOLVED_EVENTS  as the list
        if what == "unsolved":
            events = dbs.locationInfo["UNSOLVED_EVENTS"]

        # set SOLVED_EVENTS as the list
        elif what == "solved":
            events = dbs.locationInfo["SOLVED_EVENTS"]

        # catch unknown exceptions
        else:
            raise Exception("BUG: 'what' arg for writeStaticEvents() not specified")

        # print each line to EVENTS section
        while l < len(events):

            # get event text and wrap the text to fit inside the window
            eventString = '\n'.join(wrap(events[str(l)][1], 75))

            # get event's text style
            stringStyle = events[str(l)][0]

            # display the text
            eventWin.addstr(y, 0, eventString, eng.c[stringStyle])

            # move to new position
            l += 1

            # add more newlines if text will be wrapped multiple times in the window
            if len(eventString) < 75:
                y += 2
            if len(eventString) > 75 and len(eventString) < 150:
                y += 3
            elif len(eventString) > 150 and len(eventString) < 225:
                y += 4
            elif len(eventString) > 225 and len(eventString) < 300:
                y += 5

    # function to write room info to the EVENTS section
    def writeRoom(room, where, key):

        # clear and setup the window
        eventBorder.clear()
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        eventBorder.addstr(0, 65, "[ROOM EVENTS]")
        worldUI.clearScreen()

        # if this is to be the Winnibego
        if where == "winnibego":

            # set the new room data
            dbs.setLocation(room)

            # setup DOWN direction
            dbs.locations.update_one( { "NAME": "Winnibego" }, { "$set": { dbs.locationInfo["PLANET_DIRS"][dbs.PLANET][0] : dbs.locationInfo["PLANET_DIRS"][dbs.PLANET][1] } } )
            eng.refreshInfo()

            # setup the title window
            titleWin.clear()
            title = "{0}: {1}".format(dbs.PLANET, dbs.ROOM)
            titleWin.addstr(0, 0, title, eng.c["BRIGHT"])

            # display the winnibego room events based on triggers
            if dbs.locationInfo["VISITED"] == 0:
                worldUI.writeTimedEvents(3, "first")
                worldUI.updateRoomStatus("VISITED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 0:
                worldUI.writeStaticEvents("unsolved")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == True:
                worldUI.writeTimedEvents(4, "key")
                worldUI.updateRoomStatus("SOLVED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == False:
                events = dbs.locationInfo["SOLVED_EVENTS"]
                eventString = '\n'.join(wrap(events[str(0)][1], 75)).format(dbs.PLANET)
                stringStyle = events[str(0)][0]
                eventWin.addstr(1, 0, eventString, eng.c[stringStyle])

        # if this is to be Space
        elif where == "space":

            # set new room data
            dbs.setSpaceLocation(room)

            # get a list of directions that need to be displayed for this sector
            dirList = dbs.locationInfo["SECTOR_DIRS"][room]

            # for each direction, check and remove any existing directions in the db
            for direction in worldUI.LONG_DIRS:
                if direction.upper() in dbs.locationInfo:
                    dbs.locations.update_one( { "NAME": "Space" }, { "$unset": { direction.upper() : "" } } )

            # set initial position
            l = 0

            # add each new direction to the db
            while l < len(dirList):
                dbs.locations.update_one( { "NAME": "Space" }, { "$set": { dirList[str(l)][0] : dirList[str(l)][1] } } )
                l += 1

            # refresh new data
            eng.refreshInfo()

            # setup the title window
            titleWin.clear()
            title = "{0}: {1}".format(dbs.SECTOR, dbs.ROOM)
            titleWin.addstr(0, 0, title, eng.c["BRIGHT"])

            # display the space travel room
            worldUI.writeSpaceEvents(2, room)
            worldUI.updateSectorStatus(room)

        # default to being a Planet
        elif where == "planet":

            # set new room data
            dbs.setLocation(room)

            # refresh new data
            eng.refreshInfo()

            # setup the title window
            titleWin.clear()
            title = "{0}: {1}".format(dbs.PLANET, dbs.ROOM)
            titleWin.addstr(0, 0, title, eng.c["BRIGHT"])

            # display a normal room based on triggers
            if dbs.locationInfo["VISITED"] == 0:
                worldUI.writeTimedEvents(3, "first")
                worldUI.updateRoomStatus("VISITED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 0:
                worldUI.writeStaticEvents("unsolved")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == True:
                worldUI.writeTimedEvents(4, "key")
                worldUI.updateRoomStatus("SOLVED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == False:
                worldUI.writeStaticEvents("solved")

        # catch unknown exceptions
        else:
            raise Exception("BUG: writeRoom() didn't have the right arg passed.")

        # rewrite the whole UI
        worldUI.rewriteScreen()

    # function to write the SHOP menu in the EVENTS section
    def writeShop():

        # clear the EVENTS section first
        eventBorder.clear()
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        eventBorder.addstr(0, 66, "[SHOP ITEMS]")
        eventWin.clear()

        # get a list of items in the current shop
        shopItems = dbs.locationInfo["SHOP"]

        # set the starting line for text
        y = 0

        # for each item in the rooms SHOP list
        for item in shopItems:

            # set some vars
            itemInfo = dbs.items.find_one( { "NAME": item } )
            effectString = eng.getEffectString(item)
            nameString = "{0} {1}".format(itemInfo["NAME"], effectString)

            # print the name in bold
            eventWin.addstr(y, 0, nameString, eng.c["BRIGHT"])

            # move to next line
            y += 1

            # wrap the LONGDESC to fit the window before displaying it
            eventWin.addstr(y, 0, '\n'.join(wrap(itemInfo["LONGDESC"], 75)), eng.c["DIM"])

            # add empty lines appropriately if the above string is long enough
            if len(itemInfo["LONGDESC"]) < 76:
                y += 1
            else:
                y += 2

            # display the value in green
            floydsString = "[FLOYDS: {0}]".format(str(itemInfo["VALUE"]))
            eventWin.addstr(y, 0, floydsString, eng.c["GREEN"])

            # add newline between items
            y += 2

    # function to write the GROUND section
    def writeGround():

        # set the list of items on the ground
        groundList = list(dbs.locationInfo["GROUND"])

        # if there are no items, clear the window, otherwise print a list of items
        if len(groundList) == 0:
            groundWin.clear()
            pass

        # otherwise get to printin'
        else:
            groundWin.clear()

            # get a count of each item in the ITEMS list only
            itemCount = {}
            for item in groundList:
                if item in list(itemCount.keys()):
                    itemCount[item] += 1
                else:
                    itemCount[item] = 1

            # set starting rows and columns in the window
            y, x, l = 1, 0, 0

            # for each item on the ground
            for item in set(groundList):
                desc = eng.getGroundDesc(item)

                # if there is more than one, print it once with a quantity
                if itemCount[item] > 1:
                    groundString = "{0}x {1}".format(str(itemCount[item]), desc)
                    groundWin.addstr(y, x, groundString, eng.c["DIM"])

                # otherwise just print the item
                else:
                    groundString = desc
                    groundWin.addstr(y, x, groundString, eng.c["DIM"])

                # if this string is longer than the previous longest string, set a new length
                if len(groundString) > l:
                    l = len(groundString)

                # if we've reached the last line in the GROUND section, setup the next column
                if y == 4:

                    # reset to the first line
                    y = 1

                    # move to the next column
                    x = l + x + 3

                    # reset longest string length to 0
                    l = 0

                # otherwise move to a new line
                else:
                    y += 1

    # function to write the EXITS section
    def writeDirs():

        # clear the window
        dirWin.clear()

        # set the starting line in the section
        y = 1

        # run through the list of directions
        for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):

            # for each one that matches, print the info from db
            if direction in list(dbs.locationInfo):
                dirString = "{0}: {1}".format(direction, dbs.locationInfo[direction])
                dirWin.addstr(y, 1, dirString, eng.c["DIM"])
                y += 1

    # function to parse which location to write and how
    def writeLocation(room, what, key):

        # clear the event window
        eventWin.clear()

        # make sure GROUND and EXITS are still visible
        worldUI.writeGround()
        worldUI.writeDirs()

        # if this is to be a room
        if what == "room":

            # and that room is the Winnibego
            if room.lower() == "winnibego":
                worldUI.writeRoom(room, "winnibego", key)

            # and that room is Space
            elif room.lower() == "space":
                worldUI.writeRoom(dbs.SECTOR, "space", key)

            # and that room is a Sector
            elif room.endswith("Sector"):
                worldUI.writeRoom(room, "space", key)

            # otherwise default to a Planet
            else:
                worldUI.writeRoom(room, "planet", key)

        # if this is to be a shop, print it
        elif what == "shop":
            worldUI.writeShop()

        # catch unknown exceptions
        else:
            raise Exception("Forgot to specify writeout for the event window!")

    # function to write a message to the player
    def writeMsg(msg, style):

        # clear the window
        msgWin.clear()

        # display the message
        msgWin.addstr(0, 0, msg, eng.c[style])

    # funcion to clear and write the STATS section
    def writeStats():

        # clear and refresh info
        statsWin.clear()
        eng.refreshInfo()

        # put the stat values into a dict
        stats = {
            "hp": dbs.playerStats["HP"],
            "hpmax": dbs.playerStats["HPMAX"],
            "mp": dbs.playerStats["MP"],
            "mpmax": dbs.playerStats["MPMAX"],
            "lvl": dbs.playerStats["LVL"],
            "xp": dbs.playerStats["XP"],
            "floyds": dbs.playerStats["FLOYDS"],
            "lvlReq": dbs.levels.find_one( { "LEVEL": dbs.playerStats["LVL"] + 1 } )["XPREQ"]
        }

        # setup stat display
        stat1 = 'HEALTH: {hp} / {hpmax}'.format(**stats)
        stat2 = '  MOJO: {mp} / {mpmax}'.format(**stats)
        stat3 = '   LVL: {lvl}'.format(**stats)
        stat4 = '    XP: {xp} / {lvlReq}'.format(**stats)
        stat5 = 'FLOYDS: {floyds}'.format(**stats)

        # print the strings to the stats wndow
        statsWin.addstr(1, 2, stat1, eng.c["RED"])
        statsWin.addstr(2, 2, stat2, eng.c["BLUE"])
        statsWin.addstr(3, 2, stat3, eng.c["YELLOW"])
        statsWin.addstr(4, 2, stat4, eng.c["YELLOW"])
        statsWin.addstr(5, 2, stat5, eng.c["GREEN"])

    # function to clear and write the INVENTORY section
    def writeInv():

        # clear and refresh info
        invWin.clear()
        eng.refreshInfo()

        # get and sort all item lists individually
        i = list(dbs.playerInv["ITEMS"])
        k = list(dbs.playerInv["KEY_ITEMS"])
        e = list(dbs.playerInv["EQUIPPED"])
        i = natsorted(i)
        k = natsorted(k)
        e = natsorted(e)

        # if there are no items, print a message
        if len(i) == 0 and len(k) == 0 and len(e) == 0:
            writeMsg("Ted doesn't have shit in his pockets!", "RED")
            return

        # get a count of each item in the ITEMS list only
        itemCount = {}
        for item in i:
            if item in list(itemCount.keys()):
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # set starting line in the window
        s = 1

        # print items from ITEMS with their item count
        if len(i) != 0:
            for item in set(i):
                effectString = eng.getEffectString(item)
                itemString = "{0}x {1} {2}".format(str(itemCount[item]), item, effectString)
                invWin.addstr(s, 1, itemString)
                s += 1
            s += 1

        # print items from EQUIPPED
        if len(e) != 0:
            invWin.addstr(s, 0, "[EQUIPMENT]-------------", eng.c["CYAN"])
            s += 2
            for item in set(e):
                effectString = eng.getEffectString(item)
                itemString = "{0} {1}".format(item, effectString)
                invWin.addstr(s, 1, itemString, eng.c["CYAN"])
                s += 1
            s += 1

        # print items from KEY_ITEMS
        if len(k) != 0:
            invWin.addstr(s, 0, "[KEY ITEMS]-------------", eng.c["YELLOW"])
            s += 2
            for item in set(k):
                invWin.addstr(s, 1, item, eng.c["YELLOW"])
                s += 1

    # function to move the player from room to room
    def moveDirection(direction):

        # setup vars and screen
        upper = direction.upper()
        lower = direction.lower()
        combatCheck = randrange(1, 50)
        msgWin.clear()

        # link short names to long names
        if lower in worldUI.SHORT_DIRS:
            if lower == "n":
                upper = "NORTH"
            if lower == "s":
                upper = "SOUTH"
            if lower == "e":
                upper = "EAST"
            if lower == "w":
                upper = "WEST"
            if lower == "u":
                upper = "UP"
            if lower == "d":
                upper = "DOWN"

        # if the direction exists in the current locations document
        if upper in dbs.locationInfo:

            # make sure to set the Winnibego's current planet before we move, just in case the player is stepping into the Winnie itself
            dbs.locations.update_one( { "NAME": "Winnibego" }, { "$set": { "PLANET": dbs.locations.find_one( { "NAME": dbs.ROOM } )["PLANET"] } } )

            # if combat should happen, make it happen
            if combatCheck > 40:
                # TODO combatMode().fight()
                worldUI.writeLocation(dbs.locationInfo[upper], "room", False)

            # otherwise move to the new room
            else:
                worldUI.writeLocation(dbs.locationInfo[upper], "room", False)

        # let the player know if the direction can't be found
        else:
            worldUI.writeMsg("Ted can't walk through walls.", "RED")

    # function to initialize the UI and get user input
    def displayWorld():

        # write all data to the screen
        worldUI.writeStats()
        worldUI.writeInv()
        worldUI.writeMsg("", "DIM")
        worldUI.writeLocation(dbs.ROOM, "room", False)

        # main command input loop
        while True:
            userInput = worldUI.getCmd()
            worldUI.processCmd(userInput)

    # function specifically to parse commands and run their relevant functions
    def runAction(cmd, arg):

        # setup the environment
        inv = eng.tempInv()
        itemOnGround = eng.getFirstItemMatchingDesc(arg, dbs.locationInfo["GROUND"])
        itemInInv = eng.getFirstItemMatchingDesc(arg, inv)

        # some times an item might not be in the SHOP, let's make sure to catch the exception
        try:
            itemInShop = eng.getFirstItemMatchingDesc(arg, dbs.locationInfo["SHOP"])
        except KeyError:
            pass

        ## Parsing cmd and arg into actions
        # shop
        if cmd == "shop":

            # if the shop doesn't exist, let the player know
            if "SHOP" not in dbs.locationInfo:
                worldUI.writeMsg("There's no shop here, Ted!", "RED")
                return

            # otherwise print the shop info
            worldUI.writeLocation(dbs.ROOM, "shop", False)

        # look (room|item)
        elif cmd == "look":

            # with no specifics given, assume the player wants to refresh the room event
            if arg == None or arg in worldUI.ROOM_WORDS:
                worldUI.writeLocation(dbs.ROOM, "room", False)

            # if the arg is a direction, ignore it
            elif arg in worldUI.LONG_DIRS or arg in worldUI.SHORT_DIRS:
                # TODO add short descriptions for every direction so this can print something to the player
                pass

            # if the arg matches an item on the ground, display the info
            elif itemOnGround != None:

                # wrap text with textwrap instead of letting curses do it
                longdesc = '\n'.join(wrap(dbs.items.find_one( { "NAME": itemOnGround } )["LONGDESC"], 100))
                if len(longdesc) > 100:
                    worldUI.writeMsg(longdesc, "DIM")
                else:
                    worldUI.writeMsg(longdesc, "DIM")

            # if the arg matches an item in player's inventory, display the info
            elif itemInInv != None:

                # wrap text with textwrap instead of letting curses do it
                longdesc = '\n'.join(wrap(dbs.items.find_one( { "NAME": itemInInv } )["LONGDESC"], 100))
                if len(longdesc) > 100:
                    worldUI.writeMsg(longdesc, "DIM")
                else:
                    worldUI.writeMsg(longdesc, "DIM")

            # let the player know if the arg isn't found
            else:
                worldUI.writeMsg("Ted scours to room, but he doesn't see that.", "DIM")

        # take item
        elif cmd == "take":

            # if arg is empty, ask the player
            if arg == "":
                worldUI.writeMsg("What should Ted take?", "DIM")

            # if the item is on the ground
            elif itemOnGround != None:

                itemInfo = dbs.items.find_one( { "NAME": itemOnGround } )

                # if item isn't takeable, let the user know
                if itemInfo["TAKEABLE"] == False:
                    worldUI.writeMsg("Ted doesn't want to grab that.", "RED")

                # otherwise take the item
                elif itemInfo["TAKEABLE"] == True:
                    dbs.updateGround(itemInfo["NAME"], "del") # remove from ground
                    dbs.updateInv(itemInfo["NAME"], "add") # add to inventory
                    worldUI.writeInv()
                    worldUI.writeGround()
                    message = "Ted grabs {0}.".format(itemInfo["SHORTDESC"])
                    worldUI.writeMsg(message, "DIM")

            # let the player know if the item isn't found anywhere'
            else:
                worldUI.writeMsg("Ted doesn't see that.", "RED")

        # drop item
        elif cmd == "drop":

            # if arg is empty, ask the user
            if arg == "":
                worldUI.writeMsg("Whatchoo wanna drop?", "DIM")

            # if arg isn't empty, check the type
            elif itemInInv != None:

                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )

                # if it's a key item, tell the player not to drop it
                if itemInfo["TYPE"] == "key":
                    worldUI.writeMsg("You don't wanna drop that, Ted. You might need it later!", "YELLOW")

                # if it's equipped, tell the player they need to unequip first
                elif itemInInv in dbs.playerInv["EQUIPPED"]:
                    worldUI.writeMsg("You have to let go of that before you can drop it, Ted!", "CYAN")

                # otherwise drop the item
                else:
                    dbs.updateGround(itemInfo["NAME"], "add") # remove from ground
                    dbs.updateInv(itemInfo["NAME"], "del") # add to inventory
                    worldUI.writeInv()
                    worldUI.writeGround()
                    message = "Ted drops {0}.".format(itemInfo["SHORTDESC"])
                    worldUI.writeMsg(message, "DIM")

            # let the player know if the item can't be found anywhere
            else:
                worldUI.writeMsg("Ted doesn't even have that.", "RED")

        # equip item
        elif cmd == "equip":

            # if arg is empty, ask the player
            if arg == "":
                worldUI.writeMsg("Tryna equip somethin'?", "DIM")

            # if the item is in player inventory
            elif itemInInv != None:

                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )

                # if the item is a weapon and not already equipped, equip it
                if itemInfo["TYPE"] == "weapon" and itemInfo["NAME"] not in dbs.playerInv["EQUIPPED"]:
                    dbs.setWeapon(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    message = "Ted equipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")

                # if the item is an fx and not already equipped, equip it
                elif itemInfo["TYPE"] == "fx" and itemInfo["NAME"] not in dbs.playerInv["EQUIPPED"]:
                    dbs.setFX(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    message = "Ted equipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")

                # otherwise tell the player they can't equip it
                else:
                    worldUI.writeMsg("Ted can't equip that!", "RED")

            # let the player know if the item can't be found anywhere
            else:
                worldUI.writeMsg("Ted doesn't even have that.", "RED")

        # unequip item
        elif cmd == "unequip":

            # if arg is empty, ask the player
            if arg == "":
                worldUI.writeMsg("Whaddya mean, take what off?", "DIM")

            # if the player tries to unequip their fists or nothing, ask them to stop being silly
            elif itemInInv == "Fists" or itemInInv == "noFX":
                worldUI.writeMsg("There's nothing to unequip, ya dangus!", "RED")

            # if the item is in player's inventory
            elif itemInInv != None:

                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )

                # if the item is a weapon and equipped, reset to 'Fists'
                if itemInfo["TYPE"] == "weapon" and itemInfo["NAME"] in dbs.playerInv["EQUIPPED"]:
                    dbs.setWeapon("Fists")
                    worldUI.writeInv()
                    worldUI.writeStats()
                    message = "Ted unequipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")

                # if the item is an fx and equipped, reset to 'noFX'
                elif itemInfo["TYPE"] == "fx" and itemInfo["NAME"] in dbs.playerInv["EQUIPPED"]:
                    dbs.setFX("noFX")
                    worldUI.writeInv()
                    worldUI.writeStats()
                    message = "Ted unequipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")

                # otherwise you can't unequip something that isn't equipped
                else:
                    worldUI.writeMsg("Ted doesn't have that on!", "RED")

            # let the player know if the item isn't found anywhere
            else:
                worldUI.writeMsg("Ted doesn't even have that.", "RED")

        # sell item
        elif cmd == "sell":

            # if the shop doesn't exist, let the player know and return
            if "SHOP" not in dbs.locationInfo:
                worldUI.writeMsg("There's not a shop here to sell to, Ted!", "RED")
                return

            inv = eng.tempInv()

            # if the item is not in player's inventory, tell them
            if itemInInv not in inv:
                worldUI.writeMsg("Ted doesn't even have that to sell!", "RED")

            # if the item is a key item, don't sell it
            elif itemInInv in dbs.playerInv["KEY_ITEMS"]:
                worldUI.writeMsg("Don't sell it, Ted! You might need that later.", "YELLOW")

            # if the item is currently equipped, tell the player to unequip first
            elif itemInInv in dbs.playerInv["EQUIPPED"]:
                worldUI.writeMsg("You've got to unequip it first, Ted.", "CYAN")

            # otherwise sell the item
            else:
                message = eng.itemTransaction(itemInInv, "sell")
                worldUI.writeInv()
                worldUI.writeStats()
                worldUI.writeMsg(message[0], message[1])

        # buy item
        elif cmd == "buy":

            # if the shop doesn't exist, tell the user
            if "SHOP" not in dbs.locationInfo:
                worldUI.writeMsg("There's not a shop here to buy from, Ted!", "RED")
                return

            # if the item isn't in the shop's list, tell the player
            elif itemInShop not in dbs.locationInfo["SHOP"]:
                worldUI.writeMsg("The shopkeep looks confused by that request. I don't think they have it, Ted.", "RED")
                return

            # otherwise buy the item
            else:
                message = eng.itemTransaction(itemInShop, "buy")
                worldUI.writeInv()
                worldUI.writeStats()
                worldUI.writeMsg(message[0], message[1])

        # smoke item
        elif cmd in worldUI.SMOKE_CMDS:

            # if the item is in the player's inventory
            if itemInInv != None:

                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )

                # if the item is not smokeable, tell the player
                if itemInfo["TYPE"] != "smoke":
                    worldUI.writeMsg("You can't {0} that, Ted!".format(cmd), "RED")
                    return

                # if the effect list has 2 items or less, tell the player they can only use it in battle
                elif len(itemInfo["EFFECT"]) <= 2:
                    worldUI.writeMsg("You can only {0} that during a battle, Ted!".format(cmd), "RED")
                    return

                # otherwise, smoke the item
                else:
                    message = eng.useItem(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    worldUI.writeMsg(message[0], message[1])

            # let the player know if the item isn't found anywhere
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")

        # eat item
        elif cmd in worldUI.EAT_CMDS:

            # if the item is in the player's inventory
            if itemInInv != None:

                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )

                # if the type isn't food, don't eat it
                if itemInfo["TYPE"] != "food":
                    worldUI.writeMsg("You can't {0} that, Ted!".format(cmd), "RED")
                    return

                # if the effects list is 2 or less, let the player know they can only use it in battle
                elif len(itemInfo["EFFECT"]) <= 2:
                    worldUI.writeMsg("You can only {0} that during a battle, Ted!".format(cmd), "RED")
                    return

                # otherwise use the item
                else:
                    message = eng.useItem(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    worldUI.writeMsg(message[0], message[1])

            # let the player know if the item isn't found anywhere'
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")

        # drink item
        elif cmd in worldUI.DRINK_CMDS:

            # if the item is in the player's inventory
            if itemInInv != None:

                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )

                # if the type isn't drink, don't drink it
                if itemInfo["TYPE"] != "drink":
                    worldUI.writeMsg("You can't {0} that, Ted!".format(cmd), "RED")
                    return

                # if the effects list is 2 or less, let the player know they can only use it in battle
                elif len(itemInfo["EFFECT"]) <= 2:
                    worldUI.writeMsg("You can only {0} that during a battle, Ted!".format(cmd), "RED")
                    return

                # otherwise drink the item
                else:
                    message = eng.useItem(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    worldUI.writeMsg(message[0], message[1])

            # let the player know if the item isn't found anywhere'
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")

        # snort item
        elif cmd in worldUI.DRUG_CMDS:

            # if the item is in the player's inventory
            if itemInInv != None:

                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )

                # if the type isn't drug, don't snort it
                if itemInfo["TYPE"] != "drug":
                    worldUI.writeMsg("You can't {0} that, Ted!".format(cmd), "RED")
                    return

                # if the effect list is 2 or less, let the player know they can only use it in battle
                elif len(itemInfo["EFFECT"]) <= 2:
                    worldUI.writeMsg("You can only {0} that during a battle, Ted!".format(cmd), "RED")
                    return

                # otherwise snort the item
                else:
                    message = eng.useItem(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    worldUI.writeMsg(message[0], message[1])

            # let the player know if the item isn't found anywhere
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")

        # save
        elif cmd == "save":
            message = dbs.saveGame()
            worldUI.writeMsg(message[0], message[1])

        # help
        elif cmd == "help":
            # TODO create a help window with commands and tips
            worldUI.writeMsg("Sorry, Ted! I can't help you yet, my systems are too fresh.", "RED")

        # exit
        elif cmd == "quit" or cmd == "exit":
            message = dbs.saveGame()
            worldUI.writeMsg(message[0], message[1])
            eng.endGame()

        # catch possible exceptions
        else:
            raise Exception("Command not found in runAction().")

    # a function specifically to use items
    def runUseItem(args):

        # setup common vars
        cmd = args[0]
        inv = eng.tempInv()

        # if 'with' doesn't appear in the command, then do a single item
        try:
            withPos = args.index("with")
        except ValueError:
            if args[1].upper() == "FLOYDS":
                item1 = "FLOYDS"
                item2 = dbs.locationInfo["EVENT_KEYS"][1]
            elif len(args) == 3:
                item1 = eng.getFirstItemMatchingDesc("{0} {1}".format(args[1], args[2]), inv)
                item2 = None
            elif len(args) == 2:
                item1 = eng.getFirstItemMatchingDesc(args[1], inv)
                item2 = None

        # otherwise, concatenate the item names based on where the 'with' command is
        else:
            if withPos == 2 and len(args) == 4:
                item1 = eng.getFirstItemMatchingDesc(args[1], inv)
                item2 = eng.getFirstItemMatchingDesc(args[3], inv)
            elif withPos == 2 and len(args) == 5:
                item1 = eng.getFirstItemMatchingDesc(args[1], inv)
                item2 = eng.getFirstItemMatchingDesc("{0} {1}".format(args[3], args[4]), inv)
            elif withPos == 3 and len(args) == 5:
                item1 = eng.getFirstItemMatchingDesc("{0} {1}".format(args[1], args[2]), inv)
                item2 = eng.getFirstItemMatchingDesc(args[4], inv)
            elif withPos == 3 and len(args) == 6:
                item1 = eng.getFirstItemMatchingDesc("{0} {1}".format(args[1], args[2]), inv)
                item2 = eng.getFirstItemMatchingDesc("{0} {1}".format(args[4], args[5]), inv)
            else:
                worldUI.writeMsg("You gave me too many arguments, Ted! Try that again.", "RED")

        # if the second item is empty and this isn't Ted paying FLOYDS
        if item2 is None and item1 != "FLOYDS":
            # first check if the event needs a second item or not
            if len(dbs.locationInfo["EVENT_KEYS"]) > 1:
                # if it does, check user's inventory for the second item
                for item in dbs.locationInfo["EVENT_KEYS"]:
                    # if the user has it, set True
                    if item in inv:
                        reqs = True
                    # if not, set False
                    else:
                        reqs = False
            # if only one item needed, set True
            else:
                reqs = True

            # if the player has both items in their inventory and they match EVENT_KEYS list
            if item1 in dbs.locationInfo["EVENT_KEYS"] and reqs is True:
                worldUI.clearScreen()
                worldUI.writeMsg("{0} triggered an event!".format(item1), "BRIGHT_YELLOW")
                sleep(1.5)
                msgWin.clear()
                worldUI.writeTimedEvents(4, "key")
                worldUI.updateRoomStatus("SOLVED")
            elif item1 in dbs.locationInfo["EVENT_KEYS"] and reqs is False:
                worldUI.writeMsg("Ted finds a way to use {0} here, but there might be something missing.".format(item1), "DIM_YELLOW")
            else:
                worldUI.writeMsg("Ted pokes and prods the room with {0}, but nothing seems to happen.".format(item1), "DIM_YELLOW")

        # if the second item is empty and Ted is paying FLOYDS
        elif item2 is not None and item1 == "FLOYDS":

            # if the transaction function is successful, run the event
            if dbs.floydsTransaction(item2, "dec"):
                worldUI.clearScreen()
                worldUI.writeMsg("Paying {0} FLOYDS triggered an event!".format(str(item2)), "BRIGHT_YELLOW")
                sleep(1.5)
                msgWin.clear()
                worldUI.writeTimedEvents(4, "key")
                worldUI.updateRoomStatus("SOLVED")
            else:
                worldUI.writeMsg("Ted doesn't have enough FLOYDS for that".format(item1), "DIM_YELLOW")

        # if the second item is not empty, see if this item could be combined with something
        elif item2 is not None:
            # first get a list of all items that have a recipe
            itemsWithPieces = dbs.items.find( { "PIECES": { "$regex": ".*" } } )
            comboExists = False

            # run through the list and check if the item in the command is found anywhere
            for item in itemsWithPieces:
                newItem = item["NAME"]

                # if both the command item and current item in list complete a recipe, run the action to combine
                if item1 and item2 in item["PIECES"]:
                    dbs.updateInv(item1, "del")
                    dbs.updateInv(item2, "del")
                    dbs.updateInv(newItem, "add")
                    comboExists = True
                    worldUI.writeMsg("Ted crafts {0} and {1} into {2}!".format(item1, item2, newItem), "BRIGHT_YELLOW")

            # if no item combination completes a recipe, lte the user know
            if comboExists == False:
                worldUI.writeMsg("I don't think {0} and {1} were meant to be together.".format(item1, item2), "DIM_YELLOW")

        # handle unknown inputs
        else:
            worldUI.writeMsg("I'm not sure what to use, Ted.", "RED")

        # refresh screen info
        worldUI.rewriteScreen()

    def clearScreen():

        # clears content from all sections
        eventWin.clear()
        groundWin.clear()
        dirWin.clear()
        msgWin.clear()

    def rewriteScreen():

        # rewrites current data into their sections
        worldUI.writeInv()
        worldUI.writeStats()
        worldUI.writeGround()
        worldUI.writeDirs()

    # process the raw command received
    def processCmd(userInput):

        # if it's empty, go back to the loop
        if userInput == "" or userInput == None:
            return

        # split command into a list
        args = userInput.split()

        # some terminals + curses gives me a trailing "                  x x " string.
        # try fixing that if it happens. no plans to have a single 'x' as a parameter
        try:
            args.remove("x")
        except ValueError:
            pass

        # if the cmd is 'use', do runUseItem()
        if args[0] in worldUI.USE_CMDS:
            worldUI.runUseItem(args)

        # if the cmd is in ALL_COMMANDS list, setup the arguments
        elif args[0] in worldUI.ALL_COMMANDS:
            if len(args) == 3:
                # if args has 3 items, then the last two should be considered 1 argument
                worldUI.runAction(args[0], "{0} {1}".format(args[1], args[2]))
            elif len(args) == 2:
                # if args has 2 items, then simply pass it on
                worldUI.runAction(args[0], args[1])
            elif len(args) == 1:
                # if args has 1 item, then pass only the cmd
                worldUI.runAction(args[0], None)
            else:
                raise Exception("CMD ERROR: Unexpected number of arguments from user input")

        # if the cmd is a direction, move
        elif args[0] in worldUI.LONG_DIRS or args[0] in worldUI.SHORT_DIRS:
            worldUI.moveDirection(args[0])

        # if anything else, let the player know we can't do anything with it
        else:
            worldUI.writeMsg("I don't recognize that command, Ted.", "RED")
            return

    # wait for user input
    def getCmd():

        inputWin.clear()
        curses.curs_set(2)
        userInput = inputCmd.edit().lower()
        curses.curs_set(0)
        inputWin.clear()
        return userInput

    # define the main world UI screen boundaries
    # TODO center the boundaries if the terminal is larger than our UI
    # TODO resize the terminal if it's smaller than our UI
    def build(stdscr):

        # define globals
        global titleBorder
        global titleWin
        global statsBorder
        global statsWin
        global inputBorder
        global inputWin
        global inputCmd
        global msgBorder
        global msgWin
        global invBorder
        global invWin
        global eventBorder
        global eventWin
        global groundBorder
        global groundWin
        global dirBorder
        global dirWin

        # setup the main window and color dict
        stdscr.clear()
        stdscr.immedok(True)
        eng.setStyles()
        curses.curs_set(0)

        # set max size
        max_x = 110
        max_y = 40
        # TODO get current terminal size
        # TODO set initial height, width, begin_y, begin_x from terminal size
        # TODO define size formulas for every section in a dict?

        # refresh info in memory
        eng.refreshInfo()

        ### Setup Window Dimensions
        ### subwin(height, width, begin_y, begin_x)

        # LOCATION
        # define the border
        titleBorder = stdscr.subwin(3, 80, 0, 1)
        titleBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        titleBorder.immedok(True)
        titleBorder.addstr(0, 68, "[LOCATION]")
        # define the content area
        titleWin = stdscr.subwin(1, 76, 1, 3)
        titleWin.immedok(True)

        # GROUND
        # define the border
        groundBorder = stdscr.subwin(8, 50, 25, 1)
        groundBorder.immedok(True)
        groundBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        groundBorder.addstr(0, 40, "[GROUND]")
        # define the content area
        groundWin = stdscr.subwin(6, 46, 26, 3)
        groundWin.immedok(True)

        # EXITS
        # define the border
        dirBorder = stdscr.subwin(8, 29, 25, 52)
        dirBorder.immedok(True)
        dirBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll)
        dirBorder.addstr(0, 20, "[EXITS]")
        # define the content area
        dirWin = stdscr.subwin(6, 25, 26, 53)
        dirWin.immedok(True)

        # EVENTS / SHOP
        # define the border
        eventBorder = stdscr.subwin(22, 80, 3, 1)
        eventBorder.immedok(True)
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        # define the content area
        eventWin = stdscr.subwin(20, 76, 4, 3)
        eventWin.immedok(True)

        # PROMPT
        # define the border
        inputWin = stdscr.subwin(1, 72, 34, (len(eng.PROMPT) + 3))
        inputWin.immedok(True)
        # define the content area
        rectangle(stdscr, 33, 1, 35, 80)
        inputCmd = Textbox(inputWin, insert_mode=True)
        # place PROMPT in the input window
        stdscr.addstr(34, 3, eng.PROMPT, eng.c["BRIGHT_RED"])

        # MESSAGES
        # define the border
        msgBorder = stdscr.subwin(4, 109, 36, 1)
        msgBorder.immedok(True)
        msgBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        msgBorder.addstr(0, 83, "[MESSAGES]")
        # define the content area
        msgWin = stdscr.subwin(2, 105, 37, 3)
        msgWin.immedok(True)

        # STATS
        # define the border
        statsBorder = stdscr.subwin(9, 28, 0, 82)
        statsBorder.immedok(True)
        statsBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        statsBorder.addstr(0, 2, "[STATS]")
        # define the content area
        statsWin = stdscr.subwin(7, 24, 1, 84)
        statsWin.immedok(True)

        # INVENTORY
        # define the border
        invBorder = stdscr.subwin(27, 28, 9, 82)
        invBorder.immedok(True)
        invBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        invBorder.addstr(0, 2, "[INVENTORY]")
        # define content area
        invWin = stdscr.subwin(25, 24, 10, 84)
        invWin.immedok(True)

        # run the world command loop
        worldUI.displayWorld()

    # use curses wrapper in case of uncaught exceptions
    def start():
        curses.wrapper(worldUI.build)
