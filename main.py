import os, natsort, time
from colorama import Fore, Back, Style
import art
import database as dbs
import engine as eng

if __name__ == '__main__':

    print(Back.BLACK + Fore.WHITE)
    title = "open"
    while title == "open":
        eng.clear()
        art.printLogo()
        print(Style.DIM + '             =======================================')
        print(Style.DIM + '             | ' + Style.NORMAL + 'Press ' + Fore.GREEN + 'n' + Fore.WHITE + ' to fucking ROCK a new story' + Style.DIM + ' |')
        print(Style.DIM + '             | ' + Style.NORMAL + 'Press ' + Fore.CYAN + 'l' + Fore.WHITE + ' to load your shitty save' + Style.DIM + '    |')
        print(Style.DIM + '             =======================================' + Style.NORMAL)
        print('')
        holdOn = input(eng.PROMPT)
        if holdOn == 'l':
            loaded = "no"
            while loaded == "no":
                eng.clear()
                art.printLogo()
                print(Style.DIM + '             =======================================')
                print(Style.DIM + '             |        ' + Style.NORMAL + 'Enter a save slot or' + Style.DIM + '         |')
                print(Style.DIM + '             |   ' + Style.NORMAL + Fore.CYAN + 'back' + Fore.WHITE + ' to return to the main menu' + Style.DIM + '   |')
                print(Style.DIM + '             =======================================' + Style.NORMAL)
                print('')
                slots = [ "_index" ]
                i = 1
                for s in natsort.natsorted(os.listdir("./save-states")):
                    print('  [' + str(i) + '] - ' + s)
                    slots.append(s)
                    i += 1
                print('')
                slots.sort()
                if len(slots) > 1:
                    slotChoice = input(eng.PROMPT)
                    if slotChoice == "back":
                        break
                    if slotChoice.isdigit():
                        if eng.DEBUG == 1:
                            print("slotChoice # received: " + slotChoice)
                            print("slotChoice name received: " + slots[int(slotChoice)])
                            time.sleep(1)
                        try:
                            dbs.loadGame(slots[int(slotChoice)])
                            loaded = "yes"
                        except:
                            print("Save slot doesn't exist!")
                            time.sleep(2)
                            continue
                        eng.displayLocation(dbs.location)
                        eng.TextAdventureCmd().cmdloop()
                        title = "closed"
                    elif slotChoice in slots:
                        if eng.DEBUG == 1:
                            print("slotChoice received: " + slotChoice)
                        dbs.loadGame(slotChoice)
                        loaded = "yes"
                        eng.displayLocation(dbs.location)
                        eng.TextAdventureCmd().cmdloop()
                        title = "closed"
                    else:
                        print("Save slot doesn't exist!")
                        time.sleep(2)
                        continue
                else:
                    eng.clear()
                    art.printLogo()
                    print(Style.DIM + '             =======================================')
                    print(Style.DIM + '             |        ' + Style.NORMAL + 'No save slots exist!' + Style.DIM + '         |')
                    print(Style.DIM + '             |    ' + Style.NORMAL + 'Enter a new save slot name or' + Style.DIM + '    |')
                    print(Style.DIM + '             |   ' + Style.NORMAL + Fore.CYAN + 'back' + Fore.WHITE + ' to return to the main menu' + Style.DIM + '   |')
                    print(Style.DIM + '             =======================================' + Style.NORMAL)
                    print('')
                    slotName = input(eng.PROMPT)
                    if slotName == "back":
                        break
                    dbs.newGame(slotName)
                    loaded = "yes"
                    art.introAnimation()
                    eng.displayLocation(dbs.location)
                    eng.TextAdventureCmd().cmdloop()
                    title = "closed"
        elif holdOn == 'n':
            loaded = "no"
            while loaded == "no":
                eng.clear()
                art.printLogo()
                print(Style.DIM + '             =======================================')
                print(Style.DIM + '             |    ' + Style.NORMAL + 'Enter a new save slot name or' + Style.DIM + '    |')
                print(Style.DIM + '             |   ' + Style.NORMAL + Fore.CYAN + 'back' + Fore.WHITE + ' to return to the main menu' + Style.DIM + '   |')
                print(Style.DIM + '             =======================================' + Style.NORMAL)
                print('')
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
                        print(Style.DIM + '    =========================================================')
                        print(Style.DIM + '    |           ' + Style.NORMAL + 'You already have 3 slots saved!' + Style.DIM + '             |')
                        print(Style.DIM + '    | ' + Style.NORMAL + 'Create a new save with an existing name to overwrite!' + Style.DIM + ' |')
                        print(Style.DIM + '    =========================================================' + Style.NORMAL)
                        print('')
                        print("Save Slots Found:")
                        for s in slots:
                            print("  " + s)
                        time.sleep(3)
                        print("Returning to the title screen.")
                        break
                    dbs.newGame(slotName)
                    loaded = "yes"
                    art.introAnimation()
                    eng.displayLocation(dbs.location)
                    eng.TextAdventureCmd().cmdloop()
                    title = "closed"
                else:
                    eng.clear()
                    art.printLogo()
                    print(Style.DIM + '         =================================================')
                    print(Style.DIM + '         | ' + Style.NORMAL + 'Save slot already exists! Overwrite? (yes/no)' + Style.DIM + ' |')
                    print(Style.DIM + '         =================================================' + Style.NORMAL)
                    print('')
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
                        loaded = "yes"
                        art.introAnimation()
                        eng.displayLocation(dbs.location)
                        eng.TextAdventureCmd().cmdloop()
                        title = "closed"
        elif holdOn == "quit" or holdOn == "exit":
            break
        else:
            continue
    eng.clear()
    art.printLogo()
    print(Style.DIM + '             =======================================')
    print(Style.DIM + '             |        ' + Style.NORMAL + 'Thanks for rockin\'! ' + Style.DIM + '         |')
    print(Style.DIM + '             =======================================' + Style.NORMAL)
    print('')
    exit()
