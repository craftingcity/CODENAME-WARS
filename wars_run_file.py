##  This is the CODENAME-WARS Alpha V2.0
##  Coded by Ian Wuth, 5/1/2022

import curses
from curses import wrapper
from ians_toolkit import *
from brocks_toolkit import *
import json
import time


## Welcome back to the Alpha of CODENAME WARS
## Here in version two, we've cleaned up the space some, come take a look around!
## Our goals for this generation are to...
## - [ ] Create a cursor
## - [ ] Finalize major read/write structures
## - [ ] Impliment basic UI
## - [x] Integrate color



def alpha_one(stdscr):
    ##  initalization
    stdscr.clear()

    ## visualization
    game_pad = curses.newpad(20, 20)
    game_pad_box = Box(5, 5, 25, 25)
    init_menu_options = ["Move Unit", "Move Display", "Quit"]
    menu_obj = Menu(init_menu_options)

    ## colors
    cd = Color_decoder()

    ## flags
    unit_move_flag = Flag(False)
    map_move_flag = Flag(False)
    menu_engage_flag = Flag(True)

    ## variables
    world = []
    key = ""
    vert_count = 0
    run_time = 0


    ## data
    fr = FileReader("default_mod.json")
    terrain_data = fr.grab("testing_resource_fields")
    military_data = fr.grab("testing_military")


    ## supply data to objects
    for i in range(19):
        for j in range(19):
            new_terrain = Terrain(i, j, terrain_data)
            world.append(new_terrain)

    unit = Unit(0, 0, military_data)

    ## loop for mechanics
    while True:
        ## reinitilize the screen for a fresh frame
        ## refresh after clear or pads dont show
        stdscr.clear()
        stdscr.refresh()
        run_time += 1

        ## check flags
        umf = unit_move_flag.get()
        mmf = map_move_flag.get()
        mef = menu_engage_flag.get()

        ## check vars
        cs = menu_obj.get_cs()

        ## process input
        if key == "q":
            break
        if key == "KEY_UP":
            if umf:
                unit.move_north()
            if mmf:
                game_pad_box.move_north()
            if mef:
                ## this might look wrong, but remember, max y is the bottom of the scr
                ## therefore the "previous" selection would be above, making minus make sense
                menu_obj.minus()
        if key == "KEY_DOWN":
            if umf:
                unit.move_south()
            if mmf:
                game_pad_box.move_south()
            if mef:
                ## this might look wrong, but remember, max y is the bottom of the scr
                ## therefore the "next" selection would be below, making plus make sense
                menu_obj.plus()
        if key == "KEY_LEFT":
            if umf:
                unit.move_west()
            if mmf:
                game_pad_box.move_west()
            if mef:
                menu_obj.minus()
        if key == "KEY_RIGHT":
            if umf:
                unit.move_east()
            if mmf:
                game_pad_box.move_east()
            if mef:
                menu_obj.plus()
        if key == "\n":
            ## in older versions, .set() was used, causing a bug where flags would not change?
            ## using .flop() as so seems to have fixed the issue; as long as Flag is never not a bool,
            ## this should be fine, but it'd be tight if flags were more flexable than that.
            ## so this may cause further issues :)
            if umf:
                unit_move_flag.flop()
                menu_engage_flag.flop()
            if mmf:
                map_move_flag.flop()
                menu_engage_flag.flop()
            if mef:
                menu_engage_flag.flop()
                if cs == 0:
                    unit_move_flag.flop()
                if cs == 1:
                    map_move_flag.flop()
                if cs == 2:
                    break
        
        ## re-check flags
        umf = unit_move_flag.get()
        mmf = map_move_flag.get()
        mef = menu_engage_flag.get()

        ## draw to stdscr; debug assistance
        stdscr.addstr(30, 0, f"Key: {key}, UMF: {umf}, MMF: {mmf}, MEF:{mef}, Time: {run_time}")

        ## draw menu to stdscr
        vert_count = 0
        menu_options = menu_obj.get_options()
        cs = menu_obj.get_cs()
        for item in menu_options:
            vert_count += 1
            stdscr.addstr(19 + vert_count, 45, item)
        if mef:
            stdscr.addstr(20 + cs, 45, menu_options[cs], curses.A_REVERSE)
        
        ## draw to game_pad
        for cell in world:
            y_pos = cell.get_y()
            x_pos = cell.get_x()
            rep = cell.get_rep()
            colors = cell.get_colors()
            color_pair = curses.color_pair(cd.get_pair(colors[0], colors[1]))
            game_pad.addstr(y_pos, x_pos, rep, color_pair)
        
        game_pad.addstr(unit.y_pos, unit.x_pos, unit.representation, curses.color_pair(cd.get_pair(unit.colors[0], unit.colors[1])))
        game_pad.refresh(0, 0, game_pad_box.get_y_top_left(), game_pad_box.get_x_top_left(), game_pad_box.get_y_bottom_right(), game_pad_box.get_x_bottom_right())
        
        ## wait here for input
        stdscr.refresh()
        key = stdscr.getkey()

## run correctly as standalone
if __name__ == "__main__":
    wrapper(alpha_one)