import os	#for clearing the terminal
import sys  # For OS identification
import asciiGFX  # Import all the ASCII graphics assets
import time # Import time for intro GFX
from colorama import Fore, Back, Style  # Used for text coloring
import random # For random number generation
import argparse # For passing command line args

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

# engine variables
PROMPT = Fore.RED + '\m/: ' + Style.NORMAL + Fore.WHITE
nextAction = 0 # 1 = player, 0 = enemy

# worldItems variables
WEAPON = 'weapon'
FX = 'fx'
ATKBNS = 0
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
TAKEABLE = 'takeable'
EDIBLE = 'edible'
BATTLE = 'battle'
DESCWORDS = 'descwords'

# worldRooms variables
DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
UP = 'up'
DOWN = 'down'
GROUND = 'ground'
SHOP = 'shop'
PLANET = 'planet'

# enemies variables
ENDESC = 'endesc'
HP = 'hp'
MP = 'mp'
ATTACKMIN = 'attackmin'
ATTACKMAX = 'attackmax'
CRITBNS = 0 # TODO Make CRITBNS scale to current planet
CR = 'challengerating' # TODO implement challenge rating system
DIALOG = 'dialog'

# Battle system globals
enemyHP = 'hp'
enemyMP = 'mp'

# Character battle stat values go here
PLAYERHP = 100
PLAYERMP = 25
FLOYDS = 0
PLAYERLVL = 1
PLAYERXP = 0
CRIT = 1 # TODO make CRIT value based on PLAYERLVL

# Hero Attack variables
HEROMIN = 'min'
HEROMAX = 'max'
MPREQ = 'mpreq'
MAGDMG = 'magdmg'

# equipment status variables
# TODO make these default fallback values
equippedWeapon = 'Fists'
addedFX = 'noFX'

# challenge rating variable
XPAWARD = 0

# intro
INTRO1 = 'intro1'
INTRO2 = 'intro2'
INTRO3 = 'intro3'
INTRO4 = 'intro4'
INTRO5 = 'intro5'

SCREEN_WIDTH = 170

# worldRooms dictionary
# TODO convert dictionary to SQLlite3
'''
Syntax:
    '': {
        DESC: '',
        NORTH: '',
        SOUTH: '',
        EAST: '',
        WEST: '',
        UP: '',
        DOWN: '',
        PLANET: '',
        SHOP: [''],
        GROUND: ['']},
'''

