import os, sys, time, random, argparse, cmd, textwrap, json, natsort
import art
import database as dbs

# check for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Turn on debug messages for various game calculations.", action="store_true")
parser.add_argument("-nc", "--nocolor", help="Turn off text styles and color.", action="store_true")
parser.add_argument("-w", "--width", nargs=1, help="Specify console screen width.", type=int)
args = parser.parse_args()

# engine variables
NEXT_ACTION = 0 # 1 = player, 0 = enemy
global DEBUG
global COLORS
global SCREEN_WIDTH
global PROMPT
global SLOT_NAME

# debug check
if args.debug:
    print("Debug mode engaged.")
    DEBUG = 1
else:
    DEBUG = 0

# color check
if args.nocolor:
    print("Entering Black & White mode.")
    import blackwhite as clr
    COLORS = 0
else:
    import colors as clr
    COLORS = 1

# set screen width
if args.width:
    SCREEN_WIDTH = args.width[0]
else:
    SCREEN_WIDTH = 170

# setup the command prompt
RAW_PROMPT = "{FRED}\m/: {NORMAL}{FWHITE}"
PROMPT = RAW_PROMPT.format(**clr.styles)

# identify the OS
def identify_os():
    system = sys.platform
    if system == "win32":
        return "cls"
    else:
        return "clear"

# clear the terminal
def clear():
    os.system(identify_os())

# input error message
def inputError():
    print("{BRIGHT}{FRED}Damnit, Ted! That's not a valid input. Try again!{NORMAL}{FWHITE}".format(**clr.styles))
    time.sleep(2)

def tempInv():
    dbs.getInventory()
    global inv
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
    inv = natsort.natsorted(inv)
    if DEBUG == 1:
        print("Temp Inventory List")
        print(inv)

