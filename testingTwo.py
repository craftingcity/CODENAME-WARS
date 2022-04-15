import curses
import curses.ascii as cASCII
import json
print("IMPORT COMPLETE")

stdscr = curses.initscr()
curses.curs_set(2)
print("INIT COMPLETE")
print("CALLING WRAPPER")

from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()
    
    # Display preamble
    preamble = "Welcome to the PreAlpha version of W.A.R.S. \nPlease input a key."
    stdscr.addstr(0, 0, preamble)
    curses.setsyx(10,0)
    # Await user input
    testing_input = stdscr.getkey()
    
    # Clear and Refresh
    stdscr.clear()
    stdscr.refresh()
    
    # Display endamble
    endamble = "Thank you \nYou entered {}.".format(testing_input)
    stdscr.addstr(0, 0, endamble)
    
    # Await user input
    ending_input = stdscr.getkey()
    

wrapper(main)
print("KILLING CURSES")
curses.endwin()
print("END OF LINE")