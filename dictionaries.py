from colorama import Fore, Back, Style
import globalVars as vars

worldRooms = {
    'EBGB Stage': {
        vars.DESC: 'Ted finishes wrapping cables and tearing down the stage.'
            + '\n\n'
            + Fore.CYAN + 'TED: ' + Style.BRIGHT + '"I\'m gettin\' too old for this shit."' + Style.NORMAL + Fore.WHITE
            + '\n\n'
            + 'The bar is winding down for the night.'
            + '\n',
        vars.NORTH: 'EBGB Dance Floor',
        vars.EAST: 'EBGB Backstage',
        vars.WEST: 'EBGB Bathrooms',
        vars.PLANET: 'Zappa',
        vars.GROUND: ['Empty Bottle', 'Stack of Cables', 'Drums']},
    'EBGB Dance Floor': {
        vars.DESC: 'Ted walks out onto the dance floor. There are two drunk hippies making out'
            + '\n'
            + 'furiously. Ted tries to ignore them.'
            + '\n\n'
            + 'The bartender can be seen wiping down the bar; last call hasn\'t been announced.'
            + '\n',
        vars.NORTH: 'EBGB Parking Lot',
        vars.EAST: 'EBGB Bar',
        vars.SOUTH: 'EBGB Stage',
        vars.WEST: 'EBGB Jukebox',
        vars.PLANET: 'Zappa',
        vars.GROUND: ['Guitar Pick', 'Broken Drumstick']},
    'EBGB Backstage': {
        vars.DESC: 'Ted finds himself trudging through a sea of beer cans, roaches, and used'
            + '\n'
            + 'condoms. Lying on top of a case is a grungy white guitar that was used'
            + '\n'
            + 'by the cover band.'
            + '\n\n'
            + Fore.CYAN + 'TED: ' + Style.BRIGHT + '"Dumbass left his guitar."' + Style.NORMAL + Fore.WHITE
            + '\n',
        vars.WEST: 'EBGB Stage',
        vars.PLANET: 'Zappa',
        vars.GROUND: ['Squire Strat', 'Used Condom', 'Chaz Note']},
    'EBGB Bathrooms': {
        vars.DESC: 'The smell of piss and shit from the hippies at the show tonight is overbearing.'
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
        vars.EAST: 'EBGB Stage',
        vars.PLANET: 'Zappa',
        vars.GROUND: ['Lit Joint']},
    'EBGB Bar': {
        vars.DESC: 'Ted sizes up the bartender. He\'s a large rotund individual from the planet'
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
        vars.NORTH: 'EBGB Parking Lot',
        vars.WEST: 'EBGB Dance Floor',
        vars.SHOP: ['Dark Matter Ale'],
        vars.PLANET: 'Zappa',
        vars.GROUND: []},
    'EBGB Jukebox': {
        vars.DESC: 'Ted needs to listen to some tunes, so he walks over to the ratty Jukebox that\'s'
            + '\n'
            + 'probably been here for centuries.'
            + '\n\n'
            + 'There are 4 buttons, and a blinking slot with text that reads: ' + Style.BRIGHT + Fore.GREEN + 'INSERT 5 FLOYDS' + Style.NORMAL + Fore.WHITE
            + '\n',
        vars.NORTH: 'EBGB Parking Lot',
        vars.EAST: 'EBGB Dance Floor',
        vars.PLANET: 'Zappa',
        vars.GROUND: []},
    'EBGB Parking Lot': {
        vars.DESC: 'Ted leaves EBGBs to find his sweet looking Winnibego in the parking lot.'
            + '\n\n'
            + 'To the east is a swirling black wormhole. It\'s sucking in small bits of debris'
            + '\n'
            + 'from the ground around it.'
            + '\n',
        vars.EAST: 'Black Wormhole',
        vars.NORTH: 'Winnibego',
        vars.SOUTH: 'EBGB Bar',
        vars.PLANET: 'Zappa',
        vars.GROUND: []},
    'Black Wormhole': {
        vars.DESC: 'Ted steps into the black wormhole. As he reaches the event'
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
        vars.WEST: 'EBGB Parking Lot',
        vars.SHOP: ['Magic Mushies', 'ACiD', 'Mescalin', 'Amanitas'],
        vars.PLANET: 'Universe',
        vars.GROUND: []},
    'Winnibego': {
        vars.DESC: 'Ted\'s trusty steed, the ol\' Winnie. It smells of dude and weed in here.'
            + '\n\n'
            + 'Ted sees a flashing light on the console that reads: ' + Fore.GREEN + 'IGNITION' + Style.NORMAL + Fore.WHITE
            + '\n',
        vars.DOWN: 'EBGB Parking Lot',
        vars.PLANET: 'Travel',
        vars.GROUND: []},
    }

