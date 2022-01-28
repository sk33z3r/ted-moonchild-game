import curses
from textwrap import wrap
from time import sleep
from natsort import natsorted
from curses.textpad import Textbox, rectangle
from random import randrange, choice
import engine as eng
import database as dbs

class battleUI():

    # function to write a message to the player
    def writeLog(msg, style):

        # display the message
        eventWin.addstr(0, 0, msg, eng.c[style])

    # funcion to clear and write the STATS section
    def writeStats():

        # setup the strings
        hpString = "HP: {0}/{1}".format(playerBattleStats["HP"]["CUR"], playerBattleStats["HP"]["MAX"])
        mpString = "MP: {0}/{1}".format(playerBattleStats["MP"]["CUR"], playerBattleStats["MP"]["MAX"])
        atkString = "ATK: {0} +{1}".format(playerBattleStats["ATK"]["BASE"], playerBattleStats["ATK"]["BONUS"])
        defString = "DEF: {0} +{1}".format(playerBattleStats["DEF"]["BASE"], playerBattleStats["DEF"]["BONUS"])
        mojoString = "MOJO: {0} +{1}".format(playerBattleStats["MOJO"]["BASE"], playerBattleStats["MOJO"]["BONUS"])
        lukString = "LUK: {0} +{1}".format(playerBattleStats["LUK"]["BASE"], playerBattleStats["LUK"]["BONUS"])
        accString = "ACC: {0} +{1}".format(playerBattleStats["ACC"]["BASE"], playerBattleStats["ACC"]["BONUS"])

        # add each stat string
        statsWin.addstr(1, 6, hpString, eng.c["RED"])
        statsWin.addstr(2, 6, mpString, eng.c["BLUE"])
        statsWin.addstr(4, 5, atkString, eng.c["DIM_YELLOW"])
        statsWin.addstr(5, 5, defString, eng.c["DIM_YELLOW"])
        statsWin.addstr(6, 4, mojoString, eng.c["DIM_YELLOW"])
        statsWin.addstr(7, 5, lukString, eng.c["DIM_YELLOW"])
        statsWin.addstr(8, 5, accString, eng.c["DIM_YELLOW"])

        # setup the strings
        instString = "INST: {0}".format(dbs.equippedInstrument)
        fxString = "FX: {0}".format(dbs.addedFX)
        headString = "HEAD: {0}".format(dbs.equippedHead)

        # display the equipment strings
        statsBorder.addstr(11, 1, "  EQUIPPED            ", eng.c["REVERSE_DIM_CYAN"])
        statsWin.addstr(12, 1, instString, eng.c["DIM_CYAN"])
        statsWin.addstr(13, 3, fxString, eng.c["DIM_CYAN"])
        statsWin.addstr(14, 1, headString, eng.c["DIM_CYAN"])

    # function to clear and write the INVENTORY section
    def writeInv():

        # clear and refresh info
        invWin.clear()
        eng.refreshInfo()

        # get and sort all item lists individually
        i = list(dbs.playerInv["ITEMS"])
        i = natsorted(i)

        # get a count of each item in the ITEMS list only
        itemCount = {}
        for item in i:
            if item in list(itemCount.keys()):
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # set starting line in the window
        s = 2

        # set header
        invBorder.addstr(1, 1, "  BATTLE ITEMS           ", eng.c["REVERSE_DIM"])

        # print items from ITEMS with their item count
        if len(i) != 0:
            for item in set(i):
                effectString = eng.getEffectString(item)
                itemString = "{0}x {1} {2}".format(str(itemCount[item]), item, effectString)
                invWin.addstr(s, 0, itemString)
                s += 1

    # function specifically to parse commands and run their relevant functions
    def runAction(cmd, arg):

        # TODO run the selected action
        sleep(1)

    # function to pick and print the initial stats for an encounter
    def initEnemy():

        global enemyBattleStats

        # TODO pick a random enemy (weighted) from the current planet
        chosenEnemy = "Zappan"

        # setup enemy stats
        dbs.getEnemyInfo(chosenEnemy)

        # write the enemy's name onto the border
        displayName = " {0} ".format(chosenEnemy.upper())
        x = 48 - len(displayName)
        enemyStatsBorder.addstr(0, x, displayName, eng.c["REVERSE_DIM"])

        # load enemy stats into memory
        enemyBattleStats = dbs.getEnemyDict()

        # display the enemy information
        battleUI.writeEnemy(enemyBattleStats)

        # set the description to show at the bottom
        y = 19

        # print enemy shortdesc
        description = "\n".join(wrap(dbs.enemyInfo["DESC"], 44))
        enemyStatsWin.addstr(y, 0, description)

        # TODO get enemy art and print to screen

    def writeEnemy(enemyBattleStats):

        # setup the strings
        hpString = "HP: {0}/{1}".format(enemyBattleStats["HP"]["CUR"], enemyBattleStats["HP"]["MAX"])
        mpString = "MP: {0}/{1}".format(enemyBattleStats["MP"]["CUR"], enemyBattleStats["MP"]["MAX"])
        atkString = "ATK: {0}".format(enemyBattleStats["ATK"])
        defString = "DEF: {0}".format(enemyBattleStats["DEF"])
        mojoString = "MOJO: {0}".format(enemyBattleStats["MOJO"])
        lukString = "LUK: {0}".format(enemyBattleStats["LUK"])
        accString = "ACC: {0}".format(enemyBattleStats["ACC"])

        # image placeholder
        enemyImg = screen.derwin(15, 35, (begin_y + 4), (begin_x + 13))
        enemyImg.bkgd("#", eng.c["DIM"])

        # add each string
        enemyStatsWin.addstr(1, 2, hpString, eng.c["RED"])
        enemyStatsWin.addstr(1, 15, mpString, eng.c["BLUE"])
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

        # get stats
        playerBattleStats = dbs.getPlayerDict()

        # write all data to the screen
        battleUI.initEnemy()
        battleUI.writeStats()
        battleUI.writeInv()
        #battleUI.writeMenu()

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
        eventBorder.addstr(0, 2, " LOG ", eng.c["REVERSE_DIM"])
        # define the content area
        eventWin = stdscr.subwin(eng.battleEventDims["content"][0], eng.battleEventDims["content"][1], eng.battleEventDims["content"][2], eng.battleEventDims["content"][3])
        eventWin.immedok(True)

        # STATS
        # define the border
        statsBorder = stdscr.subwin(eng.battleStatDims["border"][0], eng.battleStatDims["border"][1], eng.battleStatDims["border"][2], eng.battleStatDims["border"][3])
        statsBorder.immedok(True)
        statsBorder.border(eng.lb, eng.rb, eng.tb, eng.bb, eng.tl, eng.tr, eng.ll, eng.lr)
        statsBorder.addstr(0, 2, " TED MOONCHILD ", eng.c["REVERSE_DIM"])
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
        menuBorder.addstr(0, 39, " ACTIONS ", eng.c["REVERSE_DIM"])
        # define the content area
        menuWin = stdscr.subwin(eng.battleMenuDims["content"][0], eng.battleMenuDims["content"][1], eng.battleMenuDims["content"][2], eng.battleMenuDims["content"][3])
        menuWin.immedok(True)

        # run the world command loop
        battleUI.displayBattle()
