##  This is the CODENAME-WARS Alpha 1
##  Coded by Ian Wuth, 4/26/2022

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

class Flag:
    ## Instance variables
    def __init__(self, bool):
        self.bool = bool

    ## Method for flopping the flag
    def flop(self):
        self.bool = not self.bool
    ## Method for setting the flag
    def set(self, new_val):
        self.bool = new_val
    ## Mehtod for getting the flag
    def get(self):
        return self.bool

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
    ## Method for increasing current selection
    ## decreases variable
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
                menu_obj.plus()
        if key == "KEY_DOWN":
            if umf:
                unit.move_south()
            if mmf:
                game_pad_box.move_south()
            if mef:
                menu_obj.minus()
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
        if key == "o":
            if umf:
                unit_move_flag.set(False)
                menu_engage_flag.set(True)
            if mmf:
                map_move_flag.set(False)
                menu_engage_flag.set(True)
            if mef:
                menu_engage_flag.set(False)
                if cs == 0:
                    unit_move_flag.set(True)
                if cs == 1:
                    map_move_flag.set(True)
                if cs == 2:
                    break
        


        ## draw to stdscr; debug assistance
        stdscr.addstr(20, 0, f"Key: {key}, UMF: {umf}, MMF: {mmf}, MEF:{mef}")

        ## draw menu to stdscr
        vert_count = 0
        menu_options = menu_obj.get_options()
        cs = menu_obj.get_cs()
        for item in menu_options:
            vert_count += 1
            stdscr.addstr(19 + vert_count, 45, item)
        stdscr.addstr(20 + cs, 45, menu_options[cs], curses.A_REVERSE)
        
        ## draw to game_pad
        for cell in world:
            game_pad.addstr(cell.y_pos, cell.x_pos, cell.representation)
        
        game_pad.addstr(unit.y_pos, unit.x_pos, unit.representation)
        game_pad.refresh(0, 0, game_pad_box.get_y_top_left(), game_pad_box.get_x_top_left(), game_pad_box.get_y_bottom_right(), game_pad_box.get_x_bottom_right())
        
        ## wait here for input
        stdscr.refresh()
        key = stdscr.getkey()

if __name__ == "__main__":
    wrapper(alpha_one)