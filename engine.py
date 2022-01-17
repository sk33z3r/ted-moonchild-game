import os, sys, time, random, argparse, cmd, json, natsort

# check for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Turn on debug messages for various game calculations.", action="store_true")
parser.add_argument("-nc", "--nocolor", help="Turn off text styles and color.", action="store_true")
args = parser.parse_args()

# engine variables
NEXT_ACTION = 0 # 1 = player, 0 = enemy
global DEBUG
global COLORS
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

# setup the command prompt
RAW_PROMPT = "{FRED}\m/: {NORMAL}{FWHITE}"
PROMPT = RAW_PROMPT.format(**clr.styles)

import art
import database as dbs

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

def getEffectString(item):
    global effectString
    global itemInfo
    itemInfo = dbs.items.find_one( {"NAME": item } )
    check = ""
    try:
        check = itemInfo["EFFECT"]
    except KeyError:
        pass
    if check == "def":
        effectString = "[DEF+]"
    elif check == "atk":
        effectString = "[ATK+]"
    elif check == "mag":
        effectString = "[MAG+]"
    elif itemInfo["TYPE"] == "consumable":
        # setup vars
        s = itemInfo["EFFECT"][0]
        n = itemInfo["EFFECT"][1]
        o = itemInfo["EFFECT"][2]
        effectString = "[" + s + " " + o + str(n) + "]"
    elif itemInfo["TYPE"] == "weapon" or itemInfo["TYPE"] == "fx":
        effectString = "[+" + str(itemInfo["ATKBNS"]) + "]"
    else:
        effectString = ""