# COMBAT ENGINE
class combatMode():

    def selectEnemy(self):
        # Randomly selects an enemy and sets base stats
        # TODO implement logic to only select enemies from the current planet
        global chosenEnemy
        global ENEMYHP
        global ENEMYMP
        enemyIDList = list(dbs.enemies.find( {}, { "NAME": 1 } ))
        chosenID = random.choice(enemyIDList)["_id"]
        chosenEnemy = dbs.enemies.find_one( { "_id": chosenID } )
        ENEMYHP = chosenEnemy["HP"]
        ENEMYMP = chosenEnemy["MP"]
        if DEBUG == 1:
            print(chosenEnemy)
            time.sleep(2)

    def HUD(self):
        # Prints out the players HUD
        clear()
        dbs.getStats()
        print("\n{DIM}>>  {BRIGHT}{FCYAN}TED MOONCHILD{FWHITE}{NORMAL}".format(**clr.styles))
        print("    HP: {HP}".format(**clr.styles, HP = str(dbs.playerStats["HP"])))
        print("    MP: {MP}".format(**clr.styles, MP = str(dbs.playerStats["MP"])))
        print("    WPN: {WPN} [+{BNS}]".format(**clr.styles, WPN = dbs.equippedWeapon, BNS = str(dbs.weaponInfo["ATKBNS"])))
        print("    FX: {FX} [+{BNS}]\n".format(**clr.styles, FX = dbs.addedFX, BNS = str(dbs.fxInfo["ATKBNS"])))
        print("{DIM}>>  {BRIGHT}{FYELLOW}{NAME}{FWHITE}{NORMAL}".format(**clr.styles, NAME = chosenEnemy["NAME"]))
        print("    HP: {HP}".format(**clr.styles, HP = str(ENEMYHP)))
        print("    MP: {MP}".format(**clr.styles, MP = str(ENEMYMP)))

    def story(self):
        # Prints description of enemy, dialog, ascii art.
        print("\n    [IMAGE of {NAME}]\n".format(**clr.styles, NAME = chosenEnemy["NAME"]))
        print("    {DESC}".format(**clr.styles, DESC = chosenEnemy["DESC"]))
        print("\n{DIM}+--------------------------------------------------------------------------------------------------+{NORMAL}\n".format(**clr.styles))

    def battleMenu(self):
        # Prints out the battle system menu
        global ENEMYHP
        global ENEMYMP
        global NEXT_ACTION
        dbs.getStats()
        dbs.getInventory()
        print("{DIM}>>  {NORMAL}{FRED}BATTLE MENU:{FWHITE}".format(**clr.styles))
        print("    a = attack")
        print("    m = magic")
        print("    i = item\n")
        battleChoice = input(PROMPT)
        if battleChoice == 'a':
            # Iterate over dictionary keys and print
            i = 1
            # Stores a list of all attacks in dict item as they are unordered.
            attackList = dbs.abilities.find( { "TYPE": "physical" } )
            attackIDList = [ "_index" ]
            print("\n{DIM}>> {NORMAL}Choose an Attack".format(**clr.styles))
            for item in attackList:
                print(" [" + str(i) + "] - " + item["NAME"])
                attackIDList.append(item["_id"])
                i += 1
            print()
            try:
                choice = int(input(PROMPT))
                chosenAttackInfo = dbs.abilities.find_one( { "_id": attackIDList[choice] } )
                if DEBUG == 1:
                    print(chosenAttackInfo)
            except:
                inputError()
                # Set next action to player
                NEXT_ACTION = 1
            else:
                heroAttackDamage = random.randrange(chosenAttackInfo["HEROMIN"], chosenAttackInfo["HEROMAX"])
                if DEBUG == 1:
                    print("\nHero Attack Calculator")
                    print("{DIM} Base DMG:       {DMG}{NORMAL}{FWHITE}".format(**clr.styles, DMG = str(heroAttackDamage)))
                else:
                    pass
                # determine critical strike
                heroCrit = random.randrange(0, 6)
                if DEBUG == 1:
                    print("{DIM}  >CRIT Check:   {CRIT} (5 = true){NORMAL}{FWHITE}".format(**clr.styles, CRIT = str(heroCrit)))
                else:
                    pass
                if heroCrit == 5:
                    heroAttackDamage += dbs.playerStats["CRIT"]
                else:
                    pass
                if DEBUG == 1:
                    print("{DIM} DMG + CRIT:     {DMG}{NORMAL}{FWHITE}".format(**clr.styles, DMG = str(heroAttackDamage)))
                else:
                    pass
                # Increase hero's attack damage by whatever attack bonus the weapon supplies.
                heroAttackDamage += dbs.weaponInfo["ATKBNS"]
                if DEBUG == 1:
                    print("{DIM} DMG + WPN:      {DMG}{NORMAL}{FWHITE}".format(**clr.styles, DMG = str(heroAttackDamage)))
                else:
                    pass
                heroAttackDamage += dbs.fxInfo["ATKBNS"]
                if DEBUG == 1:
                    print("{DIM} DMG + FX:       {DMG}{NORMAL}{FWHITE}".format(**clr.styles, DMG = str(heroAttackDamage)))
                else:
                    pass
                # MISS check, 4 = miss
                playerMiss = random.randrange(0,5)
                if DEBUG == 1:
                    print("\nMiss Check: {DIM}{MISS} (4 = true){NORMAL}\n".format(**clr.styles, MISS = str(playerMiss)))
                else:
                    pass
                if playerMiss == 4:
                    print("{FCYAN}{BRIGHT}A swing, and a miss!!{NORMAL}{FWHITE}".format(**clr.styles))
                else:
                    ENEMYHP = ENEMYHP - heroAttackDamage
                    if heroCrit == 5:
                        print("Ted packs a WOLLOP with his {ATK} for {FGREEN}{BRIGHT}{DMG}{NORMAL}{FWHITE} damage!!".format(**clr.styles, ATK = chosenAttackInfo["NAME"], DMG = str(heroAttackDamage)))
                    else:
                        print("Ted lands a blow with his {ATK} for {FGREEN}{BRIGHT}{DMG}{NORMAL}{FWHITE} damage!".format(**clr.styles, ATK = chosenAttackInfo["NAME"], DMG = str(heroAttackDamage)))
                time.sleep(3)
                # Set next action to enemy
                NEXT_ACTION = 0

        elif battleChoice == 'm':
            # TODO implement escape choice
            # Iterate over dictionary keys and print
            i = 1
            magicList = dbs.abilities.find( { "TYPE": "magic" } )
            magicIDList = [ "_index" ]
            print("\n{DIM}>> {NORMAL}Choose an Ability".format(**clr.styles))
            for item in magicList:
                print(" [" + str(i) + "] - " + item["NAME"])
                magicIDList.append(item["_id"])
                i += 1
            print()
            try:
                choice = int(input(PROMPT))
                chosenMagicInfo = dbs.abilities.find_one( { "_id": magicIDList[choice] } )
                if DEBUG == 1:
                    print(chosenMagicInfo)
            except:
                inputError()
                # Set next action to player
                NEXT_ACTION = 1
            else:
                if chosenMagicInfo["MPREQ"] > dbs.playerStats["MP"]:
                    print("\nTed doesn't have enough MP!")
                    # Set next action to player
                    NEXT_ACTION = 1
                else:
                    heroMagicDamage = chosenMagicInfo["MAGDMG"]
                    # magic crit check, 10 = success
                    magicCrit = random.randrange(0,20)
                    if DEBUG == 1:
                        print("\nMagic Crit Check: " + str(magicCrit) + "\n")
                    else:
                        pass
                    if magicCrit == 10:
                        heroMagicDamage += heroMagicDamage
                        ENEMYHP = ENEMYHP - heroMagicDamage
                        print("Ted totally ROCKED {NAME} for {FCYAN}{DMG}{NORMAL}{FWHITE} damage!!".format(**clr.styles, NAME = chosenMagicInfo["NAME"], DMG = str(heroMagicDamage)))
                    else:
                        ENEMYHP = ENEMYHP - heroMagicDamage
                        print("Ted performs {NAME} for {FCYAN}{DMG}{NORMAL}{FWHITE} damage!".format(**clr.styles, NAME = chosenMagicInfo["NAME"], DMG = str(heroMagicDamage)))
                    dbs.updateStat("MP", chosenMagicInfo["MPREQ"], "dec")
                    time.sleep(3)
                    # Set next action to enemy
                    NEXT_ACTION = 0

        elif battleChoice == 'i':
            # Iterate over dictionary keys and print
            i = 1
            battleItems = [ "_index" ]
            inv = list(dbs.playerInv["ITEMS"])

            if len(inv) == 0:
                print("Ted doesn't have any shit to use in battle!")
                return

            # first get a count of each distinct item in the inventory
            itemCount = {}
            for item in inv:
                if item in list(itemCount.keys()):
                    itemCount[item] += 1
                else:
                    itemCount[item] = 1

            print("\n{DIM}>> {NORMAL}Choose an Item".format(**clr.styles))
            # get a list of inventory items with duplicates removed:
            for item in set(inv):
                # If item is a duplicate, print once with the quantity in ()
                if itemCount[item] > 1:
                    print("{DIM}{FYELLOW} [{I}] - {FWHITE}{NORMAL}  {ITEM} ({COUNT})".format(**clr.styles, I = str(i), ITEM = item, COUNT = str(itemCount[item])))
                    battleItems.append(item)
                else:
                    print("{DIM}{FYELLOW} [{I}] - {FWHITE}{NORMAL}  {ITEM}".format(**clr.styles, I = str(i), ITEM = item))
                    battleItems.append(item)
                i += 1
            print()
            try:
                choice = int(input(PROMPT))
                chosenItemInfo = dbs.items.find_one( { "NAME": battleItems[choice] } )
                if DEBUG == 1:
                    print(chosenItemInfo)
            except:
                inputError()
                # Set next action to player
                NEXT_ACTION = 1
            else:
                try:
                    check = chosenItemInfo["BATTLE"]
                except KeyError:
                    pass
                if chosenItemInfo["BATTLE"] == True:
                    # TODO do something with the item
                    # then drop the item from inventory
                    dbs.updateInv(chosenItemInfo["NAME"], "del")
                    print("\nTed uses " + chosenItemInfo["NAME"] + "! Too bad item effects aren't implemented yet.")
                    print("The " + chosenItemInfo["NAME"] + " is still used up, though ;)")
                    time.sleep(3)
                    # Set next action to enemy
                    NEXT_ACTION = 0
                elif chosenItemInfo["WEAPON"] == True and chosenItemInfo["NAME"] != dbs.equippedWeapon:
                    print("\nYou have to equip it first, then use your attack!")
                    time.sleep(2)
                    # Set next action to player
                    NEXT_ACTION = 1
                elif chosenItemInfo["FX"] == True and chosenItemInfo["NAME"] != dbs.addedFX:
                    print("\nYou have to equip it first, then use your attack!")
                    time.sleep(2)
                    # Set next action to player
                    NEXT_ACTION = 1
                elif chosenItemInfo["NAME"] == dbs.addedFX:
                    print("Use Ted's attack instead!")
                    # Set next action to player
                    NEXT_ACTION = 1
                elif chosenItemInfo["NAME"] == dbs.equippedWeapon:
                    print("Use Ted's attack instead!")
                    # Set next action to player
                    NEXT_ACTION = 1
                else:
                    print("\nTed, this isn't the time!")
                    time.sleep(2)
                    # Set next action to player
                    NEXT_ACTION = 1
        else:
            inputError()
            # Set next action to player
            NEXT_ACTION = 1

    def death(self):
        # Determines if a player is dead
        # TODO implement XP award system based on chosenEnemy's challenge rating
        dbs.getStats()
        if dbs.playerStats["HP"] <= 0:
            print("{FRED}{BRIGHT}The {NAME} beat the shit out of Ted!!{NORMAL}{FWHITE}".format(**clr.styles, NAME = chosenEnemy["NAME"]))
            time.sleep(3)
            return False
        elif ENEMYHP <= 0:
            print("{FGREEN}{BRIGHT}Ted beat the fuck out of that {NAME}!!{NORMAL}{FWHITE}".format(**clr.styles, NAME = chosenEnemy["NAME"]))
            time.sleep(3)
            return False
        else:
            return True

    def fight(self):
        dbs.getStats()
        # Actually drives the battle
        global NEXT_ACTION
        # Randomly select an enemy.
        self.selectEnemy()
        NEXT_ACTION = random.randrange(0, 2)  # Randomly select who attacks first.
        # Changes color to white
        print("{FWHITE}".format(**clr.styles))
        while True:
            death = self.death()
            if death == False:
                break
            elif NEXT_ACTION == 0:
                # Print battle HUD.
                self.HUD()
                # Print description of enemy.
                self.story()
                # Get's length of attack dialog list.
                dialogSelection = len(chosenEnemy["DIALOG"])
                # Randomly chooses damage caused based on min and max defined values.
                enemyAttack = random.randrange(chosenEnemy["ATTACKMIN"], chosenEnemy["ATTACKMAX"])
                if DEBUG == 1:
                    print("Enemy Attack Calculator")
                    print("{DIM} Base DMG:       {ATK}{NORMAL}{FWHITE}".format(**clr.styles, ATK = str(enemyAttack)))
                else:
                    pass
                # determine critical strike
                enemyCrit = random.randrange(0, 10)
                if DEBUG == 1:
                    print("{DIM}  >CRIT Check:   {CRIT} (5 = true){NORMAL}{FWHITE}".format(**clr.styles, CRIT = str(enemyCrit)))
                else:
                    pass
                if enemyCrit == 5:
                    enemyAttack += chosenEnemy["CRITBNS"]
                else:
                    pass
                if DEBUG == 1:
                    print("{DIM} DMG + CRIT:     {ATK}{NORMAL}{FWHITE}".format(**clr.styles, ATK = str(enemyAttack)))
                else:
                    pass
                enemyMiss = random.randrange(0, 5)
                if DEBUG == 1:
                    print("\nMiss Check: " + str(enemyMiss) + " (4 = true)\n")
                else:
                    pass
                if enemyMiss == 4:
                    print("{FCYAN}{BRIGHT}The {NAME} missed like a dangus!{NORMAL}{FWHITE}".format(**clr.styles, NAME = chosenEnemy["NAME"]))
                else:
                    dbs.updateStat("HP", enemyAttack, "dec")
                    # Chooses a random attack dialog line.
                    print("{FGREEN}{DIAG}{FWHITE}\n".format(**clr.styles, DIAG = chosenEnemy["DIALOG"][random.randrange(0, dialogSelection)]))

                    if enemyCrit == 5:
                        print("Ted takes a whopping {FRED}{BRIGHT}{ATK}{NORMAL}{FWHITE} damage!!".format(**clr.styles, ATK = str(enemyAttack)))
                    else:
                        print("Ted suffers {FRED}{BRIGHT}{ATK}{NORMAL}{FWHITE} damage!".format(**clr.styles, ATK = str(enemyAttack)))

                time.sleep(3)
                # Set next action to player
                NEXT_ACTION = 1
            elif NEXT_ACTION == 1:
                # Print battle HUD.
                self.HUD()
                # Print description of enemy.
                self.story()
                # Print menu
                self.battleMenu()

