import curses
from curses import wrapper

class Map_tile:
    def __init__(self):
        self.terrain = "default"
        self.improvement = "none"
        self.pawn = "none"

    def get_terrain(self):
        return self.terrain

    def get_improvement(self):
        return self.improvement

    def get_pawn(self):
        return self.pawn

    def set_terrain(self, new_terrain):
        self.terrain = new_terrain

    def set_improvement(self, new_improvement):
        self.improvement = new_improvement
    
    def set_pawn(self, new_pawn):
        self.pawn = new_pawn


# Curses colors are: 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
class Color_decoder:
    def __init__(self):
        self.colortable = {
            'BLACK': {
                'BLACK': 1,
                'RED': 2,
                'GREEN': 3,
                'YELLOW': 4,
                'BLUE': 5,
                'MAGENTA': 6,
                'CYAN': 7,
                'WHITE': 8
            },
            'RED': {
                'BLACK': 9,
                'RED': 10,
                'GREEN': 11,
                'YELLOW': 12,
                'BLUE': 13,
                'MAGENTA': 14,
                'CYAN': 15,
                'WHITE': 16
            },
            'GREEN': {
                'BLACK': 17,
                'RED': 18,
                'GREEN': 19,
                'YELLOW': 20,
                'BLUE': 21,
                'MAGENTA': 22,
                'CYAN': 23,
                'WHITE': 24
            },
            'YELLOW': {
                'BLACK': 25,
                'RED': 26,
                'GREEN': 27,
                'YELLOW': 28,
                'BLUE': 29,
                'MAGENTA': 30,
                'CYAN': 31,
                'WHITE': 32
            },
            'BLUE': {
                'BLACK': 33,
                'RED': 34,
                'GREEN': 35,
                'YELLOW': 36,
                'BLUE': 37,
                'MAGENTA': 38,
                'CYAN': 39,
                'WHITE': 40
            },
            'MAGENTA': {
                'BLACK': 41,
                'RED': 42,
                'GREEN': 43,
                'YELLOW': 44,
                'BLUE': 45,
                'MAGENTA': 46,
                'CYAN': 47,
                'WHITE': 48
            },
            'CYAN': {
                'BLACK': 49,
                'RED': 50,
                'GREEN': 51,
                'YELLOW': 52,
                'BLUE': 53,
                'MAGENTA': 54,
                'CYAN': 55,
                'WHITE': 56
            },
            'WHITE': {
                'BLACK': 57,
                'RED': 58,
                'GREEN': 59,
                'YELLOW': 60,
                'BLUE': 61,
                'MAGENTA': 62,
                'CYAN': 63,
                'WHITE': 64
            }
        }
        
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
        curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_GREEN)
        curses.init_pair(12, curses.COLOR_RED, curses.COLOR_YELLOW)
        curses.init_pair(13, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(14, curses.COLOR_RED, curses.COLOR_MAGENTA)
        curses.init_pair(15, curses.COLOR_RED, curses.COLOR_CYAN)
        curses.init_pair(16, curses.COLOR_RED, curses.COLOR_WHITE)

        curses.init_pair(17, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(18, curses.COLOR_GREEN, curses.COLOR_RED)
        curses.init_pair(19, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(20, curses.COLOR_GREEN, curses.COLOR_YELLOW)
        curses.init_pair(21, curses.COLOR_GREEN, curses.COLOR_BLUE)
        curses.init_pair(22, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
        curses.init_pair(23, curses.COLOR_GREEN, curses.COLOR_CYAN)
        curses.init_pair(24, curses.COLOR_GREEN, curses.COLOR_WHITE)

        curses.init_pair(25, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(26, curses.COLOR_YELLOW, curses.COLOR_RED)
        curses.init_pair(27, curses.COLOR_YELLOW, curses.COLOR_GREEN)
        curses.init_pair(28, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        curses.init_pair(29, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(30, curses.COLOR_YELLOW, curses.COLOR_MAGENTA)
        curses.init_pair(31, curses.COLOR_YELLOW, curses.COLOR_CYAN)
        curses.init_pair(32, curses.COLOR_YELLOW, curses.COLOR_WHITE)

        curses.init_pair(33, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(34, curses.COLOR_BLUE, curses.COLOR_RED)
        curses.init_pair(35, curses.COLOR_BLUE, curses.COLOR_GREEN)
        curses.init_pair(36, curses.COLOR_BLUE, curses.COLOR_YELLOW)
        curses.init_pair(37, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(38, curses.COLOR_BLUE, curses.COLOR_MAGENTA)
        curses.init_pair(39, curses.COLOR_BLUE, curses.COLOR_CYAN)
        curses.init_pair(40, curses.COLOR_BLUE, curses.COLOR_WHITE)

        curses.init_pair(41, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(42, curses.COLOR_MAGENTA, curses.COLOR_RED)
        curses.init_pair(43, curses.COLOR_MAGENTA, curses.COLOR_GREEN)
        curses.init_pair(44, curses.COLOR_MAGENTA, curses.COLOR_YELLOW)
        curses.init_pair(45, curses.COLOR_MAGENTA, curses.COLOR_BLUE)
        curses.init_pair(46, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        curses.init_pair(47, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
        curses.init_pair(48, curses.COLOR_MAGENTA, curses.COLOR_WHITE)

        curses.init_pair(49, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(50, curses.COLOR_CYAN, curses.COLOR_RED)
        curses.init_pair(51, curses.COLOR_CYAN, curses.COLOR_GREEN)
        curses.init_pair(52, curses.COLOR_CYAN, curses.COLOR_YELLOW)
        curses.init_pair(53, curses.COLOR_CYAN, curses.COLOR_BLUE)
        curses.init_pair(54, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
        curses.init_pair(55, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(56, curses.COLOR_CYAN, curses.COLOR_WHITE)

        curses.init_pair(57, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(58, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(59, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(60, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(61, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(62, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(63, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(64, curses.COLOR_WHITE, curses.COLOR_WHITE)

    def get_pair(self, text_color, background_color):
        return self.colortable[text_color][background_color]


def colortester(stdscr):
    ##  initalization
    stdscr.clear()

    # Hide the cursor.
    curses.curs_set(0)

    decoder = Color_decoder()
    color_options = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"]

    for y in range(8):
        for x in range(8):
            txt = color_options[y]
            bkg = color_options[x]
            message = txt[0:3] + " on " + bkg[0:3]
            stdscr.addstr(y, x * 11, message, curses.color_pair(decoder.get_pair(txt, bkg)))

    stdscr.addstr(9, 20, "Press any key for a curser demo, 'q' to quit.", decoder.get_pair("WHITE", "BLACK")  | curses.A_BLINK)
  
    y = 0
    x = 0

    while True:
        key = stdscr.getkey()
        stdscr.clear()
        if key == 'q':
            break
        if key == "KEY_DOWN":
            y += 1
            if y > len(color_options) - 1:
                y = len(color_options) - 1
        if key == "KEY_UP":
            y -= 1
            if y < 0:
                y = 0
        if key == "KEY_RIGHT":
            x += 1
            if x > len(color_options) - 1:
                x = len(color_options) - 1
        if key == "KEY_LEFT":
            x -= 1
            if x < 0:
                x = 0
        stdscr.addch(y+10, x+20, "\u2655", curses.color_pair(decoder.get_pair(color_options[y], color_options[x])))
        
        

        stdscr.refresh()


## run correctly as standalone
if __name__ == "__main__":
    wrapper(colortester)