# COMBAT ENGINE
class combatMode():

    def selectEnemy(self):
        # Randomly selects an enemy and sets base stats
        global chosenEnemy
        global ratingInfo
        global ENEMYHP
        global ENEMYMP
        # set enemy list to ones available on the current planet
        planet = dbs.locationInfo["PLANET"]
        planetEnemies = dbs.enemies.find( { "PLANETS": planet } )
        enemyIDList = []
        for enemy in planetEnemies:
            enemyIDList.append(enemy["NAME"])
        if DEBUG == 1:
            print(planet)
            print(enemyIDList)
        if enemyIDList != []:
            # choose an enemy name at random from the list
            randEnemy = random.choice(enemyIDList)
            chosenEnemy = dbs.enemies.find_one( { "NAME": randEnemy } )
            ratingInfo = dbs.challenge_ratings.find_one( { "RATING": chosenEnemy["CR"] } )
            ENEMYHP = chosenEnemy["HP"]
            ENEMYMP = chosenEnemy["MP"]
            if DEBUG == 1:
                print(chosenEnemy)
                print(ratingInfo)
                time.sleep(2)
            return True
        else:
            return False

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

    def enemy(self):
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
        print("    i = item")
        print("    e = escape\n")
        battleChoice = input(PROMPT)
        if battleChoice == 'a':
            # Iterate over dictionary keys and print
            i = 1
            query = { "$and": [ { "TYPE": "physical" }, { "LEVEL": { "$lte": dbs.playerStats["LVL"] } } ] }
            attackList = dbs.abilities.find(query)
            attackIDList = [ "_index" ]
            print("\n{DIM}>>  {NORMAL}CHOOSE ATTACK:".format(**clr.styles))
            for item in attackList:
                print("    [" + str(i) + "] - " + item["NAME"])
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
                    heroAttackDamage += dbs.levelStats["CRITBNS"]
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
                playerMiss = random.randrange(1, 50)
                if DEBUG == 1:
                    print("\nMiss Check: {DIM}{MISS} (4 = true){NORMAL}\n".format(**clr.styles, MISS = str(playerMiss)))
                else:
                    pass
                if playerMiss > 40:
                    print("{FCYAN}{BRIGHT}A swing, and a miss!!{NORMAL}{FWHITE}".format(**clr.styles))
                else:
                    ENEMYHP = ENEMYHP - heroAttackDamage
                    if heroCrit == 5:
                        print("Ted packs a WOLLOP with his {ATK} for {FGREEN}{BRIGHT}{DMG}{NORMAL}{FWHITE} damage!!".format(**clr.styles, ATK = chosenAttackInfo["NAME"], DMG = str(heroAttackDamage)))
                    else:
                        print("Ted lands a blow with his {ATK} for {FGREEN}{BRIGHT}{DMG}{NORMAL}{FWHITE} damage!".format(**clr.styles, ATK = chosenAttackInfo["NAME"], DMG = str(heroAttackDamage)))
                time.sleep(2)
                # Set next action to enemy
                NEXT_ACTION = 0

        elif battleChoice == 'm':
            # Iterate over dictionary keys and print
            i = 1
            query = { "$and": [ { "TYPE": "magic" }, { "LEVEL": { "$lte": dbs.playerStats["LVL"] } } ] }
            magicList = list(dbs.abilities.find(query))

            if len(magicList) == 0:
                print("Ted doesn't have any magic to use in battle!")
                time.sleep(1)
                return

            magicIDList = [ "_index" ]
            print("\n{DIM}>>  {NORMAL}CHOOSE ABILITY:".format(**clr.styles))
            for item in magicList:
                print("    [" + str(i) + "] - " + item["NAME"])
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
                    time.sleep(2)
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
                    time.sleep(2)
                    # Set next action to enemy
                    NEXT_ACTION = 0

        elif battleChoice == 'i':
            # Iterate over dictionary keys and print
            i = 1
            battleItems = [ "_index" ]
            inv = list(dbs.playerInv["ITEMS"])

            if len(inv) == 0:
                print("Ted doesn't have any shit to use in battle!")
                time.sleep(1)
                return

            # first get a count of each distinct item in the inventory
            itemCount = {}
            for item in inv:
                if item in list(itemCount.keys()):
                    itemCount[item] += 1
                else:
                    itemCount[item] = 1

            print("\n{DIM}>>  {NORMAL}CHOOSE ITEM:".format(**clr.styles))
            # get a list of inventory items with duplicates removed:
            for item in set(inv):
                getEffectString(item)
                # If item is a duplicate, print once with the quantity in ()
                if itemCount[item] > 1:
                    print("{DIM}{FYELLOW}    [{I}] - {FWHITE}{NORMAL}{ITEM} ({COUNT}) {DIM}{FCYAN}{TEXT}{FWHITE}{NORMAL}".format(**clr.styles, I = str(i), ITEM = item, COUNT = str(itemCount[item]), TEXT = effectString))
                    battleItems.append(item)
                else:
                    print("{DIM}{FYELLOW}    [{I}] - {FWHITE}{NORMAL}{ITEM} {DIM}{FCYAN}{TEXT}{FWHITE}{NORMAL}".format(**clr.styles, I = str(i), ITEM = item, TEXT = effectString))
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
                    # do something with the item
                    # then drop the item from inventory
                    dbs.useItem(chosenItemInfo["NAME"])
                    time.sleep(2)
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

        elif battleChoice == "e":
            if random.randrange(1, 50) >= 25:
                print("{BRIGHT}{FGREEN}Ted got the fuck out of there, quick!{FWHITE}{NORMAL}".format(**clr.styles))
                time.sleep(1)
                if random.randrange(1, 100) >= 75:
                    lost = random.randrange(5, 50)
                    # Make sure the value doesn't go negative
                    if dbs.playerStats["FLOYDS"] <= lost:
                        lost = dbs.playerStats["FLOYDS"]
                        dbs.updateStat("FLOYDS", 0, "set")
                    else:
                        dbs.updateStat("FLOYDS", lost, "dec")
                    print("{BRIGHT}{FRED}Damn, Ted dropped some money! Lost {N} FLOYDS\nYou know have {C} FLOYDS in your pocket.{NORMAL}{FWHITE}".format(**clr.styles, N = lost, C = dbs.playerStats["FLOYDS"]))
                    time.sleep(2)
                NEXT_ACTION = 2
            else:
                print("{FRED}{BRIGHT}Ted tripped and fell, he couldn't escape!!{FWHITE}{NORMAL}".format(**clr.styles))
                time.sleep(2)
                NEXT_ACTION = 0

        else:
            inputError()
            # Set next action to player
            NEXT_ACTION = 1

    def death(self):
        # Determines if a player is dead
        dbs.getStats()
        if dbs.playerStats["HP"] <= 0:
            print("{FRED}{BRIGHT}The {NAME} beat the shit out of Ted!!{NORMAL}{FWHITE}".format(**clr.styles, NAME = chosenEnemy["NAME"]))
            time.sleep(2)
            clear()
            art.printLogo()
            print("{DIM}             =======================================".format(**clr.styles))
            print("{DIM}             |          {BRIGHT}{FRED}GAME OVER, MAN!{DIM}{FWHITE}            |".format(**clr.styles))
            print("{DIM}             ======================================={NORMAL}\n".format(**clr.styles))
            exit()
        elif ENEMYHP <= 0:
            clear()
            print("\n{FGREEN}{BRIGHT}Ted beat the fuck out of that {NAME}!!{NORMAL}{FWHITE}".format(**clr.styles, NAME = chosenEnemy["NAME"]))
            time.sleep(1)
            # calculate FLOYD reward
            floydAward = random.randrange(ratingInfo["FLOYDS"][0], ratingInfo["FLOYDS"][1])
            dbs.updateStat("FLOYDS", floydAward, "inc")
            print("{FGREEN}{DIM}Ted found {F} FLOYDS!".format(**clr.styles, F = str(floydAward)))
            time.sleep(1)
            # random item drop
            if random.randrange(1, 50) > 35:
                drop = random.choice(chosenEnemy["ITEMS"])
                if DEBUG == 1:
                    print("Item drop chance success. Item awarded: {ITEM}".format(**clr.styles, ITEM = drop))
                dbs.updateInv(drop, "add")
                print("{FCYAN}{DIM}Ted found {ITEM}!{NORMAL}{FWHITE}".format(**clr.styles, ITEM = dbs.items.find_one( { "NAME": drop } )["GROUNDDESC"]))
            else:
                if DEBUG == 1:
                    print("Item drop chance missed.")
            # apply XP gain
            dbs.updateStat("XP", ratingInfo["XPAWARD"], "inc")
            print("{FYELLOW}Ted has been awarded {XP} XP!{NORMAL}{FWHITE}".format(**clr.styles, XP = str(ratingInfo["XPAWARD"])))
            time.sleep(1)
            # check player level up
            playerXP = dbs.playerStats["XP"]
            nextLVL = dbs.playerStats["LVL"] + 1
            nextLVLStats = dbs.levels.find_one( { "LEVEL": nextLVL } )
            if playerXP >= nextLVLStats["XPREQ"]:
                dbs.updateStat("LVL", nextLVL, "set")
                dbs.updateStat("HPMAX", nextLVLStats["HPMAX"], "set")
                dbs.updateStat("HP", nextLVLStats["HPMAX"], "set")
                dbs.updateStat("MPMAX", nextLVLStats["MPMAX"], "set")
                dbs.updateStat("MP", nextLVLStats["MPMAX"], "set")
                print("{BRIGHT}{FYELLOW}Ted has reached level {LVL}!!{NORMAL}{FWHITE}".format(**clr.styles, LVL = str(dbs.playerStats["LVL"])))
                print(dbs.levels.find_one( { "LEVEL": dbs.playerStats["LVL"] } )["MSG"].format(**clr.styles) + "\n")
                TextAdventureCmd().do_stats("show")
            else:
                if DEBUG == 1:
                    print("Ted's XP level is below the requirement for next level.")
            time.sleep(3)
            return False
        else:
            return True

    def fight(self):
        dbs.getStats()
        # Actually drives the battle
        global NEXT_ACTION
        # Randomly select an enemy.
        if self.selectEnemy() == False:
            if DEBUG == 1:
                print("No enemies on current planet.")
            return False
        clear()
        print("{FRED}{BRIGHT}".format(**clr.styles))
        print("    An enemy has challenged Ted!\n")
        print("{DIM}{FBLACK}{BYELLOW}                                    ".format(**clr.styles))
        print("    ////////////////////////////    ")
        print("    //  {BRIGHT}ENTERING COMBAT MODE{DIM}  //    ".format(**clr.styles))
        print("    ////////////////////////////    ")
        print("                                    {BBLACK}{NORMAL}{FWHITE}".format(**clr.styles))
        time.sleep(2)
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
                self.enemy()
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
                enemyCrit = random.randrange(1, 50)
                if DEBUG == 1:
                    print("{DIM}  >CRIT Check:   {CRIT} (5 = true){NORMAL}{FWHITE}".format(**clr.styles, CRIT = str(enemyCrit)))
                else:
                    pass
                if enemyCrit > 40:
                    enemyAttack += ratingInfo["CRITBNS"]
                else:
                    pass
                if DEBUG == 1:
                    print("{DIM} DMG + CRIT:     {ATK}{NORMAL}{FWHITE}".format(**clr.styles, ATK = str(enemyAttack)))
                else:
                    pass
                enemyMiss = random.randrange(1, 50)
                if DEBUG == 1:
                    print("\nMiss Check: " + str(enemyMiss) + " (4 = true)\n")
                else:
                    pass
                if enemyMiss > 40:
                    print("{FCYAN}{BRIGHT}The {NAME} missed like a dangus!{NORMAL}{FWHITE}".format(**clr.styles, NAME = chosenEnemy["NAME"]))
                else:
                    dbs.updateStat("HP", enemyAttack, "dec")
                    # Chooses a random attack dialog line.
                    print("{FGREEN}{DIAG}{FWHITE}\n".format(**clr.styles, DIAG = chosenEnemy["DIALOG"][random.randrange(0, dialogSelection)]))

                    if enemyCrit == 5:
                        print("Ted takes a whopping {FRED}{BRIGHT}{ATK}{NORMAL}{FWHITE} damage!!".format(**clr.styles, ATK = str(enemyAttack)))
                    else:
                        print("Ted suffers {FRED}{BRIGHT}{ATK}{NORMAL}{FWHITE} damage!".format(**clr.styles, ATK = str(enemyAttack)))

                time.sleep(2)
                # Set next action to player
                NEXT_ACTION = 1
            elif NEXT_ACTION == 1:
                # Print battle HUD.
                self.HUD()
                # Print description of enemy.
                self.enemy()
                # Print menu
                self.battleMenu()
            elif NEXT_ACTION == 2:
                # Exit battle
                break

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

    g = list(locInfo["GROUND"])
    g = natsort.natsorted(g)

    # first get a count of each distinct item in the inventory
    itemCount = {}
    for item in g:
        if item in list(itemCount.keys()):
            itemCount[item] += 1
        else:
            itemCount[item] = 1

    # Print all the items on the ground.
    if len(g) > 0:
        print("{DIM}---  GROUND  ITEMS  ---{NORMAL}{FWHITE}".format(**clr.styles))
        for item in set(g):
            if itemCount[item] > 1:
                print("  {GROUNDDESC} ({COUNT})".format(**clr.styles, GROUNDDESC = dbs.items.find_one( { "NAME": item } )["GROUNDDESC"], COUNT = itemCount[item]))
            else:
                print("  {GROUNDDESC}".format(**clr.styles, GROUNDDESC = dbs.items.find_one( { "NAME": item } )["GROUNDDESC"]))
    print("")
    # Print all the exits.
    exits = []
    for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
        if direction in list(locInfo):
            exits.append(direction.title())

    if dbs.playerPrefs["EXITS"] == "full":
        print("{DIM}---  NEARBY  EXITS  ---{NORMAL}".format(**clr.styles))
        for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
            if direction in dbs.locationInfo:
                print("  " + direction.title() + ": " + dbs.locationInfo[direction])
    else:
        print("{DIM}Exits: {NORMAL}{JOIN}".format(**clr.styles, JOIN = ' '.join(exits)))
    print("")

