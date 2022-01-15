import colors as clr

text1 = "test text 1"
text2 = "test text 2"

print("{BRIGHT}{FRED}{TXT1}\n{DIM}{FYELLOW}{TXT2}{NORMAL}{FWHITE}{BBLACK}\n".format(**clr.styles, TXT1 = text1, TXT2 = text2))