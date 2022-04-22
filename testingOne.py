## testingOne.py is my testing playground.
## author: craftingcity     date: 04/19/22

import curses
from curses import wrapper

def main(stdscr):
    stdscr = curses.initscr()
    c = ""
    dimentional_tuple = stdscr.getmaxyx()
    height_dimention = dimentional_tuple[0]
    width_dimention = dimentional_tuple[1]

## currently not working
    map_window = stdscr.subwin(height_dimention // 2, width_dimention // 2, 0, 0)
    map_window.addstr(20, 20, "this is in my subwindow")


    c = stdscr.getch()




wrapper(main)