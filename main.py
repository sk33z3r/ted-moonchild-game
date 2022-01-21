import os, natsort, time
import engine as eng
import database as dbs
import art
from world import worldUI

def exitScreen():
    eng.clear()
    art.printLogo()
    print("             =======================================")
    print("             |        Thanks for rockin'!          |")
    print("             =======================================\n")

def startGame(where):
    if where == "new":
        print("Watch the intro animation? (yes/no)")
        choice = input(eng.PROMPT)
        if choice == "yes" or choice == "y":
            art.introAnimation()
        else:
            pass
    exitScreen()
    worldUI.start()

def menu():
    while True:
        eng.clear()
        art.printLogo()
        print("             =======================================")
        print("             | Press n to fucking ROCK a new story |")
        print("             | Press l to load your shitty save    |")
        print("             =======================================\n")
        holdOn = input(eng.PROMPT)
        if holdOn == 'l':
            while True:
                eng.clear()
                art.printLogo()
                print("             =======================================")
                print("             |        Enter a save slot or         |")
                print("             |   back to return to the main menu   |")
                print("             =======================================\n")
                slots = [ "_index" ]
                i = 1
                for s in natsort.natsorted(os.listdir("./save-states")):
                    print("  [" + str(i) + "] - " + s)
                    slots.append(s)
                    i += 1
                print()
                slots.sort()
                if len(slots) > 1:
                    slotChoice = input(eng.PROMPT)
                    if slotChoice == "back":
                        break
                    if slotChoice.isdigit():
                        try:
                            dbs.loadGame(slots[int(slotChoice)])
                        except:
                            print("Save slot doesn't exist!")
                            time.sleep(2)
                            continue
                        startGame("load")
                        break
                    elif slotChoice in slots:
                        dbs.loadGame(slotChoice)
                        startGame("load")
                        break
                    else:
                        print("Save slot doesn't exist!")
                        time.sleep(2)
                        continue
                else:
                    eng.clear()
                    art.printLogo()
                    print("             =======================================")
                    print("             |        No save slots exist!         |")
                    print("             |    Enter a new save slot name or    |")
                    print("             |   back to return to the main menu   |")
                    print("             =======================================\n")
                    slotName = input(eng.PROMPT)
                    if slotName == "back":
                        break
                    dbs.newGame(slotName)
                    startGame("new")
                    break
        elif holdOn == 'n':
            loaded = "no"
            while loaded == "no":
                eng.clear()
                art.printLogo()
                print("             =======================================")
                print("             |    Enter a new save slot name or    |")
                print("             |   back to return to the main menu   |")
                print("             =======================================\n")
                slotName = input(eng.PROMPT)
                slots = []
                for s in os.listdir("./save-states"):
                    slots.append(s)
                slots.sort()
                if slotName == "back":
                    break
                elif slotName not in slots:
                    if len(slots) >= 3:
                        eng.clear()
                        art.printLogo()
                        print("    =========================================================")
                        print("    |           You already have 3 slots saved!             |")
                        print("    | Create a new save with an existing name to overwrite! |")
                        print("    =========================================================\n")
                        print("Save Slots Found:")
                        for s in slots:
                            print("  " + s)
                        time.sleep(3)
                        print("Returning to the title screen.")
                        break
                    dbs.newGame(slotName)
                    startGame("new")
                    break
                else:
                    eng.clear()
                    art.printLogo()
                    print("         =================================================")
                    print("         | Save slot already exists! Overwrite? (yes/no) |")
                    print("         =================================================\n")
                    ans = input(eng.PROMPT)
                    if ans == "n" or ans == "no":
                        print("Not Overwriting.")
                        time.sleep(2)
                        continue
                    elif ans == "y" or ans == "yes":
                        print("Okay, overwriting save slot with a new game!")
                        time.sleep(1)
                        dbs.deleteSave(slotName, True)
                        dbs.newGame(slotName)
                        startGame("new")
                        break
        elif holdOn == "quit" or holdOn == "exit":
            break
        else:
            continue

if __name__ == '__main__':

    menu()