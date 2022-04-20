## testingOne.py is my testing playground.
## author: craftingcity     date: 04/19/22

import curses
from curses import wrapper

def main(stdscr):
    stdscr = curses.initscr()
    c = ""
    count = 0
    down_count = 0
    while c not in ["q", "Q"]:
        stdscr.addstr(down_count, count, str(c))
        c = stdscr.getkey()
        count += 1
        if count > 10:
            count = 0
            down_count += 1
            if down_count > 10:
                count = 0
                down_count = 0
                stdscr.clear()
                stdscr.addstr(8, 20, "Completed. Press any q or Q to quit.")
                stdscr.addstr(10, 20, "Any other keypress will continue.")




wrapper(main)