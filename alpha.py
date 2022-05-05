##  This is the CODENAME-WARS Alpha V2.0
##  Coded by Ian Wuth, 5/1/2022

import curses
from curses import wrapper
from ians_toolkit import *
from brocks_toolkit import *
import json
import time


## Welcome back to the Alpha of CODENAME WARS
## Here in version two, we've cleaned up the space some, come take a look around!
## Our goals for this generation are to...
## - [ ] Create a cursor
## - [ ] Finalize major read/write structures
## - [ ] Impliment basic UI
## - [x] Integrate color



def alpha_two(stdscr):
    ##  initalization
    stdscr.clear()

## run correctly as standalone
if __name__ == "__main__":
    wrapper(alpha_one)