worldRooms = {
    'EBGB Stage': {
        DESC: 'Ted finishes wrapping cables and tearing down the stage.'
            + '\n\n'
            + Fore.CYAN + 'TED: ' + Style.BRIGHT + '"I\'m gettin\' too old for this shit."' + Style.NORMAL + Fore.WHITE
            + '\n\n'
            + 'The bar is winding down for the night.'
            + '\n',
        NORTH: 'EBGB Dance Floor',
        EAST: 'EBGB Backstage',
        WEST: 'EBGB Bathrooms',
        PLANET: 'Zappa',
        GROUND: ['Empty Bottle', 'Stack of Cables', 'Drums']},
    'EBGB Dance Floor': {
        DESC: 'Ted walks out onto the dance floor. There are two drunk hippies making out'
            + '\n'
            + 'furiously. Ted tries to ignore them.'
            + '\n\n'
            + 'The bartender can be seen wiping down the bar; last call hasn\'t been announced.'
            + '\n',
        NORTH: 'EBGB Parking Lot',
        EAST: 'EBGB Bar',
        SOUTH: 'EBGB Stage',
        WEST: 'EBGB Jukebox',
        PLANET: 'Zappa',
        GROUND: ['Guitar Pick', 'Broken Drumstick']},
    'EBGB Backstage': {
        DESC: 'Ted finds himself trudging through a sea of beer cans, roaches, and used'
            + '\n'
            + 'condoms. Lying on top of a case is a grungy white guitar that was used'
            + '\n'
            + 'by the cover band.'
            + '\n\n'
            + Fore.CYAN + 'TED: ' + Style.BRIGHT + '"Dumbass left his guitar."' + Style.NORMAL + Fore.WHITE
            + '\n',
        WEST: 'EBGB Stage',
        PLANET: 'Zappa',
        GROUND: ['Squire Strat', 'Used Condom', 'Chaz Note']},
    'EBGB Bathrooms': {
        DESC: 'The smell of piss and shit from the hippies at the show tonight is overbearing.'
            + '\n\n'
            + Fore.CYAN + 'TED: ' + Style.BRIGHT + '"I swear I\'m going to murder every hippy in the galaxy.'
            + '\n'
            + '      Gotta finish this album first."' + Style.NORMAL + Fore.WHITE
            + '\n\n'
            + 'The faint odor of cannabis lingers from a stall. Ted kicks the door in to find'
            + '\n'
            + 'a startled hippy. Thinking quickly, the hippy offers a lit joint to Ted.'
            + '\n\n'
            + Fore.GREEN + 'HIPPY: ' + Style.BRIGHT + '"Wanna hit, dude?"' + Style.NORMAL + Fore.WHITE
            + '\n',
        EAST: 'EBGB Stage',
        PLANET: 'Zappa',
        GROUND: ['Lit Joint']},
    'EBGB Bar': {
        DESC: 'Ted sizes up the bartender. He\'s a large rotund individual from the planet'
            + '\n'
            + 'Zappa. Best not to try anything stupid with him.'
            + '\n\n'
            + Fore.CYAN + 'BONGO: ' + Style.BRIGHT + '"Whatchoo won\' Ted?"' + Style.NORMAL + Fore.WHITE
            + '\n\n'
            + Fore.GREEN + 'TED: ' + Style.BRIGHT + '"Where\'d Chaz and the band go?"' + Style.NORMAL + Fore.WHITE
            + '\n\n'
            + Fore.CYAN + 'BONGO: ' + Style.BRIGHT + '"Heh, they hitched a ride with some fancy-pants producer.'
            + '\n'
            + '        They don\' need you no more, Ted.'
            + '\n'
            + '        You bes\' buy somethin\' or get the hell outta here"' + Style.NORMAL + Fore.WHITE
            + '\n',
        NORTH: 'EBGB Parking Lot',
        WEST: 'EBGB Dance Floor',
        SHOP: ['Dark Matter Ale'],
        PLANET: 'Zappa',
        GROUND: []},
    'EBGB Jukebox': {
        DESC: 'Ted needs to listen to some tunes, so he walks over to the ratty Jukebox that\'s'
            + '\n'
            + 'probably been here for centuries.'
            + '\n\n'
            + 'There are 4 buttons, and a blinking slot with text that reads: ' + Style.BRIGHT + Fore.GREEN + 'INSERT 5 FLOYDS' + Style.NORMAL + Fore.WHITE
            + '\n',
        NORTH: 'EBGB Parking Lot',
        EAST: 'EBGB Dance Floor',
        PLANET: 'Zappa',
        GROUND: []},
    'EBGB Parking Lot': {
        DESC: 'Ted leaves EBGBs to find his sweet looking Winnibego in the parking lot.'
            + '\n\n'
            + 'To the east is a swirling black wormhole. It\'s sucking in small bits of debris'
            + '\n'
            + 'from the ground around it.'
            + '\n',
        EAST: 'Black Wormhole',
        NORTH: 'Winnibego',
        SOUTH: 'EBGB Bar',
        PLANET: 'Zappa',
        GROUND: []},
    'Black Wormhole': {
        DESC: 'Ted steps into the black wormhole. As he reaches the event'
            + '\n'
            + 'horizon he feels his body begin to warp and dissipate.'
            + '\n\n'
            + Fore.CYAN + 'TED: ' + Style.BRIGHT + '"FUU-"' + Style.NORMAL + Fore.WHITE
            + '\n\n'
            + 'After what seems like eons, Ted\'s body begins to materialize again.'
            + '\n\n'
            + Fore.CYAN + 'TED: ' + Style.BRIGHT + '"-UUCK."' + Style.NORMAL + Fore.WHITE
            + '\n\n'
            + 'Ted finds himself in a dark alley that looks like it might be on the planet'
            + '\n'
            + 'Mactel 6. Lounging before him in a mound of used condoms and empty Dark Matter'
            + '\n'
            + 'Ale bottles there\'s a rough looking buzzoid hobo smoking what looks to be a'
            + '\n'
            + 'joint made of trash.'
            + '\n\n'
            + Fore.GREEN + 'HOBO: ' + Style.BRIGHT + '"What\'ll ya be havin\', stranger?"' + Style.NORMAL + Fore.WHITE
            + '\n\n'
            + 'The hobo smirks maniacally and opens his shitty excuse for wings to reveal a'
            + '\n'
            + 'smorgasbord of psychedelic drugs.'
            + '\n',
        WEST: 'EBGB Parking Lot',
        SHOP: ['Magic Mushies', 'ACiD', 'Mescalin', 'Amanitas'],
        PLANET: 'Universe',
        GROUND: []},
    'Winnibego': {
        DESC: 'Ted\'s trusty steed, the ol\' Winnie. It smells of dude and weed in here.'
            + '\n\n'
            + 'Ted sees a flashing light on the console that reads: ' + Fore.GREEN + 'IGNITION' + Style.NORMAL + Fore.WHITE
            + '\n',
        DOWN: 'EBGB Parking Lot',
        PLANET: 'Travel',
        GROUND: []},
    }

