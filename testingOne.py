from blessed import *
from json import *

def main():
	terminal = Terminal()
	data = terminal.black_on_white("A")
	for i in range(0, (terminal.height // 2) - 5):
		for i in range(0, (terminal.width // 2) - 5):
			print(data, end='')
		print()



if __name__ == "__main__":
	main()