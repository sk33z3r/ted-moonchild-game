import os
from time import sleep
from natsort import natsorted
import engine as eng
import database as dbs
import art
from world import worldUI

# function to print the exit message
def exitScreen():

    # clear the screen and display the logo
    eng.clear()
    art.printLogo()

    # display a message
    print("             =======================================")
    print("             |        Thanks for rockin'!          |")
    print("             =======================================\n")

# function to start the game
def startGame(where):

    # it's a new game, ask about the intro
    if where == "new":
        print("Watch the intro animation? (yes/no)")
        choice = input(eng.PROMPT)
        if choice == "yes" or choice == "y":
            art.introAnimation()
        else:
            pass

    # prep the exit screen
    exitScreen()

    # initiate the curses UI
    worldUI.start()

# function for the main menu
def menu():

    # start a loop as a fallback
    while True:

        # clear the screen and display the logo
        eng.clear()
        art.printLogo()

        # ask for an option
        print("             =======================================")
        print("             | Press n to fucking ROCK a new story |")
        print("             | Press l to load your shitty save    |")
        print("             =======================================\n")
        holdOn = input(eng.PROMPT)

        # load a save
        if holdOn == 'l':

            # start another loop for the sub menu
            while True:

                # clear the screen and display the logo
                eng.clear()
                art.printLogo()

                # ask for a save slot choice
                print("             =======================================")
                print("             |        Enter a save slot or         |")
                print("             |   back to return to the main menu   |")
                print("             =======================================\n")

                # setup the for loop
                slots = [ "_index" ]
                i = 1

                # for each folder in ./save-states, print the name and its index
                for s in natsorted(os.listdir("./save-states")):
                    print("  [" + str(i) + "] - " + s)
                    slots.append(s)
                    i += 1
                print()

                # if there any slots, show them and ask for input
                if len(slots) > 1:
                    slotChoice = input(eng.PROMPT)

                    # back returns to main menu
                    if slotChoice == "back":
                        break

                    # if the user inputs a digit, try to load that index
                    if slotChoice.isdigit():
                        try:
                            dbs.loadGame(slots[int(slotChoice)])
                        except:
                            print("Save slot doesn't exist!")
                            sleep(2)
                            continue
                        startGame("load")
                        break

                    # otherwise try to match the name
                    elif slotChoice in slots:
                        dbs.loadGame(slotChoice)
                        startGame("load")
                        break

                    # if nothing works, tell the player
                    else:
                        print("Save slot doesn't exist!")
                        sleep(2)
                        continue

                # if there are no save slots, ask to make a new save instead
                else:

                    # clear the screen and display the logo
                    eng.clear()
                    art.printLogo()

                    # display the message
                    print("             =======================================")
                    print("             |        No save slots exist!         |")
                    print("             |    Enter a new save slot name or    |")
                    print("             |   back to return to the main menu   |")
                    print("             =======================================\n")

                    # ask for a slot name
                    slotName = input(eng.PROMPT)

                    # back returns to main menu
                    if slotName == "back":
                        break

                    # setup a new save slot then start the game
                    dbs.newGame(slotName)
                    startGame("new")

                    # break out of the loop
                    break

        # create a new game
        elif holdOn == 'n':

            # start a new loop for the sub menu
            while True:

                # clear the screen and display the logo
                eng.clear()
                art.printLogo()

                # display a message and ask for the slot name
                print("             =======================================")
                print("             |    Enter a new save slot name or    |")
                print("             |   back to return to the main menu   |")
                print("             =======================================\n")
                slotName = input(eng.PROMPT)

                # get a list of slots already saved
                slots = []
                for s in os.listdir("./save-states"):
                    slots.append(s)
                slots.sort()

                # if the entered name is back, return to main menu
                if slotName == "back":
                    break

                # if the slot doesn't already exist
                elif slotName not in slots:

                    # and if the slot amount is already 3
                    if len(slots) >= 3:

                        # clear the screen and display the logo
                        eng.clear()
                        art.printLogo()

                        # tell the user they need to overwrite a game
                        print("    =========================================================")
                        print("    |           You already have 3 slots saved!             |")
                        print("    | Create a new save with an existing name to overwrite! |")
                        print("    =========================================================\n")

                        # print list of found saves
                        print("Save Slots Found:")
                        for s in slots:
                            print("  " + s)

                        # return to the main menu after 3 seconds
                        sleep(3)
                        print("Returning to the title screen.")
                        break

                    # otherwise create the new game and start
                    dbs.newGame(slotName)
                    startGame("new")
                    break

                # otherwise, if the slot exists
                else:

                    # clear the screen and display the logo
                    eng.clear()
                    art.printLogo()

                    # ask the player to overwrite or not
                    print("         =================================================")
                    print("         | Save slot already exists! Overwrite? (yes/no) |")
                    print("         =================================================\n")
                    ans = input(eng.PROMPT)

                    # if no, don't do it and return to new save slot menu
                    if ans == "n" or ans == "no":
                        print("Not Overwriting.")
                        sleep(2)
                        continue

                    # if yes, delete the old save and make a new one
                    elif ans == "y" or ans == "yes":
                        print("Okay, overwriting save slot with a new game!")
                        sleep(1)
                        dbs.deleteSave(slotName, True)
                        dbs.newGame(slotName)
                        startGame("new")
                        break

        # quit the game
        elif holdOn == "quit" or holdOn == "exit":
            break

        # catch anything else
        else:
            continue

if __name__ == '__main__':

    # initiate the main menu
    menu()