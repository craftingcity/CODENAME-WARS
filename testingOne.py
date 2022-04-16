from blessed import *
from json import *

def main():
    terminal = Terminal()
    
    TERM_HEIGHT = terminal.height
    TERM_WIDTH = terminal.width
    
    
    for i in range(0, TERM_HEIGHT // 4):
        for i in range(0, TERM_WIDTH // 4):
            print(terminal.white_on_blue("."), end='')
    
    terminal.home()
    print(terminal.white_on_green("This is home."), end='')
    terminal.moveup(2)
    terminal.moveright(4)
    print(terminal.white_on_red("This is home, up 2, right 4."), end='')


if __name__ == "__main__":
	main()