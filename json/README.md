# TMATRIS JSON Schema

These files contain all the data needed for the python engine to display and move the character around the world. These values represent a new save game, starting from the beginning of the game.

Generally, there are 2 states data can be in while playing the game. There is always new data getting written to the database, and battles keep certain parameters stored for easier calculations. Although data is written directly to the database in most instances, it is not actually saved. The Mongo DB server is meant to be ephemeral, and the games are always loaded fresh from the saved states.

There are two moments currently where a snapshot of the DB is stored into files: 1) when the player requests it and 2) just before the player properly exits the game. If the game crashes, or is otherwise closed, before one of these two moments, then anything stored in the DB since the last time it occurred will be dropped upon the next load of that save state.

## Collection Dump and Import

The import process for a new game is as follows:

1. Drop any databases that already exist with a given name.
2. Iterate the list of files in this folder.
3. Create new DB and Collections based on the filenames.
4. Import each json to the respective collections.
    * NOTE: `locations_` files are broken out for simplifying maintenance. Each one is concatenated into the `locations` Collection.

The dump process for saving a game is as follows:

1. Dump each collection into json format.
2. Store each collection into their own file in `./save-states`.
3. Run regex on the files to remove an `"$oid"` from the `_id` field.
    * NOTE: For some reason, the json dumps in mongo add an extra bit of mongo code to the `_id` field. Mongo would fail to reimport the files that it had dumped, so I need to run regex on each file to fix this issue in the `_id` field.

The import process for a loaded game is as follows:

1. Drop any databases matching the name of the game to be loaded.
2. Find the matching directory in `./save-states`.
3. Iterate the folder of json to import a new collection per file.

## Schemas

### Abilities

The `abilities` collection holds data for all of Ted's potential abilities as he gains levels. There are currently only two types: physical and mojo. Each type has a set of fields that must be included with the ability.

Each document in the collection is defined by the following json:

```json
// physical attack
{
    "NAME": ${ABILITY NAME},
    "HEROMIN": ${MINIMUM DAMAGE},
    "HEROMAX": ${MAXIMUM DAMAGE},
    "TYPE": "physical"
}

// mojo attack
{
    "NAME": ${ABILITY NAME},
    "MPREQ": ${MP REQUIRED},
    "DMG": ${DAMAGE},
    "TYPE": "mojo"
}
```

### Challenge Ratings

The `challenge_ratings` collection keeps track of how strong enemies should be. Instead of hard-coding base stats per enemy, the Challenge Ratings give me a way to scale enemy strength and rewards throughout the game, so that no matter where Ted is the battles will be worth while and never too strong or too weak.

*Every rating requires all fields.*

Each document in the collection is defined by the following json:

```json
{
    "RATING": ${0 to 20},
    "XPAWARD": ${XP AWARDED},
    "FLOYDS": [ ${MIN FLOYDS}, ${MAX FLOYDS} ],
    "ATK": ${BASE ATK},
    "DEF": ${BASE DEF},
    "MOJO": ${BASE MOJO},
    "LUK": ${BASE LUK},
    "ACC": ${BASE ACC}
}
```

### Enemies

The `enemies` collection holds a document for each enemy that appears in the game. Some enemies will have stat modifiers to increase their power in special ways to add strategy to the game. If a stat is missing from the document, then python simply passes over it.

*All fields, other than stat modifiers, are required per enemy.*

Each document in the collection is defined by the following json:

```json
{
    "NAME": ${ENEMY NAME},
    "DESC": ${ENEMY DESCRIPTION},
    "HP": ${ENEMY HP},
    "MP": ${ENEMY MOJO},
    "ATK": ${ATTACK STAT MODIFIER},
    "DEF": ${DEFENSE STAT MODIFIER},
    "MOJO": ${MOJO STAT MODIFIER},
    "LUK": ${LUCK STAT MODIFIER},
    "ACC": ${ACCURACY STAT MODIFIER},
    "CR": ${CHALLENGE RATING},
    "ITEMS": [ ${LIST OF ITEMS THAT COULD DROP} ],
    "DIALOG": [ ${LIST OF DIALOGUE RESPONSES} ]
}
```

### Items

The `items` collection stores all information for each item in separate documents. Some item types require special fields, outlined below.

*Each field is required per type specifications.*

Each document in the collection is defined by the following json:

