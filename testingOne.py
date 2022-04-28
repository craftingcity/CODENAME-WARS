import curses
from curses import COLOR_BLACK, COLOR_WHITE, wrapper
import time
import json

# This is a comment meant to see changes to the file. -BW


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
    ## color
    curses.init_pair(1, COLOR_WHITE, COLOR_BLACK)
    BLACK_ON_WHITE = curses.color_pair(1)

    ## initialize working vars
    count = 0
    spacer = 4
    selected_option = 0
    current_key = ""
    fnaglin = 0


    ## populate option array
    option_array = ["Option One", "Option Two", "Bingoboard", "Option Four"]

    ## initialize input handler
    while True:
        if current_key == "q":
            break
        if current_key == "KEY_LEFT":
            if selected_option > 0:
                selected_option -= 1
        if current_key == "KEY_RIGHT":
            if selected_option < len(option_array):
                selected_option += 1
        ## display options
        stdscr.clear()
        for item in option_array:
            stdscr.addstr(0, count, item, BLACK_ON_WHITE)
            count += len(item) + spacer
        
        
        ## display current selection
        if selected_option == 0:
            fnaglin = 0
        if selected_option > 0:
            for i in range(selected_option):
                fnaglin += len(option_array[i]) + spacer
        stdscr.addstr(0, fnaglin, option_array[selected_option], curses.A_REVERSE)
        stdscr.addstr(10, 10, f"{current_key}, {selected_option}")

        count = 0
        fnaglin = 0
        stdscr.refresh()
        current_key = stdscr.getkey()


## datagrab is a tool to interact with json files, interpreting a list of strings and ints as an ordered path to the requested data
def datagrab(path, filename):
    ## i find and read default_mod.json, then close it
    open_file = open(filename)
    data = json.loads(open_file.read())
    open_file.close()

    ## i look at what i read using the path to guid my way
    for i in path:
        if i is int:
            data[i]
        if i is str:
            data = data.get(i)
            
    ## and thats it! im all done, so ill return the requested data
    return data

def alpha(stdscr):
    stdscr.clear()
    

    


## wrapper calls main, giving use of the entire terminal as stdscr
wrapper(alpha)
