##  This is the CODENAME-WARS Alpha V2.0
##  Coded by Ian Wuth, 5/1/2022

import curses
from curses import wrapper
from ians_toolkit import *
import json
import time


## Welcome back to the Alpha of CODENAME WARS
## Here in version two, we've cleaned up the space some, come take a look around!
## Our goals for this generation are to...
## - [ ] Create a cursor
## - [ ] Finalize major read/write structures
## - [ ] Impliment basic UI

## This is the World class. It's a file handler, but;
## Its been slightly modified to write some data to a file
## on initialization, but only if that file is empty.
## Which means World will recognize it's work (or anyone else's as something that exists)
## So: (Ideally, in the end,) it will one-time write a branch of metadata
## and then never touch it again, editing only the "play" data
## Pretty sick right?!

class World(FileWriter):
    ## Instance variables
    def __init__(self, w):
        FileWriter.__init__(self, w)
        ## check if this world has data
        try:
            open_file = open(self.w, "r")
        except FileNotFoundError:
            open_file = open(self.w, "x")
            open_file = open(self.w, "r")
        file_data = open_file.read()
        if file_data == "":
            self.write("World Instanced\n")
        else:
            self.append("World Loaded\n")
        open_file.close()
    
    def save(self):
        current_time = time.localtime()
        self.append(f"World Saved at {current_time}\n")

## Here we create multiple classes who all play a large part in organizing
## the systems on-stage and behind-the-scenes
## (ie, frontend and backend :) )

class VisualCell(Cell):
     ## Instance variables
    def __init__(self, y_pos, x_pos, data):
        Cell.__init__(self, y_pos, x_pos, data)
        self.name = self.data["name"]
        self.representation = self.data["representation"]

class Terrain(VisualCell):
    ## Instance variables
    def __init__(self, y_pos, x_pos, data):
        VisualCell.__init__(self, y_pos, x_pos, data)
    
class Unit(VisualCell):
    ## Instance variables
    def __init__(self, y_pos, x_pos, data):
        VisualCell.__init__(self, y_pos, x_pos, data)

def alpha_one(stdscr):
    ##  initalization
    stdscr.clear()
    game_pad = curses.newpad(20, 20)
    game_pad_box = Box(5, 5, 25, 25)
    init_menu_options = ["Move Unit", "Move Display", "Quit"]
    menu_obj = Menu(init_menu_options)

    ## colors
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)

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

    ## loop
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
            game_pad.addstr(cell.y_pos, cell.x_pos, cell.representation)
        
        game_pad.addstr(unit.y_pos, unit.x_pos, unit.representation)
        game_pad.refresh(0, 0, game_pad_box.get_y_top_left(), game_pad_box.get_x_top_left(), game_pad_box.get_y_bottom_right(), game_pad_box.get_x_bottom_right())
        
        ## wait here for input
        stdscr.refresh()
        key = stdscr.getkey()

## run correctly as standalone
if __name__ == "__main__":
    wrapper(alpha_one)