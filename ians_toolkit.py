## This is Ian's Toolkit for CODENAME-WARS, updated as of version A20
## Most of the classes here are integral to the current version of the Alpha

import json
import curses

## FileReader is FileWriter's sister class.
## FileWriter is FileReader's sister class.
## With their power's combined, I can rule all the lands! Mwah hah hah!
## Or just format my files consistantly so that nothing goes awry.
## I suppose that will do.

## Meet FileReader! She takes either a string or a list of strings and turns them
## into yummy yummy useable data

class FileReader:
    ## Instance variables
    def __init__(self, r):
        self.r = r
        self.holding = []
        self.modlist = []
        self.final = {}
        
        ## read r into holding as json data
        ## correctly interpret single string file-names and lists of string file-names
        if type(r) is list:
            for item in r:
                open_file = open(item, "r")
                self.holding.append(json.load(open_file))
                open_file.close()
        if type(r) is str:
            open_file = open(r, "r")
            self.holding.append(json.load(open_file))
            open_file.close()
        
        ## examine the contents of holding
        for data in self.holding:
            ## bind variables for this run of the loop
            content = data["content"]
            modid = data["modid"]
            version = data["version"]
            author = data["author"]
            ## append some metadata to the "modlist"
            self.modlist.append(f"{modid} - v{version}, by {author}")
            ## key seen items by their "id"
            for item in content:
                self.final.update({item["id"]:item})
    
    ## Method for getting an item loaded by FileReader by its id
    def grab(self, id):
        return self.final[id]

## Meet FileWriter! She only takes a filename, 
## but she'll mark down exactly what you what how you want it!
class FileWriter:
    ## Instance variables
    def __init__(self, w):
        self.w = w

    def write(self, input):
        open_file = open(self.w, "w")
        open_file.write(input)
        open_file.close()

    def append(self, input):
        open_file = open(self.w, "a")
        open_file.write(input)
        open_file.close()

class Logger(FileWriter):
    ## Instance variables
    def __init__(self, w):
        FileWriter.__init__(self, w)

    def log(self, message, level=10):
        self.append(f"{level}: {message}\n")

class World(FileWriter):
    ## Instance variables
    def __init__(self, f):
        FileWriter.__init__(self, f)
        self.f = f
        ## if the file exsists, read it, otherwise create it and read it
        try:
            open_file = open(self.f, "r")
        except FileNotFoundError:
            open_file = open(self.f, "x")
            open_file = open(self.f, "r")
        ## World reads json data from the passed file
        self.mass_data = json.load(open_file)
        ## stop looking at file
        open_file.close()
    
    def save(self):
        ## dump makes sure to pass a string to write
        self.write(json.dumps(self.mass_data))

    ## Current data interactions
    ### Getting

    def get_terrain_at(self, y, x):
        return self.mass_data["current"]["gamestate"]["terrain"][y][x]

    def get_asset_at(self, y, x):
        return self.mass_data["current"]["gamestate"]["asset"][y][x]

    def get_unit_at(self, y, x):
        return self.mass_data["current"]["gamestate"]["unit"][y][x]

    def get_stats_for(self, faction="Yummi's Fallen"):
        return self.mass_data["current"]["factions"][faction]["stats"]

    ### Setting

    def set_terrain_at(self, y, x, id):
        self.mass_data["current"]["gamestate"]["terrain"][y][x]["baseid"] = id

    def set_asset_at(self, y, x):
        self.mass_data["current"]["gamestate"]["asset"][y][x]["baseid"] = id

    def set_unit_at(self, y, x):
        self.mass_data["current"]["gamestate"]["unit"][y][x]["baseid"] = id

    ## Meta data interactions
    ### Getting

    def get_name(self):
        return self.mass_data["meta_data"]["game_name"]

    def get_mode(self):
        return self.mass_data["meta_data"]["mode"]

    def get_num_players(self):
        return self.mass_data["meta_data"]["num_players"]

    def get_world_height(self):
        return self.mass_data["meta_data"]["world_height"]

    def get_world_width(self):
        return self.mass_data["meta_data"]["world_height"]

## Cell is a class of definitions and variables used to represent "a board unit"
## If one does not pass it data, it could be used as a coordinate object, but so can a tuple, or a two-item list
class Cell:
    ## Instance variables
    def __init__(self, y_pos, x_pos, data="None"):
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.data = data

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

class VisualCell(Cell):
     ## Instance variables
    def __init__(self, y_pos, x_pos, data):
        Cell.__init__(self, y_pos, x_pos, data)
        self.name = self.data["name"]
        self.representation = self.data["representation"]
        self.colors = self.data["colors"]
    
    ## Methods for returning visual data
    def get_name(self):
        return self.name
    
    def get_rep(self):
        return self.representation

    def get_colors(self):
        return self.colors

class Terrain(VisualCell):
    ## Instance variables
    def __init__(self, y_pos, x_pos, data):
        VisualCell.__init__(self, y_pos, x_pos, data)
    
class Unit(VisualCell):
    ## Instance variables
    def __init__(self, y_pos, x_pos, data):
        VisualCell.__init__(self, y_pos, x_pos, data)

## Box is a class that represents two sets of coordinates
## I use this to represent pads and windows and such easily
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

    ## Methods for moving the box
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
## for now that looks like just boolieans because set() is bugged?
class Flag:
    ## Instance variables
    def __init__(self, var):
        self.var = var

    ## Method for flopping the flag
    def flop(self):
        self.var = not self.var
    ## Method for setting the flag
    ## Currently bugged when used in Alpha 1's looping input handler
    def set(self, new_val):
        self.var = new_val
    ## Mehtod for getting the flag
    def get(self):
        return self.var

## Menu is a class of variables and definitions used to represent a system
## This system, typically, is a menu
## You have a bunch of "options" which are strings or whatever you're displaying
## and the "current_selection" which is a simple int representing the user's path on that linear "options"
## as the user inputs, modulate with plus() and minus(), badabingbadaboom thats a menu
## do some fancy schmancy on the current selection if you dont hate your user (or don't if you do)
class Menu:
    ## Instance variables
    def __init__(self, options="None", current_selection=0):
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

def main():
    pass

if __name__ == "__main__":
    main()