# worldItems dictionary
# TODO convert dictionary to SQLlite3
'''
Syntax
    '': {
        GROUNDDESC: '',
        SHORTDESC: '',
        LONGDESC: '',
        TAKEABLE: True,
        WEAPON: True,
        FX: True,
        EDIBLE: True,
        BATTLE: True,
        ATKBNS: 0,
        DESCWORDS: ['']},
'''

worldItems = {
    'Fists': {
        GROUNDDESC: 'Ted\'s raw fists',
        SHORTDESC: 'his fists',
        LONGDESC: 'Ted\'s manly fucking fists. They\'ve beaten many faces into the ground.',
        TAKEABLE: True,
        WEAPON: True,
        ATKBNS: 0,
        DESCWORDS: ['fists']},
    'noFX': {
        GROUNDDESC: 'Raw tone',
        SHORTDESC: 'air',
        LONGDESC: 'Nothing but tone.',
        TAKEABLE: True,
        FX: True,
        ATKBNS: 0,
        DESCWORDS: ['nofx']},
    'Winnibego Keys': {
        GROUNDDESC: 'Keys to the Winnie',
        SHORTDESC: 'the keys to the Winnie',
        LONGDESC: 'The keys to Ted\'s sweet Winnibego',
        TAKEABLE: True,
        DESCWORDS: ['keys', 'winnie keys']},
    'Protection': {
        GROUNDDESC: 'Protection',
        SHORTDESC: 'protection',
        LONGDESC: 'The best protection the galaxy has to offer against the buzzoids.',
        TAKEABLE: True,
        BATTLE: True,
        DESCWORDS: ['protection']},
    'Squire Strat': {
        GROUNDDESC: 'Chaz Lightyear\'s Guitar',
        SHORTDESC: 'the Squire Strat',
        LONGDESC: 'A beat up strat that used to be white. It gets the job done.',
        TAKEABLE: True,
        WEAPON: True,
        ATKBNS: 1,
        DESCWORDS: ['chaz\'s guitar', 'chaz guitar', 'strat', 'stratocaster']},
    'Used Condom': {
        GROUNDDESC: 'Slimy condom',
        SHORTDESC: 'the jimmy hat',
        LONGDESC: 'It\'s stuck to the table. Probably should leave it for the cleaning crew.',
        TAKEABLE: False,
        EDIBLE: True,
        DESCWORDS: ['jimmy hat', 'condom', 'cum sock']},
    'Chaz Note': {
        GROUNDDESC: 'Handwritten note',
        SHORTDESC: 'the note',
        LONGDESC: 'A note in Chaz\'s sloppy handwriting: ' + Fore.YELLOW + 'Yo Ted, a scout at the show wants us to' + '\n' + 'sign with \'em. We\'re heading to their station after the gig, see you later bro.' + Style.NORMAL + Fore.WHITE,
        TAKEABLE: True,
        DESCWORDS: ['note']},
    'Empty Bottle': {
        GROUNDDESC: 'Empty bottle',
        SHORTDESC: 'the empty bottle',
        LONGDESC: 'An empty bottle of Dark Matter Ale. Ted wishes it was full.',
        TAKEABLE: False,
        DESCWORDS: ['bottle', 'empty bottle']},
    'Stack of Cables': {
        GROUNDDESC: 'Cables',
        SHORTDESC: 'the cables',
        LONGDESC: 'A stack of professionally coiled cables, no thanks to Ted.',
        TAKEABLE: False,
        DESCWORDS: ['cables', 'stack of cables', 'cable stack']},
    'Drums': {
        GROUNDDESC: 'Drum Kit',
        SHORTDESC: 'the kit',
        LONGDESC: 'EBGB\'s house kit. It\'s missing the cymbals.',
        TAKEABLE: False,
        DESCWORDS: ['drums', 'kit']},
    'Dark Matter Ale': {
        GROUNDDESC: 'Refreshing Dark Ale',
        SHORTDESC: 'the Dark Matter Ale',
        LONGDESC: 'A cold refreshing ale brewed in the outer rim of the galaxy. The label claims' + '\n' + 'to have an alcohol content of 2.08x10^15.',
        TAKEABLE: True,
        EDIBLE: True,
        BATTLE: True,
        DESCWORDS: ['ale', 'bottle of ale', 'dark matter ale', 'dark matter']},
    'Guitar Pick': {
        GROUNDDESC: 'Rip Curl\'s pick',
        SHORTDESC: 'the guitar pick',
        LONGDESC: 'The pick that Rip Curl threw into the crowd at EBGBs.',
        TAKEABLE: True,
        FX: True,
        ATKBNS: 1,
        DESCWORDS: ['pick', 'guitar pick']},
    'Broken Drumstick': {
        GROUNDDESC: 'Grumm\'s broken stick',
        SHORTDESC: 'the wood shard',
        LONGDESC: 'Piece of a broken stick that Grumm tossed into the crowd at EBGBs. Ted wonders' + '\n' + 'where the other half ended up.',
        TAKEABLE: True,
        DESCWORDS: ['stick', 'wood shard']},
    'Lit Joint': {
        GROUNDDESC: 'Hippy\'s J',
        SHORTDESC: 'the lit joint',
        LONGDESC: 'A cherried joint some hippy gave Ted for not beating the shit out of him.',
        TAKEABLE: True,
        BATTLE: True,
        DESCWORDS: ['joint', 'j', 'hippy j', 'jay', 'lit joint', 'lit j']},
    'Magic Mushies': {
        GROUNDDESC: 'Magic Mushies',
        SHORTDESC: 'the shrooms',
        LONGDESC: 'A bag full of shriveled brown mushrooms. Looks like enough for two people, or one roadie.',
        TAKEABLE: True,
        EDIBLE: True,
        BATTLE: True,
        DESCWORDS: ['shrooms', 'mushies', 'magic shrooms']},
    'ACiD': {
        GROUNDDESC: 'ACiD',
        SHORTDESC: 'the acid tab',
        LONGDESC: 'A small, square, white tab of paper. If you don\'t own a spaceship, this is a great alternative.',
        TAKEABLE: True,
        EDIBLE: True,
        BATTLE: True,
        DESCWORDS: ['acid', 'tab']},
    'Mescalin': {
        GROUNDDESC: 'Mescalin',
        SHORTDESC: 'the peyote',
        LONGDESC: 'It\'s a tiny peyote plant. Crack this baby open and get ready for a ride!',
        TAKEABLE: True,
        EDIBLE: True,
        BATTLE: True,
        DESCWORDS: ['mescalin', 'peyote']},
    'Amanitas': {
        GROUNDDESC: 'Amanitas',
        SHORTDESC: 'the red cap',
        LONGDESC: 'Mushrooms with bright red caps and little white dots. Let\'s hope these aren\'t the poisonus genus...',
        TAKEABLE: True,
        EDIBLE: True,
        BATTLE: True,
        DESCWORDS: ['amanitas', 'red caps', 'other mushrooms']},
    'Epiphone SG': {
        GROUNDDESC: 'Used Epiphone SG',
        SHORTDESC: 'Epiphone SG',
        LONGDESC: 'Not quite a Gibson, but it looks fuckin\' sweet.',
        TAKEABLE: True,
        WEAPON: True,
        ATKBNS: 2,
        DESCWORDS: ['sg', 'epiphone']},
    'Wormhole Delay': {
        GROUNDDESC: 'Delay pedal from Wormhole',
        SHORTDESC: 'Wormhole Delay',
        LONGDESC: 'Delay FX from another world. Use sparingly.',
        TAKEABLE: True,
        FX: True,
        ATKBNS: 2,
        DESCWORDS: ['delay', 'delay pedal', 'wormhole']},
    }

