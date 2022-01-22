from time import sleep
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

# intro text
intro1 = "The year is 4420"
intro2 = "Mankind has expanded its reach beyond the solar system"
intro3 = "Many righteous bands tour the galaxy looking for wealth, fame, and loose women,\nbut there is now an evil that lurks in the vast darkness of space."
intro4 = "The evil conglomerates of Earth's past return to enslave the Gods of Metal\nby cryogenically freezing and replacing them with their clone-step army."
intro5 = "There is only one crew that can put a stop to this madness..."

def printLogo():
  print(logo1)
  print(logo2)
  print(logo3)

def introAnimation():
    eng.clear()
    sleep(1)
    print(intro1 + "\n")
    sleep(1)
    print(intro2 + "\n")
    sleep(1)
    print(intro3 + "\n")
    sleep(1)
    print(intro4 + "\n")
    sleep(1)
    print(intro5 + "\n")
    sleep(3)
    eng.clear()
    print(logo1)
    print(logo2)
    print(logo3)
    sleep(3)
