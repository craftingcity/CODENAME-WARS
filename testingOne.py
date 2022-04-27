import curses
from curses import wrapper
import time




def basic_movement(stdscr):
    ## initialize color pairs for later use
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    RED_ON_BLACK = curses.color_pair(1)
    GREEN_ON_BLACK = curses.color_pair(2)
    RED_ON_WHITE = curses.color_pair(3)

    ## initialize pad, refresh or its not real
    padobj = curses.newpad(200, 200)
    stdscr.refresh()

    ## fill the pad
    for i in range(19):
        for j in range(19):
            padobj.addstr(i, j, ".", RED_ON_WHITE)

    ## display the pad
    padobj.refresh(0, 0, 0, 0, 20, 20)
    
    ## lets make some variables
    c = ""
    x_var = 0
    y_var = 0

    while c != "q":
        ## clear and refresh 
        stdscr.clear()
        stdscr.refresh()

        ## move the pad
        padobj.refresh(0, 0, y_var, x_var, 20 + y_var, 20 + x_var)
        c = stdscr.getkey()

        ## edit values
        if c == "1":
            y_var += 1
            x_var -= 1
        if c == "2":
            y_var += 1
        if c == "3":
            y_var += 1
            x_var += 1
        if c == "4":
            x_var -= 1
        if c == "6":
            x_var += 1
        if c == "7":
            y_var -= 1
            x_var -= 1
        if c == "8":
            y_var -= 1
        if c == "9":
            y_var -= 1
            x_var += 1
        


def rebindingv1(stdscr):
    ## initialize vars
    current_key = ""
    bound_key = ""
    rebind_key = "="
    counter = 0

    ## initialize looping
    while True:
        if current_key == "q":
            break
        
        ## screen manipulation 
        stdscr.clear()
        stdscr.addstr(10, 10, f"Your last pressed key is: {current_key} The currently bound key is: {bound_key} Press {rebind_key} to rebind.")
        stdscr.addstr(11, 10, f"Counter: {counter}")
        stdscr.refresh()

        ## wait here for input; either we increase the count OR rebind a key OR pass 
        current_key = stdscr.getkey()
        
        if current_key == bound_key:
            counter += 1
        if current_key == rebind_key:
            ## screen manipulation; ask for new input
            stdscr.clear()
            stdscr.addstr(10, 10, "Press new key...")
            stdscr.refresh()
            ## edit variables - make sure there is no overwriting
            current_key = stdscr.getkey()
            if current_key in [bound_key, rebind_key]:
                stdscr.clear()
                stdscr.addstr(10, 10, "Rebind failed; key in use. Please try again soon!")
                stdscr.refresh()
                time.sleep(0.4)
            else:
                bound_key = current_key

def menuv1(stdscr):
    ## initialize working vars
    count = 0
    spacer = 4
    ## populate option array
    option_arry = ["Option One", "Option Two", "Bingoboard", "Option Four"]
    ## display options
    stdscr.clear()
    for i in option_arry:
        stdscr.addstr(0, count, i)
        count += 1
    stdscr.refresh()


    ## initialize input handler
    c = stdscr.getkey()

    


## wrapper calls main, giving use of the entire terminal as stdscr
wrapper(menuv1)
