import os, curses, sys
from curses.textpad import Textbox, rectangle
from time import sleep
from textwrap import wrap
import engine as eng
import database as dbs
from world import worldUI
import art

class main():

    # function to display the logo
    def displayLogo(delay):

        # clear the main window
        logoWin.clear()

        # display the logo
        top = art.LOGO["TOP"]
        mid = art.LOGO["MID"]
        low = art.LOGO["LOW"]

        # set logo height
        logoHeight = len(top) + len(mid) + len(low)
        l = 0

        # setup loop for the top
        p = 0
        while p < len(top) and l < logoHeight:
            line = top[str(p)]
            style = eng.c[line[0]]
            logoWin.addstr(l, 2, "{0: ^76}".format(line[1]), style)
            p += 1
            l += 1

        sleep(delay)

        # reset loop for mid
        p = 0
        while p < len(mid) and l < logoHeight:
            line = mid[str(p)]
            style = eng.c[line[0]]
            logoWin.addstr(l, 2, "{0: ^76}".format(line[1]), style)
            p += 1
            l += 1

        sleep(delay)

        # reset loop for low
        p = 0
        while p < len(low) and l < logoHeight:
            line = low[str(p)]
            style = eng.c[line[0]]
            logoWin.addstr(l, 2, "{0: ^76}".format(line[1]), style)
            p += 1
            l += 1

    # function to run the intro animation
    def introAnimation():

        # clear everything
        main.clearAllScreens()
        sleep(1)

        # run the intro story
        l, i = 3, 0
        for line in art.INTRO:
            logoWin.addstr(l, 0, "\n".join(wrap(art.INTRO[str(i)][1], 75)), eng.c[art.INTRO[str(i)][0]])

            if len(art.INTRO[str(i)][1]) > 75:
                l += 3
                sleep(5)
            else:
                l += 2
                sleep(3)

            i += 1

        # do the logo animation
        main.displayLogo(2)

        sleep(4)

    # function to print the exit message
    def exitGame():

        # clear the screen and display the logo
        screen.clear()

        # TODO display logo and a message
        main.displayLogo(0)
        mainWin.addstr(2, 0, "{0: ^76}".format("Thanks for ROCKING with Ted. See ya later, nerd!"), eng.c["RED"])

        sleep(5)

        # exit application
        sys.exit()

    # function to start the game
    def startGame(where):

        # it's a new game
        if where == "new":

            # ask about the intro
            mainWin.clear()
            mainWin.addstr(2, 0, "{0: ^76}".format("Watch the intro animation? (yes/no)"), eng.c["CYAN"])
            choice = main.getCmd()

            # TODO port animation to mongo and curses
            if choice == "yes" or choice == "y":
                main.introAnimation()

            # otherwise just start the game
            else:
                pass

        # initiate the curses UI
        worldUI.build(screen)

        # prep the exit screen
        main.exitGame()

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

        # if the cmd is new game, start the new game menu
        if args[0] in ("new", "n", "create"):
            main.newGameMenu()

        # if the cmd is load, start the load game menu
        elif args[0] in ("load", "l"):
            main.loadGameMenu()

        # if the cmd is to exit, then exit
        elif args[0] in ("exit", "quit"):
            main.exitGame()

    # wait for user input
    def getCmd():

        # clear and get input ready
        inputWin.clear()
        curses.curs_set(2)
        userInput = inputCmd.edit().lower().strip()
        curses.curs_set(0)
        inputWin.clear()
        return userInput

    # function for the main menu
    def menu():

        main.displayLogo(0)

        # main command input loop
        while True:

            # print the options
            mainWin.clear()
            mainWin.addstr(1, 20, "COMMANDS:", eng.c["DIM"])
            mainWin.addstr(3, 24, "{0: >4} | {1: <25}".format("new", "Fucking ROCK a new story"), eng.c["DIM_YELLOW"])
            mainWin.addstr(4, 24, "{0: >4} | {1: <25}".format("load", "Load your old shitty save"), eng.c["DIM_CYAN"])
            mainWin.addstr(5, 24, "{0: >4} | {1: <25}".format("quit", "Exit this garbage"), eng.c["DIM_RED"])

            userInput = main.getCmd()
            main.processCmd(userInput)

    def loadGameMenu():

                # for each folder in ./save-states, print the name and its index
                slots = [ "_index" ]
                for s in os.listdir("./save-states"):
                    slots.append(s)

                # sort the list
                slots = sorted(slots)

                # if there any slots, show them and ask for input
                if len(slots) > 1:

                    # clear the screen
                    mainWin.clear()

                    # display a message
                    mainWin.addstr(2, 0, "{0: ^38}".format("Enter a save slot or 'back'"), eng.c["DIM_YELLOW"])
                    mainWin.addstr(3, 0, "{0: ^38}".format("to return to the main menu."), eng.c["DIM_YELLOW"])

                    # display the existing save slots
                    mainWin.addstr(0, 40, "{0: ^38}".format("Existing Save Slots:"), eng.c["CYAN"])
                    i, l = 1, 2

                    # for each folder in ./save-states, print the name and its index
                    while i < len(slots):
                        string = "[{0}] - {1}".format(str(i), slots[i])
                        mainWin.addstr(l, 40, "{0: ^38}".format(string), eng.c["DIM_CYAN"])
                        i += 1
                        l += 1

                    slotChoice = main.getCmd()

                    # set the new slotName
                    if slotChoice.isdigit():
                        slotName = slots[int(slotChoice)]
                    else:
                        slotName = slotChoice

                    # back returns to main menu
                    if slotName == "back":
                        return

                    # otherwise try to match the name
                    elif slotName in slots:
                        dbs.loadGame(slotName)
                        main.startGame("load")

                    # if nothing works, tell the player
                    else:
                        mainWin.clear()
                        mainWin.addstr(2, 0, "{0: ^76}".format("Save slot doesn't exist!"), eng.c["DIM_RED"])
                        sleep(2)
                        return

                # if there are no save slots, ask to make a new save instead
                else:
                    # clear the screen and print the message
                    mainWin.clear()
                    mainWin.addstr(1, 0, "{0: ^76}".format("No save slots exist!"), eng.c["DIM_RED"])
                    mainWin.addstr(2, 0, "{0: ^76}".format("Enter a new save slot name or"), eng.c["DIM_RED"])
                    mainWin.addstr(3, 0, "{0: ^76}".format("back to return to the main menu"), eng.c["DIM_RED"])

                    # ask for a slot name
                    slotName = main.getCmd()

                    # back returns to main menu
                    if slotName == "back":
                        return

                    # setup a new save slot then start the game
                    dbs.newGame(slotName)
                    main.startGame("new")

    def newGameMenu():

        # clear the screen
        mainWin.clear()

        # print the message
        mainWin.addstr(2, 0, "{0: ^76}".format("Enter the name for the new save slot."), eng.c["YELLOW"])

        # ask for an option
        slotName = main.getCmd()

        # get a list of slots already saved
        slots = [ "_index" ]
        for s in os.listdir("./save-states"):
            slots.append(s)

        # sort the list
        slots = sorted(slots)

        # if the entered name is back, return to main menu
        if slotName == "back":
            return

        # if the slot doesn't already exist
        elif slotName not in slots:

            # and if the slot amount is already 3
            if len(slots) >= 4:

                # clear the screen
                mainWin.clear()

                # print the message
                mainWin.addstr(2, 0, "{0: ^38}".format("You already have 3 slots saved!"), eng.c["RED"])
                mainWin.addstr(3, 0, "{0: ^38}".format("Create a new save with an existing"), eng.c["RED"])
                mainWin.addstr(4, 0, "{0: ^38}".format("name to overwrite one!"), eng.c["RED"])
                mainWin.addstr(0, 40, "{0: ^38}".format("Existing Save Slots:"), eng.c["CYAN"])

                l = 2
                # print list of found saves
                for s in slots:
                    if s == "_index":
                        pass
                    else:
                        string = "[{0}] - {1}".format(str(slots.index(s)), s)
                        mainWin.addstr(l, 40, "{0: ^38}".format(string), eng.c["DIM_CYAN"])
                        l += 1

                # get a slot name from the user again
                slotChoice = main.getCmd()

                # set the new slotName
                if slotChoice.isdigit():
                    slotName = slots[int(slotChoice)]
                else:
                    slotName = slotChoice

            else:
                # otherwise create the new game and start
                dbs.newGame(slotName)
                main.startGame("new")
                return

        # otherwise, if the slot exists
        if slotName in slots:

            # clear the screen
            mainWin.clear()

            # print the message
            mainWin.addstr(2, 0, "{0: ^76}".format("Save slot already exists! Overwrite? (yes/no)"), eng.c["RED"])

            # get the answer
            ans = main.getCmd()

            # if yes, delete the old save and make a new one
            if ans == "y" or ans == "yes":

                # if yes, remove the old slot name
                slots.remove(slotName)

                # clear the screen
                mainWin.clear()

                # print the message
                mainWin.addstr(2, 0, "{0: ^76}".format("Overwriting save game!"), eng.c["GREEN"])
                mainWin.addstr(3, 0, "{0: ^76}".format("Enter a name for this save slot:"), eng.c["GREEN"])

                # get a slot name from the user again
                newSlotName = main.getCmd()

                if newSlotName not in slots:

                    # if the delete operation is successful, run the game
                    if dbs.deleteSave(slotName, True) == True:
                        dbs.newGame(newSlotName)
                        main.startGame("new")

                    # otherwise print an error and return to the main menu
                    else:
                        mainWin.clear()
                        mainWin.addstr(2, 0, "{0: ^76}".format("Something went wrong when deleting the old save."), eng.c["BRIGHT_RED"])
                        sleep(2)
                        return

                else:

                    # clear the screen
                    mainWin.clear()

                    # print the message
                    mainWin.addstr(2, 0, "{0: ^76}".format("That name matches another slot!"), eng.c["RED"])

                    # return to menu
                    sleep(2)
                    return

            # otherwise, don't do it
            else:

                # clear the screen
                mainWin.clear()

                # print the message
                mainWin.addstr(2, 0, "{0: ^76}".format("Not overwriting save slot."), eng.c["RED"])

                # return to menu
                sleep(2)
                return

        else:

            # clear the screen
            mainWin.clear()

            # print the message
            mainWin.addstr(2, 0, "{0: ^76}".format("That slot doesn't exist, but you already have 3 slots saved. Try again."), eng.c["RED"])

            # return to menu
            sleep(2)
            return

    # function to clear all screens
    def clearAllScreens():

        screen.clear()
        logoWin.clear()
        mainBorder.clear()
        mainWin.clear()
        inputWin.clear()

    # function for the initial UI definitions
    def build(stdscr):

        # define globals
        global logoWin
        global mainBorder
        global mainWin
        global inputBorder
        global inputWin
        global inputCmd
        global begin_y
        global begin_x
        global max_x
        global max_y
        global screen

        screen = stdscr

        # define max size
        max_x = 80
        max_y = 30

        # get current terminal size and setup UI positions
        height, width = stdscr.getmaxyx()
        begin_y, begin_x = eng.calculateWindows(height, width, max_y, max_x, "main")

        # setup the main window and color dict
        stdscr.clear()
        stdscr.immedok(True)
        eng.setStyles()
        curses.curs_set(0)

        # LOGO
        logoWin = stdscr.subwin(eng.mainDims["logo"][0], eng.mainDims["logo"][1], eng.mainDims["logo"][2], eng.mainDims["logo"][3])
        logoWin.immedok(True)

        # MAIN
        # define the border
        mainBorder = stdscr.subwin(eng.mainDims["border"][0], eng.mainDims["border"][1], eng.mainDims["border"][2], eng.mainDims["border"][3])
        mainBorder.immedok(True)
        # define the content area
        mainWin = stdscr.subwin(eng.mainDims["content"][0], eng.mainDims["content"][1], eng.mainDims["content"][2], eng.mainDims["content"][3])
        mainWin.immedok(True)

        # PROMPT
        # define the border
        inputBorder = stdscr.subwin(eng.mainInputDims["border"][0], eng.mainInputDims["border"][1], eng.mainInputDims["border"][2], eng.mainInputDims["border"][3])
        inputBorder.immedok(True)
        # define the content area
        inputWin = stdscr.subwin(eng.mainInputDims["content"][0], eng.mainInputDims["content"][1], eng.mainInputDims["content"][2], eng.mainInputDims["content"][3])
        inputWin.immedok(True)
        inputCmd = Textbox(inputWin, insert_mode=True)
        # place PROMPT in the input window
        stdscr.addstr(eng.mainInputDims["prompt"][0], eng.mainInputDims["prompt"][1], eng.PROMPT, eng.c["RED"])

        # run the menu
        main.menu()

if __name__ == '__main__':

    curses.wrapper(main.build)