def displayLocation(loc):
    # A helper function for displaying an area's description and exits.
    clear()
    dbs.getStats()
    dbs.getInventory()
    locInfo = dbs.rooms.find_one( { "NAME": loc } )
    # Print the room name.
    print(loc)
    print(('=' * len(loc)))

    print(locInfo['DESC'].format(**clr.styles))

    # Print all the items on the ground.
    if len(locInfo["GROUND"]) > 0:
        print("{DIM}--- GROUND ITEMS ---{NORMAL}{FWHITE}".format(**clr.styles))
        for item in locInfo["GROUND"]:
            print("  {GROUNDDESC}".format(**clr.styles, GROUNDDESC = dbs.items.find_one( { "NAME": item } )["GROUNDDESC"]))
    print("\n")
    # Print all the exits.
    exits = []
    for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
        if direction in list(locInfo):
            exits.append(direction.title())

    if dbs.playerPrefs["EXITS"] == "full":
        print("{DIM}--- NEARBY EXITS ---{NORMAL}".format(**clr.styles))
        for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
            if direction in dbs.locationInfo:
                print("  " + direction.title() + ": " + dbs.locationInfo[direction])
    else:
        print("{DIM}Exits: {NORMAL}{JOIN}".format(**clr.styles, JOIN = ' '.join(exits)))
    print("\n")

