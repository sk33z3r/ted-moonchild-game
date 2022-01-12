import os, sys, time, random, argparse, cmd, textwrap, json
from colorama import Fore, Back, Style
import globalVars as vars
import database as dbs

# check for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Turn on debug messages for various game calculations.", action="store_true")
parser.add_argument("-nc", "--nocolor", help="Turn off text styles and color.", action="store_true")
parser.add_argument("-w", "--width", nargs=1, help="Specify console screen width.", type=int)
args = parser.parse_args()

# debug check
if args.debug:
    print("Debug mode engaged.")
    debug = 1
else:
    debug = 0

# color check
if args.nocolor:
    print("Entering Black & White mode.")
    colors = 0
else:
    colors = 1

# set screen width
if args.width:
    SCREEN_WIDTH = args.width[0]
else:
    SCREEN_WIDTH = 170

# setup the command prompt
if colors == 0:
    PROMPT = '\m/: '
else:
    PROMPT = Fore.RED + '\m/: ' + Style.NORMAL + Fore.WHITE

def setLocation(name):
    global location
    global locationInfo
    location = name
    locationInfo = dbs.rooms.find_one( { "NAME": location } )

def setWeapon(name):
    global equippedWeapon
    global weaponInfo
    equippedWeapon = name
    weaponInfo = dbs.items.find_one( {"NAME": name } )

def setFX(name):
    global addedFX
    global fxInfo
    addedFX = name
    fxInfo = dbs.items.find_one( {"NAME": name } )

def identify_os():
    """Identifies the OS."""
    system = sys.platform
    if system == "win32":
        return "cls"

    else:
        return "clear"


def clear():
    """Clears the terminal."""
    os.system(identify_os())


"""
These variables track where the player is and what is in their inventory.
The value in the location variable will always be a key in the world variable
and the value in the inventory list will always be a key in the worldItems
variable.
"""
# TODO create "New Game" save file and force a load every time a new game is selected
# engine variables
nextAction = 0 # 1 = player, 0 = enemy
location = "location"
locationInfo = "locationInfo"
equippedWeapon = "equippedWeapon"
weaponInfo = "weaponInfo"
addedFX = "addedFX"
fxInfo = "fxInfo"
inventory = ['Winnibego Keys', 'Protection']
showFullExits = True

# input error message
def inputError():
    if colors == 0:
        print('Damnit, Ted! That\'s not a valid input. Try again!')
    else:
        print(Style.BRIGHT + Fore.RED + 'Damnit, Ted! That\'s not a valid input. Try again!' + Style.NORMAL + Fore.WHITE)
    time.sleep(2)