# worldItems dictionary
# TODO convert dictionary to SQLlite3
'''
Syntax
    '': {
        vars.GROUNDDESC: '',
        vars.SHORTDESC: '',
        vars.LONGDESC: '',
        vars.TAKEABLE: True,
        vars.WEAPON: True,
        vars.FX: True,
        vars.EDIBLE: True,
        vars.BATTLE: True,
        vars.ATKBNS: 0,
        vars.DESCWORDS: ['']},
'''

worldItems = {
    'Fists': {
        vars.GROUNDDESC: 'Ted\'s raw fists',
        vars.SHORTDESC: 'his fists',
        vars.LONGDESC: 'Ted\'s manly fucking fists. They\'ve beaten many faces into the ground.',
        vars.TAKEABLE: True,
        vars.WEAPON: True,
        vars.ATKBNS: 0,
        vars.DESCWORDS: ['fists']},
    'noFX': {
        vars.GROUNDDESC: 'Raw tone',
        vars.SHORTDESC: 'air',
        vars.LONGDESC: 'Nothing but tone.',
        vars.TAKEABLE: True,
        vars.FX: True,
        vars.ATKBNS: 0,
        vars.DESCWORDS: ['nofx']},
    'Winnibego Keys': {
        vars.GROUNDDESC: 'Keys to the Winnie',
        vars.SHORTDESC: 'the keys to the Winnie',
        vars.LONGDESC: 'The keys to Ted\'s sweet Winnibego',
        vars.TAKEABLE: True,
        vars.DESCWORDS: ['keys', 'winnie keys']},
    'Protection': {
        vars.GROUNDDESC: 'Protection',
        vars.SHORTDESC: 'protection',
        vars.LONGDESC: 'The best protection the galaxy has to offer against the buzzoids.',
        vars.TAKEABLE: True,
        vars.BATTLE: True,
        vars.DESCWORDS: ['protection']},
    'Squire Strat': {
        vars.GROUNDDESC: 'Chaz Lightyear\'s Guitar',
        vars.SHORTDESC: 'the Squire Strat',
        vars.LONGDESC: 'A beat up strat that used to be white. It gets the job done.',
        vars.TAKEABLE: True,
        vars.WEAPON: True,
        vars.ATKBNS: 1,
        vars.DESCWORDS: ['chaz\'s guitar', 'chaz guitar', 'strat', 'stratocaster']},
    'Used Condom': {
        vars.GROUNDDESC: 'Slimy condom',
        vars.SHORTDESC: 'the jimmy hat',
        vars.LONGDESC: 'It\'s stuck to the table. Probably should leave it for the cleaning crew.',
        vars.TAKEABLE: False,
        vars.EDIBLE: True,
        vars.DESCWORDS: ['jimmy hat', 'condom', 'cum sock']},
    'Chaz Note': {
        vars.GROUNDDESC: 'Handwritten note',
        vars.SHORTDESC: 'the note',
        vars.LONGDESC: 'A note in Chaz\'s sloppy handwriting: ' + Fore.YELLOW + 'Yo Ted, a scout at the show wants us to' + '\n' + 'sign with \'em. We\'re heading to their station after the gig, see you later bro.' + Style.NORMAL + Fore.WHITE,
        vars.TAKEABLE: True,
        vars.DESCWORDS: ['note']},
    'Empty Bottle': {
        vars.GROUNDDESC: 'Empty bottle',
        vars.SHORTDESC: 'the empty bottle',
        vars.LONGDESC: 'An empty bottle of Dark Matter Ale. Ted wishes it was full.',
        vars.TAKEABLE: False,
        vars.DESCWORDS: ['bottle', 'empty bottle']},
    'Stack of Cables': {
        vars.GROUNDDESC: 'Cables',
        vars.SHORTDESC: 'the cables',
        vars.LONGDESC: 'A stack of professionally coiled cables, no thanks to Ted.',
        vars.TAKEABLE: False,
        vars.DESCWORDS: ['cables', 'stack of cables', 'cable stack']},
    'Drums': {
        vars.GROUNDDESC: 'Drum Kit',
        vars.SHORTDESC: 'the kit',
        vars.LONGDESC: 'EBGB\'s house kit. It\'s missing the cymbals.',
        vars.TAKEABLE: False,
        vars.DESCWORDS: ['drums', 'kit']},
    'Dark Matter Ale': {
        vars.GROUNDDESC: 'Refreshing Dark Ale',
        vars.SHORTDESC: 'the Dark Matter Ale',
        vars.LONGDESC: 'A cold refreshing ale brewed in the outer rim of the galaxy. The label claims' + '\n' + 'to have an alcohol content of 2.08x10^15.',
        vars.TAKEABLE: True,
        vars.EDIBLE: True,
        vars.BATTLE: True,
        vars.DESCWORDS: ['ale', 'bottle of ale', 'dark matter ale', 'dark matter']},
    'Guitar Pick': {
        vars.GROUNDDESC: 'Rip Curl\'s pick',
        vars.SHORTDESC: 'the guitar pick',
        vars.LONGDESC: 'The pick that Rip Curl threw into the crowd at EBGBs.',
        vars.TAKEABLE: True,
        vars.FX: True,
        vars.ATKBNS: 1,
        vars.DESCWORDS: ['pick', 'guitar pick']},
    'Broken Drumstick': {
        vars.GROUNDDESC: 'Grumm\'s broken stick',
        vars.SHORTDESC: 'the wood shard',
        vars.LONGDESC: 'Piece of a broken stick that Grumm tossed into the crowd at EBGBs. Ted wonders' + '\n' + 'where the other half ended up.',
        vars.TAKEABLE: True,
        vars.DESCWORDS: ['stick', 'wood shard']},
    'Lit Joint': {
        vars.GROUNDDESC: 'Hippy\'s J',
        vars.SHORTDESC: 'the lit joint',
        vars.LONGDESC: 'A cherried joint some hippy gave Ted for not beating the shit out of him.',
        vars.TAKEABLE: True,
        vars.BATTLE: True,
        vars.DESCWORDS: ['joint', 'j', 'hippy j', 'jay', 'lit joint', 'lit j']},
    'Magic Mushies': {
        vars.GROUNDDESC: 'Magic Mushies',
        vars.SHORTDESC: 'the shrooms',
        vars.LONGDESC: 'A bag full of shriveled brown mushrooms. Looks like enough for two people, or one roadie.',
        vars.TAKEABLE: True,
        vars.EDIBLE: True,
        vars.BATTLE: True,
        vars.DESCWORDS: ['shrooms', 'mushies', 'magic shrooms']},
    'ACiD': {
        vars.GROUNDDESC: 'ACiD',
        vars.SHORTDESC: 'the acid tab',
        vars.LONGDESC: 'A small, square, white tab of paper. If you don\'t own a spaceship, this is a great alternative.',
        vars.TAKEABLE: True,
        vars.EDIBLE: True,
        vars.BATTLE: True,
        vars.DESCWORDS: ['acid', 'tab']},
    'Mescalin': {
        vars.GROUNDDESC: 'Mescalin',
        vars.SHORTDESC: 'the peyote',
        vars.LONGDESC: 'It\'s a tiny peyote plant. Crack this baby open and get ready for a ride!',
        vars.TAKEABLE: True,
        vars.EDIBLE: True,
        vars.BATTLE: True,
        vars.DESCWORDS: ['mescalin', 'peyote']},
    'Amanitas': {
        vars.GROUNDDESC: 'Amanitas',
        vars.SHORTDESC: 'the red cap',
        vars.LONGDESC: 'Mushrooms with bright red caps and little white dots. Let\'s hope these aren\'t the poisonus genus...',
        vars.TAKEABLE: True,
        vars.EDIBLE: True,
        vars.BATTLE: True,
        vars.DESCWORDS: ['amanitas', 'red caps', 'other mushrooms']},
    'Epiphone SG': {
        vars.GROUNDDESC: 'Used Epiphone SG',
        vars.SHORTDESC: 'Epiphone SG',
        vars.LONGDESC: 'Not quite a Gibson, but it looks fuckin\' sweet.',
        vars.TAKEABLE: True,
        vars.WEAPON: True,
        vars.ATKBNS: 2,
        vars.DESCWORDS: ['sg', 'epiphone']},
    'Wormhole Delay': {
        vars.GROUNDDESC: 'Delay pedal from Wormhole',
        vars.SHORTDESC: 'Wormhole Delay',
        vars.LONGDESC: 'Delay FX from another world. Use sparingly.',
        vars.TAKEABLE: True,
        vars.FX: True,
        vars.ATKBNS: 2,
        vars.DESCWORDS: ['delay', 'delay pedal', 'wormhole']},
    }

