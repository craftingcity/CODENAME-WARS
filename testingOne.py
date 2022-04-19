import curses
from curses import wrapper

def main(stdscr):
    stdscr = curses.initscr()
    stdscr.addstr(0, 0, "GAMER")
    c = stdscr.getch()

wrapper(main)