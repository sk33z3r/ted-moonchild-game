import curses, natsort, time, textwrap, random
from curses.textpad import Textbox, rectangle
import engine as eng
import database as dbs

class worldUI():

    BASE_COMMANDS = [ "save", "shop", "look", "take", "drop", "sell", "buy", "equip", "unequip", "quit", "exit", "help", "use" ]
    EAT_CMDS = [ "eat", "gobble", "consume" ]
    DRINK_CMDS = [ "swallow", "gulp", "slurp", "drink" ]
    SMOKE_CMDS = [ "smoke", "toke", "inhale" ]
    DRUG_CMDS = [ "swallow", "snort", "lick" ]
    ALL_COMMANDS = BASE_COMMANDS + EAT_CMDS + DRINK_CMDS + SMOKE_CMDS + DRUG_CMDS
    LONG_DIRS = [ "north", "south", "east", "west", "up", "down" ]
    SHORT_DIRS = [ "n", "s", "e", "w", "u", "d" ]
    ROOM_WORDS = [ "here", "room", "around", "ground", "there", "floor", "area" ]

    def updateRoomStatus(what):
        if what == "VISITED":
            status = dbs.locationInfo["VISITED"]
            dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$set": { "VISITED": 1 } } )
        elif what == "SOLVED":
            status = dbs.locationInfo["SOLVED"]
            dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$set": { "SOLVED": 1 } } )
            if "ADD_GROUND" in dbs.locationInfo:
                for item in dbs.locationInfo["ADD_GROUND"]:
                    dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$push": { "GROUND" : item } } )
            if "ADD_DIRS" in dbs.locationInfo:
                d = 0
                while d <= len(dbs.locationInfo["ADD_DIRS"]):
                    dbs.locations.update_one( { "NAME": dbs.ROOM }, { "$set": { dbs.locationInfo["ADD_DIRS"][str(d)][0] : dbs.locationInfo["ADD_DIRS"][str(d)][1] } } )
                    d += 1
        eng.refreshInfo()

    def writeTimedEvents(speed, what):
        # print the FIRST_EVENTS or KEY_EVENTS text
        y, l = 1, 0
        if what == "first":
            events = dbs.locationInfo["FIRST_EVENTS"]
        elif what == "key":
            events = dbs.locationInfo["KEY_EVENTS"]
        else:
            raise Exception("BUG: 'what' arg for writeTimedEvents() not specified")
        while l < len(events):
            # get event text and wrap the text to fit inside the window
            eventString = '\n'.join(textwrap.wrap(events[str(l)][1], 75))
            # get event's text style
            stringStyle = events[str(l)][0]
            eventWin.addstr(y, 0, eventString, eng.c[stringStyle])
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
            time.sleep(speed)
            # if the dialogue is taking up the whole window, we need to clear it and start writing at the beginning again
            if y >= 16:
                eventWin.addstr(y, 0, ". . .", eng.c["BLINK_BRIGHT_YELLOW"])
                time.sleep(speed)
                y = 1
                eventWin.clear()

    def writeStaticEvents(what):
        # print the UNSOLVED_EVENTS or SOLVED_EVENTS text
        y, l = 1, 0
        if what == "unsolved":
            events = dbs.locationInfo["UNSOLVED_EVENTS"]
        elif what == "solved":
            events = dbs.locationInfo["SOLVED_EVENTS"]
        else:
            raise Exception("BUG: 'what' arg for writeStaticEvents() not specified")
        while l < len(events):
            # get event text and wrap the text to fit inside the window
            eventString = '\n'.join(textwrap.wrap(events[str(l)][1], 75))
            # get event's text style
            stringStyle = events[str(l)][0]
            eventWin.addstr(y, 0, eventString, eng.c[stringStyle])
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

    def writeRoom(room, where, key):
        eventBorder.clear()
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        eventBorder.addstr(0, 65, "[ROOM EVENTS]")
        eventWin.clear()
        groundWin.clear()
        dirWin.clear()
        # write events to the event window
        curses.curs_set(0)
        if where == "winnibego":
            # setup DOWN direction
            dbs.locations.update_one( { "NAME": "Winnibego" }, { "$set": { dbs.locationInfo["PLANET_DIRS"][dbs.PLANET][0] : dbs.locationInfo["PLANET_DIRS"][dbs.PLANET][1] } } )
            dbs.setLocation(room)
            eng.refreshInfo()
            # setup the title window
            titleWin.clear()
            title = "{0}: {1}".format(dbs.PLANET, dbs.ROOM)
            titleWin.addstr(0, 0, title, eng.c["BRIGHT"])
            # display the winnibego room
            if dbs.locationInfo["VISITED"] == 0:
                worldUI.writeTimedEvents(2, "first")
                worldUI.updateRoomStatus("VISITED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 0:
                worldUI.writeStaticEvents("unsolved")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == True:
                worldUI.writeTimedEvents(2, "key")
                worldUI.updateRoomStatus("SOLVED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == False:
                worldUI.writeStaticEvents("solved")
        elif where == "space":
            dbs.setLocation(room)
            eng.refreshInfo()
            # setup the title window
            titleWin.clear()
            title = "{0}: {1}".format(dbs.PLANET, dbs.ROOM)
            titleWin.addstr(0, 0, title, eng.c["BRIGHT"])
            # display the space travel room
            if dbs.locationInfo["VISITED"] == 0:
                worldUI.writeTimedEvents(2, "first")
                worldUI.updateRoomStatus("VISITED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 0:
                worldUI.writeStaticEvents("unsolved")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == True:
                worldUI.writeTimedEvents(2, "key")
                worldUI.updateRoomStatus("SOLVED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == False:
                worldUI.writeStaticEvents("solved")
        elif where == "planet":
            dbs.setLocation(room)
            eng.refreshInfo()
            # setup the title window
            titleWin.clear()
            title = "{0}: {1}".format(dbs.PLANET, dbs.ROOM)
            titleWin.addstr(0, 0, title, eng.c["BRIGHT"])
            # display a normal room
            if dbs.locationInfo["VISITED"] == 0:
                worldUI.writeTimedEvents(2, "first")
                worldUI.updateRoomStatus("VISITED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 0:
                worldUI.writeStaticEvents("unsolved")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == True:
                worldUI.writeTimedEvents(2, "key")
                worldUI.updateRoomStatus("SOLVED")
            elif dbs.locationInfo["VISITED"] == 1 and dbs.locationInfo["SOLVED"] == 1 and key == False:
                worldUI.writeStaticEvents("solved")
        else:
            raise Exception("BUG: writeRoom() didn't have the right arg passed.")
        worldUI.writeInv()
        worldUI.writeGround()
        worldUI.writeStats()
        worldUI.writeDirs()

    def writeShop():
        eventBorder.clear()
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        eventBorder.addstr(0, 66, "[SHOP ITEMS]")
        eventWin.clear()
        shopItems = dbs.locationInfo["SHOP"]
        y = 0
        for item in shopItems:
            itemInfo = dbs.items.find_one( { "NAME": item } )
            effectString = eng.getEffectString(item)
            nameString = "{0} {1}".format(itemInfo["NAME"], effectString)
            eventWin.addstr(y, 0, nameString, eng.c["BRIGHT"])
            y += 1
            # wrap the LONGDESC to fit the window before displaying it
            eventWin.addstr(y, 0, '\n'.join(textwrap.wrap(itemInfo["LONGDESC"], 75)), eng.c["DIM"])
            if len(itemInfo["LONGDESC"]) < 76:
                y += 1
            else:
                y += 2
            floydsString = "[FLOYDS: {0}]".format(str(itemInfo["VALUE"]))
            eventWin.addstr(y, 0, floydsString, eng.c["GREEN"])
            y += 2

    def writeGround():
        # get items on the ground and display them
        groundList = list(dbs.locationInfo["GROUND"])
        # if there are no items, hide the window, otherwise print a list of items
        if len(groundList) == 0:
            groundWin.clear()
            pass
        else:
            groundWin.clear()
            # get a count of each item in the ITEMS list only
            itemCount = {}
            for item in groundList:
                if item in list(itemCount.keys()):
                    itemCount[item] += 1
                else:
                    itemCount[item] = 1
            # set starting lines in the window
            y, x, l = 1, 0, 0
            # print item count with duplicates, otherwise just print the item
            for item in set(groundList):
                if itemCount[item] > 1:
                    groundString = "{0}x {1}".format(str(itemCount[item]), item)
                    groundWin.addstr(y, x, groundString, eng.c["DIM"])
                else:
                    groundString = item
                    groundWin.addstr(y, x, groundString, eng.c["DIM"])
                if len(groundString) > l:
                    l = len(groundString)
                if y == 4:
                    y = 1
                    x = l + x + 3
                    l = 0
                else:
                    y += 1

    def writeDirs():
        # get event exits and display them
        dirWin.clear()
        y = 1
        for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
            if direction in list(dbs.locationInfo):
                dirString = "{0}: {1}".format(direction, dbs.locationInfo[direction])
                dirWin.addstr(y, 1, dirString, eng.c["DIM"])
                y += 1

    def writeLocation(room, what, key):
        # clear the event window
        eventWin.clear()
        worldUI.writeGround()
        worldUI.writeDirs()
        if what == "room":
            if dbs.ROOM.lower() == "winnibego":
                worldUI.writeRoom(room, "winnibego", key)
                worldUI.getCmd()
            elif dbs.ROOM.lower() == "space":
                worldUI.writeRoom(room, "space", key)
                worldUI.getCmd()
            else:
                worldUI.writeRoom(room, "planet", key)
                worldUI.getCmd()
        elif what == "shop":
            worldUI.writeShop()
            worldUI.getCmd()
        else:
            raise Exception("Forgot to specify writeout for the event window!")

    def writeMsg(msg, style):
        # write message to the message wndow, clearing old ones
        curses.curs_set(0)
        msgWin.clear()
        msgWin.addstr(0, 0, msg, eng.c[style])

    def writeStats():
        statsWin.clear()
        # refresh info in memory
        eng.refreshInfo()
        # get stat values
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
        # setup stat strings
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

    def writeInv():
        invWin.clear()
        # refresh info in memory
        eng.refreshInfo()
        # get and sort all item lists
        i = list(dbs.playerInv["ITEMS"])
        k = list(dbs.playerInv["KEY_ITEMS"])
        e = list(dbs.playerInv["EQUIPPED"])
        i = natsort.natsorted(i)
        k = natsort.natsorted(k)
        e = natsort.natsorted(e)
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

    def moveDirection(direction):
        # setup vars
        upper = direction.upper()
        lower = direction.lower()
        combatCheck = random.randrange(1, 50)
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
        if upper in dbs.locationInfo:
            dbs.locations.update_one( { "NAME": "Winnibego" }, { "$set": { "PLANET": dbs.locations.find_one( { "NAME": dbs.ROOM } )["PLANET"] } } )
            if combatCheck > 40:
                #combatMode().fight()
                worldUI.writeLocation(dbs.locationInfo[upper], "room", False)
            else:
                worldUI.writeLocation(dbs.locationInfo[upper], "room", False)
        else:
            worldUI.writeMsg("Ted can't walk through walls.", "RED")

    def displayWorld():
        # write all data to the screen
        worldUI.writeStats()
        worldUI.writeInv()
        worldUI.writeMsg("", "DIM")
        worldUI.writeLocation(dbs.ROOM, "room", False)

    def runAction(cmd, arg):
        # setup the environment
        inv = eng.tempInv()
        itemOnGround = eng.getFirstItemMatchingDesc(arg, dbs.locationInfo["GROUND"])
        itemInInv = eng.getFirstItemMatchingDesc(arg, inv)
        try:
            itemInShop = eng.getFirstItemMatchingDesc(arg, dbs.locationInfo["SHOP"])
        except KeyError:
            pass
        # run the shop command
        if cmd == "shop":
            if "SHOP" not in dbs.locationInfo:
                worldUI.writeMsg("There's no shop here, Ted!", "RED")
                return
            worldUI.writeLocation(dbs.ROOM, "shop", False)
        # run the look command
        elif cmd == "look":
            if arg == None or arg in worldUI.ROOM_WORDS:
                worldUI.writeLocation(dbs.ROOM, "room", False)
            elif arg in worldUI.LONG_DIRS or arg in worldUI.SHORT_DIRS:
                pass
            elif itemOnGround != None:
                longdesc = '\n'.join(textwrap.wrap(dbs.items.find_one( { "NAME": itemOnGround } )["LONGDESC"], 100))
                if len(longdesc) > 100:
                    worldUI.writeMsg(longdesc, "DIM")
                else:
                    worldUI.writeMsg(longdesc, "DIM")
            elif itemInInv != None:
                longdesc = '\n'.join(textwrap.wrap(dbs.items.find_one( { "NAME": itemInInv } )["LONGDESC"], 100))
                if len(longdesc) > 100:
                    worldUI.writeMsg(longdesc, "DIM")
                else:
                    worldUI.writeMsg(longdesc, "DIM")
            else:
                worldUI.writeMsg("Ted scours to room, but he doesn't see that.", "DIM")
        # run the take command
        elif cmd == "take":
            if arg == "":
                worldUI.writeMsg("What should Ted take?", "DIM")
            elif itemOnGround != None:
                itemInfo = dbs.items.find_one( { "NAME": itemOnGround } )
                if itemInfo["TAKEABLE"] == False:
                    worldUI.writeMsg("Ted doesn't want to grab that.", "RED")
                elif itemInfo["TAKEABLE"] == True:
                    dbs.updateGround(itemInfo["NAME"], "del") # remove from ground
                    dbs.updateInv(itemInfo["NAME"], "add") # add to inventory
                    worldUI.writeInv()
                    worldUI.writeGround()
                    message = "Ted grabs {0}.".format(itemInfo["SHORTDESC"])
                    worldUI.writeMsg(message, "DIM")
            else:
                worldUI.writeMsg("Ted doesn't see that.", "RED")
        # run the drop command
        elif cmd == "drop":
            if arg == "":
                worldUI.writeMsg("Whatchoo wanna drop?", "DIM")
            elif itemInInv != None:
                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )
                if itemInfo["TYPE"] == "key":
                    worldUI.writeMsg("You don't wanna drop that, Ted. You might need it later!", "YELLOW")
                elif itemInInv in dbs.playerInv["EQUIPPED"]:
                    worldUI.writeMsg("You have to let go of that before you can drop it, Ted!", "CYAN")
                else:
                    dbs.updateGround(itemInfo["NAME"], "add") # remove from ground
                    dbs.updateInv(itemInfo["NAME"], "del") # add to inventory
                    worldUI.writeInv()
                    worldUI.writeGround()
                    message = "Ted drops {0}.".format(itemInfo["SHORTDESC"])
                    worldUI.writeMsg(message, "DIM")
            else:
                worldUI.writeMsg("Ted doesn't even have that.", "RED")
        # run the equip command
        elif cmd == "equip":
            if arg == "":
                worldUI.writeMsg("Tryna equip somethin'?", "DIM")
            elif itemInInv != None:
                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )
                if itemInfo["TYPE"] == "weapon" and itemInfo["NAME"] not in dbs.playerInv["EQUIPPED"]:
                    dbs.setWeapon(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    message = "Ted equipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")
                elif itemInfo["TYPE"] == "fx" and itemInfo["NAME"] not in dbs.playerInv["EQUIPPED"]:
                    dbs.setFX(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    message = "Ted equipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")
                else:
                    worldUI.writeMsg("Ted can't equip that!", "RED")
            else:
                worldUI.writeMsg("Ted doesn't even have that.", "RED")
        # run the unequip command
        elif cmd == "unequip":
            if arg == "":
                worldUI.writeMsg("Whaddya mean, take what off?", "DIM")
            elif itemInInv == "Fists" or itemInInv == "noFX":
                worldUI.writeMsg("There's nothing to unequip, ya dangus!", "RED")
            elif itemInInv != None:
                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )
                if itemInfo["TYPE"] == "weapon" and itemInfo["NAME"] in dbs.playerInv["EQUIPPED"]:
                    dbs.setWeapon("Fists")
                    worldUI.writeInv()
                    worldUI.writeStats()
                    message = "Ted unequipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")
                elif itemInfo["TYPE"] == "fx" and itemInfo["NAME"] in dbs.playerInv["EQUIPPED"]:
                    dbs.setFX("noFX")
                    worldUI.writeInv()
                    worldUI.writeStats()
                    message = "Ted unequipped {0}.".format(itemInfo["NAME"])
                    worldUI.writeMsg(message, "CYAN")
                else:
                    worldUI.writeMsg("Ted doesn't have that on!", "RED")
            else:
                worldUI.writeMsg("Ted doesn't even have that.", "RED")
        # run the sell command
        elif cmd == "sell":
            if "SHOP" not in dbs.locationInfo:
                worldUI.writeMsg("There's not a shop here to sell to, Ted!", "RED")
                return
            inv = eng.tempInv()
            if itemInInv not in inv:
                worldUI.writeMsg("Ted doesn't even have that to sell!", "RED")
            elif itemInInv in dbs.playerInv["KEY_ITEMS"]:
                worldUI.writeMsg("Don't sell it, Ted! You might need that later.", "YELLOW")
            elif itemInInv in dbs.playerInv["EQUIPPED"]:
                worldUI.writeMsg("You've got to unequip it first, Ted.", "CYAN")
            else:
                message = eng.itemTransaction(itemInInv, "sell")
                worldUI.writeInv()
                worldUI.writeStats()
                worldUI.writeMsg(message[0], message[1])
        # run the buy command
        elif cmd == "buy":
            if "SHOP" not in dbs.locationInfo:
                worldUI.writeMsg("There's not a shop here to buy from, Ted!", "RED")
                return
            elif itemInShop not in dbs.locationInfo["SHOP"]:
                worldUI.writeMsg("The shopkeep looks confused by that request. I don't think they have it, Ted.", "RED")
                return
            else:
                message = eng.itemTransaction(itemInShop, "buy")
                worldUI.writeInv()
                worldUI.writeStats()
                worldUI.writeMsg(message[0], message[1])
        # run the smoke command
        elif cmd in worldUI.SMOKE_CMDS:
            if itemInInv != None:
                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )
                if itemInfo["TYPE"] != "smoke":
                    worldUI.writeMsg("You can't {0} that, Ted!".format(cmd), "RED")
                    return
                elif len(itemInfo["EFFECT"]) <= 2:
                    worldUI.writeMsg("You can only {0} that during a battle, Ted!".format(cmd), "RED")
                    return
                else:
                    message = eng.useItem(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    worldUI.writeMsg(message[0], message[1])
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")
        # run the eat command
        elif cmd in worldUI.EAT_CMDS:
            if itemInInv != None:
                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )
                if itemInfo["TYPE"] != "food":
                    worldUI.writeMsg("You can't {0} that, Ted!".format(cmd), "RED")
                    return
                elif len(itemInfo["EFFECT"]) <= 2:
                    worldUI.writeMsg("You can only {0} that during a battle, Ted!".format(cmd), "RED")
                    return
                else:
                    message = eng.useItem(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    worldUI.writeMsg(message[0], message[1])
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")
        # run the drink command
        elif cmd in worldUI.DRINK_CMDS:
            if itemInInv != None:
                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )
                if itemInfo["TYPE"] != "drink":
                    worldUI.writeMsg("You can't {0} that, Ted!".format(cmd), "RED")
                    return
                elif len(itemInfo["EFFECT"]) <= 2:
                    worldUI.writeMsg("You can only {0} that during a battle, Ted!".format(cmd), "RED")
                    return
                else:
                    message = eng.useItem(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    worldUI.writeMsg(message[0], message[1])
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")
        # run the drugs command
        elif cmd in worldUI.DRUG_CMDS:
            if itemInInv != None:
                itemInfo = dbs.items.find_one( { "NAME": itemInInv } )
                if itemInfo["TYPE"] != "drug":
                    worldUI.writeMsg("You can't {0} that, Ted!".format(cmd), "RED")
                    return
                elif len(itemInfo["EFFECT"]) <= 2:
                    worldUI.writeMsg("You can only {0} that during a battle, Ted!".format(cmd), "RED")
                    return
                else:
                    message = eng.useItem(itemInfo["NAME"])
                    worldUI.writeInv()
                    worldUI.writeStats()
                    worldUI.writeMsg(message[0], message[1])
            else:
                worldUI.writeMsg("Ted doesn't even see that anywhere.", "RED")
        # run the use command
        elif cmd == "use":
            # TODO `use item` in a room triggers the key event
            # TODO `use item with item` combines two items into one
            worldUI.writeMsg("TODO: This should allow Ted to use items with the environment, or with another item.", "MAGENTA")
        # run the save command
        elif cmd == "save":
            message = dbs.saveGame()
            worldUI.writeMsg(message[0], message[1])
        # run the help command
        elif cmd == "help":
            worldUI.writeMsg("Sorry, Ted! I can't help you yet, my systems are too fresh.", "RED")
        # run the exit command
        elif cmd == "quit" or cmd == "exit":
            message = dbs.saveGame()
            worldUI.writeMsg(message[0], message[1])
            eng.endGame()
        else:
            raise Exception("Command not found in runAction().")

    def getCmd():
        # wait for user input
        while True:
            msgWin.clear()
            inputWin.clear()
            curses.curs_set(2)
            userInput = inputCmd.edit().lower()
            inputWin.clear()
            if userInput == "" or userInput == None:
                continue
            args = userInput.split()
            try:
                args.remove("x")
            except ValueError:
                pass
            if args[0] in worldUI.ALL_COMMANDS:
                if len(args) == 3:
                    worldUI.runAction(args[0], "{0} {1}".format(args[1], args[2]))
                elif len(args) == 2:
                    worldUI.runAction(args[0], args[1])
                elif len(args) == 1:
                    worldUI.runAction(args[0], None)
                else:
                    raise Exception("CMD ERROR: Unexpected number of arguments from user input")
            elif args[0] in worldUI.LONG_DIRS or args[0] in worldUI.SHORT_DIRS:
                worldUI.moveDirection(args[0])
            else:
                worldUI.writeMsg("I don't recognize that command, Ted.", "RED")
            continue

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
        # set max size
        term_x = 110
        term_y = 40
        # refresh info in memory
        eng.refreshInfo()
        # setup title window
        # define the border of the window
        # subwin(height, width, begin_y, begin_x)
        titleBorder = stdscr.subwin(3, 80, 0, 1)
        titleBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        titleBorder.immedok(True)
        titleBorder.addstr(0, 68, "[LOCATION]")
        # define the content area of the window
        titleWin = stdscr.subwin(1, 76, 1, 3)
        titleWin.immedok(True)
        # setup event description and ground item area
        # define the border of the ground window
        groundBorder = stdscr.subwin(8, 50, 25, 1)
        groundBorder.immedok(True)
        groundBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        groundBorder.addstr(0, 40, "[GROUND]")
        # define the content area of the ground window
        groundWin = stdscr.subwin(6, 46, 26, 3)
        groundWin.immedok(True)
        # define the border of the direction window
        dirBorder = stdscr.subwin(8, 29, 25, 52)
        dirBorder.immedok(True)
        dirBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll)
        dirBorder.addstr(0, 20, "[EXITS]")
        # define the content area of the direction window
        dirWin = stdscr.subwin(6, 25, 26, 53)
        dirWin.immedok(True)
        # define the border of the event window
        eventBorder = stdscr.subwin(22, 80, 3, 1)
        eventBorder.immedok(True)
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        # define the content area of the event window
        eventWin = stdscr.subwin(20, 76, 4, 3)
        eventWin.immedok(True)
        # setup user input field
        # define border of input window
        inputWin = stdscr.subwin(1, 72, 34, (len(eng.PROMPT) + 3))
        inputWin.immedok(True)
        rectangle(stdscr, 33, 1, 35, 80)
        inputCmd = Textbox(inputWin, insert_mode=True)
        # place the PROMPT in the input window
        stdscr.addstr(34, 3, eng.PROMPT, eng.c["BRIGHT_RED"])
        # setup message window
        # define border of the window
        msgBorder = stdscr.subwin(4, 109, 36, 1)
        msgBorder.immedok(True)
        msgBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        msgBorder.addstr(0, 83, "[MESSAGES]")
        # define the content area of the window
        msgWin = stdscr.subwin(2, 105, 37, 3)
        msgWin.immedok(True)
        # setup stats window
        # define the border of the window
        statsBorder = stdscr.subwin(9, 28, 0, 82)
        statsBorder.immedok(True)
        statsBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        statsBorder.addstr(0, 2, "[STATS]")
        # define the content area of the window
        statsWin = stdscr.subwin(7, 24, 1, 84)
        statsWin.immedok(True)
        # setup inv window
        # define border of the window
        invBorder = stdscr.subwin(27, 28, 9, 82)
        invBorder.immedok(True)
        invBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        invBorder.addstr(0, 2, "[INVENTORY]")
        # define content area of the window
        invWin = stdscr.subwin(25, 24, 10, 84)
        invWin.immedok(True)
        # actually display everything
        worldUI.displayWorld()

    def start():
        # use curses wrapper in case of uncaught exceptions
        curses.wrapper(worldUI.build)
