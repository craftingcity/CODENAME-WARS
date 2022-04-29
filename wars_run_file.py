##  This is the CODENAME-WARS Alpha 1
##  Coded by Ian Wuth, 4/26/2022

import curses
from curses import wrapper
from enum import Flag
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
    
    ## Method to return the current value of bool
    def get(self):
        return self.bool
    
    ## Method to set the current value of bool
    def set(self, new_val):
        self.bool = new_val

def alpha_one(stdscr):
    ##  intilize some objects; pad for the map, box for coordinates for the pad
    game_pad = curses.newpad(20, 20)
    game_pad_box = Box(5, 5, 25, 25)

    menu_pad = curses.newpad(20, 20)
    menu_pad_box = Box(40, 40, 60, 60)

    ## flags
    unit_move = False
    map_move = False
    menu_flag = True


    ## variables
    current_menu_selection = 0
    menu_options = ["Move Map", "Move Unit"]
    menu_iteratable = 0
    world = []
    key = None

    ## constants
    MAX_TUPLE = stdscr.getmaxyx()
    MAX_HEIGHT = MAX_TUPLE[0]
    MAX_WIDTH = MAX_TUPLE[1]

    ## data
    terrain_data = datagrab(["content", "terrain", 0], "default_mod.json")
    military_data = datagrab(["content", "military", 0], "default_mod.json")

    ## logic makes the world go round
    for i in range(19):
        for j in range(19):
            new_cell = Cell(i, j, terrain_data)
            world.append(new_cell)

    unit = Cell(0, 0, military_data)

    ## loop for input and screen manipulation
    while True:
        ## process input
        if key == "q":
            break
        if key == "KEY_UP":
            if unit_move == True:
                unit.move_north()
            if map_move == True:
                game_pad_box.move_north()
            if menu_flag == True:
                current_menu_selection -= 1
        if key == "KEY_DOWN":
            if unit_move == True:
                unit.move_south()
            if map_move == True:
                game_pad_box.move_south()
            if menu_flag == True:
                current_menu_selection += 1
        if key == "KEY_RIGHT":
            if unit_move == True:
                unit.move_east()
            if map_move == True:
                game_pad_box.move_east()
            if menu_flag == True:
                current_menu_selection += 1
        if key == "KEY_LEFT":
            if unit_move == True:
                unit.move_west()
            if map_move == True:
                game_pad_box.move_west()
            if menu_flag == True:
                current_menu_selection -= 1
        if key == "e":
            if unit_move == True:
                menu_flag = True
                unit_move = False
            if map_move == True:
                menu_flag = True
                map_move = False
            if menu_flag == True:
                menu_flag = False
                if current_menu_selection == 0:
                    map_move = True
                if current_menu_selection == 1:
                    unit_move = True



        ## begin screen write sequence
        stdscr.clear()
        stdscr.refresh()

        ## draw to stdscr
        stdscr.addstr(MAX_HEIGHT - 10, 40, f"Key: {key} UnitMove: {unit_move} MapMove: {map_move} MenuFlag: {menu_flag}")
        stdscr.refresh()

        ## draw to gamepad 
        for cell in world:
            game_pad.addstr(cell.y_pos, cell.x_pos, cell.representation)
        game_pad.addstr(unit.y_pos, unit.x_pos, unit.representation)
        game_pad.refresh(0, 0, game_pad_box.get_y_top_left(), game_pad_box.get_x_top_left(), game_pad_box.get_y_bottom_right(), game_pad_box.get_x_bottom_right())
        
        ## draw to menu_pad
        menu_iteratable = 0
        for option in menu_options:
            menu_pad.addstr(menu_iteratable, 0, option)
            menu_iteratable += 1
        menu_iteratable = current_menu_selection
        if menu_flag == True:
            menu_pad.addstr(menu_iteratable, 0, menu_options[current_menu_selection], curses.A_REVERSE)
        menu_pad.refresh(0, 0, menu_pad_box.get_y_top_left(), menu_pad_box.get_x_top_left(), menu_pad_box.get_y_bottom_right(), menu_pad_box.get_x_bottom_right())

        ## wait here for a new input to process
        key = stdscr.getkey()

## run a wrapper over alpha_one for proper as-file runs
if __name__ == "__main__":
    wrapper(alpha_one)