def moveDirection(direction):
    # A helper function that changes the location of the player.

    combatCheck = random.randrange(1, 50)

    if direction in dbs.locationInfo:
        if combatCheck > 40:
            combatMode().fight()
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

        i = list(dbs.playerInv["ITEMS"])
        k = list(dbs.playerInv["KEY_ITEMS"])
        e = list(dbs.playerInv["EQUIPPED"])

        i = natsort.natsorted(i)
        k = natsort.natsorted(k)
        e = natsort.natsorted(e)

        if len(i) == 0 and len(k) == 0 and len(e) == 0:
            print("Ted doesn't have shit.")
            return

        # first get a count of each distinct item in the inventory
        itemCount = {}
        for item in i:
            if item in list(itemCount.keys()):
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        print("{DIM}--------- INV ---------{NORMAL}{FWHITE}".format(**clr.styles))

        if len(i) != 0:
            for item in set(i):
                getEffectString(item)
                # print the info
                if itemCount[item] > 1:
                    print("  " + item + " (" + str(itemCount[item]) + ") {DIM}{FCYAN}{TEXT}{FWHITE}{NORMAL}".format(**clr.styles, TEXT = effectString))
                else:
                    print("  " + item + " {DIM}{FCYAN}{TEXT}{FWHITE}{NORMAL}".format(**clr.styles, TEXT = effectString))
            print("")

        if len(e) != 0:
            print("{DIM}  [EQUIPMENT]{NORMAL}".format(**clr.styles))
            for item in set(e):
                print("  {FCYAN}{ITEM} {DIM}[+{N}]{FWHITE}{NORMAL}".format(**clr.styles, ITEM = item, N = str(dbs.items.find_one( {"NAME": item } )["ATKBNS"])))
            print("")

        if len(k) != 0:
            print("{DIM}  [KEY ITEMS]{NORMAL}".format(**clr.styles))
            for item in set(k):
                print("  {FYELLOW}{ITEM}{FWHITE}".format(**clr.styles, ITEM = item))

        print("{DIM}======================={NORMAL}{FWHITE}".format(**clr.styles))

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
            print(dbs.items.find_one( { "NAME": item } )["LONGDESC"].format(**clr.styles))
            return

        # see if the item being looked at is in the inventory
        tempInv()

        item = getFirstItemMatchingDesc(lookingAt, inv)
        if item != None:
            print(dbs.items.find_one( { "NAME": item } )["LONGDESC"].format(**clr.styles))
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

        print("{DIM}--- STORE ---{NORMAL}{FWHITE}\n".format(**clr.styles))
        for item in dbs.locationInfo["SHOP"]:
            getEffectString(item)
            print("  " + item)
            print("{DIM}{FGREEN}  [FLOYDS: {C}] {FYELLOW}{TEXT}{FWHITE}".format(**clr.styles, C = str(itemInfo["VALUE"]), TEXT = effectString))
            print("  {INFO}{NORMAL}\n".format(**clr.styles, INFO = itemInfo["LONGDESC"]))

        print("{DIM}============={NORMAL}{FWHITE}".format(**clr.styles))

    def do_buy(self, arg):
        # buy <item>" - buy an item at the current location's shop.
        if "SHOP" not in dbs.locationInfo:
            print("Ain't shit to buy, Ted.")
            return

        dbs.getInventory()
        dbs.getStats()
        money = dbs.playerStats["FLOYDS"]
        itemToBuy = arg.lower()

        if itemToBuy == '':
            print("Gotta be more specific.{DIM} Type \"list\" to see items{NORMAL}{FWHITE}".format(**clr.styles))
            return

        item = getFirstItemMatchingDesc(itemToBuy, dbs.locationInfo["SHOP"])
        if item != None:
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if money >= itemInfo["VALUE"]:
                dbs.updateStat("FLOYDS", itemInfo["VALUE"], "dec")
                dbs.updateInv(item, "add")
                print("Ted just bought " + itemInfo["SHORTDESC"])
            elif money < itemInfo["VALUE"]:
                print("{FRED}You don't have enough money, Ted!{FWHITE}".format(**clr.styles))
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
        dbs.getStats()
        # "sell <item>" - sell an item at the current location's shop.
        if "SHOP" not in dbs.locationInfo:
            print("Ain't no one to sell it to.")
            return

        inv = list(dbs.playerInv["ITEMS"])
        itemToSell = arg.lower()

        if itemToSell == '':
            print("Whatchoo wanna sell?{DIM} Type \"inv\" to see items{NORMAL}{FWHITE}".format(**clr.styles))
            return
        elif itemToSell in dbs.playerInv["KEY_ITEMS"]:
            print("{FYELLOW}I don't think you want to sell that, it may come in handy later.{FWHITE}".format(**clr.styles))
            return
        elif itemToSell in dbs.playerInv["EQUIPPED"]:
            print("{FCYAN}You need to un-equip it first!{FWHITE}".format(**clr.styles))
            return

        for item in inv:
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemToSell in itemInfo["DESCWORDS"]:
                price = round(itemInfo["VALUE"] * 0.75)
                dbs.updateStat("FLOYDS", price, "inc")
                dbs.updateInv(item, "del")
                print("{FGREEN}Ted sold {ITEM} for {N} FLOYDS.{FWHITE}".format(**clr.styles, ITEM = itemInfo["SHORTDESC"], N = price))
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
            dbs.useItem(item)
            return

        if cantEat:
            print("Ted doesn't want to eat that...")
        else:
            print("Ted is confused by \"" + itemToEat + "\"")

    # map drink to eat
    do_drink = do_eat
    do_smoke = do_eat

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
        nextLVL = dbs.levelStats["LEVEL"] + 1
        nextLVLStats = dbs.levels.find_one( { "LEVEL": nextLVL } )
        print("{DIM}-------- STATS --------{NORMAL}{FWHITE}".format(**clr.styles))
        print("  HP: " + str(dbs.playerStats["HP"]) + "/" + str(dbs.playerStats["HPMAX"]))
        print("  MP: " + str(dbs.playerStats["MP"]) + "/" + str(dbs.playerStats["MPMAX"]))
        print("  {FYELLOW}Hero Level: ".format(**clr.styles) + str(dbs.playerStats["LVL"]))
        print("  Hero XP: {XP}/{NEXT}".format(**clr.styles, XP = str(dbs.playerStats["XP"]), NEXT = str(nextLVLStats["XPREQ"])))
        print("  {FGREEN}You have ".format(**clr.styles) + str(dbs.playerStats["FLOYDS"]) + " FLOYDS.")
        print("  {FWHITE}Equipped Weapon: ".format(**clr.styles) + dbs.equippedWeapon + " [+" + str(dbs.weaponInfo["ATKBNS"]) + "]")
        print("  Added FX: " + dbs.addedFX + " [+" + str(dbs.fxInfo["ATKBNS"]) + "]")
        print("{DIM}======================={NORMAL}{FWHITE}".format(**clr.styles))

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
            if itemInfo["TYPE"] != "weapon" and itemInfo["TYPE"] != "fx":
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print("Ted equips " + itemInfo["SHORTDESC"])
            if itemInfo["TYPE"] == "weapon":
                dbs.setWeapon(item)
            elif itemInfo["TYPE"] == "fx":
                dbs.setFX(item)
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
            if itemInfo["TYPE"] != "weapon" and itemInfo["TYPE"] != "fx":
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print("Ted unequips " + itemInfo["SHORTDESC"])
            if itemInfo["TYPE"] == "weapon":
                dbs.setWeapon("Fists")
            elif itemInfo["TYPE"] == "fx":
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
        combatMode().fight()

    do_fight = do_combat
