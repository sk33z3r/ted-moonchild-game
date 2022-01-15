import time
from colorama import Fore, Back, Style
import database as dbs
import engine as eng

# http://www.text-image.com/convert/ascii.html
# set size to 40 character width

logo1 = """
          (         *       )     )     )          ) (   (   (
  *   )   )\ )    (  `   ( /(  ( /(  ( /(   (   ( /( )\ ))\ ))\ )
` )  /(( (()/(    )\))(  )\()) )\()) )\())  )\  )\()|()/(()/(()/(
 ( )(_))\ /(_))  ((_)()\((_)\ ((_)\ ((_)\ (((_)((_)\ /(_))(_))(_))
(_(_()|(_|_))_   (_()((_) ((_)  ((_) _((_))\___ _((_|_))(_))(_))_
|_   _| __|   \  |  \/  |/ _ \ / _ \| \| ((/ __| || |_ _| |  |   \\
  | | | _|| |) | | |\/| | (_) | (_) | .` || (__| __ || || |__| |) |
  |_| |___|___/  |_|  |_|\___/ \___/|_|\_| \___|_||_|___|____|___/
"""

logo2 = """
                             AND THE
"""

logo3 = """
          __  __      __   __ __         __ __      __ __
         |__)/  \ /\ |  \||_ (_   . _   (_ |__) /\ /  |_
         | \ \__//--\|__/||____)  || )  __)|   /--\\\\__|__
"""

def printLogo():
  print(Fore.YELLOW + Style.NORMAL + logo1 + Style.NORMAL + Fore.WHITE)
  print(Fore.YELLOW + Style.NORMAL + logo2 + Style.NORMAL + Fore.WHITE)
  print(Fore.YELLOW + Style.NORMAL + logo3 + Style.NORMAL + Fore.WHITE)
  print()

def introAnimation():
    introText = dbs.engine.find_one( { "INTRO1": { "$regex": ".*" } } )
    eng.clear()
    time.sleep(1)
    print(Style.BRIGHT + introText["INTRO1"] + '\n')
    time.sleep(2)
    eng.clear()
    print(Style.DIM + introText["INTRO2"] + '\n')
    time.sleep(0.1)
    eng.clear()
    print(Style.NORMAL + introText["INTRO2"] + '\n')
    print(Style.DIM + introText["INTRO3"] + '\n')
    time.sleep(0.1)
    eng.clear()
    print(Style.BRIGHT + introText["INTRO2"] + '\n')
    print(Style.NORMAL + introText["INTRO3"] + '\n')
    print(Style.DIM + introText["INTRO4"] + '\n')
    time.sleep(0.1)
    eng.clear()
    print(Style.NORMAL + introText["INTRO2"] + '\n')
    print(Style.BRIGHT + introText["INTRO3"] + '\n')
    print(Style.NORMAL + introText["INTRO4"] + '\n')
    print(Style.DIM + introText["INTRO5"] + '\n')
    time.sleep(0.1)
    eng.clear()
    print(Style.NORMAL + introText["INTRO2"] + '\n')
    print(Style.NORMAL + introText["INTRO3"] + '\n')
    print(Style.BRIGHT + introText["INTRO4"] + '\n')
    print(Style.NORMAL + introText["INTRO5"] + '\n')
    time.sleep(0.1)
    eng.clear()
    print(Style.NORMAL + introText["INTRO2"] + '\n')
    print(Style.NORMAL + introText["INTRO3"] + '\n')
    print(Style.NORMAL + introText["INTRO4"] + '\n')
    print(Style.BRIGHT + introText["INTRO5"] + '\n')
    time.sleep(0.1)
    eng.clear()
    print(Style.NORMAL + introText["INTRO2"] + '\n')
    print(Style.NORMAL + introText["INTRO3"] + '\n')
    print(Style.NORMAL + introText["INTRO4"] + '\n')
    print(Style.NORMAL + introText["INTRO5"] + '\n')
    time.sleep(0.1)
    eng.clear()
    print(Style.NORMAL + introText["INTRO2"] + '\n')
    print(Style.NORMAL + introText["INTRO3"] + '\n')
    print(Style.NORMAL + introText["INTRO4"] + '\n')
    print(Style.NORMAL + introText["INTRO5"] + '\n')
    time.sleep(13)
    eng.clear()
    print(Fore.YELLOW + Style.NORMAL + logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(0.5)
    eng.clear()
    print(Fore.YELLOW + Style.BRIGHT + logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(1)
    eng.clear()
    print(Fore.YELLOW + Style.NORMAL + logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.BRIGHT + logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(0.5)
    eng.clear()
    print(Fore.YELLOW + Style.NORMAL + logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.BRIGHT + logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(1)
    eng.clear()
    print(Fore.YELLOW + Style.NORMAL + logo1 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + logo2 + Style.NORMAL + Fore.WHITE)
    print(Fore.YELLOW + Style.NORMAL + logo3 + Style.NORMAL + Fore.WHITE)
    time.sleep(2)
    eng.clear()