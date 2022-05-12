##  This is the CODENAME-WARS Alpha V2.01
##  Coded by Ian Wuth, 5/6/2022

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

def update_term_size(stdscr, logger):
    logger.log("New terminal size:")
    TERM_TUPLE = stdscr.getmaxyx()
    TERM_HEIGHT = TERM_TUPLE[0]
    TERM_WIDTH = TERM_TUPLE[1]
    logger.log(f"h: {TERM_HEIGHT}")
    logger.log(f"w: {TERM_WIDTH}")
    return TERM_TUPLE

def return_world_file_name(fn="example_world.json"):
    return str(fn)
    

def alpha_two(stdscr):
    ## initilize logger - log 0
    logger = Logger("alpha_two.log")
    logger.log("Logger Initilized", 0)

    ## grab our variables - log 1
    ### screen size
    TERM_Tup = update_term_size(stdscr, logger)
    TERM_h = TERM_Tup[0]
    TER_w = TERM_Tup[1]

    ### world name
    world_name = return_world_file_name()
    logger.log(f"World Name fetched as {world_name}", 1)
    
    ## initilize "large" / "global" flags

    main_menu_FLAG = Flag(True)
    reactive_menu_FLAG = Flag(False)


    ## data initilization - log 1
    ### main structure is World

    world = World(world_name)
    world_h = world.get_world_height()
    world_w = world.get_world_width()
    world_mode = world.get_mode()
    world_num_players = world.get_num_players()

    logger.log(f"World Initilizing from {world_name}...", 1)
    logger.log(f"... Mode: {world_mode}")
    logger.log(f"... numPlayers: {world_num_players}")
    logger.log(f"... Height: {world_h}")
    logger.log(f"... Width: {world_w}")
    logger.log("...Done")

    ### initilize perma_menu
    logger.log("Building Perma-Menu...", 1)

    perma_Menu = Menu()

    logger.log("...Done")

    ### initilize reactive_menu
    logger.log("Building React-Menu...", 1)

    reactive_Menu = Menu()

    logger.log("...Done")

    ### initilize log
    logger.log("Building Log...", 1)

    in_game_log = Logger(f"{world.get_name()}.log")

    logger.log("...Done")

    ### initilize stats
    logger.log("Building Stats...", 1)

    stats = {}
    world_stats = world.get_stats_for()
    for i in world_stats:
        stats.update({i:world_stats[i]})

    logger.log("...Done")

    ### initilize map
    logger.log("Building Map...", 1)

    map  = curses.newpad(world_h, world_w)

    logger.log("...Done")

    ### create 5 boxes for 5 windows
    logger.log("Creating Coordinate Boxes...", 1)

    mBy = math.floor(((7 / 8) * (2 / 3)) * TERM_h)
    mBx = math.floor((3 / 4) * TER_w)
    map_Box = Box(0, 0, mBy, mBx)

    logger.log("...Map Done")

    lBy = math.floor((2 / 3) * TERM_h)
    lBx = mBx + 1
    log_Box = Box(0, lBx, lBy, TER_w - 1)

    logger.log("...Log Done")

    stats_Box = Box(mBy + 1, 0, lBy, lBx - 1)

    logger.log("...Stats Done")

    pmBy = lBy + 1
    pmBx = math.floor((1 / 2) * TER_w)
    perma_menu_Box = Box(pmBy, 0, TERM_h - 1, pmBx)

    logger.log("...PMenu Done")

    reactive_menu_Box = Box(pmBy, pmBx + 1, TERM_h - 1, TER_w - 1)

    logger.log("...RMenu Done")

    cursor_Box = Box(mBy, mBx, mBy, mBx)

    ## initilize curses objects - log 2
    ### create 5 windows
    logger.log("Creating Display Windows...", 2)

    map_Window = curses.newwin(map_Box.get_y_top_left, map_Box.get_x_top_left, map_Box.get_y_bottom_right, map_Box.get_x_bottom_right)
    
    logger.log("...Map Done")

    log_Window = curses.newwin(log_Box.get_y_top_left, log_Box.get_x_top_left, log_Box.get_y_bottom_right, log_Box.get_x_bottom_right)
    
    logger.log("...Map Done")

    stats_Window = curses.newwin(stats_Box.get_y_top_left, stats_Box.get_x_top_left, stats_Box.get_y_bottom_right, stats_Box.get_x_bottom_right)
    
    logger.log("...Stats Done")

    perma_menu_Window = curses.newwin(perma_menu_Box.get_y_top_left, perma_menu_Box.get_x_top_left, perma_menu_Box.get_y_bottom_right, perma_menu_Box.get_x_bottom_right)
    
    logger.log("...PMenu Done")
    
    reactive_menu_Window = curses.newwin(reactive_menu_Box.get_y_top_left, reactive_menu_Box.get_x_top_left, reactive_menu_Box.get_y_bottom_right, reactive_menu_Box.get_x_bottom_right)

    logger.log("...Stats Done")
    
    ## game loop - log 3
    ### prepare for loop
    ## initilize Color_decoder
    cd = Color_decoder()
    logger.log("Color_decoder Initilized", 3)

    ## prepare stdscr
    logger.log("Preparing stdscr for loop...", 3)

    stdscr.clear()
    stdscr.refresh()
    
    logger.log("...Done")
    ### begin loop
    logger.log("Entering Loop", 3)
    current_key = "None"
    while True:
        ### handle input - log 4
        logger.log("*Begin input handling*", 4)
        current_key = stdscr.getkey()
        logger.log(f"*Grabbed current_key as {current_key} *")
        #### emergency exit
        if current_key == "q":
            logger.log("*Emergency Exit input called*", 4)
            break

        #### when in the main menu
        if main_menu_FLAG:
            if pre_game_FLAG:
                pass
            if in_game_FLAG:
                pass

        #### when in the reactive menu
        if reactive_menu_FLAG:
            pass
            
        ####

        ### adjust values for process - log 5


        ### display buffer - log 6
        #### refresh pads
        #### refresh windows
        #### refresh stdscr

    
    ## end of the line - log 100
    logger.log("End of Process...", 100)
    logger.log("...Goodbye!", 100)


## run correctly as standalone
if __name__ == "__main__":
    wrapper(alpha_two)