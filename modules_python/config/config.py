class fg:
    # couleur du texte
    black       = u"\u001b[30m"
    red         = u"\u001b[31m"
    green       = u"\u001b[32m"
    yellow      = u"\u001b[33m"
    blue        = u"\u001b[34m"
    magenta     = u"\u001b[35m"
    cyan        = u"\u001b[36m"
    white       = u"\u001b[37m"
    black_L     = u"\u001b[30;1m"
    red_L       = u"\u001b[31;1m"
    green_L     = u"\u001b[32;1m"
    yellow_L    = u"\u001b[33;1m"
    blue_L      = u"\u001b[34;1m"
    magenta_M   = u"\u001b[35;1m"
    cyan_L      = u"\u001b[36;1m"
    white_L     = u"\u001b[1m"+f"\u001b[38;2;{255};{255};{255}m"

    # couleur du texte en rgb
    def rbg(r, g, b): 
        return f"\u001b[38;2;{r};{g};{b}m"

class bg:
    # couleur arrière plan
    black       = u"\u001b[40m"
    red         = u"\u001b[41m"
    green       = u"\u001b[42m"
    yellow      = u"\u001b[43m"
    blue        = u"\u001b[44m"
    magenta     = u"\u001b[45m"
    cyan        = u"\u001b[46m"
    white       = u"\u001b[47m"
    black_L     = u"\u001b[40;1m"
    red_L       = u"\u001b[41;1m"
    green_L     = u"\u001b[42;1m"
    yellow_L    = u"\u001b[43;1m"
    blue_L      = u"\u001b[44;1m"
    magenta_L   = u"\u001b[45;1m"
    cyan_L      = u"\u001b[46;1m"
    white_L     = u"\u001b[47;1m"

    #couleur arrière plan en rgb
    def rgb(r, g, b): 
        return f"\u001b[48;2;{r};{g};{b}m"

# nettoyage ecran    
class screen:
    #40 * 25 monochrome
    s0 = u"\u001b[0h"
    #40 * 25 color
    s1 = u"\u001b[1h"

# configuration du curseur 
class init:
    reset       = u"\u001b[0m"
    bold        = u"\u001b[1m"
    italic      = u"\u001b[3m"
    underline   = u"\u001b[4m"
    blink       = u"\u001b[5m"
    rapid_blink = u"\u001b[6m"
    reverse     = u"\u001b[7m"
    hide        = u"\u001b[8m"
    bare        = u"\u001b[9m"
    double_underline= u"\u001b[21m"
    high_intensity  = u"\u001b[22m"
    eyes            = u"\u001b[25m"
    remove_reverse  = u"\u001b[27m"
    link        = u"\u001b[8;;https://github.com/amiehe-essomba ST"

# nettoyage et formatage de l'écran 
class clear:
    clear       = u"\u001b[2J"
    def line( pos : int ):
        # 2 = entire line
        # 1 = from the cursor to start of line
        # 0 = from the cursor to end of line
        clearline   = u"\u001b[" + f"{pos}" + "K"
        return clearline
    def screen(pos : int ):
        # 0 = clears from cursor until end of screen,
        # 1 = clears from cursor to beginning of screen
        # 2 = clears entire screen
        clearScreen = u"\u001b[" + f"{pos}" + "J"
        return clearScreen 
    
    def move_and_clear(pos : int=3 ):
        # 0 = clears from cursor until end of screen,
        # 1 = clears from cursor to beginning of screen
        # 2 = clears entire screen
        clearScreen = u"\u001b[H" + clear.screen(pos)
        return clearScreen 

# déplacement du curseur 
class cursorPos:
    def to(x:int, y:int):
        return f"\u001b[{y};{x}H"