def moveDirection(direction):
    # A helper function that changes the location of the player.

    combatCheck = random.randrange(0,6)

    if direction in dbs.locationInfo:
        if combatCheck == 5:
            clear()
            print("{FRED}{BRIGHT}".format(**clr.styles))
            print("    An enemy has challenged Ted!\n")
            print("{DIM}{FBLACK}{BYELLOW}                                    ".format(**clr.styles))
            print("    ////////////////////////////    ")
            print("    //  {BRIGHT}ENTERING COMBAT MODE{DIM}  //    ".format(**clr.styles))
            print("    ////////////////////////////    ")
            print("                                    {BBLACK}{NORMAL}{FWHITE}".format(**clr.styles))
            time.sleep(3)
            combat = combatMode()
            combat.fight()
            dbs.setLocation(dbs.locationInfo[direction])
            displayLocation(dbs.location)
        else:
            dbs.setLocation(dbs.locationInfo[direction])
            displayLocation(dbs.location)
    else:
        print("Ted can't walk through walls.")

def getAllDescWords(itemList):
    # Returns a list of "description words" for each item named in itemList.
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.extend(dbs.items.find_one( { "NAME": item } )["DESCWORDS"])
    return list(set(descWords))

def getAllFirstDescWords(itemList):
    # Returns a list of the first "description word" in the list of description words for each item named in itemList.
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.append(dbs.items.find_one( { "NAME": item } )["DESCWORDS"][0])
    return list(set(descWords))