# enemies dictionary
# TODO convert dictionary to SQLlite3
'''
Syntax
    '': {
        vars.ENDESC: '',
        vars.HP: 0,
        vars.MP: 0,
        vars.ATTACKMIN: 0,
        vars.ATTACKMAX: 0,
        vars.CRITBNS: 0,
        vars.CR: 0,
        vars.DIALOG: ['']},
'''

enemies = {
    'Buzzoid': {
        vars.ENDESC: 'A hideous bug like creature that smells of liquor and sewage.'
            + '\n',
        vars.HP: 15,
        vars.MP: 10,
        vars.ATTACKMIN: 1,
        vars.ATTACKMAX: 3,
        vars.CRITBNS: 1,
        vars.DIALOG: ['It spits in your face!', 'It flaps its pathetic wings with great force!']},
    'Zappan': {
        vars.ENDESC: 'Ted isn\'t quite sure what to make of this round object that gargles at him.'
            + '\n',
        vars.HP: 20,
        vars.MP: 15,
        vars.ATTACKMIN: 2,
        vars.ATTACKMAX: 5,
        vars.CRITBNS: 2,
        vars.DIALOG: ['It throws a dog-doo snow cone!', 'It rubs yellow snow in your eye!']},
    }

# challenge rating dictionary
challenge = {
    '0': { vars.XPAWARD: 50, vars.CRITBNS: 1 },
    '1': { vars.XPAWARD: 100, vars.CRITBNS: 1 },
    '2': { vars.XPAWARD: 250, vars.CRITBNS: 1 },
    '3': { vars.XPAWARD: 500, vars.CRITBNS: 2 },
    '4': { vars.XPAWARD: 1000, vars.CRITBNS: 2 },
    '5': { vars.XPAWARD: 1800, vars.CRITBNS: 2 },
    '6': { vars.XPAWARD: 2300, vars.CRITBNS: 2 },
    '7': { vars.XPAWARD: 2900, vars.CRITBNS: 3 },
    '8': { vars.XPAWARD: 3900, vars.CRITBNS: 3 },
    '9': { vars.XPAWARD: 5000, vars.CRITBNS: 3 },
    '10': { vars.XPAWARD: 5900, vars.CRITBNS: 3 },
    '11': { vars.XPAWARD: 7200, vars.CRITBNS: 4 },
    '12': { vars.XPAWARD: 8400, vars.CRITBNS: 4 },
    '13': { vars.XPAWARD: 10000, vars.CRITBNS: 4 },
    '14': { vars.XPAWARD: 11500, vars.CRITBNS: 4 },
    '15': { vars.XPAWARD: 13000, vars.CRITBNS: 5 },
    '16': { vars.XPAWARD: 15000, vars.CRITBNS: 5 },
    '17': { vars.XPAWARD: 18000, vars.CRITBNS: 5 },
    '18': { vars.XPAWARD: 20000, vars.CRITBNS: 6 },
    '19': { vars.XPAWARD: 22000, vars.CRITBNS: 6 },
    '20': { vars.XPAWARD: 25000, vars.CRITBNS: 7 },
}

# Contains all available hero attacks
heroAttacks = {
    'Punch': {
        vars.HEROMIN: 0,
        vars.HEROMAX: 3,},
    'Headbang': {
        vars.HEROMIN: 2,
        vars.HEROMAX: 5,},
    }

# Contains all available hero magic
'''
Syntax
    '' = {
        vars.MPREQ: 0,
        vars.MAGDMG: 0,},
'''
heroMagic = {
    'Rising Force': {
        vars.MPREQ: 2,
        vars.MAGDMG: 2,},
    'Purple Rain': {
        vars.MPREQ: 3,
        vars.MAGDMG: 3,},
    }

# intro
introtext = {
    vars.INTRO1: 'The year is 4420',
    vars.INTRO2: 'Mankind has expanded its reach beyond the solar system',
    vars.INTRO3: 'Many righteous bands tour the galaxy looking for wealth, fame, and loose women,'
        + '\n'
        + 'but there is now an evil that lurks in the vast darkness of space.',
    vars.INTRO4: 'The evil conglomerates of Earth\'s past return to enslave the Gods of Metal'
        + '\n'
        + 'by cryogenically freezing and replacing them with their clone-step army.',
    vars.INTRO5: 'There is only one crew that can put a stop to this madness...',
    }