import curses
from curses import panel
from textwrap import wrap
from time import sleep
from curses.textpad import Textbox, rectangle
from random import randrange, choice, choices
import engine as eng
import database as dbs
import art

class Menu(object):
    def __init__(self, items, stdscr):
        self.window = stdscr.subwin(eng.battleMenuDims["content"][0], eng.battleMenuDims["content"][1], eng.battleMenuDims["content"][2], eng.battleMenuDims["content"][3])
        self.window.immedok(True)
        self.window.keypad(True)
        curses.mousemask(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        # main menu loop
        while True:
            self.window.refresh()
            curses.doupdate()
            pos = 1
            for index, item in enumerate(self.items):

                # define the style for active and inactive buttons
                if index == self.position:
                    # active
                    style = "REVERSE"
                else:
                    # inactive
                    style = "REVERSE_DIM"

                # define each button's position
                if pos == 1:
                    self.window.addstr(1, 2, "{0: ^20}".format(""), eng.c[style])
                    self.window.addstr(2, 2, "{0: ^20}".format(item[0]), eng.c[style])
                    self.window.addstr(3, 2, "{0: ^20}".format(""), eng.c[style])
                elif pos == 2:
                    self.window.addstr(5, 2, "{0: ^20}".format(""), eng.c[style])
                    self.window.addstr(6, 2, "{0: ^20}".format(item[0]), eng.c[style])
                    self.window.addstr(7, 2, "{0: ^20}".format(""), eng.c[style])
                elif pos == 3:
                    self.window.addstr(1, 24, "{0: ^20}".format(""), eng.c[style])
                    self.window.addstr(2, 24, "{0: ^20}".format(item[0]), eng.c[style])
                    self.window.addstr(3, 24, "{0: ^20}".format(""), eng.c[style])
                elif pos == 4:
                    self.window.addstr(5, 24, "{0: ^20}".format(""), eng.c[style])
                    self.window.addstr(6, 24, "{0: ^20}".format(item[0]), eng.c[style])
                    self.window.addstr(7, 24, "{0: ^20}".format(""), eng.c[style])

                pos += 1

            # wait for the next key
            key = self.window.getch()

            # if it's ENTER, run the command at the current position
            if key in [ curses.KEY_ENTER, ord("\n"), ord(" "), 343 ]:
                self.items[self.position][1]()
                if exit_battle is True:
                    break

            # define clickable areas
            elif key == curses.KEY_MOUSE:

                try:
                    # get the current position of the click
                    _, mx, my, _, _ = curses.getmouse()

                    # top-left
                    if 50 <= mx <= 69 and 35 <= my <= 37:
                        self.position = 0
                        self.items[0][1]()

                    # bottom-left
                    elif 50 <= mx <= 69 and 39 <= my <= 41 and len(self.items) > 1:
                        self.position = 1
                        self.items[1][1]()

                    # top-right
                    elif 72 <= mx <= 91 and 35 <= my <= 37 and len(self.items) > 2:
                        self.position = 2
                        self.items[2][1]()

                    # bottom-right
                    elif 72 <= mx <= 91 and 39 <= my <= 41 and len(self.items) > 3:
                        self.position = 3
                        self.items[3][1]()
                        if exit_battle is True:
                            break

                # if an ERR is encountered, ignore it and move on
                except curses.error:
                    pass

            # if it's a number, try to move to that position
            elif key in [ ord("1"), ord("2"), ord("3"), ord("4") ] and int(chr(key)) <= len(self.items):
                self.position = int(chr(key)) - 1

            # if it's HOME or BACKSPACE, return to the previous menu
            elif key in [ curses.KEY_BACKSPACE, curses.KEY_HOME, 27 ]:
                break

            # Define where UP takes you from each position
            elif key in [ curses.KEY_UP, ord("w"), ord("W") ]:
                if self.position == 0:
                    self.position = 0
                elif self.position == 1:
                    self.position = 0
                elif self.position == 2:
                    self.position = 2
                elif self.position == 3:
                    self.position = 2

            # Define where LEFT takes you from each position
            elif key in [ curses.KEY_LEFT, ord("a"), ord("A") ]:
                if self.position == 0:
                    self.position = 0
                elif self.position == 1:
                    self.position = 1
                elif self.position == 2:
                    self.position = 0
                elif self.position == 3:
                    self.position = 1

            # Define where DOWN takes you from each position
            elif key in [ curses.KEY_DOWN, ord("s"), ord("S") ]:
                if self.position == 0 and len(self.items) > 1:
                    self.position = 1
                elif self.position == 1:
                    self.position = 1
                elif self.position == 2 and len(self.items) > 3:
                    self.position = 3
                elif self.position == 3:
                    self.position = 3

            # Define where RIGHT takes you from each position
            elif key in [ curses.KEY_RIGHT, ord("d"), ord("D") ]:
                if self.position == 0 and len(self.items) > 2:
                    self.position = 2
                elif self.position == 1 and len(self.items) > 3:
                    self.position = 3
                elif self.position == 2:
                    self.position = 2
                elif self.position == 3:
                    self.position = 3

        # clear and hide the panel when the loop exits
        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

class battleUI():

    # function to write a message to the player
    def writeLog(msg, style):

        global eventLine

        if eventLine >= 15:
            eventWin.clear()
            eventLine = 1

        # display the message
        eventWin.addstr(eventLine, 1, msg, eng.c[style])

        eventLine += 1

    # funcion to clear and write the STATS section
    def writeStats():

        # setup the strings
        hpString = "{0: >5} {1: >4} / {2: <6}".format("HP:", playerBattleStats["HP"]["CUR"], playerBattleStats["HP"]["MAX"])
        mpString = "{0: >5} {1: >4} / {2: <6}".format("MP:", playerBattleStats["MP"]["CUR"], playerBattleStats["MP"]["MAX"])

        # check if each bonus is negative or not, and adjust printout
        atkBase = playerBattleStats["ATK"]["BASE"]
        atkBns = playerBattleStats["ATK"]["BONUS"]
        atkString = "{0:>5} {1:>3}{2:<+4} = {3:^4}".format("ATK:", atkBase, atkBns, (atkBase + atkBns))

        defBase = playerBattleStats["DEF"]["BASE"]
        defBns = playerBattleStats["DEF"]["BONUS"]
        defString = "{0:>5} {1:>3}{2:<+4} = {3:^4}".format("DEF:", defBase, defBns, (defBase + defBns))

        mojoBase = playerBattleStats["MOJO"]["BASE"]
        mojoBns = playerBattleStats["MOJO"]["BONUS"]
        mojoString = "{0:>5} {1:>3}{2:<+4} = {3:^4}".format("MOJO:", mojoBase, mojoBns, (atkBase + mojoBns))

        lukBase = playerBattleStats["LUK"]["BASE"]
        lukBns = playerBattleStats["LUK"]["BONUS"]
        lukString = "{0:>5} {1:>3}{2:<+4} = {3:^4}".format("LUK:", lukBase, lukBns, (lukBase + lukBns))

        accBase = playerBattleStats["ACC"]["BASE"]
        accBns = playerBattleStats["ACC"]["BONUS"]
        accString = "{0:>5} {1:>3}{2:<+4} = {3:^4}".format("ACC:", accBase, accBns, (accBase + accBns))

        # add each stat string
        statsWin.addstr(1, 0, hpString, eng.c["RED"])
        statsWin.addstr(2, 0, mpString, eng.c["BLUE"])
        statsWin.addstr(4, 0, atkString, eng.c["DIM_YELLOW"])
        statsWin.addstr(5, 0, defString, eng.c["DIM_YELLOW"])
        statsWin.addstr(6, 0, mojoString, eng.c["DIM_YELLOW"])
        statsWin.addstr(7, 0, lukString, eng.c["DIM_YELLOW"])
        statsWin.addstr(8, 0, accString, eng.c["DIM_YELLOW"])

        # setup the strings
        instString = "{0: >5} {1: ^14}".format("INST:", dbs.equippedInstrument)
        fxString = "{0: >5} {1: ^14}".format("FX:", dbs.addedFX)
        headString = "{0: >5} {1: ^14}".format("HEAD:", dbs.equippedHead)

        # display the equipment strings
        statsBorder.addstr(11, 1, "{0: ^22}".format("EQUIPPED"), eng.c["REVERSE_DIM_CYAN"])
        statsWin.addstr(12, 0, headString, eng.c["DIM_CYAN"])
        statsWin.addstr(13, 0, instString, eng.c["DIM_CYAN"])
        statsWin.addstr(14, 0, fxString, eng.c["DIM_CYAN"])

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
        invBorder.addstr(2, 1, "{0: >3} {1: <12} {2: <8}".format('#', 'ITEM', 'EFFECT'), eng.c["REVERSE_DIM_GREEN"])

        # print items from ITEMS with their item count
        if len(i) != 0:
            for item in set(i):
                if "BATTLE" in dbs.items.find_one( { "NAME": item } ):
                    effectString = eng.getEffectString(item)
                    itemString = "{0:>2}x {1:<12} {2:<7}".format(str(itemCount[item]), item, effectString)
                    invWin.addstr(s, 0, itemString, eng.c["DIM"])
                    s += 1

    # function specifically to parse commands and run their relevant functions
    def runAction(cmd, arg):

        # TODO run the selected action
        sleep(1)

    # function to pick and print the initial stats for an encounter
    def initEnemy():

        # define globals
        global enemyBattleStats

        # setup enemy name list and weights from the planets db
        enemies = dbs.planets.find_one( { "PLANET": dbs.PLANET } )["ENEMY"]["NAMES"]
        weights = dbs.planets.find_one( { "PLANET": dbs.PLANET } )["ENEMY"]["WEIGHTS"]

        # choose a random enemy based on the weights
        chosenEnemy = choices(enemies, weights=weights)

        # setup enemy stats
        dbs.getEnemyInfo(chosenEnemy[0])

        # write the enemy's name onto the border
        displayName = " ENEMY: {0} ".format(chosenEnemy[0].upper())
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

    # function to initialize the UI and get user input
    def displayBattle():

        # define globals
        global playerBattleStats
        global eventLine
        global exit_battle
        global next_turn

        # get stats
        playerBattleStats = dbs.getPlayerDict()

        # set the event starting line
        eventLine = 1

        # set initial states
        exit_battle = False

        # decide who goes first
        rand = randrange(1, 100)
        if rand > 50:
            next_turn = "enemy"
            battleUI.writeLog("The enemy flanked you, Ted!", "DIM_RED")
        else:
            next_turn = "ted"
            battleUI.writeLog("You beat 'em to the punch, Ted!", "DIM_GREEN")

        # write all data to the screen
        battleUI.initEnemy()
        battleUI.writeStats()
        battleUI.writeInv()

        # main command input loop
        while exit_battle is False:
            battleUI.runMenu()

    def mojoAbility():
        battleUI.writeLog("You used a mojo ability!", "BLUE")

    def atkAbility():
        battleUI.writeLog("You used a regular attack!", "CYAN")

    def chooseItem():
        battleUI.writeLog("Item Menu coming soon!", "YELLOW")

    def escape():

        global exit_battle
        global next_turn

        # roll to see if the escape attempt is successful
        rand = randrange(1, 100)
        if rand >= 75:
            attempt = True
        else:
            attempt = False

        # if it fails, display a message and return to battle
        if attempt is False:
            battleUI.writeLog("Ted tripped when he tried to run!", "RED")
            exit_battle = False
            next_turn = "enemy"

        # if it succeeds, display a message and pause
        elif attempt is True:
            battleUI.writeLog("Ted is gettin' the fuck outta here!", "YELLOW")

            # if the player doesn't have any FLOYDS, don't bother trying to drop any
            if dbs.playerStats["FLOYDS"] != 0:

                # roll to see if the player loses any FLOYDS
                rand = randrange(1, 100)
                if rand >= 60:
                    drop_floyds = True
                else:
                    drop_floyds = False

                # if it fails, exit battle
                if drop_floyds is False:
                    battleUI.writeLog("Ted managed to hang onto all his coin.", "GREEN")
                    sleep(2)
                    exit_battle = True

                # if it succeeds, how many will they lose
                elif drop_floyds is True:

                    # pick an amount to remove
                    rand = randrange(0, 100)

                    # try to remove the FLOYDS from player
                    if dbs.floydsTransaction(rand, "dec") is True:
                        # print a message if they still have some FLOYDS left
                        battleUI.writeLog("Ted dropped {0} FLOYDS on the way out!".format(str(rand)), "YELLOW")
                    else:
                        # if not, set FLOYDS to 0 and tell the player about it
                        dbs.floydsTransaction(0, "set")
                        battleUI.writeLog("Ted lost his FLOYDS on the way out!".format(str(rand)), "YELLOW")

            # pause
            sleep (3)

            # exit battle
            exit_battle = True

    # wait for user input
    def runMenu():

        # make sure the cursor is hidden
        curses.curs_set(0)

        # define the attack menu
        attack_menu_items = [
            ("PUNCH",  battleUI.atkAbility)
        ]
        attack_menu = Menu(attack_menu_items, screen)

        # define the mojo menu
        mojo_menu_items = [
            ("RISING FORCE", battleUI.mojoAbility),
            ("PURPLE RAIN", battleUI.mojoAbility)
        ]
        mojo_menu = Menu(mojo_menu_items, screen)

        # define the main menu
        main_menu_items = [
            ("ATTACK", attack_menu.display),
            ("MOJO ABILITIES", mojo_menu.display),
            ("USE ITEM", battleUI.chooseItem),
            ("ESCAPE", battleUI.escape)
        ]
        main_menu = Menu(main_menu_items, screen)

        # run the main menu
        main_menu.display()

        return True

    # function to clear all screens
    def clearAllScreens():

        screen.clear()
        enemyStatsBorder.clear()
        enemyStatsWin.clear()
        menuBorder.clear()
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
        global next_turn
        global exit_battle

        screen = stdscr

        # define max size
        max_x = 101
        max_y = 36

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

        # run the world command loop
        battleUI.displayBattle()

        # clear screens before changing UIs
        battleUI.clearAllScreens()

        return True
