import time
import engine as eng

if eng.COLORS == 0:
    import blackwhite as clr
elif eng.COLORS == 1:
    import colors as clr

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
  print("{FYELLOW}{NORMAL}{logo1}{NORMAL}{FWHITE}".format(**clr.styles, logo1 = logo1))
  print("{FYELLOW}{NORMAL}{logo2}{NORMAL}{FWHITE}".format(**clr.styles, logo2 = logo2))
  print("{FYELLOW}{NORMAL}{logo3}{NORMAL}{FWHITE}\n".format(**clr.styles, logo3 = logo3))

def introAnimation():
    eng.clear()
    time.sleep(1)
    print("{BRIGHT}{intro1}\n".format(**clr.styles, intro1 = intro1))
    time.sleep(2)
    eng.clear()
    print("{DIM}{intro2}\n".format(**clr.styles, intro2 = intro2))
    time.sleep(0.1)
    eng.clear()
    print("{NORMAL}{intro2}\n".format(**clr.styles, intro2 = intro2))
    print("{DIM}{intro3}\n".format(**clr.styles, intro3 = intro3))
    time.sleep(0.1)
    eng.clear()
    print("{BRIGHT}{intro2}\n".format(**clr.styles, intro2 = intro2))
    print("{NORMAL}{intro3}\n".format(**clr.styles, intro3 = intro3))
    print("{DIM}{intro4}\n".format(**clr.styles, intro4 = intro4))
    time.sleep(0.1)
    eng.clear()
    print("{NORMAL}{intro2}\n".format(**clr.styles, intro2 = intro2))
    print("{BRIGHT}{intro3}\n".format(**clr.styles, intro3 = intro3))
    print("{NORMAL}{intro4}\n".format(**clr.styles, intro4 = intro4))
    print("{DIM}{intro5}\n".format(**clr.styles, intro5 = intro5))
    time.sleep(0.1)
    eng.clear()
    print("{NORMAL}{intro2}\n".format(**clr.styles, intro2 = intro2))
    print("{NORMAL}{intro3}\n".format(**clr.styles, intro3 = intro3))
    print("{BRIGHT}{intro4}\n".format(**clr.styles, intro4 = intro4))
    print("{NORMAL}{intro5}\n".format(**clr.styles, intro5 = intro5))
    time.sleep(0.1)
    eng.clear()
    print("{NORMAL}{intro2}\n".format(**clr.styles, intro2 = intro2))
    print("{NORMAL}{intro3}\n".format(**clr.styles, intro3 = intro3))
    print("{NORMAL}{intro4}\n".format(**clr.styles, intro4 = intro4))
    print("{BRIGHT}{intro5}\n".format(**clr.styles, intro5 = intro5))
    time.sleep(0.1)
    eng.clear()
    print("{NORMAL}{intro2}\n".format(**clr.styles, intro2 = intro2))
    print("{NORMAL}{intro3}\n".format(**clr.styles, intro3 = intro3))
    print("{NORMAL}{intro4}\n".format(**clr.styles, intro4 = intro4))
    print("{NORMAL}{intro5}\n".format(**clr.styles, intro5 = intro5))
    time.sleep(0.1)
    eng.clear()
    print("{NORMAL}{intro2}\n".format(**clr.styles, intro2 = intro2))
    print("{NORMAL}{intro3}\n".format(**clr.styles, intro3 = intro3))
    print("{NORMAL}{intro4}\n".format(**clr.styles, intro4 = intro4))
    print("{NORMAL}{intro5}\n".format(**clr.styles, intro5 = intro5))
    time.sleep(13)
    eng.clear()
    print("{FYELLOW}{NORMAL}{logo1}{NORMAL}{FWHITE}".format(**clr.styles, logo1 = logo1))
    print("{FYELLOW}{NORMAL}{logo2}{NORMAL}{FWHITE}".format(**clr.styles, logo2 = logo2))
    print("{FYELLOW}{NORMAL}{logo3}{NORMAL}{FWHITE}".format(**clr.styles, logo3 = logo3))
    time.sleep(0.5)
    eng.clear()
    print("{FYELLOW}{BRIGHT}{logo1}{NORMAL}{FWHITE}".format(**clr.styles, logo1 = logo1))
    print("{FYELLOW}{NORMAL}{logo2}{NORMAL}{FWHITE}".format(**clr.styles, logo2 = logo2))
    print("{FYELLOW}{NORMAL}{logo3}{NORMAL}{FWHITE}".format(**clr.styles, logo3 = logo3))
    time.sleep(1)
    eng.clear()
    print("{FYELLOW}{NORMAL}{logo1}{NORMAL}{FWHITE}".format(**clr.styles, logo1 = logo1))
    print("{FYELLOW}{BRIGHT}{logo2}{NORMAL}{FWHITE}".format(**clr.styles, logo2 = logo2))
    print("{FYELLOW}{NORMAL}{logo3}{NORMAL}{FWHITE}".format(**clr.styles, logo3 = logo3))
    time.sleep(0.5)
    eng.clear()
    print("{FYELLOW}{NORMAL}{logo1}{NORMAL}{FWHITE}".format(**clr.styles, logo1 = logo1))
    print("{FYELLOW}{NORMAL}{logo2}{NORMAL}{FWHITE}".format(**clr.styles, logo2 = logo2))
    print("{FYELLOW}{BRIGHT}{logo3}{NORMAL}{FWHITE}".format(**clr.styles, logo3 = logo3))
    time.sleep(1)
    eng.clear()
    print("{FYELLOW}{NORMAL}{logo1}{NORMAL}{FWHITE}".format(**clr.styles, logo1 = logo1))
    print("{FYELLOW}{NORMAL}{logo2}{NORMAL}{FWHITE}".format(**clr.styles, logo2 = logo2))
    print("{FYELLOW}{NORMAL}{logo3}{NORMAL}{FWHITE}".format(**clr.styles, logo3 = logo3))
    time.sleep(2)
    eng.clear()