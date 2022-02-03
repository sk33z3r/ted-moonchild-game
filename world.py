import curses
from textwrap import wrap
from time import sleep
from curses.textpad import Textbox, rectangle
from random import randrange, choice
import engine as eng
import database as dbs
from battle import battleUI

class worldUI():

    # updates room visited and solved status
    def updateRoomStatus(what):

        # check if we're in the winnie or not
        if dbs.ROOM.lower() in [ "winnibego", "space" ] or dbs.ROOM.endswith("Sector"):
            space = True
        else:
            space = False

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
                    if space is True:
                        dbs.player.update_one( { "SECTION": "inventory" }, { "$push": { "WINNIE" : item } } )
                    else:
                        dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$push": { "GROUND" : item } } )

            # remove an item from the ground if specified
            if "DEL_GROUND" in dbs.locationInfo:
                for item in dbs.locationInfo["DEL_GROUND"]:
                    if space is True:
                        dbs.player.update_one( { "SECTION": "inventory" }, { "$pull": { "WINNIE" : item } } )
                    else:
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
                eventWin.addstr(20, 65, ">>>>>", eng.c["BLINK_BRIGHT_YELLOW"])
                sleep(speed)
                y = 1
                eventWin.clear()
                sleep(0.5)

            # get event text and wrap the text to fit inside the window
            eventString = '\n'.join(wrap(events[str(l)][1], 75))

            # get event's text style
            stringStyle = events[str(l)][0]

            # display the text
            eventWin.addstr(y, 0, eventString.format(dbs.SECTOR), eng.c[stringStyle])

            # move to new position
            l += 1

            # add more newlines if text will be wrapped multiple times in the window
            if len(eventString) < 75:
                y += 2
                sleep(speed)
            if len(eventString) > 75 and len(eventString) < 150:
                y += 3
                sleep((speed * 2))
            elif len(eventString) > 150 and len(eventString) < 225:
                y += 4
                sleep((speed * 3))
            elif len(eventString) > 225 and len(eventString) < 300:
                y += 5
                sleep((speed * 4))

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

                # first give a visual warning
                eventWin.addstr(20, 65, ">>>>>", eng.c["BLINK_BRIGHT_YELLOW"])
                sleep(speed)

                # then reset
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
                sleep((speed * 2))
            elif len(eventString) > 150 and len(eventString) < 225:
                y += 4
                sleep((speed * 3))
            elif len(eventString) > 225 and len(eventString) < 300:
                y += 5
                sleep((speed * 4))

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
        eventBorder.addstr(0, 65, " ROOM EVENTS ", eng.c["DIM"])
        worldUI.clearScreen()

        # if this is to be the Winnibego
        if where == "winnibego":

            # setup DOWN direction
            dbs.locations.update_one( { "NAME": "Winnibego" }, { "$set": { dbs.locationInfo["PLANET_DIRS"][dbs.PLANET][0] : dbs.locationInfo["PLANET_DIRS"][dbs.PLANET][1] } } )
            eng.refreshInfo()

            # setup the title window
            titleWin.clear()
            title = "{0}, Planet {1}: {2}".format(dbs.SECTOR, dbs.PLANET, dbs.ROOM)
            titleWin.addstr(0, 0, title, eng.c["BRIGHT"])

            # display the winnibego room events based on triggers
            if dbs.locationInfo["VISITED"] == 0:
                worldUI.writeTimedEvents(eng.GAME_SPEED, "first")
                worldUI.updateRoomStatus("VISITED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 0:
                worldUI.writeStaticEvents("unsolved")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == True:
                worldUI.writeTimedEvents(eng.GAME_SPEED, "key")
                worldUI.updateRoomStatus("SOLVED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == False:
                events = dbs.locationInfo["SOLVED_EVENTS"]
                eventString = '\n'.join(wrap(events[str(0)][1], 75)).format(dbs.PLANET)
                stringStyle = events[str(0)][0]
                eventWin.addstr(1, 0, eventString, eng.c[stringStyle])

        # if this is to be Space
        elif where == "space":

            # get a list of directions that need to be displayed for this sector
            dirList = dbs.locationInfo["SECTOR_DIRS"][room]

            # for each direction, check and remove any existing directions in the db
            for direction in eng.LONG_DIRS:
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
            worldUI.writeSpaceEvents((eng.GAME_SPEED), room)
            worldUI.updateSectorStatus(room)

        # default to being a Planet
        elif where == "planet":

            # refresh new data
            eng.refreshInfo()

            # setup the title window
            titleWin.clear()
            title = "{0}, Planet {1}: {2}".format(dbs.SECTOR, dbs.PLANET, dbs.ROOM)
            titleWin.addstr(0, 0, title, eng.c["BRIGHT"])

            # display a normal room based on triggers
            if dbs.locationInfo["VISITED"] == 0:
                worldUI.writeTimedEvents(eng.GAME_SPEED, "first")
                worldUI.updateRoomStatus("VISITED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 0:
                worldUI.writeStaticEvents("unsolved")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == True:
                worldUI.writeTimedEvents(eng.GAME_SPEED, "key")
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
        eventBorder.addstr(0, 66, " SHOP ITEMS ", eng.c["DIM"])
        eventWin.clear()

        # get a list of items in the current shop
        shopItems = dbs.locationInfo["SHOP"]

        # set the starting line for text
        y = 1

        # for each item in the rooms SHOP list
        for item in shopItems:

            beginning = y

            # set some vars
            itemInfo = dbs.items.find_one( { "NAME": item } )
            nameString = "{0: <14}".format(itemInfo["NAME"])
            effectString = "{0: <14}".format(eng.getEffectString(item))
            floydsString = "{0: <7} {1: <6}".format("FLOYDS:", str(itemInfo["VALUE"]))

            # print the name in bold
            eventWin.addstr(y, 0, nameString, eng.c["DIM"])
            y += 1
            eventWin.addstr(y, 0, effectString, eng.c["DIM_YELLOW"])
            y += 1
            eventWin.addstr(y, 0, floydsString, eng.c["DIM_GREEN"])

            # move back to first line
            y = beginning

            # wrap the description text to fit
            itemDesc = wrap(itemInfo["LONGDESC"], 60)

            # wrap the LONGDESC to fit the window before displaying it
            l = 0
            while l < len(itemDesc):
                eventWin.addstr(y, 15, "{0: <60}".format(itemDesc[l]), eng.c["DIM"])
                y += 1
                l += 1

            # add empty lines appropriately if the above string is long enough
            if len(itemInfo["LONGDESC"]) > 180:
                y += 3
            else:
                y += 2

    # function to write the HELP screen in the EVENTS section
    def writeHelp():

        # clear the EVENTS section first
        eventBorder.clear()
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        eventBorder.addstr(0, 72, " HELP ", eng.c["DIM"])
        eventWin.clear()

        # print the help text to screen
        eventWin.addstr(1, 0, "{0: ^76}".format("TED MOONCHILD AND THE ROADIES IN SPACE: THE COMMANDS"), eng.c["BRIGHT_YELLOW"])
        eventWin.addstr(3, 0, "{0: ^76}".format("CHANGE ROOMS BY TYPING A DIRECTION, OR THE FIRST LETTER OF A DIRECTION"), eng.c["REVERSE_DIM_MAGENTA"])
        eventWin.addstr(4, 0, "{0: ^76}".format("TYPICAL COMMAND USAGE: [command] [item/room/direction]"), eng.c["REVERSE_DIM_MAGENTA"])

        eventWin.addstr(6, 0, "{0: <38} {1: <38}".format("BASIC Commands", "SHOP Commands"), eng.c["MAGENTA"])

        eventWin.addstr(7, 3, "{0: >4}:".format("save"))
        eventWin.addstr(8, 3, "{0: >4}:".format("quit"))
        eventWin.addstr(9, 3, "{0: >4}:".format("help"))
        eventWin.addstr(7, 41, "{0: >4}:".format("shop"))
        eventWin.addstr(8, 41, "{0: >4}:".format("sell"))
        eventWin.addstr(9, 41, "{0: >4}:".format("buy"))

        eventWin.addstr(7, 9, "{0: <24}".format("save progress"), eng.c["DIM"])
        eventWin.addstr(8, 9, "{0: <24}".format("save game and exit"), eng.c["DIM"])
        eventWin.addstr(9, 9, "{0: <24}".format("this help message"), eng.c["DIM"])
        eventWin.addstr(7, 47, "{0: <24}".format("display the room's stock"), eng.c["DIM"])
        eventWin.addstr(8, 47, "{0: <24}".format("sell an item"), eng.c["DIM"])
        eventWin.addstr(9, 47, "{0: <24}".format("buy an item"), eng.c["DIM"])

        eventWin.addstr(11, 0, "{0: <38} {1: <38}".format("ITEM Commands", "CONSUME Commands"), eng.c["MAGENTA"])

        eventWin.addstr(12, 0, "{0: >7}:".format("look"))
        eventWin.addstr(13, 0, "{0: >7}:".format("take"))
        eventWin.addstr(14, 0, "{0: >7}:".format("drop"))
        eventWin.addstr(15, 0, "{0: >7}:".format("equip"))
        eventWin.addstr(16, 0, "{0: >7}:".format("unequip"))
        eventWin.addstr(17, 0, "{0: >7}:".format("use"))
        eventWin.addstr(12, 40, "{0: >5}:".format("eat"))
        eventWin.addstr(13, 40, "{0: >5}:".format("drink"))
        eventWin.addstr(14, 40, "{0: >5}:".format("smoke"))
        eventWin.addstr(15, 40, "{0: >5}:".format("snort"))

        eventWin.addstr(12, 9, "look at an item or the room", eng.c["DIM"])
        eventWin.addstr(13, 9, "take an item", eng.c["DIM"])
        eventWin.addstr(14, 9, "drop an item on the ground", eng.c["DIM"])
        eventWin.addstr(15, 9, "equip an item", eng.c["DIM"])
        eventWin.addstr(16, 9, "remove an equipped item", eng.c["DIM"])
        eventWin.addstr(17, 9, "use a key item", eng.c["DIM"])
        eventWin.addstr(12, 47, "consume food for effects", eng.c["DIM"])
        eventWin.addstr(13, 47, "drink for effects", eng.c["DIM"])
        eventWin.addstr(14, 47, "smoke for effects", eng.c["DIM"])
        eventWin.addstr(15, 47, "consume drugs for effects", eng.c["DIM"])

        eventWin.addstr(19, 0, "{0: ^36}".format("Some items can be combined:"), eng.c["DIM_YELLOW"])
        eventWin.addstr(20, 0, "{0: ^36}".format("use [item] with [item]"), eng.c["DIM_YELLOW"])

        eventWin.addstr(18, 37, "{0: ^38}".format("There are lots of alternate words"), eng.c["DIM_GREEN"])
        eventWin.addstr(19, 37, "{0: ^38}".format("for consuming items. Try different"), eng.c["DIM_GREEN"])
        eventWin.addstr(20, 37, "{0: ^38}".format("words with different items!"), eng.c["DIM_GREEN"])

    # function to write the GROUND section
    def writeGround(where):

        # set the list of items on the ground
        # if this is the winnie, we need to grab special inventory
        if where.lower() in [ "winnibego", "space" ] or where.endswith("Sector"):
            groundList = list(dbs.playerInv["WINNIE"])

        # otherwise get the room's ground items
        else:
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

            if dbs.ROOM in [ "Winnibego", "Space" ]:
                count = len(groundList)
                cap = 10
                capacity = " STORAGE CAPACITY: {0}/{1} ".format(count, cap)
                x = 48 - len(capacity)

                groundBorder.addstr(10, x, capacity, eng.c["DIM"])

            # set starting rows and columns in the window
            y, x, l = 1, 1, 0

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
        exitWin.clear()

        # set the starting line in the section
        y = 1

        # run through the list of directions
        for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):

            # for each one that matches, print the info from db
            if direction in list(dbs.locationInfo):
                dirString = "{0}: {1}".format(direction, dbs.locationInfo[direction])
                exitWin.addstr(y, 1, dirString, eng.c["DIM"])
                y += 1

    # function to parse which location to write and how
    def writeLocation(room, what, key):

        # clear the event window
        eventWin.clear()

        # make sure GROUND and EXITS are still visible
        worldUI.writeGround(room)
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

        # wrap the message text
        msg = "\n".join(wrap(msg, 100))

        # display the message
        msgWin.addstr(0, 0, msg, eng.c[style])

    # funcion to clear and write the STATS section
    def writeChar():

        # clear and refresh info
        charWin.clear()
        eng.refreshInfo()

        charWin.addstr(7, 0, "{0: ^28}".format("EQUIPPED"), eng.c["REVERSE_DIM_CYAN"])

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
        stat1 = "{0: >10} {hp: >6} / {hpmax: <6}".format("HEALTH:", **stats)
        stat2 = "{0: >10} {mp: >6} / {mpmax: <6}".format("MOJO:", **stats)
        stat3 = "{0: >10} {lvl: ^15}".format("LEVEL:", **stats)
        stat4 = "{0: >10} {xp: >6} / {lvlReq: <6}".format("TO NEXT:", **stats)
        stat5 = "{0: >10} {floyds: ^15}".format("FLOYDS:", **stats)

        # print the strings to the stats wndow
        charWin.addstr(1, 0, stat1, eng.c["RED"])
        charWin.addstr(2, 0, stat2, eng.c["BLUE"])
        charWin.addstr(3, 0, stat3, eng.c["YELLOW"])
        charWin.addstr(4, 0, stat4, eng.c["YELLOW"])
        charWin.addstr(5, 0, stat5, eng.c["GREEN"])

        # get and sort all item lists individually
        i = list(dbs.playerInv["ITEMS"])
        k = list(dbs.playerInv["KEY_ITEMS"])

        count = len(i)
        cap = dbs.playerInv["CAP"]

        headerString = "INVENTORY ({0}/{1})".format(count, cap)
        charWin.addstr(13, 0, "{0: ^28}".format(headerString), eng.c["REVERSE_DIM"])
        charWin.addstr(14, 0, "{0: >4} {1: <14} {2: <8}".format('#', 'ITEM', 'EFFECT'), eng.c["REVERSE_DIM"])

        # sort the lists
        i = sorted(i)
        k = sorted(k)

        # if there are no items, print a message
        if len(i) == 0 and len(k) == 0:
            return

        # get a count of each item in the ITEMS list only
        itemCount = {}
        for item in i:
            if item in list(itemCount.keys()):
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # set starting line in the window
        s = 16

        # print items from ITEMS with their item count
        if len(i) != 0:
            for item in set(i):
                effectString = eng.getEffectString(item)
                itemString = "{0: >3}x {1: <14} {2: <8}".format(str(itemCount[item]), item, effectString)
                charWin.addstr(s, 0, itemString)
                s += 1
            s += 1

        # print items from KEY_ITEMS
        if len(k) != 0:
            charWin.addstr(s, 0, "{0: ^28}".format("KEY ITEMS"), eng.c["REVERSE_DIM_YELLOW"])
            s += 2
            for item in set(k):
                charWin.addstr(s, 2, item, eng.c["YELLOW"])
                s += 1

        # setup strings
        headString = "{0: >9} {1: ^15}".format("HEAD:", dbs.playerEquip["HEAD"])
        instString = "{0: >9} {1: ^15}".format("INST:", dbs.playerEquip["INSTRUMENT"])
        fxString = "{0: >9} {1: ^15}".format("FX:", dbs.playerEquip["FX"])

        # display the strings
        charWin.addstr(9, 0, headString, eng.c["CYAN"])
        charWin.addstr(10, 0, instString, eng.c["CYAN"])
        charWin.addstr(11, 0, fxString, eng.c["CYAN"])

    # function to move the player from room to room
    def moveDirection(direction):

        # setup vars and screen
        upper = direction.upper()
        lower = direction.lower()
        combatCheck = randrange(1, 50)
        msgWin.clear()

        # link short names to long names
        if lower in eng.SHORT_DIRS:
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
            dbs.locations.update_one( { "NAME": "Winnibego" }, { "$set": { "PLANET": dbs.PLANET } } )
            dbs.locations.update_one( { "NAME": "Space" }, { "$set": { "SECTOR": dbs.SECTOR } } )

            # set the new location
            if dbs.locationInfo[upper].endswith("Sector"):
                dbs.setSpaceLocation(dbs.locationInfo[upper])
            else:
                dbs.setLocation(dbs.locationInfo[upper])

            # if combat should happen, make it happen
            if combatCheck > 40 and dbs.locationInfo["BATTLES"] is True:

                battleUI.build(screen)
                worldUI.rewriteUI()
                worldUI.writeLocation(dbs.locationInfo["NAME"], "room", False)

            # otherwise move to the new room
            else:
                worldUI.writeLocation(dbs.locationInfo["NAME"], "room", False)

        # let the player know if the direction can't be found
        else:
            worldUI.writeMsg("Ted can't walk through walls.", "RED")

    # function specifically to parse commands and run their relevant functions
    def runAction(cmd, arg):

        # setup the environment
        inv, count = eng.tempInv()
        itemInInv = eng.getFirstItemMatchingDesc(arg, inv)

        # check if we're in the winnie or not
        if dbs.ROOM.lower() in [ "winnibego", "space" ] or dbs.ROOM.endswith("Sector"):
            itemOnGround = eng.getFirstItemMatchingDesc(arg, dbs.playerInv["WINNIE"])
        else:
            itemOnGround = eng.getFirstItemMatchingDesc(arg, dbs.locationInfo["GROUND"])

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

        # look (room|item|direction)
        elif cmd == "look":

            # get a list of room names from the available exits in this room
            exits = {}
            for direction in eng.LONG_DIRS:
                try:
                    exits[dbs.locationInfo[direction.upper()].lower()] = direction.upper()
                except:
                    pass

            # with no specifics given, assume the player wants to refresh the room event
            if arg == None or arg in eng.ROOM_WORDS:
                worldUI.writeLocation(dbs.ROOM, "room", False)

            # if the arg is a name in available exits
            elif arg in exits.keys():
                roomInDirection = dbs.locations.find_one( { "NAME": dbs.locationInfo[exits[arg]] } )
                worldUI.writeMsg(roomInDirection["SHORTDESC"][1], roomInDirection["SHORTDESC"][0])

            # if the arg is a direction
            elif arg in eng.LONG_DIRS or arg in eng.SHORT_DIRS:

                # link short names to long names
                if arg in eng.SHORT_DIRS:
                    if arg == "n":
                        upper = "NORTH"
                    elif arg == "s":
                        upper = "SOUTH"
                    elif arg == "e":
                        upper = "EAST"
                    elif arg == "w":
                        upper = "WEST"
                    elif arg == "u":
                        upper = "UP"
                    elif arg == "d":
                        upper = "DOWN"
                else:
                    # if there isn't a matching shortname, then make the arg uppercase
                    upper = arg.upper()

                # check if the direction exists in the current room
                if upper in dbs.locationInfo:
                    roomInDirection = dbs.locations.find_one( { "NAME": dbs.locationInfo[upper] } )
                    worldUI.writeMsg(roomInDirection["SHORTDESC"][1], roomInDirection["SHORTDESC"][0])

                # if it doesn't print something whimsical
                else:

                    # list of responses
                    msgList = [
                        "Ted cops a feel on the wall, hoping for a hidden latch or some secret button. All he finds is disappointment.",
                        "Ted stares at nothing for a while.",
                        "I don't think there's anything to look at in that direction, Ted.",
                        "Why don't you take a look somewhere else, Ted?",
                        "Oh, look! Nothing."
                    ]

                    # pick a response randomly and display it
                    message = choice(msgList)
                    worldUI.writeMsg(message, "RED")

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

                # if the player is already carrying too much, let them know
                elif count == dbs.playerInv["CAP"]:
                    worldUI.writeMsg("Ted is already carrying too much, you need to drop something first!", "RED")

                # otherwise take the item
                elif itemInfo["TAKEABLE"] == True:
                    dbs.updateGround(itemInfo["NAME"], "del") # remove from ground
                    dbs.updateInv(itemInfo["NAME"], "add") # add to inventory
                    worldUI.writeChar()
                    worldUI.writeGround(dbs.locationInfo["NAME"])
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
                    return

                # if it's equipped, tell the player they need to unequip first
                elif itemInInv in dbs.playerInv["EQUIPPED"]:
                    worldUI.writeMsg("You have to let go of that before you can drop it, Ted!", "CYAN")
                    return

                elif dbs.ROOM in [ "Winnibego", "Space" ]:
                    if len(list(dbs.playerInv["WINNIE"])) == 10:
                        worldUI.writeMsg("There's too much shit in the Winnie, Ted. Clean this place up, will ya!", "RED")
                        return

                elif len(list(dbs.locationInfo["GROUND"])) == 10:
                    worldUI.writeMsg("There's too many items on the ground, Ted.", "RED")
                    return

                # drop the item
                dbs.updateGround(itemInfo["NAME"], "add") # remove from ground
                dbs.updateInv(itemInfo["NAME"], "del") # add to inventory
                worldUI.writeChar()
                worldUI.writeGround(dbs.locationInfo["NAME"])
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

                # if the item is an instrument and not already equipped, equip it
                if itemInfo["TYPE"] == "instrument" and itemInfo["NAME"] not in dbs.playerInv["EQUIPPED"]:
                    dbs.setInstrument(itemInfo["NAME"])
                    worldUI.writeChar()
                    message = "Ted equipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")

                # if the item is an fx and not already equipped, equip it
                elif itemInfo["TYPE"] == "fx" and itemInfo["NAME"] not in dbs.playerInv["EQUIPPED"]:
                    dbs.setFX(itemInfo["NAME"])
                    worldUI.writeChar()
                    message = "Ted equipped {0}.".format(itemInfo["SHORTDESC"])
                    worldUI.writeMsg(message, "CYAN")

                # if the item is head gear and not already equipped, equip it
                elif itemInfo["TYPE"] == "head" and itemInfo["NAME"] not in dbs.playerInv["EQUIPPED"]:
                    dbs.setHead(itemInfo["NAME"])
                    worldUI.writeChar()
                    message = "Ted equipped {0}.".format(itemInfo["SHORTDESC"])
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

                # if the player is already carrying too much, let them know
                if count == dbs.playerInv["CAP"]:
                    worldUI.writeMsg("Ted is carrying too much, you need to drop something before you can unequip this!", "RED")

                # if the item is an instrument and equipped, reset to 'Fists'
                elif itemInfo["TYPE"] == "instrument" and itemInfo["NAME"] in dbs.playerInv["EQUIPPED"]:
                    dbs.setInstrument("Fists")
                    worldUI.writeChar()
                    message = "Ted unequipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")

                # if the item is an fx and equipped, reset to 'noFX'
                elif itemInfo["TYPE"] == "fx" and itemInfo["NAME"] in dbs.playerInv["EQUIPPED"]:
                    dbs.setFX("noFX")
                    worldUI.writeChar()
                    message = "Ted unequipped {0}.".format(itemInfo["SHORTDESC"])
                    worldUI.writeMsg(message, "CYAN")

                # if the item is head gear and equipped, reset to 'Hair'
                elif itemInfo["TYPE"] == "head" and itemInfo["NAME"] in dbs.playerInv["EQUIPPED"]:
                    dbs.setHead("Hair")
                    worldUI.writeChar()
                    message = "Ted unequipped {0}.".format(itemInfo["SHORTDESC"])
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

            inv, count = eng.tempInv()

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
                worldUI.writeChar()
                worldUI.writeMsg(message[0], message[1])

        # buy item
        elif cmd == "buy":

            inv, count = eng.tempInv()

            # if the shop doesn't exist, tell the user
            if "SHOP" not in dbs.locationInfo:
                worldUI.writeMsg("There's not a shop here to buy from, Ted!", "RED")
                return

            # if the item isn't in the shop's list, tell the player
            elif itemInShop not in dbs.locationInfo["SHOP"]:
                worldUI.writeMsg("The shopkeep looks confused by that request. I don't think they have it, Ted.", "RED")
                return

            elif count == dbs.playerInv["CAP"]:
                worldUI.writeMsg("You have too much shit, already Ted! Sell or drop something first.", "RED")
                return

            # otherwise buy the item
            else:
                message = eng.itemTransaction(itemInShop, "buy")
                worldUI.writeChar()
                worldUI.writeMsg(message[0], message[1])

        # smoke item
        elif cmd in eng.SMOKE_CMDS:

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
                    worldUI.writeChar()
                    worldUI.writeMsg(message[0], message[1])

            # let the player know if the item isn't found anywhere
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")

        # eat item
        elif cmd in eng.EAT_CMDS:

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
                    worldUI.writeChar()
                    worldUI.writeMsg(message[0], message[1])

            # let the player know if the item isn't found anywhere'
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")

        # drink item
        elif cmd in eng.DRINK_CMDS:

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
                    worldUI.writeChar()
                    worldUI.writeMsg(message[0], message[1])

            # let the player know if the item isn't found anywhere'
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")

        # snort item
        elif cmd in eng.DRUG_CMDS:

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
                    worldUI.writeChar()
                    worldUI.writeMsg(message[0], message[1])

            # let the player know if the item isn't found anywhere
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")

        # save
        elif cmd == "save":
            message = dbs.saveGame()
            worldUI.writeMsg(message[0], message[1])

        # battle
        elif cmd == "fight" or cmd == "battle":

            global exit_battle

            exit_battle = battleUI.build(screen)

        # help
        elif cmd == "help":
            worldUI.writeHelp()

        # exit
        elif cmd == "quit" or cmd == "exit":

            global exit_game

            message = dbs.saveGame()
            worldUI.writeMsg(message[0], message[1])
            sleep(2)
            worldUI.clearAllScreens()
            exit_game = True

        # catch possible exceptions
        else:
            raise Exception("Command not found in runAction().")

    # a function specifically to use items
    def runUseItem(args):

        # setup common vars
        cmd = args[0]
        inv, count = eng.tempInv()

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
                worldUI.writeTimedEvents(eng.GAME_SPEED, "key")
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
                worldUI.writeTimedEvents(eng.GAME_SPEED, "key")
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
        exitWin.clear()
        msgWin.clear()

    def rewriteScreen():

        # rewrites current data into their sections
        worldUI.writeChar()
        worldUI.writeGround(dbs.locationInfo["NAME"])
        worldUI.writeDirs()

    # function to initialize the UI and get user input
    def displayWorld():

        global exit_game
        global exit_battle

        # write all data to the screen
        worldUI.writeChar()
        worldUI.writeMsg("", "DIM")
        worldUI.writeLocation(dbs.ROOM, "room", False)

        # set initial state of when to change to each UI
        exit_battle = False
        exit_game = False

        # main command input loop
        while exit_game is False:
            userInput = worldUI.getCmd()
            worldUI.processCmd(userInput)

            # if we just exited a battle, we need to redraw the screen sections
            if exit_battle is True:

                # write all data to the screen
                worldUI.rewriteUI()
                worldUI.writeChar()
                worldUI.writeMsg("", "DIM")
                worldUI.writeLocation(dbs.ROOM, "room", False)

                # reset battle status
                exit_battle = False

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
        if args[0] in eng.USE_CMDS:
            worldUI.runUseItem(args)

        # if the cmd is in ALL_COMMANDS list, setup the arguments
        elif args[0] in eng.ALL_COMMANDS:
            if len(args) == 4:
                # if args has 3 items, then the last two should be considered 1 argument
                worldUI.runAction(args[0], "{0} {1} {2}".format(args[1], args[2], args[3]))
            elif len(args) == 3:
                # if args has 3 items, then the last two should be considered 1 argument
                worldUI.runAction(args[0], "{0} {1}".format(args[1], args[2]))
            elif len(args) == 2:
                # if args has 2 items, then simply pass it on
                worldUI.runAction(args[0], args[1])
            elif len(args) == 1:
                # if args has 1 item, then pass only the cmd
                worldUI.runAction(args[0], None)
            else:
                worldUI.writeMsg("You entered too many words for that item, Ted. Try again.", "RED")
                return

        # if the cmd is a direction, move
        elif args[0] in eng.LONG_DIRS or args[0] in eng.SHORT_DIRS or args[0] in eng.MOVE_CMDS:

            # i don't want to discourage trying new words to solve puzzles, so if the player enters "move direction",
            # just ignore the first command and pass the direction along
            if args[0] in eng.MOVE_CMDS:
                worldUI.moveDirection(args[1])
            else:
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

    # function to clear all screens
    def clearAllScreens():

        screen.clear()
        titleBorder.clear()
        titleWin.clear()
        charBorder.clear()
        charWin.clear()
        inputWin.clear()
        msgBorder.clear()
        msgWin.clear()
        eventBorder.clear()
        eventWin.clear()
        groundBorder.clear()
        groundWin.clear()
        exitBorder.clear()
        exitWin.clear()

    def rewriteUI():

        # refresh info in memory
        eng.refreshInfo()

        # LOCATION
        titleBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        titleBorder.addstr(0, 68, " LOCATION ", eng.c["DIM"])

        # GROUND
        groundBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        groundBorder.addstr(0, 40, " GROUND ", eng.c["DIM"])

        # EXITS
        exitBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll)
        exitBorder.addstr(0, 21, " EXITS ", eng.c["DIM"])

        # EVENTS / SHOP
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)

        # PROMPT
        # define the border
        rectangle(screen, eng.worldInputDims["border"][0], eng.worldInputDims["border"][1], eng.worldInputDims["border"][2], eng.worldInputDims["border"][3])
        # place PROMPT in the input window
        screen.addstr(eng.worldInputDims["prompt"][0], eng.worldInputDims["prompt"][1], eng.PROMPT, eng.c["RED"])

        # MESSAGES
        msgBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        msgBorder.addstr(0, 83, " MESSAGES ", eng.c["DIM"])

        # CHARACTER
        charBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        charBorder.addstr(0, 2, " TED MOONCHILD ", eng.c["DIM"])

    # define the main world UI screen boundaries
    def build(stdscr):

        # define globals
        global titleBorder
        global titleWin
        global charBorder
        global charWin
        global inputWin
        global inputCmd
        global msgBorder
        global msgWin
        global eventBorder
        global eventWin
        global groundBorder
        global groundWin
        global exitBorder
        global exitWin
        global begin_y
        global begin_x
        global max_x
        global max_y
        global screen
        global invStart

        screen = stdscr

        # define max size
        max_x = 111
        max_y = 43

        # get current terminal size and setup UI positions
        height, width = stdscr.getmaxyx()
        begin_y, begin_x = eng.calculateWindows(height, width, max_y, max_x, "world")

        # refresh info in memory
        eng.refreshInfo()

        # setup the main window and color dict
        stdscr.clear()
        stdscr.immedok(True)
        eng.setStyles()
        curses.curs_set(0)

        # LOCATION
        # define the border
        titleBorder = stdscr.subwin(eng.worldTitleDims["border"][0], eng.worldTitleDims["border"][1], eng.worldTitleDims["border"][2], eng.worldTitleDims["border"][3])
        titleBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        titleBorder.immedok(True)
        titleBorder.addstr(0, 68, " LOCATION ", eng.c["DIM"])
        # define the content area
        titleWin = stdscr.subwin(eng.worldTitleDims["content"][0], eng.worldTitleDims["content"][1], eng.worldTitleDims["content"][2], eng.worldTitleDims["content"][3])
        titleWin.immedok(True)

        # GROUND
        # define the border
        groundBorder = stdscr.subwin(eng.worldGroundDims["border"][0], eng.worldGroundDims["border"][1], eng.worldGroundDims["border"][2], eng.worldGroundDims["border"][3])
        groundBorder.immedok(True)
        groundBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        groundBorder.addstr(0, 40, " GROUND ", eng.c["DIM"])
        # define the content area
        groundWin = stdscr.subwin(eng.worldGroundDims["content"][0], eng.worldGroundDims["content"][1], eng.worldGroundDims["content"][2], eng.worldGroundDims["content"][3])
        groundWin.immedok(True)

        # EXITS
        # define the border
        exitBorder = stdscr.subwin(eng.worldExitDims["border"][0], eng.worldExitDims["border"][1], eng.worldExitDims["border"][2], eng.worldExitDims["border"][3])
        exitBorder.immedok(True)
        exitBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll)
        exitBorder.addstr(0, 21, " EXITS ", eng.c["DIM"])
        # define the content area
        exitWin = stdscr.subwin(eng.worldExitDims["content"][0], eng.worldExitDims["content"][1], eng.worldExitDims["content"][2], eng.worldExitDims["content"][3])
        exitWin.immedok(True)

        # EVENTS / SHOP
        # define the border
        eventBorder = stdscr.subwin(eng.worldEventDims["border"][0], eng.worldEventDims["border"][1], eng.worldEventDims["border"][2], eng.worldEventDims["border"][3])
        eventBorder.immedok(True)
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        # define the content area
        eventWin = stdscr.subwin(eng.worldEventDims["content"][0], eng.worldEventDims["content"][1], eng.worldEventDims["content"][2], eng.worldEventDims["content"][3])
        eventWin.immedok(True)

        # PROMPT
        # define the border
        rectangle(stdscr, eng.worldInputDims["border"][0], eng.worldInputDims["border"][1], eng.worldInputDims["border"][2], eng.worldInputDims["border"][3])
        # define the content area
        inputWin = stdscr.subwin(eng.worldInputDims["content"][0], eng.worldInputDims["content"][1], eng.worldInputDims["content"][2], eng.worldInputDims["content"][3])
        inputWin.immedok(True)
        inputCmd = Textbox(inputWin, insert_mode=True)
        # place PROMPT in the input window
        stdscr.addstr(eng.worldInputDims["prompt"][0], eng.worldInputDims["prompt"][1], eng.PROMPT, eng.c["RED"])

        # MESSAGES
        # define the border
        msgBorder = stdscr.subwin(eng.worldMsgDims["border"][0], eng.worldMsgDims["border"][1], eng.worldMsgDims["border"][2], eng.worldMsgDims["border"][3])
        msgBorder.immedok(True)
        msgBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        msgBorder.addstr(0, 83, " MESSAGES ", eng.c["DIM"])
        # define the content area
        msgWin = stdscr.subwin(eng.worldMsgDims["content"][0], eng.worldMsgDims["content"][1], eng.worldMsgDims["content"][2], eng.worldMsgDims["content"][3])
        msgWin.immedok(True)

        # CHARACTER
        # define the border
        charBorder = stdscr.subwin(eng.worldCharDims["border"][0], eng.worldCharDims["border"][1], eng.worldCharDims["border"][2], eng.worldCharDims["border"][3])
        charBorder.immedok(True)
        charBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        charBorder.addstr(0, 2, " TED MOONCHILD ", eng.c["DIM"])
        invStart = 22
        # define the content area
        charWin = stdscr.subwin(eng.worldCharDims["content"][0], eng.worldCharDims["content"][1], eng.worldCharDims["content"][2], eng.worldCharDims["content"][3])
        charWin.immedok(True)

        # run the world command loop
        worldUI.displayWorld()