def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    for item in itemList:
        if desc in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
            return item
    return None

def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
            matchingItems.append(item)
    return matchingItems

class TextAdventureCmd(cmd.Cmd):
    prompt = PROMPT

    # The default() method is called when none of the other do_*() command methods match.
    def default(self, arg):
        print("Ted's feeble brain doesn't understand.")

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        # Quit the game.
        dbs.saveGame()
        time.sleep(1)
        dbs.deleteSave(SLOT_NAME, False)
        time.sleep(1)
        return True # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

    # These direction commands have a long (i.e. north) and show (i.e. n) form.
    # Since the code is basically the same, I put it in the moveDirection()
    # function.
    def do_north(self, arg):
        # Go to the area to the north, if possible.
        moveDirection("NORTH")

    def do_south(self, arg):
        # Go to the area to the south, if possible.
        moveDirection("SOUTH")

    def do_east(self, arg):
        # Go to the area to the east, if possible.
        moveDirection("EAST")

    def do_west(self, arg):
        # Go to the area to the west, if possible.
        moveDirection("WEST")

    def do_up(self, arg):
        # Go to the area upwards, if possible.
        moveDirection("UP")

    def do_down(self, arg):
        #Go to the area downwards, if possible.
        moveDirection("DOWN")

    # Since the code is the exact same, we can just copy the
    # methods with shortened names:
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down

    def do_exits(self, arg):
        # toggle showing full exit descriptions or brief exit descriptions.
        dbs.getPrefs()
        if dbs.playerPrefs["EXITS"] == "full":
            dbs.player.update_one( { "SECTION": "prefs" }, { "$set": { "EXITS": "short" } } )
        else:
            dbs.player.update_one( { "SECTION": "prefs" }, { "$set": { "EXITS": "full" } } )
        dbs.getPrefs()
        # print a message to the user
        if dbs.playerPrefs["EXITS"] == "full":
            print("{DIM}Showing full exit descriptions.{NORMAL}".format(**clr.styles))
        else:
            print("{DIM}Showing brief exit descriptions.{NORMAL}".format(**clr.styles))

    def do_inventory(self, arg):
        # Display a list of the items in Ted\'s possession.
        dbs.getInventory()
        if DEBUG == 1:
            print("Current Inventory")
            print(dbs.playerInv["ITEMS"])
            print(dbs.playerInv["KEY_ITEMS"])
            print(dbs.playerInv["EQUIPPED"])

        tempInv()

        if len(inv) == 0:
            print("Ted doesn't have shit.")
            return

        # first get a count of each distinct item in the inventory
        itemCount = {}
        for item in inv:
            if item in list(itemCount.keys()):
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # get a list of inventory items with duplicates removed:
        print("{DIM}---- INV ----{NORMAL}{FWHITE}".format(**clr.styles))
        for item in set(inv):
            # If item is an equipped weapon, display a [e]
            if item == dbs.equippedWeapon:
                print("  {DIM}{ITEM} [e]{NORMAL}".format(**clr.styles, ITEM = item))
            elif item == dbs.addedFX:
                print("  {DIM}{ITEM} [e]{NORMAL}".format(**clr.styles, ITEM = item))
            elif dbs.items.find_one( { "NAME": item } )["TYPE"] == "key":
                print("  {FYELLOW}{ITEM} [k]{FWHITE}".format(**clr.styles, ITEM = item))
            elif itemCount[item] > 1:
                print("  " + item + " (" + str(itemCount[item]) + ")")
            else:
                print("  " + item)
        print("{DIM}============={NORMAL}{FWHITE}".format(**clr.styles))

    do_inv = do_inventory

    def do_take(self, arg):
        dbs.getInventory()
        # take <item> - Take an item on the ground.
        # put this value in a more suitably named variable
        itemToTake = arg.lower()

        if itemToTake == '':
            print("What should Ted take?")
            return

        cantTake = False

        # get the item name that the player's command describes
        for item in getAllItemsMatchingDesc(itemToTake, dbs.locationInfo["GROUND"]):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemInfo["TAKEABLE"] == False:
                cantTake = True
                continue # there may be other items named this that Ted can take, so we continue checking
            print("Ted grabs " + itemInfo["SHORTDESC"] + ".")
            dbs.updateGround(item, "del") # remove from ground
            dbs.updateInv(item, "add") # add to inventory
            return

        if cantTake:
            print("Ted doesn't want to grab\"" + itemToTake + "\".")
        else:
            print("Ted doesn't see that.")

    def do_drop(self, arg):
        dbs.getInventory()
        # drop <item>" - Drop an item from Ted\'s inventory onto the ground.
        # put this value in a more suitably named variable
        itemToDrop = arg.lower()
        inv = list(dbs.playerInv["ITEMS"])

        if itemToDrop == '':
            print("Whatchoo wanna drop?")
            return

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inv)

        # find out if the player doesn't have that item
        if itemToDrop not in invDescWords:
            print("Ted can't drop \"" + itemToDrop + "\". Maybe it's equipped or a key item?")
            return

        # get the item name that the player's command describes
        item = getFirstItemMatchingDesc(itemToDrop, inv)
        if item != None:
            dbs.updateGround(item, "add") # add to ground
            dbs.updateInv(item, "del") # remove from inventory
            print("Ted drops " + dbs.items.find_one( { "NAME": item } )["SHORTDESC"] + ".")

    def complete_take(self, text, line, begidx, endidx):
        possibleItems = []
        text = text.lower()

        # if the user has only typed "take" but no item name:
        if not text:
            return getAllFirstDescWords(dbs.locationInfo["GROUND"])

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for item in list(set(dbs.locationInfo["GROUND"])):
            for descWord in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
                if descWord.startswith(text) and dbs.items.find_one( { "NAME": item } )["TAKEABLE"] == True:
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def complete_drop(self, text, line, begidx, endidx):
        possibleItems = []
        itemToDrop = text.lower()
        inv = list(dbs.playerInv["ITEMS"])

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inv)

        for descWord in invDescWords:
            if line.startswith('drop %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "drop" but no item name:
        if itemToDrop == '':
            return getAllFirstDescWords(inv)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(text):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_look(self, arg):
        dbs.getInventory()
        dbs.getStats()
        # Look at an item, direction, or the area:
        # "look" - display the current area's description
        # "look <direction>" - display the description of the area in that direction
        # "look exits" - display the description of all adjacent areas
        # "look <item>" - display the description of an item on the ground or in Ted's inventory

        lookingAt = arg.lower()
        if lookingAt == '':
            # "look" will re-print the area description
            displayLocation(dbs.location)
            return

        if lookingAt == 'exits':
            for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
                if direction in dbs.locationInfo:
                    print(direction.title() + ": " + dbs.locationInfo[direction])
            return

        if lookingAt in ('north', 'west', 'east', 'south', 'up', 'down', 'n', 'w', 'e', 's', 'u', 'd'):
            if lookingAt.startswith("n") and "NORTH" in dbs.locationInfo:
                print(dbs.locationInfo["NORTH"])
            elif lookingAt.startswith("w") and "WEST" in dbs.locationInfo:
                print(dbs.locationInfo["WEST"])
            elif lookingAt.startswith("e") and "EAST" in dbs.locationInfo:
                print(dbs.locationInfo["EAST"])
            elif lookingAt.startswith("s") and "SOUTH" in dbs.locationInfo:
                print(dbs.locationInfo["SOUTH"])
            elif lookingAt.startswith("u") and "UP" in dbs.locationInfo:
                print(dbs.locationInfo["UP"])
            elif lookingAt.startswith("d") and "DOWN" in dbs.locationInfo:
                print(dbs.locationInfo["DOWN"])
            else:
                print("Ted can't walk through walls.")
            return

        # see if the item being looked at is on the ground at this location
        item = getFirstItemMatchingDesc(lookingAt, dbs.locationInfo["GROUND"])
        if item != None:
            print('\n'.join(textwrap.wrap(dbs.items.find_one( { "NAME": item } )["LONGDESC"].format(**clr.styles), SCREEN_WIDTH)))
            return

        # see if the item being looked at is in the inventory
        tempInv()

        item = getFirstItemMatchingDesc(lookingAt, inv)
        if item != None:
            print('\n'.join(textwrap.wrap(dbs.items.find_one( { "NAME": item } )["LONGDESC"].format(**clr.styles), SCREEN_WIDTH)))
            return

        print("Ted scours to room, but he doesn't see that.")

    def complete_look(self, text, line, begidx, endidx):
        possibleItems = []
        lookingAt = text.lower()
        tempInv()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inv)
        groundDescWords = getAllDescWords(dbs.locationInfo["GROUND"])
        shopDescWords = getAllDescWords(dbs.locationInfo["SHOP"])

        for descWord in invDescWords + groundDescWords + shopDescWords + ["north", "south", "east", "west", "up", "down"]:
            if line.startswith('look %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "look" but no item name, show all items on ground, shop and directions:
        if lookingAt == '':
            possibleItems.extend(getAllFirstDescWords(dbs.locationInfo["GROUND"]))
            possibleItems.extend(getAllFirstDescWords(dbs.locationInfo["SHOP"]))
            for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
                if direction in dbs.locationInfo:
                    possibleItems.append(direction)
            return list(set(possibleItems)) # make list unique

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for descWord in groundDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        # otherwise, get a list of all "description words" for items for sale at the shop (if this is one):
        for descWord in shopDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        # check for matching directions
        for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
            if direction.startswith(lookingAt):
                possibleItems.append(direction)

        # get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_list(self, arg):
        # List the items for sale at the current location's shop.
        if "SHOP" not in dbs.locationInfo:
            print("Ain't no store here, Ted.")
            return

        arg = arg.lower()

        print("{DIM}--- STORE ---{NORMAL}{FWHITE}".format(**clr.styles))
        for item in dbs.locationInfo["SHOP"]:
            itemInfo = dbs.items.find_one( { "NAME": item } )
            print("  " + item)
            print("{DIM}".format(**clr.styles), '  \n  '.join(textwrap.wrap(itemInfo["LONGDESC"].format(**clr.styles), SCREEN_WIDTH)) + "{NORMAL}{FWHITE}".format(**clr.styles))
            if arg == 'full':
                print("{DIM}".format(**clr.styles), '\n'.join(textwrap.wrap(itemInfo["LONGDESC"].format(**clr.styles), SCREEN_WIDTH)) + "{NORMAL}{FWHITE}".format(**clr.styles))

        print("{DIM}============={NORMAL}{FWHITE}".format(**clr.styles))

    def do_buy(self, arg):
        # buy <item>" - buy an item at the current location's shop.
        if "SHOP" not in dbs.locationInfo:
            print("Ain't shit to buy, Ted.")
            return

        itemToBuy = arg.lower()

        if itemToBuy == '':
            print("Gotta be more specific.{DIM} Type \"list\" to see items{NORMAL}{FWHITE}".format(**clr.styles))
            return

        item = getFirstItemMatchingDesc(itemToBuy, dbs.locationInfo["SHOP"])
        if item != None:
            # NOTE - If Ted wanted to implement money, here is where Ted would add
            # code that checks if the player has enough, then deducts the price
            # from their money.
            print("Ted just bought " + dbs.items.find_one( { "NAME": item } )["SHORTDESC"])
            dbs.updateInv(item, "add")
            return

        print("They don't have any \"" + itemToBuy + ".\" Try again, Ted.")

    def complete_buy(self, text, line, begidx, endidx):
        if "SHOP" not in dbs.locationInfo:
            return []

        itemToBuy = text.lower()
        possibleItems = []

        # if the user has only typed "buy" but no item name:
        if not itemToBuy:
            return getAllFirstDescWords(dbs.locationInfo["SHOP"])

        # otherwise, get a list of all "description words" for shop items matching the command text so far:
        for item in list(set(dbs.locationInfo["SHOP"])):
            for descWord in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_sell(self, arg):
        dbs.getInventory()
        # "sell <item>" - sell an item at the current location's shop.
        if "SHOP" not in dbs.locationInfo:
            print("Ain't no one to sell it.")
            return

        inv = list(dbs.playerInv["ITEMS"])
        itemToSell = arg.lower()

        if itemToSell == '':
            print("Whatchoo wanna sell?{DIM} Type \"inv\" to see items{NORMAL}{FWHITE}".format(**clr.styles))
            return

        for item in inv:
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemToSell in itemInfo["DESCWORDS"]:
                # NOTE - If Ted wanted to implement money, here is where Ted would add
                # code that gives the player money for selling the item.
                print("Ted sold " + itemInfo["SHORTDESC"])
                dbs.updateInv(item, "del")
                return

        print("You don't have \"" + itemToSell + "\", Ted.")

    def complete_sell(self, text, line, begidx, endidx):
        dbs.getInventory()
        if "SHOP" not in dbs.locationInfo:
            return []

        inv = list(dbs.playerInv["ITEMS"])
        itemToSell = text.lower()
        possibleItems = []

        # if the user has only typed "sell" but no item name:
        if not itemToSell:
            return getAllFirstDescWords(inv)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for item in list(set(inv)):
            for descWord in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_eat(self, arg):
        dbs.getInventory()
        # "eat <item>" - eat an item in Ted\'s inventory."""
        itemToEat = arg.lower()
        tempInv()

        if itemToEat == '':
            print("Whatchoo wanna eat?")
            return

        cantEat = False

        for item in getAllItemsMatchingDesc(itemToEat, inv):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            try:
                check = itemInfo["EDIBLE"]
            except KeyError:
                cantEat = True
                continue # there may be other items named this that Ted can eat, so we continue checking
            print("Ted eats " + itemInfo["SHORTDESC"])
            dbs.updateInv(item, "del")
            return

        if cantEat:
            print("Ted doesn't want to eat that...")
        else:
            print("Ted is confused by \"" + itemToEat + "\"")

    def complete_eat(self, text, line, begidx, endidx):
        dbs.getInventory()
        itemToEat = text.lower()
        possibleItems = []
        tempInv()

        # if the user has only typed "eat" but no item name:
        if itemToEat == '':
            return getAllFirstDescWords(inv)

        # otherwise, get a list of all "description words" for edible inventory items matching the command text so far:
        for item in list(set(inv)):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            for descWord in itemInfo["DESCWORDS"]:
                if descWord.startswith(text) and itemInfo["EDIBLE"] == False:
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_stats(self, arg):
        # Display player stats, weapon, and accessory
        print("{DIM}--- Stats ---{NORMAL}{FWHITE}".format(**clr.styles))
        print("  HP: " + str(dbs.playerStats["HP"]) + "/" + str(dbs.playerStats["HPMAX"]))
        print("  MP: " + str(dbs.playerStats["MP"]) + "/" + str(dbs.playerStats["MPMAX"]))
        print("  Hero Level: " + str(dbs.playerStats["LVL"]))
        print("  Hero XP: " + str(dbs.playerStats["XP"]))
        print("  You have " + str(dbs.playerStats["FLOYDS"]) + " Floyds.")
        print("  Equipped Weapon: " + dbs.equippedWeapon + " [+" + str(dbs.weaponInfo["ATKBNS"]) + "]")
        print("  Added FX: " + dbs.addedFX + " [+" + str(dbs.fxInfo["ATKBNS"]) + "]")
        print("{DIM}============={NORMAL}{FWHITE}".format(**clr.styles))

    # TODO add un-equip functions for weapon and fx

    def do_equip(self, arg):
        dbs.getInventory()
        # Equip an item in Ted\'s inventory.
        itemToEquip = arg.lower()
        inv = list(dbs.playerInv["ITEMS"])

        if itemToEquip == '':
            print("Whatchoo wanna equip?")
            return

        cantEquip = False

        for item in getAllItemsMatchingDesc(itemToEquip, inv):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemInfo["TYPE"] != "weapon":
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print("Ted equips " + itemInfo["SHORTDESC"])
            dbs.setWeapon(item)
            return

        if cantEquip:
            print("Ted can't equip that...")
        else:
            print("Ted is confused by \"" + itemToEquip + "\"")

    def do_unequip(self, arg):
        dbs.getInventory()
        # Equip an item in Ted\'s inventory.
        itemToUnequip = arg.lower()
        inv = list(dbs.playerInv["EQUIPPED"])

        if itemToUnequip == '':
            print("Whatchoo wanna unequip?")
            return

        cantEquip = False

        for item in getAllItemsMatchingDesc(itemToUnequip, inv):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemInfo["TYPE"] != "weapon":
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print("Ted unequips " + itemInfo["SHORTDESC"])
            dbs.setWeapon("Fists")
            return

        if cantEquip:
            print("Ted can't unequip that...")
        else:
            print("Ted is confused by \"" + itemToUnequip + "\"")

    def do_addfx(self, arg):
        dbs.getInventory()
        # Add and effect to Ted's weapon.
        itemToAdd = arg.lower()
        inv = list(dbs.playerInv["ITEMS"])

        if itemToAdd == '':
            print("What's your tone, bro?")
            return

        cantAdd = False

        for item in getAllItemsMatchingDesc(itemToAdd, inv):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemInfo["TYPE"] != "fx":
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print("Ted adds " + itemInfo["SHORTDESC"])
            dbs.setFX(item)
            return

        if cantAdd:
            print("That's not an effect...")
        else:
            print("Ted is confused by \"" + itemToAdd + "\"")

    def do_delfx(self, arg):
        dbs.getInventory()
        # Equip an item in Ted\'s inventory.
        itemToUnequip = arg.lower()
        inv = list(dbs.playerInv["EQUIPPED"])

        if itemToUnequip == '':
            print("Whatchoo wanna unequip?")
            return

        cantEquip = False

        for item in getAllItemsMatchingDesc(itemToUnequip, inv):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemInfo["TYPE"] != "fx":
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print("Ted unequips " + itemInfo["SHORTDESC"])
            dbs.setFX("noFX")
            return

        if cantEquip:
            print("Ted can't unequip that...")
        else:
            print("Ted is confused by \"" + itemToUnequip + "\"")

    def do_save(self, arg):
        # Save the current state of the game to file.
        dbs.saveGame()

    def do_combat(self, arg):
        # Enter combat with a random enemy
        combat = combatMode()
        combat.fight()