# enemies dictionary
# TODO convert dictionary to SQLlite3
'''
Syntax
    '': {
        ENDESC: '',
        HP: 0,
        MP: 0,
        ATTACKMIN: 0,
        ATTACKMAX: 0,
        CRITBNS: 0,
        CR: 0,
        DIALOG: ['']},
'''

enemies = {
    'Buzzoid': {
        ENDESC: 'A hideous bug like creature that smells of liquor and sewage.'
            + '\n',
        HP: 15,
        MP: 10,
        ATTACKMIN: 1,
        ATTACKMAX: 3,
        CRITBNS: 1,
        DIALOG: ['It spits in your face!', 'It flaps its pathetic wings with great force!']},
    'Zappan': {
        ENDESC: 'Ted isn\'t quite sure what to make of this round object that gargles at him.'
            + '\n',
        HP: 20,
        MP: 15,
        ATTACKMIN: 2,
        ATTACKMAX: 5,
        CRITBNS: 2,
        DIALOG: ['It throws a dog-doo snow cone!', 'It rubs yellow snow in your eye!']},
    }

# challenge rating dictionary
challenge = {
    '0': { XPAWARD: 50, CRITBNS: 1 },
    '1': { XPAWARD: 100, CRITBNS: 1 },
    '2': { XPAWARD: 250, CRITBNS: 1 },
    '3': { XPAWARD: 500, CRITBNS: 2 },
    '4': { XPAWARD: 1000, CRITBNS: 2 },
    '5': { XPAWARD: 1800, CRITBNS: 2 },
    '6': { XPAWARD: 2300, CRITBNS: 2 },
    '7': { XPAWARD: 2900, CRITBNS: 3 },
    '8': { XPAWARD: 3900, CRITBNS: 3 },
    '9': { XPAWARD: 5000, CRITBNS: 3 },
    '10': { XPAWARD: 5900, CRITBNS: 3 },
    '11': { XPAWARD: 7200, CRITBNS: 4 },
    '12': { XPAWARD: 8400, CRITBNS: 4 },
    '13': { XPAWARD: 10000, CRITBNS: 4 },
    '14': { XPAWARD: 11500, CRITBNS: 4 },
    '15': { XPAWARD: 13000, CRITBNS: 5 },
    '16': { XPAWARD: 15000, CRITBNS: 5 },
    '17': { XPAWARD: 18000, CRITBNS: 5 },
    '18': { XPAWARD: 20000, CRITBNS: 6 },
    '19': { XPAWARD: 22000, CRITBNS: 6 },
    '20': { XPAWARD: 25000, CRITBNS: 7 },
}

