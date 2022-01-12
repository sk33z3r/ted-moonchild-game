import os
from colorama import Fore, Back, Style
import art
import database as dbs
import engine as eng

if __name__ == '__main__':

    print(Back.BLACK + Fore.WHITE)
    clear()
    print(Fore.YELLOW + Style.NORMAL + art.logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + art.logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + art.logo3 + Style.NORMAL + Fore.WHITE)
    print()
    print(Style.DIM + '             =======================================')
    print(Style.DIM + '             | ' + Style.NORMAL + 'Press ' + Fore.GREEN + 'n' + Fore.WHITE + ' to fucking ROCK a new story ' + Style.DIM + '|')
    print(Style.DIM + '             | ' + Style.NORMAL + 'Press ' + Fore.CYAN + 'l' + Fore.WHITE + ' to load your shitty save    ' + Style.DIM + '|')
    print(Style.DIM + '             =======================================' + Style.NORMAL)
    print('')
    holdOn = input(eng.PROMPT)
    if holdOn == 'l':
        loaded = "no"
        while loaded === "no":
            print("Pick a save slot")
            slots = [ "_index" ]
            i = 1
            for s in os.listdir("./save-states"):
                print('  [' + str(i) + '] - ' + s)
                slots.append(s)
                i += 1
            slotChoice = input(eng.PROMPT)
            if slotChoice.isdigit():
                try:
                    dbs.loadGame(slots[slotChoice])
                except:
                    print("Save slot doesn't exist!")
                    continue
                eng.displayLocation(dbs.location)
                eng.TextAdventureCmd().cmdloop()
                loaded = "yes"
            elif slotChoice in slots:
                dbs.loadGame(slotChoice)
                eng.displayLocation(dbs.location)
                eng.TextAdventureCmd().cmdloop()
                loaded = "yes"
            else:
                print("Save slot doesn't exist!")
                continue
    elif holdOn == 'n':
        print("Enter a save slot name")
        slotName = input(eng.PROMPT)
        dbs.newGame(slotName)
        eng.introAnimation()
        eng.displayLocation(dbs.location)
        eng.TextAdventureCmd().cmdloop()
    else:
        pass
    print('Thanks for ROCKIN\'!' + Style.NORMAL)
    exit()
