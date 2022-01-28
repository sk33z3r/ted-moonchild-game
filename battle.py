import curses
from textwrap import wrap
from time import sleep
from curses.textpad import Textbox, rectangle
from random import randrange, choice
import engine as eng
import database as dbs
import art

class battleUI():

    # function to write a message to the player
    def writeLog(msg, style):

        global eventLine

        if eventLine >= 15:
            eventWin.clear()
            eventLine = 1

        # display the message
        eventWin.addstr(eventLine, 0, msg, eng.c[style])

        eventLine += 1

    # funcion to clear and write the STATS section
    def writeStats():

        # setup the strings
        hpString = "HP:   {0}/{1}".format(playerBattleStats["HP"]["CUR"], playerBattleStats["HP"]["MAX"])
        mpString = "MP:   {0}/{1}".format(playerBattleStats["MP"]["CUR"], playerBattleStats["MP"]["MAX"])

        # check if each bonus is negative or not, and adjust printout
        atkBase = playerBattleStats["ATK"]["BASE"]
        atkBns = playerBattleStats["ATK"]["BONUS"]
        atkString = "{0:>6} {1:>2}{2:<+3} = {3:^2}".format("ATK:", atkBase, atkBns, (atkBase + atkBns))

        defBase = playerBattleStats["DEF"]["BASE"]
        defBns = playerBattleStats["DEF"]["BONUS"]
        defString = "{0:>6} {1:>2}{2:<+3} = {3:^2}".format("DEF:", defBase, defBns, (defBase + defBns))

        mojoBase = playerBattleStats["MOJO"]["BASE"]
        mojoBns = playerBattleStats["MOJO"]["BONUS"]
        mojoString = "{0:>6} {1:>2}{2:<+3} = {3:^2}".format("MOJO:", mojoBase, mojoBns, (atkBase + mojoBns))

        lukBase = playerBattleStats["LUK"]["BASE"]
        lukBns = playerBattleStats["LUK"]["BONUS"]
        lukString = "{0:>6} {1:>2}{2:<+3} = {3:^2}".format("LUK:", lukBase, lukBns, (lukBase + lukBns))

        accBase = playerBattleStats["ACC"]["BASE"]
        accBns = playerBattleStats["ACC"]["BONUS"]
        accString = "{0:>6} {1:>2}{2:<+3} = {3:^2}".format("ACC:", accBase, accBns, (accBase + accBns))

        # add each stat string
        statsWin.addstr(1, 4, hpString, eng.c["RED"])
        statsWin.addstr(2, 4, mpString, eng.c["BLUE"])
        statsWin.addstr(4, 1, atkString, eng.c["DIM_YELLOW"])
        statsWin.addstr(5, 1, defString, eng.c["DIM_YELLOW"])
        statsWin.addstr(6, 1, mojoString, eng.c["DIM_YELLOW"])
        statsWin.addstr(7, 1, lukString, eng.c["DIM_YELLOW"])
        statsWin.addstr(8, 1, accString, eng.c["DIM_YELLOW"])

        # setup the strings
        instString = "INST: {0}".format(dbs.equippedInstrument)
        fxString = "FX: {0}".format(dbs.addedFX)
        headString = "HEAD: {0}".format(dbs.equippedHead)

        # display the equipment strings
        statsBorder.addstr(11, 1, "  EQUIPPED            ", eng.c["REVERSE_DIM_CYAN"])
        statsWin.addstr(12, 0, headString, eng.c["DIM_CYAN"])
        statsWin.addstr(13, 0, instString, eng.c["DIM_CYAN"])
        statsWin.addstr(14, 2, fxString, eng.c["DIM_CYAN"])

    # function to clear and write the INVENTORY section
    def writeInv():

        # clear and refresh info
        invWin.clear()
        eng.refreshInfo()

        # get and sort all item lists individually
        i = list(dbs.playerInv["ITEMS"])
        i = sorted(i)

        # get a count of each item in the ITEMS list only
        itemCount = {}
        for item in i:
            if item in list(itemCount.keys()):
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # set starting line in the window
        s = 3

        # set header
        invBorder.addstr(1, 1, "{0: ^25}".format("BATTLE ITEMS"), eng.c["REVERSE_DIM_GREEN"])
        invBorder.addstr(2, 1, "{0: >3} {1: <12} {2: <8}".format('#', 'Item', 'Effect'), eng.c["REVERSE_DIM_GREEN"])

        # print items from ITEMS with their item count
        if len(i) != 0:
            for item in set(i):
                if "BATTLE" in dbs.items.find_one( { "NAME": item } ):
                    effectString = eng.getEffectString(item)
                    itemString = "{0:>2}x {1:<12} {2:<7}".format(str(itemCount[item]), item, effectString)
                    invWin.addstr(s, 0, itemString, eng.c["DIM"])
                    s += 1

    def writeMenu():

        menuWin.clear()

        menuWin.addstr(1, 2, "{0: ^20}".format(""), eng.c["REVERSE_DIM"])
        menuWin.addstr(2, 2, "{0: ^20}".format("ATTACK"), eng.c["REVERSE_DIM"])
        menuWin.addstr(3, 2, "{0: ^20}".format(""), eng.c["REVERSE_DIM"])

        menuWin.addstr(5, 2, "{0: ^20}".format(""), eng.c["REVERSE_DIM"])
        menuWin.addstr(6, 2, "{0: ^20}".format("MOJO ABILITIES"), eng.c["REVERSE_DIM"])
        menuWin.addstr(7, 2, "{0: ^20}".format(""), eng.c["REVERSE_DIM"])

        menuWin.addstr(1, 24, "{0: ^20}".format(""), eng.c["REVERSE_DIM"])
        menuWin.addstr(2, 24, "{0: ^20}".format("USE ITEM"), eng.c["REVERSE_DIM"])
        menuWin.addstr(3, 24, "{0: ^20}".format(""), eng.c["REVERSE_DIM"])

        menuWin.addstr(5, 24, "{0: ^20}".format(""), eng.c["REVERSE_DIM"])
        menuWin.addstr(6, 24, "{0: ^20}".format("ESCAPE"), eng.c["REVERSE_DIM"])
        menuWin.addstr(7, 24, "{0: ^20}".format(""), eng.c["REVERSE_DIM"])

    # function specifically to parse commands and run their relevant functions
    def runAction(cmd, arg):

        # TODO run the selected action
        sleep(1)

    # function to pick and print the initial stats for an encounter
    def initEnemy():

        global enemyBattleStats

        # TODO pick a random enemy (weighted) from the current planet
        availableEnemies = []

        for e in dbs.enemies.find( { } ):
            if dbs.PLANET in e["PLANETS"]:
                availableEnemies.append(e["NAME"])

        chosenEnemy = choice(availableEnemies)

        # setup enemy stats
        dbs.getEnemyInfo(chosenEnemy)

        # write the enemy's name onto the border
        displayName = " ENEMY: {0} ".format(chosenEnemy.upper())
        x = 48 - len(displayName)
        enemyStatsBorder.addstr(0, x, displayName, eng.c["DIM"])

        # load enemy stats into memory
        enemyBattleStats = dbs.getEnemyDict()

        # display the enemy information
        battleUI.writeEnemy(enemyBattleStats)

        # set the description to show at the bottom
        y = 19

        # print enemy shortdesc
        description = "\n".join(wrap(dbs.enemyInfo["DESC"], 44))
        enemyStatsWin.addstr(y, 0, description)

    def writeEnemy(enemyBattleStats):

        # setup the strings
        hpString = "HP: {0}/{1}".format(enemyBattleStats["HP"]["CUR"], enemyBattleStats["HP"]["MAX"])
        mpString = "MP: {0}/{1}".format(enemyBattleStats["MP"]["CUR"], enemyBattleStats["MP"]["MAX"])
        atkString = "ATK: {0}".format(enemyBattleStats["ATK"])
        defString = "DEF: {0}".format(enemyBattleStats["DEF"])
        mojoString = "MOJO: {0}".format(enemyBattleStats["MOJO"])
        lukString = "LUK: {0}".format(enemyBattleStats["LUK"])
        accString = "ACC: {0}".format(enemyBattleStats["ACC"])

        # display the enemy's image from the art module
        y, l = 4, 0
        enemyArt = art.ENEMIES[dbs.enemyInfo["NAME"]]

        # print each line with style from the art dict
        while l < len(enemyArt):
            enemyStatsBorder.addstr(y, 13, enemyArt[str(l)][1], eng.c[enemyArt[str(l)][0]])
            l += 1
            y += 1

        # add each string
        enemyStatsWin.addstr(1, 15, hpString, eng.c["RED"])
        enemyStatsWin.addstr(1, 28, mpString, eng.c["BLUE"])
        enemyStatsWin.addstr(3, 1, atkString, eng.c["DIM_YELLOW"])
        enemyStatsWin.addstr(4, 1, defString, eng.c["DIM_YELLOW"])
        enemyStatsWin.addstr(5, 0, mojoString, eng.c["DIM_YELLOW"])
        enemyStatsWin.addstr(6, 1, lukString, eng.c["DIM_YELLOW"])
        enemyStatsWin.addstr(7, 1, accString, eng.c["DIM_YELLOW"])

    def rewriteScreen():

        # rewrites current data into their sections
        battleUI.writeInv()
        battleUI.writeStats()
        battleUI.writeEnemy()
        battleUI.writeMenu()

    # function to initialize the UI and get user input
    def displayBattle():

        # define globals
        global playerBattleStats
        global eventLine

        # get stats
        playerBattleStats = dbs.getPlayerDict()

        # set the event starting line
        eventLine = 1

        # write all data to the screen
        battleUI.initEnemy()
        battleUI.writeStats()
        battleUI.writeInv()
        battleUI.writeMenu()

        t = 0
        while t < 25:
            battleUI.writeLog("Ted smashes the {0} for 10 damage!".format(dbs.enemyInfo["NAME"]), "RED")
            sleep(0.5)
            t += 1

        # main command input loop
        while True:
            userInput = battleUI.getCmd()
            #battleUI.processCmd(userInput)

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

    # wait for user input
    def getCmd():

        sleep(5)

    # function to clear all screens
    def clearAllScreens():

        screen.clear()
        enemyStatsBorder.clear()
        enemyStatsWin.clear()
        menuBorder.clear()
        menuWin.clear()
        invBorder.clear()
        invWin.clear()
        eventBorder.clear()
        eventWin.clear()
        statsBorder.clear()
        statsWin.clear()

    # define the main world UI screen boundaries
    def build(stdscr):

        # define globals
        global statsBorder
        global statsWin
        global menuBorder
        global menuWin
        global invBorder
        global invWin
        global eventBorder
        global eventWin
        global enemyStatsBorder
        global enemyStatsWin
        global begin_y
        global begin_x
        global max_x
        global max_y
        global screen

        screen = stdscr

        # define max size
        max_x = 110
        max_y = 40

        # get current terminal size and setup UI positions
        height, width = stdscr.getmaxyx()
        begin_y, begin_x = eng.calculateWindows(height, width, max_y, max_x, "battle")

        # refresh info in memory
        eng.refreshInfo()

        # setup the main window and color dict
        stdscr.clear()
        stdscr.immedok(True)
        eng.setStyles()
        curses.curs_set(0)

        # ENEMY INFO
        # define the border
        enemyStatsBorder = stdscr.subwin(eng.battleEnemyDims["border"][0], eng.battleEnemyDims["border"][1], eng.battleEnemyDims["border"][2], eng.battleEnemyDims["border"][3])
        enemyStatsBorder.immedok(True)
        enemyStatsBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        # define the content area
        enemyStatsWin = stdscr.subwin(eng.battleEnemyDims["content"][0], eng.battleEnemyDims["content"][1], eng.battleEnemyDims["content"][2], eng.battleEnemyDims["content"][3])
        enemyStatsWin.immedok(True)

        # EVENTS
        # define the border
        eventBorder = stdscr.subwin(eng.battleEventDims["border"][0], eng.battleEventDims["border"][1], eng.battleEventDims["border"][2], eng.battleEventDims["border"][3])
        eventBorder.immedok(True)
        eventBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        eventBorder.addstr(0, 2, " LOG ", eng.c["DIM"])
        # define the content area
        eventWin = stdscr.subwin(eng.battleEventDims["content"][0], eng.battleEventDims["content"][1], eng.battleEventDims["content"][2], eng.battleEventDims["content"][3])
        eventWin.immedok(True)

        # STATS
        # define the border
        statsBorder = stdscr.subwin(eng.battleStatDims["border"][0], eng.battleStatDims["border"][1], eng.battleStatDims["border"][2], eng.battleStatDims["border"][3])
        statsBorder.immedok(True)
        statsBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        statsBorder.addstr(0, 2, " TED MOONCHILD ", eng.c["DIM"])
        # define the content area
        statsWin = stdscr.subwin(eng.battleStatDims["content"][0], eng.battleStatDims["content"][1], eng.battleStatDims["content"][2], eng.battleStatDims["content"][3])
        statsWin.immedok(True)

        # INVENTORY
        # define the border
        invBorder = stdscr.subwin(eng.battleInvDims["border"][0], eng.battleInvDims["border"][1], eng.battleInvDims["border"][2], eng.battleInvDims["border"][3])
        invBorder.immedok(True)
        invBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, curses.ACS_TTEE, eng.tr, curses.ACS_BTEE, eng.lr)
        # define content area
        invWin = stdscr.subwin(eng.battleInvDims["content"][0], eng.battleInvDims["content"][1], eng.battleInvDims["content"][2], eng.battleInvDims["content"][3])
        invWin.immedok(True)

        # MENU
        # define the border
        menuBorder = stdscr.subwin(eng.battleMenuDims["border"][0], eng.battleMenuDims["border"][1], eng.battleMenuDims["border"][2], eng.battleMenuDims["border"][3])
        menuBorder.immedok(True)
        menuBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        menuBorder.addstr(0, 39, " ACTIONS ", eng.c["DIM"])
        # define the content area
        menuWin = stdscr.subwin(eng.battleMenuDims["content"][0], eng.battleMenuDims["content"][1], eng.battleMenuDims["content"][2], eng.battleMenuDims["content"][3])
        menuWin.immedok(True)

        # run the world command loop
        battleUI.displayBattle()

        return
