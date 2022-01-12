from colorama import Fore, Back, Style

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