# Contains all available hero attacks
heroAttacks = {
    'Punch': {
        HEROMIN: 0,
        HEROMAX: 3,},
    'Headbang': {
        HEROMIN: 2,
        HEROMAX: 5,},
    }

# Contains all available hero magic
'''
Syntax
    '' = {
        MPREQ: 0,
        MAGDMG: 0,},
'''
heroMagic = {
    'Rising Force': {
        MPREQ: 2,
        MAGDMG: 2,},
    'Purple Rain': {
        MPREQ: 3,
        MAGDMG: 3,},
    }

# intro
introtext = {
    INTRO1: 'The year is 4420',
    INTRO2: 'Mankind has expanded its reach beyond the solar system',
    INTRO3: 'Many righteous bands tour the galaxy looking for wealth, fame, and loose women,'
        + '\n'
        + 'but there is now an evil that lurks in the vast darkness of space.',
    INTRO4: 'The evil conglomerates of Earth\'s past return to enslave the Gods of Metal'
        + '\n'
        + 'by cryogenically freezing and replacing them with their clone-step army.',
    INTRO5: 'There is only one crew that can put a stop to this madness...',
    }

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
        allKeys = list(enemies.keys())
        chosenEnemy = random.choice(allKeys)
        print(chosenEnemy)

    def HUD(self):
        """Prints out the players HUD"""
        clear()
        print('')
        print(Style.DIM + '>>  ' + Style.BRIGHT + Fore.CYAN + 'TED MOONCHILD' + Fore.WHITE + Style.NORMAL)
        print('    HP: ' + str(PLAYERHP))
        print('    MP: ' + str(PLAYERMP))
        print('    WPN: ' + equippedWeapon + ' [+' + str(worldItems[equippedWeapon][ATKBNS]) + ']')
        print('    FX: ' + addedFX + ' [+' + str(worldItems[addedFX][ATKBNS]) + ']')
        print('')
        print(Style.DIM + '>>  ' + Style.BRIGHT + Fore.YELLOW + chosenEnemy + Fore.WHITE + Style.NORMAL)
        print('    HP: ' + str(enemyHP))
        print('    MP: ' + str(enemies[chosenEnemy][MP]))

    def story(self):
        """Prints description of enemy, dialog, ascii art."""
        print('')
        print('    [IMAGE of ' + chosenEnemy + ']')
        print('')
        print('    ' + enemies[chosenEnemy][ENDESC])
        print(Style.DIM + '+--------------------------------------------------------------------------------------------------+' + Style.NORMAL)
        print('')

    def battleMenu(self):
        """Prints out the battle system menu"""
        global enemyHP
        global PLAYERMP
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
            for item in list(heroAttacks.keys()):
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
                heroAttackDamage = random.randrange(heroAttacks[chosenAttack][HEROMIN], heroAttacks[chosenAttack][HEROMAX])
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
                    heroAttackDamage += int(CRIT)
                else:
                    pass
                if debug == 1:
                    print(Style.DIM + ' DMG + CRIT:     ' + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                # Increase hero's attack damage by whatever attack bonus the weapon supplies.
                heroAttackDamage += worldItems[equippedWeapon][int(ATKBNS)]
                if debug == 1:
                    print(Style.DIM + ' DMG + WPN:      ' + str(heroAttackDamage) + Style.NORMAL + Fore.WHITE)
                else:
                    pass
                heroAttackDamage += worldItems[addedFX][int(ATKBNS)]
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
            for item in list(heroMagic.keys()):
                magicList.append(item)
                print(Style.DIM + Fore.YELLOW + ' [' + str(i) + '] - ' + Fore.WHITE + Style.NORMAL + item + Fore.CYAN + ' [MP: ' + str(heroMagic[item][MPREQ]) + ']' + Fore.WHITE)
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
                if heroMagic[chosenMagic][MPREQ] > int(PLAYERMP):
                    print('')
                    print('Ted doesn\'t have enough MP!')
                    # Set next action to player
                    nextAction = 1

                else:
                    heroMagicDamage = heroMagic[chosenMagic][MAGDMG]
                    # magic crit check
                    magicCrit = random.randrange(0,20)
                    if debug == 1:
                        print('')
                        print('Magic Crit Check: ' + str(magicCrit))
                        print('')
                    else:
                        pass
                    if magicCrit == 10:
                        heroMagicDamage += heroMagicDamage
                        enemyHP = enemyHP - heroMagicDamage
                        print('Ted totally ROCKED ' + chosenMagic + ' for ' + Fore.CYAN + str(heroMagicDamage) + Style.NORMAL + Fore.WHITE + ' damage!!')
                    else:
                        enemyHP = enemyHP - heroMagicDamage
                        print('Ted performs ' + chosenMagic + ' for ' + Fore.CYAN + str(heroMagicDamage) + Style.NORMAL + Fore.WHITE + ' damage!')
                    PLAYERMP = int(PLAYERMP) - heroMagic[chosenMagic][MPREQ]
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
                if worldItems[chosenItem].get(BATTLE) == True:
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
                elif worldItems[chosenItem].get(WEAPON) == True and chosenItem != equippedWeapon:
                    print('')
                    print('Equip it first, then use an attack!')
                    time.sleep(3)
                    # Set next action to player
                    nextAction = 1
                elif worldItems[chosenItem].get(FX) == True and chosenItem != addedFX:
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
        if int(PLAYERHP) <= 0:
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
        global PLAYERHP
        global PLAYERMP
        global enemyHP
        global nextAction
        # Randomly select an enemy.
        self.selectEnemy()
        enemyHP = enemies[chosenEnemy][HP]
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
                dialogSelection = len(enemies[chosenEnemy][DIALOG])
                # Randomly chooses damage caused based on min and max defined values.
                enemyAttack = random.randrange(enemies[chosenEnemy][ATTACKMIN], enemies[chosenEnemy][ATTACKMAX])
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
                    enemyAttack += enemies[chosenEnemy][int(CRITBNS)]
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
                    PLAYERHP = int(PLAYERHP) - enemyAttack
                    # Chooses a random attack dialog line.
                    print(Fore.GREEN + enemies[chosenEnemy][DIALOG][random.randrange(0, dialogSelection)] + Fore.WHITE)
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
    global PLAYERHP
    global PLAYERMP
    global PLAYERLVL
    global PLAYERXP
    global FLOYDS
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
        PLAYERHP = f.readline()
        PLAYERHP = PLAYERHP.replace('\n', '')
        PLAYERMP = f.readline()
        PLAYERMP = PLAYERMP.replace('\n', '')
        PLAYERLVL = f.readline()
        PLAYERLVL = PLAYERLVL.replace('\n', '')
        PLAYERXP = f.readline()
        PLAYERXP = PLAYERXP.replace('\n', '')
        FLOYDS = f.readline()
        FLOYDS = FLOYDS.replace('\n', '')
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
    global PLAYERHP
    global PLAYERMP
    global PLAYERLVL
    global PLAYERXP
    global FLOYDS
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
    f.write(str(PLAYERHP))
    f.write('\n')
    f.write(str(PLAYERMP))
    f.write('\n')
    f.write(str(PLAYERLVL))
    f.write('\n')
    f.write(str(PLAYERXP))
    f.write('\n')
    f.write(str(FLOYDS))
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
    print((worldRooms[loc][DESC]))

    # Print all the items on the ground.
    if len(worldRooms[loc][GROUND]) > 0:
        print(Style.DIM + '--- ITEMS ON GROUND ---' + Style.NORMAL + Fore.WHITE)
        for item in worldRooms[loc][GROUND]:
            print(('  ' + worldItems[item][GROUNDDESC]))

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        if direction in list(worldRooms[loc].keys()):
            exits.append(direction.title())
    print(Style.DIM + '=======================' + Style.NORMAL + Fore.WHITE)
    print('\n')
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction in worldRooms[location]:
                print(('%s: %s' % (direction.title(), worldRooms[location][direction])))
    else:
        print(('Exits: %s' % ' '.join(exits)))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location

    combatCheck = random.randrange(0,6)

    if direction in worldRooms[location]:
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
            location = worldRooms[location][direction]
            displayLocation(location)
        else:
            location = worldRooms[location][direction]
            displayLocation(location)
    else:
        print('Ted can\'t walk through walls.')


def getAllDescWords(itemList):
    """Returns a list of "description words" for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.extend(worldItems[item][DESCWORDS])
    return list(set(descWords))

def getAllFirstDescWords(itemList):
    """Returns a list of the first "description word" in the list of
    description words for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.append(worldItems[item][DESCWORDS][0])
    return list(set(descWords))

def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    for item in itemList:
        if desc in worldItems[item][DESCWORDS]:
            return item
    return None

def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in worldItems[item][DESCWORDS]:
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
        for item in getAllItemsMatchingDesc(itemToTake, worldRooms[location][GROUND]):
            if worldItems[item].get(TAKEABLE, True) == False:
                cantTake = True
                continue # there may be other items named this that Ted can take, so we continue checking
            print(('Ted grabs %s.' % (worldItems[item][SHORTDESC])))
            worldRooms[location][GROUND].remove(item) # remove from the ground
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
            print(('Ted drops %s.' % (worldItems[item][SHORTDESC])))
            inventory.remove(item) # remove from inventory
            worldRooms[location][GROUND].append(item) # add to the ground


    def complete_take(self, text, line, begidx, endidx):
        possibleItems = []
        text = text.lower()

        # if the user has only typed "take" but no item name:
        if not text:
            return getAllFirstDescWords(worldRooms[location][GROUND])

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for item in list(set(worldRooms[location][GROUND])):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text) and worldItems[item].get(TAKEABLE, True):
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
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in worldRooms[location]:
                    print(('%s: %s' % (direction.title(), worldRooms[location][direction])))
            return

        if lookingAt in ('north', 'west', 'east', 'south', 'up', 'down', 'n', 'w', 'e', 's', 'u', 'd'):
            if lookingAt.startswith('n') and NORTH in worldRooms[location]:
                print((worldRooms[location][NORTH]))
            elif lookingAt.startswith('w') and WEST in worldRooms[location]:
                print((worldRooms[location][WEST]))
            elif lookingAt.startswith('e') and EAST in worldRooms[location]:
                print((worldRooms[location][EAST]))
            elif lookingAt.startswith('s') and SOUTH in worldRooms[location]:
                print((worldRooms[location][SOUTH]))
            elif lookingAt.startswith('u') and UP in worldRooms[location]:
                print((worldRooms[location][UP]))
            elif lookingAt.startswith('d') and DOWN in worldRooms[location]:
                print((worldRooms[location][DOWN]))
            else:
                print('Ted can\'t walk through walls.')
            return

        # see if the item being looked at is on the ground at this location
        item = getFirstItemMatchingDesc(lookingAt, worldRooms[location][GROUND])
        if item != None:
            print(('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH))))
            return

        # see if the item being looked at is in the inventory
        item = getFirstItemMatchingDesc(lookingAt, inventory)
        if item != None:
            print(('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH))))
            return

        print('Ted scours to room, but he doesn\'t see that.')


    def complete_look(self, text, line, begidx, endidx):
        possibleItems = []
        lookingAt = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)
        groundDescWords = getAllDescWords(worldRooms[location][GROUND])
        shopDescWords = getAllDescWords(worldRooms[location].get(SHOP, []))

        for descWord in invDescWords + groundDescWords + shopDescWords + [NORTH, SOUTH, EAST, WEST, UP, DOWN]:
            if line.startswith('look %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "look" but no item name, show all items on ground, shop and directions:
        if lookingAt == '':
            possibleItems.extend(getAllFirstDescWords(worldRooms[location][GROUND]))
            possibleItems.extend(getAllFirstDescWords(worldRooms[location].get(SHOP, [])))
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in worldRooms[location]:
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
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction.startswith(lookingAt):
                possibleItems.append(direction)

        # get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_list(self, arg):
        """List the items for sale at the current location's shop."""
        if SHOP not in worldRooms[location]:
            print('Ain\'t no store here, Ted.')
            return

        arg = arg.lower()

        print((Style.DIM + '--- STORE ---' + Style.NORMAL + Fore.WHITE))
        for item in worldRooms[location][SHOP]:
            print(('  %s' % (item)))
            print(('  ' + Style.DIM + '\n  '.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)) + Style.NORMAL + Fore.WHITE))
            if arg == 'full':
                print((Style.DIM + '\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)) + Style.NORMAL + Fore.WHITE))

        print((Style.DIM + '=============' + Style.NORMAL + Fore.WHITE))


    def do_buy(self, arg):
        """"buy <item>" - buy an item at the current location's shop."""
        if SHOP not in worldRooms[location]:
            print('Ain\'t shit to buy, Ted.')
            return

        itemToBuy = arg.lower()

        if itemToBuy == '':
            print(('Gotta be more specific.' + Style.DIM + ' Type "list" to see items' + Style.NORMAL + Fore.WHITE))
            return

        item = getFirstItemMatchingDesc(itemToBuy, worldRooms[location][SHOP])
        if item != None:
            # NOTE - If Ted wanted to implement money, here is where Ted would add
            # code that checks if the player has enough, then deducts the price
            # from their money.
            print(('Ted just bought %s' % (worldItems[item][SHORTDESC])))
            inventory.append(item)
            return

        print(('They don\'t have any "%s". Try again, Ted.' % (itemToBuy)))


    def complete_buy(self, text, line, begidx, endidx):
        if SHOP not in worldRooms[location]:
            return []

        itemToBuy = text.lower()
        possibleItems = []

        # if the user has only typed "buy" but no item name:
        if not itemToBuy:
            return getAllFirstDescWords(worldRooms[location][SHOP])

        # otherwise, get a list of all "description words" for shop items matching the command text so far:
        for item in list(set(worldRooms[location][SHOP])):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_sell(self, arg):
        """"sell <item>" - sell an item at the current location's shop."""
        if SHOP not in worldRooms[location]:
            print('Ain\'t no one to sell it.')
            return

        itemToSell = arg.lower()

        if itemToSell == '':
            print(('Whatchoo wanna sell?' + Style.DIM + ' Type "inv" to see items' + Style.NORMAL + Fore.WHITE))
            return

        for item in inventory:
            if itemToSell in worldItems[item][DESCWORDS]:
                # NOTE - If Ted wanted to implement money, here is where Ted would add
                # code that gives the player money for selling the item.
                print(('Ted sold %s' % (worldItems[item][SHORTDESC])))
                inventory.remove(item)
                return

        print(('You don\'t have "%s", Ted.' % (itemToSell)))


    def complete_sell(self, text, line, begidx, endidx):
        if SHOP not in worldRooms[location]:
            return []

        itemToSell = text.lower()
        possibleItems = []

        # if the user has only typed "sell" but no item name:
        if not itemToSell:
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in worldItems[item][DESCWORDS]:
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
            if worldItems[item].get(EDIBLE, False) == False:
                cantEat = True
                continue # there may be other items named this that Ted can eat, so we continue checking
            # NOTE - If Ted wanted to implement hunger levels, here is where
            # Ted would add code that changes the player's hunger level.
            print(('Ted eats %s' % (worldItems[item][SHORTDESC])))
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
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text) and worldItems[item].get(EDIBLE, False):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_stats(self, arg):
        """Display player stats, weapon, and accessory"""
        print(Style.DIM + '--- Stats ---' + Style.NORMAL + Fore.WHITE)
        print('  HP: ' + str(PLAYERHP) + '/ MP: ' + str(PLAYERMP))
        print('  Hero Level: ' + str(PLAYERLVL))
        print('  Hero XP: '+ str(PLAYERXP))
        print('  You have ' + str(FLOYDS) + ' Floyds.')
        print('  Equipped Weapon: ' + equippedWeapon + ' [+' + str(worldItems[equippedWeapon][ATKBNS]) + ']')
        print('  Added FX: ' + addedFX + ' [+' + str(worldItems[addedFX][ATKBNS]) + ']')
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
            if worldItems[item].get(WEAPON, False) == False:
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print(('Ted equips %s' % (worldItems[item][SHORTDESC])))
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
            if worldItems[item].get(FX, False) == False:
                cantEquip = True
                continue # there may be other items named this that Ted can equip, so we continue checking
            print(('Ted adds %s' % (worldItems[item][SHORTDESC])))
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
    print(Style.BRIGHT + introtext[INTRO1] + '\n')
    time.sleep(2)
    clear()
    print(Style.DIM + introtext[INTRO2] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + introtext[INTRO2] + '\n')
    print(Style.DIM + introtext[INTRO3] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.BRIGHT + introtext[INTRO2] + '\n')
    print(Style.NORMAL + introtext[INTRO3] + '\n')
    print(Style.DIM + introtext[INTRO4] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + introtext[INTRO2] + '\n')
    print(Style.BRIGHT + introtext[INTRO3] + '\n')
    print(Style.NORMAL + introtext[INTRO4] + '\n')
    print(Style.DIM + introtext[INTRO5] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + introtext[INTRO2] + '\n')
    print(Style.NORMAL + introtext[INTRO3] + '\n')
    print(Style.BRIGHT + introtext[INTRO4] + '\n')
    print(Style.NORMAL + introtext[INTRO5] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + introtext[INTRO2] + '\n')
    print(Style.NORMAL + introtext[INTRO3] + '\n')
    print(Style.NORMAL + introtext[INTRO4] + '\n')
    print(Style.BRIGHT + introtext[INTRO5] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + introtext[INTRO2] + '\n')
    print(Style.NORMAL + introtext[INTRO3] + '\n')
    print(Style.NORMAL + introtext[INTRO4] + '\n')
    print(Style.NORMAL + introtext[INTRO5] + '\n')
    time.sleep(0.1)
    clear()
    print(Style.NORMAL + introtext[INTRO2] + '\n')
    print(Style.NORMAL + introtext[INTRO3] + '\n')
    print(Style.NORMAL + introtext[INTRO4] + '\n')
    print(Style.NORMAL + introtext[INTRO5] + '\n')
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