```json
// TYPE: instrument, fx, or head
{
    "NAME": ${ITEM NAME},
    "GROUNDDESC": ${GROUND DESCRIPTION},
    "SHORTDESC": ${SHORT DESCRIPTION},
    "LONGDESC": ${LONG DESCRIPTION},
    "TAKEABLE": true,
    "VALUE": ${ITEM COST},
    "TYPE": "instrument" or "fx" or "head",
    "BONUS": {
        "ATK": ${ATTACK STAT MODIFIER},
        "DEF": ${DEFENSE STAT MODIFIER},
        "MOJO": ${MOJO STAT MODIFIER},
        "LUK": ${LUCK STAT MODIFIER},
        "ACC": ${ACCURACY STAT MODIFIER}
    },
    "DESCWORDS": [ ${LIST OF WORDS FOR COMMANDS} ]
}

// TYPE: key
{
    "NAME": ${ITEM NAME},
    "GROUNDDESC": ${GROUND DESCRIPTION},
    "SHORTDESC": ${SHORT DESCRIPTION},
    "LONGDESC": ${LONG DESCRIPTION},
    "TAKEABLE": true,
    "VALUE": ${ITEM COST},
    "TYPE": "key",
    "DESCWORDS": [ ${LIST OF WORDS FOR COMMANDS} ]
}

// TYPE: crafted key
{
    "NAME": ${ITEM NAME},
    "GROUNDDESC": ${GROUND DESCRIPTION},
    "SHORTDESC": ${SHORT DESCRIPTION},
    "LONGDESC": ${LONG DESCRIPTION},
    "PIECES": [
        ${FIRST ITEM NEEDED},
        ${SECOND ITEM NEEDED}
    ],
    "TAKEABLE": true,
    "VALUE": ${ITEM COST},
    "TYPE": "key",
    "DESCWORDS": [ ${LIST OF WORDS FOR COMMANDS} ]
}

// TYPE: consumable
{
    "NAME": ${ITEM NAME},
    "GROUNDDESC": ${GROUND DESCRIPTION},
    "SHORTDESC": ${SHORT DESCRIPTION},
    "LONGDESC": ${LONG DESCRIPTION},
    "TAKEABLE": true,
    "BATTLE": true,
    "VALUE": ${ITEM COST},
    "TYPE": "food" or "drug" or "smoke" or "drink",
    "EFFECT": [
        ${STAT TO EFFECT},
        ${ONE OF: +, ++, +++, -, --, ---},
        ${VALUE OF EFFECT}
    ],
    "DESCWORDS": [ ${LIST OF WORDS FOR COMMANDS} ]
}

//TYPE: static
{
    "NAME": ${ITEM NAME},
    "GROUNDDESC": ${GROUND DESCRIPTION},
    "SHORTDESC": ${SHORT DESCRIPTION},
    "LONGDESC": ${LONG DESCRIPTION},
    "TAKEABLE": false,
    "VALUE": ${ITEM COST},
    "TYPE": "static",
    "DESCWORDS": [ ${LIST OF WORDS FOR COMMANDS} ]
}
```

### Levels

The `levels` collection stores all information for Ted's level progression. It determines how much XP is required to reach the level, defines max HP/MP, and awards the player with stat points to increase attributes.

*All fields are required for each level.*

Each document in the collection is defined by the following json:

```json
{
    "LEVEL": ${LEVEL},
    "XPREQ": ${XP REQUIRED},
    "HPMAX": ${MAXIMUM HP},
    "MPMAX": ${MAXIMUM MP},
    "SP": ${STAT POINTS AWARDED},
    "ABILITIES": [ ${LIST OF ABILITIES TO ADD} ],
    "MSG": [ ${LIST OF MESSAGES FOR THE PLAYER} ]
}
```

### Locations

The `locations` collection is actually a concatenation of several files. For maintenance purposes, I broke out each sector into their own files to store all of the planet rooms in. Once loaded into Mongo, there is no separation between sectors; all rooms have their own document inside the collection.

Every room type has mechanisms for whether the room has been visited, dialogue animation sequence definitions, and potential items or directions to add upon solving a puzzle.

#### Sector Files

These files contain all the main rooms that Ted navigates through. These are the rooms where battles and puzzles occur.

*All fields are required, other than directions and key event changes.*

Each document in the collection is defined by the following json:

