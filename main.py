import os	#for clearing the terminal
import sys  # For OS identification
import asciiGFX  # Import all the ASCII graphics assets
import time # Import time for intro GFX
from colorama import Fore, Back, Style  # Used for text coloring
import random # For random number generation
import argparse # For passing command line args
import dictionaries
import globalVars as vars

# check for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Turn on debug messages for various game calculations.", action="store_true")
parser.add_argument("-nc", "--nocolor", help="Turn off text styles and color.", action="store_true")
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

PROMPT = Fore.RED + '\m/: ' + Style.NORMAL + Fore.WHITE

# engine variables
nextAction = 0 # 1 = player, 0 = enemy

# Battle system globals
enemyHP = 'hp'
enemyMP = 'mp'

# equipment status variables
# TODO make these default fallback values
equippedWeapon = 'Fists'
addedFX = 'noFX'

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
location = 'EBGB Stage'
inventory = ['Winnibego Keys', 'Protection']
showFullExits = True

import cmd, textwrap

# input error message
def inputError():
    print(Style.BRIGHT + Fore.RED + 'Damnit, Ted! That\'s not a valid input. Try again!' + Style.NORMAL + Fore.WHITE)
    time.sleep(2)

# COMBAT ENGINE
class combatMode():

    def selectEnemy(self):
        """Randomly selects an enemy"""
        global chosenEnemy
        allKeys = list(dictionaries.enemies.keys())
        chosenEnemy = random.choice(allKeys)
        print(chosenEnemy)

    def HUD(self):
        """Prints out the players HUD"""
        clear()
        print('')
        print(Style.DIM + '>>  ' + Style.BRIGHT + Fore.CYAN + 'TED MOONCHILD' + Fore.WHITE + Style.NORMAL)
        print('    HP: ' + str(vars.PLAYERHP))
        print('    MP: ' + str(vars.PLAYERMP))
        print('    WPN: ' + equippedWeapon + ' [+' + str(dictionaries.worldItems[equippedWeapon][vars.ATKBNS]) + ']')
        print('    FX: ' + addedFX + ' [+' + str(dictionaries.worldItems[addedFX][vars.ATKBNS]) + ']')
        print('')
        print(Style.DIM + '>>  ' + Style.BRIGHT + Fore.YELLOW + chosenEnemy + Fore.WHITE + Style.NORMAL)
        print('    HP: ' + str(enemyHP))
        print('    MP: ' + str(dictionaries.enemies[chosenEnemy][vars.MP]))

    def story(self):
        """Prints description of enemy, dialog, ascii art."""
        print('')
        print('    [IMAGE of ' + chosenEnemy + ']')
        print('')
        print('    ' + dictionaries.enemies[chosenEnemy][vars.ENDESC])
        print(Style.DIM + '+--------------------------------------------------------------------------------------------------+' + Style.NORMAL)
        print('')

    def battleMenu(self):
        """Prints out the battle system menu"""
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
            i = 0
            # Stores a list of all attacks in dict item as they are unordered.
            attackList = []
            print('')
            print(Style.DIM + '>> ' + Style.NORMAL + 'Choose an Attack')
            for item in list(dictionaries.heroAttacks.keys()):
                attackList.append(item)
                print(Style.DIM + Fore.YELLOW + ' [' + str(i) + '] - ' + Fore.WHITE + Style.NORMAL + item)
                i += 1
            print('')
            try:
                attackChoice = int(input(PROMPT))
                chosenAttack = attackList[int(attackChoice)]
            except:
                inputError()
                # Set next action to player
                nextAction = 1
            else:
                heroAttackDamage = random.randrange(dictionaries.heroAttacks[chosenAttack][vars.HEROMIN], dictionaries.heroAttacks[chosenAttack][vars.HEROMAX])
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
                heroAttackDamage += dictionaries.worldItems[equippedWeapon][int(vars.ATKBNS)]
                if debug == 1:
                    print(Style.DIM + ' DMG + WPN:      ' + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                heroAttackDamage += dictionaries.worldItems[addedFX][int(vars.ATKBNS)]
                if debug == 1:
                    print(Style.DIM + ' DMG + FX:       ' + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                # MISS check
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
                    enemyHP = enemyHP - heroAttackDamage
                    if heroCrit == 5:
                        print('Ted packs a WOLLOP with his ' + chosenAttack + ' for ' + Fore.GREEN + Style.BRIGHT + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE + ' damage!!')
                    else:
                        print('Ted lands a blow with his ' + chosenAttack + ' for ' + Fore.GREEN + Style.BRIGHT + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE + ' damage!')
                time.sleep(3)
                # Set next action to enemy
                nextAction = 0

        elif battleChoice == 'm':
            # TODO implement escape choice
            # Iterate over dictionary keys and print
            i = 0
            magicList = []
            print('')
            print(Style.DIM + '>> ' + Style.NORMAL + 'Choose an Ability')
            for item in list(dictionaries.heroMagic.keys()):
                magicList.append(item)
                print(Style.DIM + Fore.YELLOW + ' [' + str(i) + '] - ' + Fore.WHITE + Style.NORMAL + item + Fore.CYAN + ' [MP: ' + str(dictionaries.heroMagic[item][vars.MPREQ]) + ']' + Fore.WHITE)
                i += 1
            print('')
            try:
                magicChoice = int(input(PROMPT))
                chosenMagic = magicList[int(magicChoice)]
            except:
                inputError()
                # Set next action to player
                nextAction = 1
            else:
                if dictionaries.heroMagic[chosenMagic][vars.MPREQ] > int(vars.PLAYERMP):
                    print('')
                    print('Ted doesn\'t have enough MP!')
                    # Set next action to player
                    nextAction = 1

                else:
                    dictionaries.heroMagicDamage = dictionaries.heroMagic[chosenMagic][vars.MAGDMG]
                    # magic crit check
                    magicCrit = random.randrange(0,20)
                    if debug == 1:
                        print('')
                        print('Magic Crit Check: ' + str(magicCrit))
                        print('')
                    else:
                        pass
                    if magicCrit == 10:
                        dictionaries.heroMagicDamage += dictionaries.heroMagicDamage
                        enemyHP = enemyHP - dictionaries.heroMagicDamage
                        print('Ted totally ROCKED ' + chosenMagic + ' for ' + Fore.CYAN + str(dictionaries.heroMagicDamage) + Style.NORMAL + Fore.WHITE + ' damage!!')
                    else:
                        enemyHP = enemyHP - dictionaries.heroMagicDamage
                        print('Ted performs ' + chosenMagic + ' for ' + Fore.CYAN + str(dictionaries.heroMagicDamage) + Style.NORMAL + Fore.WHITE + ' damage!')
                    vars.PLAYERMP = int(vars.PLAYERMP) - dictionaries.heroMagic[chosenMagic][vars.MPREQ]
                    time.sleep(3)
                    # Set next action to enemy
                    nextAction = 0

        elif battleChoice == 'i':
            # Iterate over dictionary keys and print
            i = 0
            battleItems = []
            print('')
            print(Style.DIM + '>> ' + Style.NORMAL + 'Choose an Item')
            for item in inventory:
                battleItems.append(item)
                print(Style.DIM + Fore.YELLOW + ' [' + str(i) + '] - ' + Fore.WHITE + Style.NORMAL + item)
                i += 1
            print('')
            try:
                itemChoice = int(input(PROMPT))
                chosenItem = battleItems[int(itemChoice)]
            except:
                inputError()
                # Set next action to player
                nextAction = 1
            else:
                if dictionaries.worldItems[chosenItem].get(vars.BATTLE) == True:
                    # TODO do something with the item
                    # then drop the item from inventory
                    inventory.remove(chosenItem)
                    print('')
                    print('Ted uses ' + chosenItem + '! Too bad item effects aren\'t implemented yet.')
                    print('The ' + chosenItem + ' is still used up, though ;)')
                    time.sleep(3)
                    # Set next action to enemy
                    nextAction = 0
                elif chosenItem == addedFX:
                    print('Use Ted\'s attack instead!')
                    # Set next action to player
                    nextAction = 1
                elif chosenItem == equippedWeapon:
                    print('Use Ted\'s attack instead!')
                    # Set next action to player
                    nextAction = 1
                elif dictionaries.worldItems[chosenItem].get(vars.WEAPON) == True and chosenItem != equippedWeapon:
                    print('')
                    print('Equip it first, then use an attack!')
                    time.sleep(3)
                    # Set next action to player
                    nextAction = 1
                elif dictionaries.worldItems[chosenItem].get(vars.FX) == True and chosenItem != addedFX:
                    print('')
                    print('Equip it first, then use an attack!')
                    time.sleep(3)
                    # Set next action to player
                    nextAction = 1
                else:
                    print('')
                    print('Ted, this isn\'t the time!')
                    time.sleep(3)
                    # Set next action to player
                    nextAction = 1

        else:
            inputError()
            # Set next action to player
            nextAction = 1

    def death(self):
        """Determines if a player is dead"""
        # TODO implement XP award system based on chosenEnemy's challenge rating
        global enemyHP
        if int(vars.PLAYERHP) <= 0:
            print(Fore.RED + Style.BRIGHT + 'The ' + chosenEnemy + ' beat the shit out of Ted!!' + Style.NORMAL + Fore.WHITE)
            time.sleep(3)
            return False
        elif enemyHP <= 0:
            print(Fore.GREEN + Style.BRIGHT + 'Ted beat the fuck out of that ' + chosenEnemy + '!!' + Style.NORMAL + Fore.WHITE)
            time.sleep(3)
            return False
        else:
            return True

    def fight(self):
        """Actually drives the battle"""
        global enemyHP
        global nextAction
        # Randomly select an enemy.
        self.selectEnemy()
        enemyHP = dictionaries.enemies[chosenEnemy][vars.HP]
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
                dialogSelection = len(dictionaries.enemies[chosenEnemy][vars.DIALOG])
                # Randomly chooses damage caused based on min and max defined values.
                enemyAttack = random.randrange(dictionaries.enemies[chosenEnemy][vars.ATTACKMIN], dictionaries.enemies[chosenEnemy][vars.ATTACKMAX])
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
                    enemyAttack += dictionaries.enemies[chosenEnemy][int(vars.CRITBNS)]
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
                    print(Fore.CYAN + Style.BRIGHT + 'The ' + chosenEnemy + ' missed like a dangus!' + Style.NORMAL + Fore.WHITE)
                else:
                    vars.PLAYERHP = int(vars.PLAYERHP) - enemyAttack
                    # Chooses a random attack dialog line.
                    print(Fore.GREEN + dictionaries.enemies[chosenEnemy][vars.DIALOG][random.randrange(0, dialogSelection)] + Fore.WHITE)
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
    """A helper function for displaying an area's description and exits."""
    clear()
    # Print the room name.
    print(loc)
    print(('=' * len(loc)))

    # Print the room's description (using textwrap.wrap())
    print((dictionaries.worldRooms[loc][vars.DESC]))

    # Print all the items on the ground.
    if len(dictionaries.worldRooms[loc][vars.GROUND]) > 0:
        print(Style.DIM + '--- ITEMS ON GROUND ---' + Style.NORMAL + Fore.WHITE)
        for item in dictionaries.worldRooms[loc][vars.GROUND]:
            print(('  ' + dictionaries.worldItems[item][vars.GROUNDDESC]))

    # Print all the exits.
    exits = []
    for direction in (vars.NORTH, vars.SOUTH, vars.EAST, vars.WEST, vars.UP, vars.DOWN):
        if direction in list(dictionaries.worldRooms[loc].keys()):
            exits.append(direction.title())
    print(Style.DIM + '=======================' + Style.NORMAL + Fore.WHITE)
    print('\n')
    if showFullExits:
        for direction in (vars.NORTH, vars.SOUTH, vars.EAST, vars.WEST, vars.UP, vars.DOWN):
            if direction in dictionaries.worldRooms[location]:
                print(('%s: %s' % (direction.title(), dictionaries.worldRooms[location][direction])))
    else:
        print(('Exits: %s' % ' '.join(exits)))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location

    combatCheck = random.randrange(0,6)

    if direction in dictionaries.worldRooms[location]:
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
            location = dictionaries.worldRooms[location][direction]
            displayLocation(location)
        else:
            location = dictionaries.worldRooms[location][direction]
            displayLocation(location)
    else:
        print('Ted can\'t walk through walls.')


def getAllDescWords(itemList):
    """Returns a list of "description words" for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.extend(dictionaries.worldItems[item][vars.DESCWORDS])
    return list(set(descWords))

def getAllFirstDescWords(itemList):
    """Returns a list of the first "description word" in the list of
    description words for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.append(dictionaries.worldItems[item][vars.DESCWORDS][0])
    return list(set(descWords))

def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    for item in itemList:
        if desc in dictionaries.worldItems[item][vars.DESCWORDS]:
            return item
    return None

def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in dictionaries.worldItems[item][vars.DESCWORDS]:
            matchingItems.append(item)
    return matchingItems


class TextAdventureCmd(cmd.Cmd):
    prompt = PROMPT

    # The default() method is called when none of the other do_*() command methods match.
    def default(self, arg):
        print('Ted\'s feeble brain doesn\'t understand.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        """Quit the game."""
        return True # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

# These direction commands have a long (i.e. north) and show (i.e. n) form.
    # Since the code is basically the same, I put it in the moveDirection()
    # function.
    def do_north(self, arg):
        """Go to the area to the north, if possible."""
        moveDirection('north')

    def do_south(self, arg):
        """Go to the area to the south, if possible."""
        moveDirection('south')

    def do_east(self, arg):
        """Go to the area to the east, if possible."""
        moveDirection('east')

    def do_west(self, arg):
        """Go to the area to the west, if possible."""
        moveDirection('west')

    def do_up(self, arg):
        """Go to the area upwards, if possible."""
        moveDirection('up')

    def do_down(self, arg):
        """Go to the area downwards, if possible."""
        moveDirection('down')

    # Since the code is the exact same, we can just copy the
    # methods with shortened names:
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down

    def do_exits(self, arg):
        """Toggle showing full exit descriptions or brief exit descriptions."""
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing full exit descriptions.')
        else:
            print('Showing brief exit descriptions.')

    def do_inventory(self, arg):
        """Display a list of the items in Ted\'s possession."""

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
        """"take <item> - Take an item on the ground."""

        # put this value in a more suitably named variable
        itemToTake = arg.lower()

        if itemToTake == '':
            print('What should Ted take?')
            return

        cantTake = False

        # get the item name that the player's command describes
        for item in getAllItemsMatchingDesc(itemToTake, dictionaries.worldRooms[location][vars.GROUND]):
            if dictionaries.worldItems[item].get(vars.TAKEABLE, True) == False:
                cantTake = True
                continue # there may be other items named this that Ted can take, so we continue checking
            print(('Ted grabs %s.' % (dictionaries.worldItems[item][vars.SHORTDESC])))
            dictionaries.worldRooms[location][vars.GROUND].remove(item) # remove from the ground
            inventory.append(item) # add to inventory
            return

        if cantTake:
            print(('Ted doesn\'t want to grab "%s".' % (itemToTake)))
        else:
            print('Ted doesn\'t see that.')


    def do_drop(self, arg):
        """"drop <item>" - Drop an item from Ted\'s inventory onto the ground."""

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
            print(('Ted drops %s.' % (dictionaries.worldItems[item][vars.SHORTDESC])))
            inventory.remove(item) # remove from inventory
            dictionaries.worldRooms[location][vars.GROUND].append(item) # add to the ground


    def complete_take(self, text, line, begidx, endidx):
        possibleItems = []
        text = text.lower()

        # if the user has only typed "take" but no item name:
        if not text:
            return getAllFirstDescWords(dictionaries.worldRooms[location][vars.GROUND])

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for item in list(set(dictionaries.worldRooms[location][vars.GROUND])):
            for descWord in dictionaries.worldItems[item][vars.DESCWORDS]:
                if descWord.startswith(text) and dictionaries.worldItems[item].get(vars.TAKEABLE, True):
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
        """Look at an item, direction, or the area:
        "look" - display the current area's description
        "look <direction>" - display the description of the area in that direction
        "look exits" - display the description of all adjacent areas
        "look <item>" - display the description of an item on the ground or in Ted\'s inventory"""

        lookingAt = arg.lower()
        if lookingAt == '':
            # "look" will re-print the area description
            displayLocation(location)
            return

        if lookingAt == 'exits':
            for direction in (vars.NORTH, vars.SOUTH, vars.EAST, vars.WEST, vars.UP, vars.DOWN):
                if direction in dictionaries.worldRooms[location]:
                    print(('%s: %s' % (direction.title(), dictionaries.worldRooms[location][direction])))
            return

        if lookingAt in ('north', 'west', 'east', 'south', 'up', 'down', 'n', 'w', 'e', 's', 'u', 'd'):
            if lookingAt.startswith('n') and vars.NORTH in dictionaries.worldRooms[location]:
                print((dictionaries.worldRooms[location][vars.NORTH]))
            elif lookingAt.startswith('w') and vars.WEST in dictionaries.worldRooms[location]:
                print((dictionaries.worldRooms[location][vars.WEST]))
            elif lookingAt.startswith('e') and vars.EAST in dictionaries.worldRooms[location]:
                print((dictionaries.worldRooms[location][vars.EAST]))
            elif lookingAt.startswith('s') and vars.SOUTH in dictionaries.worldRooms[location]:
                print((dictionaries.worldRooms[location][vars.SOUTH]))
            elif lookingAt.startswith('u') and vars.UP in dictionaries.worldRooms[location]:
                print((dictionaries.worldRooms[location][vars.UP]))
            elif lookingAt.startswith('d') and vars.DOWN in dictionaries.worldRooms[location]:
                print((dictionaries.worldRooms[location][vars.DOWN]))
            else:
                print('Ted can\'t walk through walls.')
            return

        # see if the item being looked at is on the ground at this location
        item = getFirstItemMatchingDesc(lookingAt, dictionaries.worldRooms[location][vars.GROUND])
        if item != None:
            print(('\n'.join(textwrap.wrap(dictionaries.worldItems[item][vars.LONGDESC], vars.SCREEN_WIDTH))))
            return

        # see if the item being looked at is in the inventory
        item = getFirstItemMatchingDesc(lookingAt, inventory)
        if item != None:
            print(('\n'.join(textwrap.wrap(dictionaries.worldItems[item][vars.LONGDESC], vars.SCREEN_WIDTH))))
            return

        print('Ted scours to room, but he doesn\'t see that.')


    def complete_look(self, text, line, begidx, endidx):
        possibleItems = []
        lookingAt = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)
        groundDescWords = getAllDescWords(dictionaries.worldRooms[location][vars.GROUND])
        shopDescWords = getAllDescWords(dictionaries.worldRooms[location].get(vars.SHOP, []))

        for descWord in invDescWords + groundDescWords + shopDescWords + [vars.NORTH, vars.SOUTH, vars.EAST, vars.WEST, vars.UP, vars.DOWN]:
            if line.startswith('look %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "look" but no item name, show all items on ground, shop and directions:
        if lookingAt == '':
            possibleItems.extend(getAllFirstDescWords(dictionaries.worldRooms[location][vars.GROUND]))
            possibleItems.extend(getAllFirstDescWords(dictionaries.worldRooms[location].get(vars.SHOP, [])))
            for direction in (vars.NORTH, vars.SOUTH, vars.EAST, vars.WEST, vars.UP, vars.DOWN):
                if direction in dictionaries.worldRooms[location]:
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
        for direction in (vars.NORTH, vars.SOUTH, vars.EAST, vars.WEST, vars.UP, vars.DOWN):
            if direction.startswith(lookingAt):
                possibleItems.append(direction)

        # get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_list(self, arg):
        """List the items for sale at the current location's shop."""
        if vars.SHOP not in dictionaries.worldRooms[location]:
            print('Ain\'t no store here, Ted.')
            return

        arg = arg.lower()

        print((Style.DIM + '--- STORE ---' + Style.NORMAL + Fore.WHITE))
        for item in dictionaries.worldRooms[location][vars.SHOP]:
            print(('  %s' % (item)))
            print(('  ' + Style.DIM + '\n  '.join(textwrap.wrap(dictionaries.worldItems[item][vars.LONGDESC], vars.SCREEN_WIDTH)) + Style.NORMAL + Fore.WHITE))
            if arg == 'full':
                print((Style.DIM + '\n'.join(textwrap.wrap(dictionaries.worldItems[item][vars.LONGDESC], vars.SCREEN_WIDTH)) + Style.NORMAL + Fore.WHITE))

        print((Style.DIM + '=============' + Style.NORMAL + Fore.WHITE))


    def do_buy(self, arg):
        """"buy <item>" - buy an item at the current location's shop."""
        if vars.SHOP not in dictionaries.worldRooms[location]:
            print('Ain\'t shit to buy, Ted.')
            return

        itemToBuy = arg.lower()

        if itemToBuy == '':
            print(('Gotta be more specific.' + Style.DIM + ' Type "list" to see items' + Style.NORMAL + Fore.WHITE))
            return

        item = getFirstItemMatchingDesc(itemToBuy, dictionaries.worldRooms[location][vars.SHOP])
        if item != None:
            # NOTE - If Ted wanted to implement money, here is where Ted would add
            # code that checks if the player has enough, then deducts the price
            # from their money.
            print(('Ted just bought %s' % (dictionaries.worldItems[item][vars.SHORTDESC])))
            inventory.append(item)
            return

        print(('They don\'t have any "%s". Try again, Ted.' % (itemToBuy)))


    def complete_buy(self, text, line, begidx, endidx):
        if vars.SHOP not in dictionaries.worldRooms[location]:
            return []

        itemToBuy = text.lower()
        possibleItems = []

        # if the user has only typed "buy" but no item name:
        if not itemToBuy:
            return getAllFirstDescWords(dictionaries.worldRooms[location][vars.SHOP])

        # otherwise, get a list of all "description words" for shop items matching the command text so far:
        for item in list(set(dictionaries.worldRooms[location][vars.SHOP])):
            for descWord in dictionaries.worldItems[item][vars.DESCWORDS]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_sell(self, arg):
        """"sell <item>" - sell an item at the current location's shop."""
        if vars.SHOP not in dictionaries.worldRooms[location]:
            print('Ain\'t no one to sell it.')
            return

        itemToSell = arg.lower()

        if itemToSell == '':
            print(('Whatchoo wanna sell?' + Style.DIM + ' Type "inv" to see items' + Style.NORMAL + Fore.WHITE))
            return

        for item in inventory:
            if itemToSell in dictionaries.worldItems[item][vars.DESCWORDS]:
                # NOTE - If Ted wanted to implement money, here is where Ted would add
                # code that gives the player money for selling the item.
                print(('Ted sold %s' % (dictionaries.worldItems[item][vars.SHORTDESC])))
                inventory.remove(item)
                return

        print(('You don\'t have "%s", Ted.' % (itemToSell)))


    def complete_sell(self, text, line, begidx, endidx):
        if vars.SHOP not in dictionaries.worldRooms[location]:
            return []

        itemToSell = text.lower()
        possibleItems = []

        # if the user has only typed "sell" but no item name:
        if not itemToSell:
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in dictionaries.worldItems[item][vars.DESCWORDS]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_eat(self, arg):
        """"eat <item>" - eat an item in Ted\'s inventory."""
        itemToEat = arg.lower()

        if itemToEat == '':
            print('Whatchoo wanna eat?')
            return

        cantEat = False

        for item in getAllItemsMatchingDesc(itemToEat, inventory):
            if dictionaries.worldItems[item].get(vars.EDIBLE, False) == False:
                cantEat = True
                continue # there may be other items named this that Ted can eat, so we continue checking
            # NOTE - If Ted wanted to implement hunger levels, here is where
            # Ted would add code that changes the player's hunger level.
            print(('Ted eats %s' % (dictionaries.worldItems[item][vars.SHORTDESC])))
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
            for descWord in dictionaries.worldItems[item][vars.DESCWORDS]:
                if descWord.startswith(text) and dictionaries.worldItems[item].get(vars.EDIBLE, False):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_stats(self, arg):
        """Display player stats, weapon, and accessory"""
        print(Style.DIM + '--- Stats ---' + Style.NORMAL + Fore.WHITE)
        print('  HP: ' + str(vars.PLAYERHP) + '/ MP: ' + str(vars.PLAYERMP))
        print('  Hero Level: ' + str(vars.PLAYERLVL))
        print('  Hero XP: '+ str(vars.PLAYERXP))
        print('  You have ' + str(vars.FLOYDS) + ' Floyds.')
        print('  Equipped Weapon: ' + equippedWeapon + ' [+' + str(dictionaries.worldItems[equippedWeapon][vars.ATKBNS]) + ']')
        print('  Added FX: ' + addedFX + ' [+' + str(dictionaries.worldItems[addedFX][vars.ATKBNS]) + ']')
        print(Style.DIM + '=============' + Style.NORMAL + Fore.WHITE)

    def do_equip(self, arg):
        """Equip an item in Ted\'s inventory."""
        global equippedWeapon
        itemToEquip = arg.lower()

        if itemToEquip == '':
            print('Whatchoo wanna equip?')
            return

        cantEquip = False

        for item in getAllItemsMatchingDesc(itemToEquip, inventory):
            if dictionaries.worldItems[item].get(vars.WEAPON, False) == False:
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print(('Ted equips %s' % (dictionaries.worldItems[item][vars.SHORTDESC])))
            equippedWeapon = item
            return

        if cantEquip:
            print('Ted can\'t equip that...')
        else:
            print(('Ted is confused by "%s".' % (itemToEquip)))

    def do_addfx(self, arg):
        """Add and effect to Ted\'s weapon."""
        global addedFX
        itemToAdd = arg.lower()

        if itemToAdd == '':
            print('What\'s your tone, bro?')
            return

        cantAdd = False

        for item in getAllItemsMatchingDesc(itemToAdd, inventory):
            if dictionaries.worldItems[item].get(vars.FX, False) == False:
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print(('Ted adds %s' % (dictionaries.worldItems[item][vars.SHORTDESC])))
            addedFX = item
            return

        if cantAdd:
            print('That\'s not an effect...')
        else:
            print(('Ted is confused by "%s".' % (itemToAdd)))

    def do_save(self, arg):
        """Save the current state of the game to file."""
        saveState()

    def do_combat(self, arg):
        """Enter combat with a random enemy"""
        combat = combatMode()
        combat.fight()

def introAnimation():
    clear()
    time.sleep(1)
    print(Style.BRIGHT + dictionaries.introtext[vars.INTRO1] + '\n')
    time.sleep(2)
    clear()
    print(Style.DIM + dictionaries.introtext[vars.INTRO2] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO2] + '\n')
    print(Style.DIM + dictionaries.introtext[vars.INTRO3] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.BRIGHT + dictionaries.introtext[vars.INTRO2] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO3] + '\n')
    print(Style.DIM + dictionaries.introtext[vars.INTRO4] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO2] + '\n')
    print(Style.BRIGHT + dictionaries.introtext[vars.INTRO3] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO4] + '\n')
    print(Style.DIM + dictionaries.introtext[vars.INTRO5] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO2] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO3] + '\n')
    print(Style.BRIGHT + dictionaries.introtext[vars.INTRO4] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO5] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO2] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO3] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO4] + '\n')
    print(Style.BRIGHT + dictionaries.introtext[vars.INTRO5] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO2] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO3] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO4] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO5] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO2] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO3] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO4] + '\n')
    print(Style.NORMAL + dictionaries.introtext[vars.INTRO5] + '\n')
    time.sleep(13)
    clear()
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(0.5)
    clear()
    print(Fore.YELLOW + Style.BRIGHT + asciiGFX.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(1)
    clear()
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.BRIGHT + asciiGFX.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(0.5)
    clear()
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.BRIGHT + asciiGFX.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(1)
    clear()
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(2)
    clear()

if __name__ == '__main__':

    print(Back.BLACK + Fore.WHITE)
    clear()
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + asciiGFX.logo3 + Style.NORMAL + Fore.WHITE)
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
        displayLocation(location)
        TextAdventureCmd().cmdloop()
    else:
        pass
    print('Thanks for ROCKIN\'!' + Style.NORMAL)
