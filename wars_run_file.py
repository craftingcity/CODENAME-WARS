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
    def __init__(self, y_pos, x_pos, data):
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.data = data
        self.name = data["name"]
        self.representation = data["representation"]

def alpha_one(stdscr):
    ## flags
    MOVE_FLAG = False

    ## variables
    world = []
    c = ""

    ## data
    terrain_data = datagrab(["content", "terrain", 0], "default_mod.json")
    military_data = datagrab(["content", "military", 0], "default_mod.json")

    ## logic makes the world go round
    for i in range(5):
        for j in range(5):
            new_cell = Cell(i, j, terrain_data)
            world.append(new_cell)

    unit = Cell(0, 0, military_data)

    ## loop
    while True:
        ## process input
        if (c == "q"):
            break
        if (c == "m") and not MOVE_FLAG:
            MOVE_FLAG = True
        if (c == "m") and MOVE_FLAG:
            MOVE_FLAG = False
        if (c == "KEY_UP") and MOVE_FLAG:
            unit.y_pos += 1
        if (c == "KEY_DOWN") and MOVE_FLAG:
            unit.y_pos -= 1
        if (c == "KEY_RIGHT") and MOVE_FLAG:
            unit.x_pos += 1
        if (c == "KEY_LEFT") and MOVE_FLAG:
            unit.x_pos -= 1



        ## draw to screen
        for cell in world:
            stdscr.addstr(cell.y_pos, cell.x_pos, cell.representation)
        stdscr.addstr(unit.y_pos, unit.x_pos, unit.representation)
        c = stdscr.getkey()

if __name__ == "__main__":
    wrapper(alpha_one)