```json
{
    "NAME": ${ROOM NAME},
    "SHORTDESC": [ ${STYLE}, ${STRING} ],
    "FIRST_EVENTS": {
        "0": [ ${STYLE}, ${STRING} ],
        "1": [ ${STYLE}, ${STRING} ]
    },
    "UNSOLVED_EVENTS": {
        "0": [ ${STYLE}, ${STRING} ],
        "1": [ ${STYLE}, ${STRING} ]
    },
    "KEY_EVENTS": {
        "0": [ ${STYLE}, ${STRING} ],
        "1": [ ${STYLE}, ${STRING} ]
    },
    "SOLVED_EVENTS": {
        "0": [ ${STYLE}, ${STRING} ],
        "1": [ ${STYLE}, ${STRING} ]
    },
    "EVENT_KEYS": [ ${LIST OF KEY ITEMS NEEDED TO SOLVE} ],
    "ADD_DIRS": {
        "0": [ ${DIRECTION}, ${ROOM NAME} ]
    },
    "DEL_GROUND": [ ${LIST OF ITEM NAMES} ],
    "ADD_GROUND": [ ${LIST OF ITEM NAMES} ],
    "NORTH": ${ROOM NAME},
    "SOUTH": ${ROOM NAME},
    "EAST": ${ROOM NAME},
    "WEST": ${ROOM NAME},
    "UP": ${ROOM NAME},
    "DOWN": ${ROOM NAME},
    "PLANET": ${PLANET NAME},
    "GROUND": [ ${LIST OF ITEM NAMES} ],
    "VISITED": ${0 or 1},
    "BATTLES": ${TRUE or FALSE},
    "SOLVED": ${0 or 1}
}
```

#### Winnibego Files

There are two files, `_winnibego` and `_space`, that are specifically for the Winnibego and its scenes and have slightly different mechanics than regular rooms. These are still ultimately stored in the `locations` collection. The data stored in these documents is more or less immutable. There should be no reason to duplicate these documents for any reason, only additions to them. The structure for each location is largely the same as other locations. Look into each file to see how it is laid out.

* Winnibego has a storage mechanism, so the user can store equipment or other items to free up inventory space if needed, and change their battle strategy with a cache of gear. This inventory is stored in the `player` collection.
* Whenever the Winnibego travels to a new planet, the DOWN direction has to change and so there is a special array for this.
* Each new sector in space will have its own visited parameter and set of dialogue to display on first visit. There are special dialogue arrays for each sector, and visited indicators to match.
* Each sector visited has a different set of available directions, so there is a special array to handle this.

*All fields are required.*

### Planets

The `planets` collection is mainly to keep track of what planets and enemies should appear in each sector.

*All fields are required.*

Each document in the collection is defined by the following json:

```json
{
    "PLANET": ${PLANET NAME},
    "SECTOR": ${SECTOR NAME},
    "ENEMY": {
        "NAMES": [ ${LIST OF ENEMY NAMES} ],
        "WEIGHTS": [ ${LIST OF WEIGHTS FOR EACH ENEMY} ]
    }
}
```

### Player

The `player` collection stores all details for the player's current state. This collection is split into separate documents to keep track of each category.

*All fields are required.*

Each document in the collection is defined by the following json:

```json
[
    {
        "SECTION": "location",
        "ROOM": ${CURRENT LOCATION},
        "PLANET": ${CURRENT PLANET},
        "SECTOR": ${CURRENT SECTOR}
    },
    {
        "SECTION": "stats",
        "HP": ${CURRENT HP},
        "HPMAX": ${MAXIMUM HP},
        "MP": ${CURRENT MP},
        "MPMAX": ${MAXIMUM MP},
        "ATK": ${BASE ATK STAT},
        "DEF": ${BASE DEF STAT},
        "MOJO": ${BASE MOJO STAT},
        "LUK": ${BASE LUK STAT},
        "ACC": ${BASE ACC STAT},
        "FLOYDS": ${CURRENT FLOYD COUNT},
        "LVL": ${CURRENT LEVEL},
        "XP": ${CURRENT XP AMOUNT}
    },
    {
        "SECTION": "inventory",
        "ITEMS": [ ${LIST OF ITEM NAMES} ],
        "KEY_ITEMS": [ ${LIST OF KEY ITEMS} ],
        "EQUIPPED": [ ${LIST OF ITEMS EQUIPPED} ],
        "WINNIE": [ ${LIST OF ITEMS ON WINNIE GROUND} ],
        "CAP": ${INVENTORY CARRY LIMIT}
    },
    {
        "SECTION": "equipped",
        "INSTRUMENT": ${CURRENT INSTRUMENT},
        "FX": ${CURRENT FX},
        "HEAD": ${CURRENT HEAD},
        "ATTACKS": [ ${LIST OF PHYSICAL ABILITIES} ],
        "MOJO": [ ${LIST OF MOJO ABILITIES} ]
    }
]
```
