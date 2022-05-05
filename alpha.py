##  This is the CODENAME-WARS Alpha V2.0
##  Coded by Ian Wuth, 5/1/2022

import curses
from curses import wrapper
from ians_toolkit import *
from brocks_toolkit import *
import json
import time
import math

## Welcome back to the Alpha of CODENAME WARS
## Here in version two, we've cleaned up the space some, come take a look around!
## Our goals for this generation are to...
## - [ ] Create a cursor
## - [ ] Finalize major read/write structures
## - [ ] Impliment basic UI
## - [x] Integrate color

def update_term_size(stdscr):
    global TERM_HEIGHT
    global TERM_WIDTH
    TERM_TUPLE = stdscr.getmaxyx()
    TERM_HEIGHT = TERM_TUPLE[0]
    TERM_WIDTH = TERM_TUPLE[1]

def alpha_two(stdscr):
    ## grab our global variables
    global TERM_HEIGHT
    global TERM_WIDTH
    ## initilize stdscr and get its dimentions
    stdscr.clear()
    update_term_size(stdscr)

    ## create 5 boxes for 5 windows
    mBy = math.floor(((7 / 8) * (2 / 3)) * TERM_HEIGHT)
    mBx = math.floor((3 / 4) * TERM_WIDTH)
    map_Box = Box(0, 0, mBy, mBx)

    lBy = math.floor((2 / 3) * TERM_HEIGHT)
    lBx = mBx + 1
    log_Box = Box(0, lBx, lBy, TERM_WIDTH - 1)

    perma_stats_Box = Box(mBy + 1, 0, lBy, lBx - 1)

    pmBy = lBy + 1
    pmBx = math.floor((1 / 2) * TERM_WIDTH)
    perma_menu_Box = Box(pmBy, 0, TERM_HEIGHT - 1, pmBx)

    reactive_menu_Box = Box(pmBy, pmBx + 1, TERM_HEIGHT - 1, TERM_WIDTH - 1)

    ## create 5 windows
    map_Window = curses.newwin(map_Box.get_y_top_left, map_Box.get_x_top_left, map_Box.get_y_bottom_right, map_Box.get_x_bottom_right)
    log_Window = curses.newwin(log_Box.get_y_top_left, log_Box.get_x_top_left, log_Box.get_y_bottom_right, log_Box.get_x_bottom_right)
    perma_stats_Window = curses.newwin(perma_stats_Box.get_y_top_left, perma_stats_Box.get_x_top_left, perma_stats_Box.get_y_bottom_right, perma_stats_Box.get_x_bottom_right)
    perma_menu_Window = curses.newwin(perma_menu_Box.get_y_top_left, perma_menu_Box.get_x_top_left, perma_menu_Box.get_y_bottom_right, perma_menu_Box.get_x_bottom_right)
    reactive_menu_Window = curses.newwin(reactive_menu_Box.get_y_top_left, reactive_menu_Box.get_x_top_left, reactive_menu_Box.get_y_bottom_right, reactive_menu_Box.get_x_bottom_right)






## run correctly as standalone
if __name__ == "__main__":
    wrapper(alpha_two)