# COMBAT ENGINE
class combatMode():

    def selectEnemy(self):
        # Randomly selects an enemy and sets base stats
        # TODO implement logic to only select enemies from the current planet
        global chosenEnemy
        enemyIDList = list(dbs.enemies.find( {}, { "NAME": 1 } ))
        chosenID = random.choice(enemyIDList)["_id"]
        chosenEnemy = dbs.enemies.find_one( { "_id": chosenID } )
        vars.ENEMYHP = chosenEnemy["HP"]
        vars.ENEMYMP = chosenEnemy["MP"]
        if debug == 1:
            print(chosenEnemy)
            time.sleep(2)

    def HUD(self):
        """Prints out the players HUD"""
        clear()
        print('')
        print(Style.DIM + '>>  ' + Style.BRIGHT + Fore.CYAN + 'TED MOONCHILD' + Fore.WHITE + Style.NORMAL)
        print('    HP: ' + str(vars.PLAYERHP))
        print('    MP: ' + str(vars.PLAYERMP))
        print('    WPN: ' + equippedWeapon + ' [+' + str(weaponInfo["ATKBNS"]) + ']')
        print('    FX: ' + addedFX + ' [+' + str(fxInfo["ATKBNS"]) + ']')
        print('')
        print(Style.DIM + '>>  ' + Style.BRIGHT + Fore.YELLOW + chosenEnemy["NAME"] + Fore.WHITE + Style.NORMAL)
        print('    HP: ' + str(vars.ENEMYHP))
        print('    MP: ' + str(vars.ENEMYMP))

    def story(self):
        # Prints description of enemy, dialog, ascii art.
        print('')
        print('    [IMAGE of ' + chosenEnemy["NAME"] + ']')
        print('')
        print('    ' + chosenEnemy["ENDESC"])
        print(Style.DIM + '+--------------------------------------------------------------------------------------------------+' + Style.NORMAL)
        print('')

    def battleMenu(self):
        # Prints out the battle system menu
        global enemyHP
        global nextAction
        print(Style.DIM + '>>  ' + Style.NORMAL + Fore.RED + 'BATTLE MENU:' + Fore.WHITE)
        print('    a = attack')
        print('    m = magic')
        print('    i = item')
        print('')
        battleChoice = input(PROMPT)
        if battleChoice == 'a':
            # Iterate over dictionary keys and print
            i = 1
            # Stores a list of all attacks in dict item as they are unordered.
            attackList = dbs.abilities.find( { "TYPE": "physical" } )
            attackIDList = [ "_index" ]
            print('')
            print(Style.DIM + '>> ' + Style.NORMAL + 'Choose an Attack')
            for item in attackList:
                print(' [' + str(i) + '] - ' + item["NAME"])
                attackIDList.append(item["_id"])
                i += 1
            print('')
            try:
                choice = int(input(PROMPT))
                chosenAttackInfo = dbs.abilities.find_one( { "_id": attackIDList[choice] } )
                if debug == 1:
                    print(chosenAttackInfo)
            except:
                inputError()
                # Set next action to player
                nextAction = 1
            else:
                heroAttackDamage = random.randrange(chosenAttackInfo["HEROMIN"], chosenAttackInfo["HEROMAX"])
                if debug == 1:
                    print('')
                    print('Hero Attack Calculator')
                    print(Style.DIM + ' Base DMG:       ' + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                # determine critical strike
                heroCrit = random.randrange(0, 6)
                if debug == 1:
                    print(Style.DIM + '  >CRIT Check:   ' + str(heroCrit) + ' (5 = true)' + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                if heroCrit == 5:
                    heroAttackDamage += int(vars.CRIT)
                else:
                    pass
                if debug == 1:
                    print(Style.DIM + ' DMG + CRIT:     ' + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                # Increase hero's attack damage by whatever attack bonus the weapon supplies.
                heroAttackDamage += weaponInfo["ATKBNS"]
                if debug == 1:
                    print(Style.DIM + ' DMG + WPN:      ' + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                heroAttackDamage += fxInfo["ATKBNS"]
                if debug == 1:
                    print(Style.DIM + ' DMG + FX:       ' + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                # MISS check, 4 = miss
                playerMiss = random.randrange(0,5)
                if debug == 1:
                    print('')
                    print('Miss Check: ' + Style.DIM + str(playerMiss) + '(4 = true)' + Style.NORMAL)
                    print('')
                else:
                    pass
                if playerMiss == 4:
                    print(Fore.CYAN + Style.BRIGHT + 'A swing, and a miss!!' + Style.NORMAL + Fore.WHITE)
                else:
                    vars.ENEMYHP = vars.ENEMYHP - heroAttackDamage
                    if heroCrit == 5:
                        print('Ted packs a WOLLOP with his ' + chosenAttackInfo["NAME"] + ' for ' + Fore.GREEN + Style.BRIGHT + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE + ' damage!!')
                    else:
                        print('Ted lands a blow with his ' + chosenAttackInfo["NAME"] + ' for ' + Fore.GREEN + Style.BRIGHT + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE + ' damage!')
                time.sleep(3)
                # Set next action to enemy
                nextAction = 0

        elif battleChoice == 'm':
            # TODO implement escape choice
            # Iterate over dictionary keys and print
            i = 1
            magicList = dbs.abilities.find( { "TYPE": "magic" } )
            magicIDList = [ "_index" ]
            print('')
            print(Style.DIM + '>> ' + Style.NORMAL + 'Choose an Ability')
            for item in magicList:
                print(' [' + str(i) + '] - ' + item["NAME"])
                magicIDList.append(item["_id"])
                i += 1
            print('')
            try:
                choice = int(input(PROMPT))
                chosenMagicInfo = dbs.abilities.find_one( { "_id": magicIDList[choice] } )
                if debug == 1:
                    print(chosenMagicInfo)
            except:
                inputError()
                # Set next action to player
                nextAction = 1
            else:
                if chosenMagicInfo["MPREQ"] > int(vars.PLAYERMP):
                    print('')
                    print('Ted doesn\'t have enough MP!')
                    # Set next action to player
                    nextAction = 1

                else:
                    heroMagicDamage = chosenMagicInfo["MAGDMG"]
                    # magic crit check, 10 = success
                    magicCrit = random.randrange(0,20)
                    if debug == 1:
                        print('')
                        print('Magic Crit Check: ' + str(magicCrit))
                        print('')
                    else:
                        pass
                    if magicCrit == 10:
                        heroMagicDamage += heroMagicDamage
                        vars.ENEMYHP = vars.ENEMYHP - heroMagicDamage
                        print('Ted totally ROCKED ' + chosenMagicInfo["NAME"] + ' for ' + Fore.CYAN + str(heroMagicDamage) + Style.NORMAL + Fore.WHITE + ' damage!!')
                    else:
                        vars.ENEMYHP = vars.ENEMYHP - heroMagicDamage
                        print('Ted performs ' + chosenMagicInfo["NAME"] + ' for ' + Fore.CYAN + str(heroMagicDamage) + Style.NORMAL + Fore.WHITE + ' damage!')
                    vars.PLAYERMP = int(vars.PLAYERMP) - chosenMagicInfo["MPREQ"]
                    time.sleep(3)
                    # Set next action to enemy
                    nextAction = 0

        elif battleChoice == 'i':
            # Iterate over dictionary keys and print
            i = 1
            battleItems = [ "_index" ]

            if len(inventory) == 0:
                print('Ted doesn\'t have shit.')
                return

            # first get a count of each distinct item in the inventory
            itemCount = {}
            for item in inventory:
                if item in list(itemCount.keys()):
                    itemCount[item] += 1
                else:
                    itemCount[item] = 1

            print('')
            print(Style.DIM + '>> ' + Style.NORMAL + 'Choose an Item')
            # get a list of inventory items with duplicates removed:
            for item in set(inventory):
                # If item is an equipped weapon, display a [e]
                if item == equippedWeapon:
                    print((Style.DIM + Fore.YELLOW + ' [' + str(i) + '] - ' + Fore.WHITE + Style.NORMAL + '  ' + item + ' [e]'))
                    battleItems.append(item)
                elif item == addedFX:
                    print((Style.DIM + Fore.YELLOW + ' [' + str(i) + '] - ' + Fore.WHITE + Style.NORMAL + '  ' + item + ' [e]'))
                    battleItems.append(item)
                elif itemCount[item] > 1:
                    print((Style.DIM + Fore.YELLOW + ' [' + str(i) + '] - ' + Fore.WHITE + Style.NORMAL + '  %s (%s)' % (item, itemCount[item])))
                    battleItems.append(item)
                else:
                    print((Style.DIM + Fore.YELLOW + ' [' + str(i) + '] - ' + Fore.WHITE + Style.NORMAL + '  ' + item))
                    battleItems.append(item)
                i += 1
            print('')
            try:
                choice = int(input(PROMPT))
                chosenItemInfo = dbs.items.find_one( { "NAME": battleItems[choice] } )
                if debug == 1:
                    print(chosenItemInfo)
            except:
                inputError()
                # Set next action to player
                nextAction = 1
            else:
                try:
                    check = chosenItemInfo["BATTLE"]
                except KeyError:
                    pass
                else:
                    if chosenItemInfo["BATTLE"] == True:
                        # TODO do something with the item
                        # then drop the item from inventory
                        inventory.remove(chosenItemInfo["NAME"])
                        print('')
                        print('Ted uses ' + chosenItemInfo["NAME"] + '! Too bad item effects aren\'t implemented yet.')
                        print('The ' + chosenItemInfo["NAME"] + ' is still used up, though ;)')
                        time.sleep(3)
                        # Set next action to enemy
                        nextAction = 0
                try:
                    check = chosenItemInfo["WEAPON"]
                except KeyError:
                    pass
                else:
                    if chosenItemInfo["WEAPON"] == True and chosenItemInfo["NAME"] != equippedWeapon:
                        print('')
                        print('Equip it first, then use an attack!')
                        time.sleep(2)
                        # Set next action to player
                        nextAction = 1
                    else:
                        pass
                try:
                    check = chosenItemInfo["FX"]
                except KeyError:
                    pass
                else:
                    if chosenItemInfo["FX"] == True and chosenItemInfo["NAME"] != addedFX:
                        print('')
                        print('Equip it first, then use an attack!')
                        time.sleep(2)
                        # Set next action to player
                        nextAction = 1
                    else:
                        pass
                if chosenItemInfo["NAME"] == addedFX:
                    print('Use Ted\'s attack instead!')
                    # Set next action to player
                    nextAction = 1
                elif chosenItemInfo["NAME"] == equippedWeapon:
                    print('Use Ted\'s attack instead!')
                    # Set next action to player
                    nextAction = 1
                else:
                    print('')
                    print('Ted, this isn\'t the time!')
                    time.sleep(2)
                    # Set next action to player
                    nextAction = 1

        else:
            inputError()
            # Set next action to player
            nextAction = 1

    def death(self):
        # Determines if a player is dead
        # TODO implement XP award system based on chosenEnemy's challenge rating
        if int(vars.PLAYERHP) <= 0:
            print(Fore.RED + Style.BRIGHT + 'The ' + chosenEnemy["NAME"] + ' beat the shit out of Ted!!' + Style.NORMAL + Fore.WHITE)
            time.sleep(3)
            return False
        elif vars.ENEMYHP <= 0:
            print(Fore.GREEN + Style.BRIGHT + 'Ted beat the fuck out of that ' + chosenEnemy["NAME"] + '!!' + Style.NORMAL + Fore.WHITE)
            time.sleep(3)
            return False
        else:
            return True

    def fight(self):
        # Actually drives the battle
        global nextAction
        # Randomly select an enemy.
        self.selectEnemy()
        nextAction = random.randrange(0, 2)  # Randomly select who attacks first.
        # Changes color to white
        print(Fore.WHITE)
        while True:
            death = self.death()
            if death == False:
                break
            elif nextAction == 0:
                # Print battle HUD.
                self.HUD()
                # Print description of enemy.
                self.story()
                # Get's length of attack dialog list.
                dialogSelection = len(chosenEnemy["DIALOG"])
                # Randomly chooses damage caused based on min and max defined values.
                enemyAttack = random.randrange(chosenEnemy["ATTACKMIN"], chosenEnemy["ATTACKMAX"])
                if debug == 1:
                    print('Enemy Attack Calculator')
                    print(Style.DIM + ' Base DMG:       ' + str(enemyAttack) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                # determine critical strike
                enemyCrit = random.randrange(0, 10)
                if debug == 1:
                    print(Style.DIM + '  >CRIT Check:   ' + str(enemyCrit) + ' (5 = true)' + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                if enemyCrit == 5:
                    enemyAttack += chosenEnemy["CRITBNS"]
                else:
                    pass
                if debug == 1:
                    print(Style.DIM + ' DMG + CRIT:     ' + str(enemyAttack) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                enemyMiss = random.randrange(0, 5)
                if debug == 1:
                    print('')
                    print('Miss Check: ' + str(enemyMiss) + '(4 = true)')
                    print('')
                else:
                    pass
                if enemyMiss == 4:
                    print(Fore.CYAN + Style.BRIGHT + 'The ' + chosenEnemy["NAME"] + ' missed like a dangus!' + Style.NORMAL + Fore.WHITE)
                else:
                    vars.PLAYERHP = int(vars.PLAYERHP) - enemyAttack
                    # Chooses a random attack dialog line.
                    print(Fore.GREEN + chosenEnemy["DIALOG"][random.randrange(0, dialogSelection)] + Fore.WHITE)
                    print('')

                    if enemyCrit == 5:
                        print('Ted takes a whopping ' + Fore.RED + Style.BRIGHT + str(enemyAttack) + Style.NORMAL + Fore.WHITE + ' damage!!')
                    else:
                        print('Ted suffers ' + Fore.RED + Style.BRIGHT + str(enemyAttack) + Style.NORMAL + Fore.WHITE + ' damage!')

                time.sleep(3)
                # Set next action to player
                nextAction = 1
            elif nextAction == 1:
                # Print battle HUD.
                self.HUD()
                # Print description of enemy.
                self.story()
                # Print menu
                self.battleMenu()

def openSave():
    global location
    global inventory
    global addedFX
    global equippedWeapon
    if os.path.exists('./save.txt') == True:
        f = open('save.txt', 'r')
        location = f.readline()
        location = location.replace('\n', '')
        inventoryTemp = f.readline()
        inventoryTemp = inventoryTemp.replace(', ', ',')
        inventoryTemp = inventoryTemp.replace('\n', '')
        inventory = inventoryTemp.split(',')
        equippedWeapon = f.readline()
        equippedWeapon = equippedWeapon.replace('\n', '')
        addedFX = f.readline()
        addedFX = addedFX.replace('\n', '')
        vars.PLAYERHP = f.readline()
        vars.PLAYERHP = vars.PLAYERHP.replace('\n', '')
        vars.PLAYERMP = f.readline()
        vars.PLAYERMP = vars.PLAYERMP.replace('\n', '')
        vars.PLAYERLVL = f.readline()
        vars.PLAYERLVL = vars.PLAYERLVL.replace('\n', '')
        vars.PLAYERXP = f.readline()
        vars.PLAYERXP = vars.PLAYERXP.replace('\n', '')
        vars.FLOYDS = f.readline()
        vars.FLOYDS = vars.FLOYDS.replace('\n', '')
        f.close()
        setWeapon(equippedWeapon)
        setFX(addedFX)
        setLocation(location)
        print(Style.BRIGHT + Fore.GREEN + 'Huzzah, we loaded the game!' + Style.NORMAL + Fore.WHITE)
        time.sleep(1)
    else:
        print(Style.BRIGHT + Fore.RED + 'There is no save game! Moving on any way.' + Style.NORMAL + Fore.WHITE)
        time.sleep(1)

def saveState():
    global location
    global inventory
    global equippedWeapon
    global addedFX
    if os.path.exists('./save.txt') == True:
        print(Fore.RED + Style.BRIGHT + 'WARNING: Save Game Exists. Overwrite? (y/n)' + Style.NORMAL + Fore.WHITE)
        check = input(PROMPT)
        if check == 'y':
            s = Style.BRIGHT + Fore.GREEN + 'Save game overwritten!' + Style.NORMAL + Fore.WHITE
        else:
            print(Style.BRIGHT + Fore.RED + 'Save aborted.' + Style.NORMAL + Fore.WHITE)
            return
    else:
        s = Style.BRIGHT + Fore.GREEN + 'Save game created!' + Style.NORMAL + Fore.WHITE
    inventoryTemp = str(inventory)
    inventoryTemp = inventoryTemp.replace('\'', '')
    inventoryTemp = inventoryTemp.replace('[', '')
    inventoryTemp = inventoryTemp.replace(']', '')
    inventoryTemp = inventoryTemp.replace(', ', ',')
    f = open('save.txt', 'w')
    f.write(str(location))
    f.write('\n')
    f.write(inventoryTemp)
    f.write('\n')
    f.write(str(equippedWeapon))
    f.write('\n')
    f.write(str(addedFX))
    f.write('\n')
    f.write(str(vars.PLAYERHP))
    f.write('\n')
    f.write(str(vars.PLAYERMP))
    f.write('\n')
    f.write(str(vars.PLAYERLVL))
    f.write('\n')
    f.write(str(vars.PLAYERXP))
    f.write('\n')
    f.write(str(vars.FLOYDS))
    f.write('\n')
    f.close()
    print(s)
    time.sleep(1)

def displayLocation(loc):
    # A helper function for displaying an area's description and exits.
    clear()
    locInfo = dbs.rooms.find_one( { "NAME": loc } )
    # Print the room name.
    print(loc)
    print(('=' * len(loc)))

    # Print the room's description (using textwrap.wrap())
    print(locInfo["DESC"])

    # Print all the items on the ground.
    if len(locInfo["GROUND"]) > 0:
        print(Style.DIM + '--- ITEMS ON GROUND ---' + Style.NORMAL + Fore.WHITE)
        for item in locInfo["GROUND"]:
            print(('  ' + dbs.items.find_one( { "NAME": item } )["GROUNDDESC"]))

    # Print all the exits.
    exits = []
    for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
        if direction in list(locInfo):
            exits.append(direction.title())
    print(Style.DIM + '=======================' + Style.NORMAL + Fore.WHITE)
    print('\n')
    if showFullExits:
        for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
            if direction in locationInfo:
                print(('%s: %s' % (direction.title(), locationInfo[direction])))
    else:
        print(('Exits: %s' % ' '.join(exits)))


def moveDirection(direction):
    # A helper function that changes the location of the player.
    global location
    global locationInfo

    combatCheck = random.randrange(0,6)

    if direction in locationInfo:
        if combatCheck == 5:
            clear()
            print(Fore.RED + Style.BRIGHT)
            print('    An enemy has challenged Ted!\n')
            print(Style.DIM + Fore.BLACK + Back.YELLOW + '                                    ')
            print('    ////////////////////////////    ')
            print('    //  ' + Style.BRIGHT + 'ENTERING COMBAT MODE' + Style.DIM + '  //    ')
            print('    ////////////////////////////    ')
            print('                                    ' + Back.BLACK + Style.NORMAL + Fore.WHITE)
            time.sleep(3)
            combat = combatMode()
            combat.fight()
            setLocation(locationInfo[direction])
            displayLocation(location)
        else:
            setLocation(locationInfo[direction])
            displayLocation(location)
    else:
        print('Ted can\'t walk through walls.')


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
        print('Ted\'s feeble brain doesn\'t understand.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        # Quit the game.
        return True # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

# These direction commands have a long (i.e. north) and show (i.e. n) form.
    # Since the code is basically the same, I put it in the moveDirection()
    # function.
    def do_north(self, arg):
        # Go to the area to the north, if possible.
        moveDirection('NORTH')

    def do_south(self, arg):
        # Go to the area to the south, if possible.
        moveDirection('SOUTH')

    def do_east(self, arg):
        # Go to the area to the east, if possible.
        moveDirection('EAST')

    def do_west(self, arg):
        # Go to the area to the west, if possible.
        moveDirection('WEST')

    def do_up(self, arg):
        # Go to the area upwards, if possible.
        moveDirection('UP')

    def do_down(self, arg):
        #Go to the area downwards, if possible.
        moveDirection('DOWN')

    # Since the code is the exact same, we can just copy the
    # methods with shortened names:
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down

    def do_exits(self, arg):
        # Toggle showing full exit descriptions or brief exit descriptions.
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing full exit descriptions.')
        else:
            print('Showing brief exit descriptions.')

    def do_inventory(self, arg):
        # Display a list of the items in Ted\'s possession.

        if len(inventory) == 0:
            print('Ted doesn\'t have shit.')
            return

        # first get a count of each distinct item in the inventory
        itemCount = {}
        for item in inventory:
            if item in list(itemCount.keys()):
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # get a list of inventory items with duplicates removed:
        print(Style.DIM + '---- INV ----' + Style.NORMAL + Fore.WHITE)
        for item in set(inventory):
            # If item is an equipped weapon, display a [e]
            if item == equippedWeapon:
                print(('  ' + item + ' [e]'))
            elif item == addedFX:
                print(('  ' + item + ' [e]'))
            elif itemCount[item] > 1:
                print(('  %s (%s)' % (item, itemCount[item])))
            else:
                print(('  ' + item))
        print(Style.DIM + '=============' + Style.NORMAL + Fore.WHITE)

    do_inv = do_inventory


    def do_take(self, arg):
        # take <item> - Take an item on the ground.
        # put this value in a more suitably named variable
        itemToTake = arg.lower()

        if itemToTake == '':
            print('What should Ted take?')
            return

        cantTake = False

        # get the item name that the player's command describes
        for item in getAllItemsMatchingDesc(itemToTake, locationInfo["GROUND"]):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemInfo["TAKEABLE"] == False:
                cantTake = True
                continue # there may be other items named this that Ted can take, so we continue checking
            print(('Ted grabs %s.' % (itemInfo["SHORTDESC"])))
            dbs.rooms.update_one( { "NAME": location }, { "$pull": { "GROUND": item } } ) # remove from the ground
            setLocation(location)
            inventory.append(item) # add to inventory
            return

        if cantTake:
            print(('Ted doesn\'t want to grab "%s".' % (itemToTake)))
        else:
            print('Ted doesn\'t see that.')


    def do_drop(self, arg):
        # drop <item>" - Drop an item from Ted\'s inventory onto the ground.

        # put this value in a more suitably named variable
        itemToDrop = arg.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)

        # find out if the player doesn't have that item
        if itemToDrop not in invDescWords:
            print(('Ted\'s pockets don\'t have "%s".' % (itemToDrop)))
            return

        # get the item name that the player's command describes
        item = getFirstItemMatchingDesc(itemToDrop, inventory)
        if item != None:
            print(('Ted drops %s.' % (dbs.items.find_one( { "NAME": item } )["SHORTDESC"])))
            # add item to the ground
            groundTemp = list(locationInfo["GROUND"])
            groundTemp.append(item)
            dbs.rooms.update_one( { "NAME": location }, { "$set": { "GROUND": groundTemp } } )
            setLocation(location)
            inventory.remove(item) # remove from inventory

    def complete_take(self, text, line, begidx, endidx):
        possibleItems = []
        text = text.lower()

        # if the user has only typed "take" but no item name:
        if not text:
            return getAllFirstDescWords(locationInfo["GROUND"])

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for item in list(set(locationInfo["GROUND"])):
            for descWord in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
                if descWord.startswith(text) and dbs.items.find_one( { "NAME": item } )["TAKEABLE"] == True:
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def complete_drop(self, text, line, begidx, endidx):
        possibleItems = []
        itemToDrop = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)

        for descWord in invDescWords:
            if line.startswith('drop %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "drop" but no item name:
        if itemToDrop == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(text):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_look(self, arg):
        # Look at an item, direction, or the area:
        # "look" - display the current area's description
        # "look <direction>" - display the description of the area in that direction
        # "look exits" - display the description of all adjacent areas
        # "look <item>" - display the description of an item on the ground or in Ted's inventory

        lookingAt = arg.lower()
        if lookingAt == '':
            # "look" will re-print the area description
            displayLocation(location)
            return

        if lookingAt == 'exits':
            for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
                if direction in locationInfo:
                    print(('%s: %s' % (direction.title(), locationInfo[direction])))
            return

        if lookingAt in ('north', 'west', 'east', 'south', 'up', 'down', 'n', 'w', 'e', 's', 'u', 'd'):
            if lookingAt.startswith('n') and "NORTH" in locationInfo:
                print((locationInfo["NORTH"]))
            elif lookingAt.startswith('w') and "WEST" in locationInfo:
                print((locationInfo["WEST"]))
            elif lookingAt.startswith('e') and "EAST" in locationInfo:
                print((locationInfo["EAST"]))
            elif lookingAt.startswith('s') and "SOUTH" in locationInfo:
                print((locationInfo["SOUTH"]))
            elif lookingAt.startswith('u') and "UP" in locationInfo:
                print((locationInfo["UP"]))
            elif lookingAt.startswith('d') and "DOWN" in locationInfo:
                print((locationInfo["DOWN"]))
            else:
                print('Ted can\'t walk through walls.')
            return

        # see if the item being looked at is on the ground at this location
        item = getFirstItemMatchingDesc(lookingAt, locationInfo["GROUND"])
        if item != None:
            print(('\n'.join(textwrap.wrap(dbs.items.find_one( { "NAME": item } )["LONGDESC"], SCREEN_WIDTH))))
            return

        # see if the item being looked at is in the inventory
        item = getFirstItemMatchingDesc(lookingAt, inventory)
        if item != None:
            print(('\n'.join(textwrap.wrap(dbs.items.find_one( { "NAME": item } )["LONGDESC"], SCREEN_WIDTH))))
            return

        print('Ted scours to room, but he doesn\'t see that.')


    def complete_look(self, text, line, begidx, endidx):
        possibleItems = []
        lookingAt = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)
        groundDescWords = getAllDescWords(locationInfo["GROUND"])
        shopDescWords = getAllDescWords(locationInfo["SHOP"])

        for descWord in invDescWords + groundDescWords + shopDescWords + ["north", "south", "east", "west", "up", "down"]:
            if line.startswith('look %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "look" but no item name, show all items on ground, shop and directions:
        if lookingAt == '':
            possibleItems.extend(getAllFirstDescWords(locationInfo["GROUND"]))
            possibleItems.extend(getAllFirstDescWords(locationInfo["SHOP"]))
            for direction in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"):
                if direction in locationInfo:
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
        if "SHOP" not in locationInfo:
            print('Ain\'t no store here, Ted.')
            return

        arg = arg.lower()

        print((Style.DIM + '--- STORE ---' + Style.NORMAL + Fore.WHITE))
        for item in locationInfo["SHOP"]:
            itemInfo = dbs.items.find_one( { "NAME": item } )
            print(('  %s' % (item)))
            print(('  ' + Style.DIM + '\n  '.join(textwrap.wrap(itemInfo["LONGDESC"], SCREEN_WIDTH)) + Style.NORMAL + Fore.WHITE))
            if arg == 'full':
                print((Style.DIM + '\n'.join(textwrap.wrap(itemInfo["LONGDESC"], SCREEN_WIDTH)) + Style.NORMAL + Fore.WHITE))

        print((Style.DIM + '=============' + Style.NORMAL + Fore.WHITE))


    def do_buy(self, arg):
        # buy <item>" - buy an item at the current location's shop.
        if "SHOP" not in locationInfo:
            print('Ain\'t shit to buy, Ted.')
            return

        itemToBuy = arg.lower()

        if itemToBuy == '':
            print(('Gotta be more specific.' + Style.DIM + ' Type "list" to see items' + Style.NORMAL + Fore.WHITE))
            return

        item = getFirstItemMatchingDesc(itemToBuy, locationInfo["SHOP"])
        if item != None:
            # NOTE - If Ted wanted to implement money, here is where Ted would add
            # code that checks if the player has enough, then deducts the price
            # from their money.
            print(('Ted just bought %s' % (dbs.items.find_one( { "NAME": item } )["SHORTDESC"])))
            inventory.append(item)
            return

        print(('They don\'t have any "%s". Try again, Ted.' % (itemToBuy)))


    def complete_buy(self, text, line, begidx, endidx):
        if "SHOP" not in locationInfo:
            return []

        itemToBuy = text.lower()
        possibleItems = []

        # if the user has only typed "buy" but no item name:
        if not itemToBuy:
            return getAllFirstDescWords(locationInfo["SHOP"])

        # otherwise, get a list of all "description words" for shop items matching the command text so far:
        for item in list(set(locationInfo["SHOP"])):
            for descWord in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_sell(self, arg):
        # "sell <item>" - sell an item at the current location's shop.
        if "SHOP" not in locationInfo:
            print('Ain\'t no one to sell it.')
            return

        itemToSell = arg.lower()

        if itemToSell == '':
            print(('Whatchoo wanna sell?' + Style.DIM + ' Type "inv" to see items' + Style.NORMAL + Fore.WHITE))
            return

        for item in inventory:
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemToSell in itemInfo["DESCWORDS"]:
                # NOTE - If Ted wanted to implement money, here is where Ted would add
                # code that gives the player money for selling the item.
                print(('Ted sold %s' % (itemInfo["SHORTDESC"])))
                inventory.remove(item)
                return

        print(('You don\'t have "%s", Ted.' % (itemToSell)))


    def complete_sell(self, text, line, begidx, endidx):
        if "SHOP" not in locationInfo:
            return []

        itemToSell = text.lower()
        possibleItems = []

        # if the user has only typed "sell" but no item name:
        if not itemToSell:
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in dbs.items.find_one( { "NAME": item } )["DESCWORDS"]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_eat(self, arg):
        # "eat <item>" - eat an item in Ted\'s inventory."""
        itemToEat = arg.lower()

        if itemToEat == '':
            print('Whatchoo wanna eat?')
            return

        cantEat = False

        for item in getAllItemsMatchingDesc(itemToEat, inventory):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            try:
                check = itemInfo["EDIBLE"]
            except KeyError:
                cantEat = True
                continue # there may be other items named this that Ted can eat, so we continue checking
            print(('Ted eats %s' % (itemInfo["SHORTDESC"])))
            inventory.remove(item)
            return

        if cantEat:
            print('Ted doesn\'t want to eat that...')
        else:
            print(('Ted is confused by "%s".' % (itemToEat)))

    def complete_eat(self, text, line, begidx, endidx):
        itemToEat = text.lower()
        possibleItems = []

        # if the user has only typed "eat" but no item name:
        if itemToEat == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for edible inventory items matching the command text so far:
        for item in list(set(inventory)):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            for descWord in itemInfo["DESCWORDS"]:
                if descWord.startswith(text) and itemInfo["EDIBLE"] == False:
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_stats(self, arg):
        # Display player stats, weapon, and accessory
        print(Style.DIM + '--- Stats ---' + Style.NORMAL + Fore.WHITE)
        print('  HP: ' + str(vars.PLAYERHP) + '/ MP: ' + str(vars.PLAYERMP))
        print('  Hero Level: ' + str(vars.PLAYERLVL))
        print('  Hero XP: '+ str(vars.PLAYERXP))
        print('  You have ' + str(vars.FLOYDS) + ' Floyds.')
        print('  Equipped Weapon: ' + equippedWeapon + ' [+' + str(weaponInfo["ATKBNS"]) + ']')
        print('  Added FX: ' + addedFX + ' [+' + str(fxInfo["ATKBNS"]) + ']')
        print(Style.DIM + '=============' + Style.NORMAL + Fore.WHITE)

    def do_equip(self, arg):
        # Equip an item in Ted\'s inventory.
        global equippedWeapon
        itemToEquip = arg.lower()

        if itemToEquip == '':
            print('Whatchoo wanna equip?')
            return

        cantEquip = False

        for item in getAllItemsMatchingDesc(itemToEquip, inventory):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemInfo["WEAPON"] == False:
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print(('Ted equips %s' % (itemInfo["SHORTDESC"])))
            setWeapon(item)
            return

        if cantEquip:
            print('Ted can\'t equip that...')
        else:
            print(('Ted is confused by "%s".' % (itemToEquip)))

    def do_addfx(self, arg):
        # Add and effect to Ted's weapon.
        global addedFX
        itemToAdd = arg.lower()

        if itemToAdd == '':
            print('What\'s your tone, bro?')
            return

        cantAdd = False

        for item in getAllItemsMatchingDesc(itemToAdd, inventory):
            itemInfo = dbs.items.find_one( { "NAME": item } )
            if itemInfo["FX"] == False:
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print(('Ted adds %s' % (itemInfo["SHORTDESC"])))
            setFX(item)
            return

        if cantAdd:
            print('That\'s not an effect...')
        else:
            print(('Ted is confused by "%s".' % (itemToAdd)))

    def do_save(self, arg):
        # Save the current state of the game to file.
        saveState()

    def do_combat(self, arg):
        # Enter combat with a random enemy
        combat = combatMode()
        combat.fight()

def introAnimation():
    engine = dbs.engine.find_one( { "INTRO1": { "$regex": ".*" } } )
    clear()
    time.sleep(1)
    print(Style.BRIGHT + engine["INTRO1"] + '\n')
    time.sleep(2)
    clear()
    print(Style.DIM + engine["INTRO2"] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + engine["INTRO2"] + '\n')
    print(Style.DIM + engine["INTRO3"] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.BRIGHT + engine["INTRO2"] + '\n')
    print(Style.NORMAL + engine["INTRO3"] + '\n')
    print(Style.DIM + engine["INTRO4"] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + engine["INTRO2"] + '\n')
    print(Style.BRIGHT + engine["INTRO3"] + '\n')
    print(Style.NORMAL + engine["INTRO4"] + '\n')
    print(Style.DIM + engine["INTRO5"] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + engine["INTRO2"] + '\n')
    print(Style.NORMAL + engine["INTRO3"] + '\n')
    print(Style.BRIGHT + engine["INTRO4"] + '\n')
    print(Style.NORMAL + engine["INTRO5"] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + engine["INTRO2"] + '\n')
    print(Style.NORMAL + engine["INTRO3"] + '\n')
    print(Style.NORMAL + engine["INTRO4"] + '\n')
    print(Style.BRIGHT + engine["INTRO5"] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + engine["INTRO2"] + '\n')
    print(Style.NORMAL + engine["INTRO3"] + '\n')
    print(Style.NORMAL + engine["INTRO4"] + '\n')
    print(Style.NORMAL + engine["INTRO5"] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + engine["INTRO2"] + '\n')
    print(Style.NORMAL + engine["INTRO3"] + '\n')
    print(Style.NORMAL + engine["INTRO4"] + '\n')
    print(Style.NORMAL + engine["INTRO5"] + '\n')
    time.sleep(13)
    clear()
    print(Fore.YELLOW + Style.NORMAL + vars.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(0.5)
    clear()
    print(Fore.YELLOW + Style.BRIGHT + vars.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(1)
    clear()
    print(Fore.YELLOW + Style.NORMAL + vars.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.BRIGHT + vars.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(0.5)
    clear()
    print(Fore.YELLOW + Style.NORMAL + vars.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.BRIGHT + vars.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(1)
    clear()
    print(Fore.YELLOW + Style.NORMAL + vars.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(2)
    clear()

if __name__ == '__main__':

    print(Back.BLACK + Fore.WHITE)
    clear()
    print(Fore.YELLOW + Style.NORMAL + vars.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + vars.logo3 + Style.NORMAL + Fore.WHITE)
    print()
    print(Style.DIM + '             =======================================')
    print(Style.DIM + '             | ' + Style.NORMAL + 'Press ' + Fore.GREEN + 'n' + Fore.WHITE + ' to fucking ROCK a new story ' + Style.DIM + '|')
    print(Style.DIM + '             | ' + Style.NORMAL + 'Press ' + Fore.CYAN + 'l' + Fore.WHITE + ' to load your shitty save    ' + Style.DIM + '|')
    print(Style.DIM + '             =======================================' + Style.NORMAL)
    print('')
    holdOn = input(PROMPT)
    if holdOn == 'l':
        openSave()
        displayLocation(location)
        TextAdventureCmd().cmdloop()
    elif holdOn == 'n':
        introAnimation()
        dbs.initDB()
        setWeapon("Fists")
        setFX("noFX")
        setLocation("EBGB Stage")
        displayLocation(location)
        TextAdventureCmd().cmdloop()
    else:
        pass
    print('Thanks for ROCKIN\'!' + Style.NORMAL)
