import os, curses, sys
from curses.textpad import Textbox, rectangle
from time import sleep
from natsort import natsorted
import engine as eng
import database as dbs
import art
from world import worldUI

class main():

    # function to print the exit message
    def exitGame():

        # clear the screen and display the logo
        mainWin.clear()
        inputWin.clear()

        # TODO display logo and a message

        # exit application
        sys.exit()

    # function to start the game
    def startGame(where):

        # it's a new game
        if where == "new":

            # ask about the intro
            mainWin.clear()
            mainWin.addstr(2, 18, "Watch the intro animation? (yes/no)", eng.c["CYAN"])
            choice = main.getCmd()

            # if yes, run the intro
            if choice == "yes" or choice == "y":
                art.introAnimation()

            # otherwise just start the game
            else:
                pass

        # initiate the curses UI
        worldUI.build()

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

        # clear the main window
        logoWin.clear()

        # display the logo
        l = 0
        while l < len(art.logo):
            logoWin.addstr(l, 5, art.logo[str(l)][1], eng.c["YELLOW"])
            l += 1

        # main command input loop
        while True:

            # print the options
            mainWin.clear()
            mainWin.addstr(1, 19, "COMMANDS:", eng.c["DIM"])
            mainWin.addstr(3, 19, "     new |  Fucking ROCK a new story", eng.c["DIM_YELLOW"])
            mainWin.addstr(4, 19, "    load |  Load your old shitty save", eng.c["DIM_CYAN"])
            mainWin.addstr(5, 19, "    quit |  Exit this garbage", eng.c["DIM_RED"])

            userInput = main.getCmd()
            main.processCmd(userInput)

    def loadGameMenu():

                # for each folder in ./save-states, print the name and its index
                slots = [ "_index" ]
                for s in natsorted(os.listdir("./save-states")):
                    slots.append(s)

                # if there any slots, show them and ask for input
                if len(slots) > 1:

                    # clear the screen
                    mainWin.clear()

                    # display a message
                    mainWin.addstr(2, 12, "Enter a save slot or 'back'", eng.c["DIM_YELLOW"])
                    mainWin.addstr(3, 12, "to return to the main menu.", eng.c["DIM_YELLOW"])

                    # display the existing save slots
                    mainWin.addstr(1, 47, "Existing Save Slots:", eng.c["CYAN"])
                    i, l = 1, 2

                    # for each folder in ./save-states, print the name and its index
                    while i < len(slots):
                        string = "[{0}] - {1}".format(str(i), slots[i])
                        mainWin.addstr(l, 51, string, eng.c["DIM_CYAN"])
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
                        #main.startGame("load") # TODO enable startGame

                    # if nothing works, tell the player
                    else:
                        mainWin.clear()
                        mainWin.addstr(2, 24, "Save slot doesn't exist!", eng.c["DIM_RED"])
                        sleep(2)
                        return

                # if there are no save slots, ask to make a new save instead
                else:
                    # clear the screen and print the message
                    mainWin.clear()
                    mainWin.addstr(1, 26, "No save slots exist!", eng.c["DIM_RED"])
                    mainWin.addstr(2, 21, "Enter a new save slot name or", eng.c["DIM_RED"])
                    mainWin.addstr(3, 20, "back to return to the main menu", eng.c["DIM_RED"])

                    # ask for a slot name
                    slotName = main.getCmd()

                    # back returns to main menu
                    if slotName == "back":
                        return

                    # setup a new save slot then start the game
                    dbs.newGame(slotName)
                    #main.startGame("new") # TODO enable startGame

    def newGameMenu():

        # clear the screen
        mainWin.clear()

        # print the message
        mainWin.addstr(2, 18, "Enter the name for the new save slot.", eng.c["YELLOW"])

        # ask for an option
        slotName = main.getCmd()

        # get a list of slots already saved
        slots = [ "_index" ]
        for s in os.listdir("./save-states"):
            slots.append(s)
        slots.sort()

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
                mainWin.addstr(2, 10, "You already have 3 slots saved!", eng.c["RED"])
                mainWin.addstr(3, 9, "Create a new save with an existing", eng.c["RED"])
                mainWin.addstr(4, 15, "name to overwrite one!", eng.c["RED"])
                mainWin.addstr(1, 47, "Existing Save Slots:", eng.c["CYAN"])

                l = 2
                # print list of found saves
                for s in slots:
                    if s == "_index":
                        pass
                    else:
                        string = "[{0}] - {1}".format(str(slots.index(s)), s)
                        mainWin.addstr(l, 51, string, eng.c["DIM_CYAN"])
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
                #main.startGame("new") # TODO enable startGame
                return

        # otherwise, if the slot exists
        if slotName in slots:

            # clear the screen
            mainWin.clear()

            # print the message
            mainWin.addstr(2, 13, "Save slot already exists! Overwrite? (yes/no)", eng.c["RED"])

            # get the answer
            ans = main.getCmd()

            # if yes, delete the old save and make a new one
            if ans == "y" or ans == "yes":

                # if yes, remove the old slot name
                slots.remove(slotName)

                # clear the screen
                mainWin.clear()

                # print the message
                mainWin.addstr(2, 25, "Overwriting save game!", eng.c["GREEN"])
                mainWin.addstr(3, 19, "Enter a name for this save slot:", eng.c["GREEN"])

                # get a slot name from the user again
                newSlotName = main.getCmd()

                if newSlotName not in slots:

                    dbs.deleteSave(slotName, True)
                    dbs.newGame(newSlotName)
                    #main.startGame("new") # TODO enable startGame

                else:

                    # clear the screen
                    mainWin.clear()

                    # print the message
                    mainWin.addstr(2, 22, "That name matches another slot!", eng.c["RED"])

                    # return to menu
                    sleep(2)
                    return

            # otherwise, don't do it
            else:

                # clear the screen
                mainWin.clear()

                # print the message
                mainWin.addstr(2, 23, "Not overwriting save slot.", eng.c["RED"])

                # return to menu
                sleep(2)
                return

        else:

            # clear the screen
            mainWin.clear()

            # print the message
            mainWin.addstr(2, 2, "That slot doesn't exist, but you already have 3 slots saved. Try again.", eng.c["RED"])

            # return to menu
            sleep(2)
            return

    # function to clear all screens
    def clearAllScreens():

        logoWin.clear()
        mainBorder.clear()
        mainWin.clear()
        inputBorder.clear()
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
        rectangle(stdscr, eng.mainInputDims["border"][0], eng.mainInputDims["border"][1], eng.mainInputDims["border"][2], eng.mainInputDims["border"][3])
        # define the content area
        inputWin = stdscr.subwin(eng.mainInputDims["content"][0], eng.mainInputDims["content"][1], eng.mainInputDims["content"][2], eng.mainInputDims["content"][3])
        inputWin.immedok(True)
        inputCmd = Textbox(inputWin, insert_mode=True)
        # place PROMPT in the input window
        stdscr.addstr(eng.mainInputDims["prompt"][0], eng.mainInputDims["prompt"][1], eng.PROMPT, eng.c["BRIGHT_RED"])

        # run the menu
        main.menu()

if __name__ == '__main__':

    curses.wrapper(main.build)
