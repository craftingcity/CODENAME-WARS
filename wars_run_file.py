##  This is the CODENAME-WARS Alpha V1.8
##  Coded by Ian Wuth, 5/1/2022

import curses
from curses import wrapper
import json


## The purpose of Alpha one is twofold;
## First, a file read-write to a json
## Second, an implimentation of "the big three" - the map (and most everything else you see), menu (and the basic controlls), and log (specifically what my cursor is looking at)


## datagrab is a tool to read json files, interpreting a list of strings and ints as an ordered path to the requested data
def datagrab(path, filename):
    ## i find and read default_mod.json, then close it
    open_file = open(filename)
    data = json.load(open_file)
    open_file.close()
    ## then i interprit the path to find the requested data
    for i in path:
        data = data[i]
    ## and then i give it back!
    return data

## FileToucher is a class of definitions used to interact with data on disk
class FileToucher:
    ## Instance variables
    def __init__(self, f):
        self.f = f
        
    
    ## Method for interpriting f as a string refrencing a json file or list of strings refrencing json files
    def interp(self):
        if self.f is list:
            data_pack = []
            for i in self.f:
                open_file = open(i)
                data = json.load(open_file)
                open_file.close()
                data_pack.append(data)
            self.data = data_pack
        if self.f is str:
            open_file = open(self.f)
            data = json.load(open_file)
            open_file.close()
            self.data = data

    ## Method for searching a given object for a given target recusively,
    ## allowing for something akin to an id lookup
    def recursive_search(self, obj, target):
        for item in obj:
            if item == target:
                return obj
            if item is (list or dict):
                self.recursive_search(item, target)


## Cell is a class of definitions and variables used to represent "a board unit"
class Cell:
    ## Instance variables
    def __init__(self, y_pos, x_pos, data):
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.data = data
        self.name = data["name"]
        self.representation = data["representation"]

    ## Methods for returning y_pos and x_pos
    def get_y(self):
        return self.y_pos
    def get_x(self):
        return self.x_pos

    ## Methods for adjusting y_pos and x_pos in increments of one
    def move_north(self):
        self.y_pos = self.y_pos - 1
    def move_south(self):
        self.y_pos = self.y_pos + 1
    def move_east(self):
        self.x_pos = self.x_pos + 1
    def move_west(self):
        self.x_pos = self.x_pos - 1

## Box is a class of definitions and variables used to store coordinates for my ease of use
class Box:
    ## Instance variables
    def __init__(self, y_top_left, x_top_left, y_bottom_right, x_bottom_right):
        self.y_top_left = y_top_left
        self.x_top_left = x_top_left
        self.y_bottom_right = y_bottom_right
        self.x_bottom_right = x_bottom_right

    ## Methods for returning the positional data
    def get_y_top_left(self):
        return self.y_top_left
    def get_x_top_left(self):
        return self.x_top_left
    def get_y_bottom_right(self):
        return self.y_bottom_right
    def get_x_bottom_right(self):
        return self.x_bottom_right

    ## Methods for moving the whole box
    def move_north(self):
        self.y_bottom_right = self.y_bottom_right - 1
        self.y_top_left = self.y_top_left - 1
    def move_south(self):
        self.y_bottom_right = self.y_bottom_right + 1
        self.y_top_left = self.y_top_left + 1
    def move_east(self):
        self.x_bottom_right = self.x_bottom_right + 1
        self.x_top_left = self.x_top_left + 1
    def move_west(self):
        self.x_bottom_right = self.x_bottom_right - 1
        self.x_top_left = self.x_top_left - 1

## Flag is a class of variables and definitions used to represent portions of game-state/internal-state
class Flag:
    ## Instance variables
    def __init__(self, var):
        self.var = var

    ## Method for flopping the flag
    def flop(self):
        self.var = not self.var
    ## Method for setting the flag
    def set(self, new_val):
        self.var = new_val
    ## Mehtod for getting the flag
    def get(self):
        return self.var

## Menu is a class of variables and definitions used to represent a menu system
class Menu:
    ## Instance variables
    def __init__(self, options, current_selection=0):
        self.options = options
        self.current_selection = current_selection
    
    ## Method for returning options in its original form
    def get_options(self):
        return self.options
    ## Method for returning options in its original form
    def set_options(self, new_val):
        self.options = new_val
    ## Method for "increasing" current selection
    def plus(self):
        self.current_selection += 1
    ## Method for decreasing current selection
    def minus(self):
        self.current_selection -= 1
    ## Method for getting current selection
    def get_cs(self):
        return self.current_selection
    ## Method for setting current selection
    def set_cs(self, new_val):
        self.current_selection = new_val


def alpha_one(stdscr):
    ##  initalization
    stdscr.clear()
    game_pad = curses.newpad(20, 20)
    game_pad_box = Box(5, 5, 25, 25)
    init_menu_options = ["Move Unit", "Move Display", "Quit"]
    menu_obj = Menu(init_menu_options)

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
    terrain_data = datagrab(["content", "terrain", 0], "default_mod.json")
    military_data = datagrab(["content", "military", 0], "default_mod.json")

    ## logic makes the world go round
    for i in range(19):
        for j in range(19):
            new_cell = Cell(i, j, terrain_data)
            world.append(new_cell)

    unit = Cell(0, 0, military_data)

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
        ## "o" is used bc I dont quite know how to use 'Enter'
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