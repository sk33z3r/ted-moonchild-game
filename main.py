import os, natsort, time
import engine as eng
import database as dbs
import art

if eng.COLORS == 0:
    import blackwhite as clr
elif eng.COLORS == 1:
    import colors as clr

def startGame(where):
    if where == "new":
        if eng.DEBUG == 0:
            print("Watch the intro animation? (yes/no)")
            skip = input(eng.PROMPT)
            if skip == "yes" or skip == "y":
                art.introAnimation()
            else:
                pass
    eng.displayLocation(dbs.location)
    eng.TextAdventureCmd().cmdloop()

if __name__ == '__main__':

    print("{BBLACK}{FWHITE}".format(**clr.styles))
    title = "open"
    while title == "open":
        eng.clear()
        art.printLogo()
        print("{DIM}             =======================================".format(**clr.styles))
        print("{DIM}             | {NORMAL}Press {FGREEN}n{FWHITE} to fucking ROCK a new story{DIM} |".format(**clr.styles))
        print("{DIM}             | {NORMAL}Press {FCYAN}l{FWHITE} to load your shitty save{DIM}    |".format(**clr.styles))
        print("{DIM}             ======================================={NORMAL}\n".format(**clr.styles))
        holdOn = input(eng.PROMPT)
        if holdOn == 'l':
            loaded = "no"
            while loaded == "no":
                eng.clear()
                art.printLogo()
                print("{DIM}             =======================================".format(**clr.styles))
                print("{DIM}             |        {NORMAL}Enter a save slot or{DIM}         |".format(**clr.styles))
                print("{DIM}             |   {NORMAL}{FCYAN}back{FWHITE} to return to the main menu{DIM}   |".format(**clr.styles))
                print("{DIM}             ======================================={NORMAL}\n".format(**clr.styles))
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
                        startGame("load")
                        title = "closed"
                    elif slotChoice in slots:
                        if eng.DEBUG == 1:
                            print("slotChoice received: " + slotChoice)
                        dbs.loadGame(slotChoice)
                        loaded = "yes"
                        startGame("load")
                        title = "closed"
                    else:
                        print("Save slot doesn't exist!")
                        time.sleep(2)
                        continue
                else:
                    eng.clear()
                    art.printLogo()
                    print("{DIM}             =======================================".format(**clr.styles))
                    print("{DIM}             |        {NORMAL}No save slots exist!{DIM}         |".format(**clr.styles))
                    print("{DIM}             |    {NORMAL}Enter a new save slot name or{DIM}    |".format(**clr.styles))
                    print("{DIM}             |   {NORMAL}{FCYAN}back{FWHITE} to return to the main menu{DIM}   |".format(**clr.styles))
                    print("{DIM}             ======================================={NORMAL}\n".format(**clr.styles))
                    slotName = input(eng.PROMPT)
                    if slotName == "back":
                        break
                    dbs.newGame(slotName)
                    loaded = "yes"
                    startGame("new")
                    title = "closed"
        elif holdOn == 'n':
            loaded = "no"
            while loaded == "no":
                eng.clear()
                art.printLogo()
                print("{DIM}             =======================================".format(**clr.styles))
                print("{DIM}             |    {NORMAL}Enter a new save slot name or{DIM}    |".format(**clr.styles))
                print("{DIM}             |   {NORMAL}{FCYAN}back{FWHITE} to return to the main menu{DIM}   |".format(**clr.styles))
                print("{DIM}             ======================================={NORMAL}\n".format(**clr.styles))
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
                        print("{DIM}    =========================================================".format(**clr.styles))
                        print("{DIM}    |           {NORMAL}You already have 3 slots saved!{DIM}             |".format(**clr.styles))
                        print("{DIM}    | {NORMAL}Create a new save with an existing name to overwrite!{DIM} |".format(**clr.styles))
                        print("{DIM}    ========================================================={NORMAL}\n".format(**clr.styles))
                        print("Save Slots Found:")
                        for s in slots:
                            print("  " + s)
                        time.sleep(3)
                        print("Returning to the title screen.")
                        break
                    dbs.newGame(slotName)
                    loaded = "yes"
                    startGame("new")
                    title = "closed"
                else:
                    eng.clear()
                    art.printLogo()
                    print("{DIM}         =================================================".format(**clr.styles))
                    print("{DIM}         | {NORMAL}Save slot already exists! Overwrite? (yes/no){DIM} |".format(**clr.styles))
                    print("{DIM}         ================================================={NORMAL}\n".format(**clr.styles))
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
                        startGame("new")
                        title = "closed"
        elif holdOn == "quit" or holdOn == "exit":
            break
        else:
            continue
    eng.clear()
    art.printLogo()
    print("{DIM}             =======================================".format(**clr.styles))
    print("{DIM}             |        {NORMAL}Thanks for rockin'! {DIM}         |".format(**clr.styles))
    print("{DIM}             ======================================={NORMAL}\n".format(**clr.styles))
    exit()
