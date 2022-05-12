# CODENAME-WARS
Warfare ASCII Replication Simulator, aka WARS, is a political/warfare/country simulation game. I'll try to build it to be silky smooth to mod, but no promises.
Written in Python, using Curses (https://docs.python.org/3/library/curses.html) as a main library.

## Todo

1. First and foremost, I need to relearn the tools. Its been a while since I've worked in Python, and I've never used JSON, but I think I understand it to a degree.
2. Secondarily, I need to build the engine before the content. Clearly I'm going to need some basic content to test my engine, but thats not what I mean.
	2a. Cursor
	2b. Hotkeys
3. Finally, after building the engine, I can build the content of the game. Unit and Building types, Reasearch, goodies galore.

### The Big Four
On the right of the screen, a log and psuedo-topbar-thing with constantly relevant or changing information, on the left, the Gameboard. Appearing only when needed, a contextual Menu that layers and displays relevent information. I call these the big three. I bring the concept from Dwarf Fortress and CDDA, although I'm sure many other games have used it.
Underneath them, python runs the Engine that makes everything click.
It seems like a simple concept to back this game with.

#### Log
The log will be split into three parts, the first displays major information, such as TIME. The second displays a rolling log of your moves and all opponent's. The third displays information about what is under your cursor.

#### Gameboard
The Gameboard needs a few things;
- Layers; i dont want to be able to go underground, but a background for LAND, a foreground for ASSET, MILITARY
- Cursor; the main form of interaction the player has with the gameboard, decisions and the like will directly effect what youre looking at.

#### Menu
The menu, I think, will be the most dependent of the big three. In its simplest, all it needs to do is process input and hand it to the engine.

#### Engine
Build with Curses, run under everything. Handle input via menu, impact gameboard and log.

### Content
Ideally, everything is somewhat connected; I like CDDA for that.

PLAYER controls FACTION, DECISION
	DECISION controls RESEARCH, CONSTRUCTION, LAWS, COMMANDS
	FACTION controls TERRAIN, RESOURCE, TECH, IDEOLOGY, CITIZEN, MILITARY, ASSET
			has LAWS as IDEOLOGY
		TERRAIN
			has BUILDABLES
		RESOURCE
			used by ANY
		TECH
			required by ANY
			examples:
				PREAGRARRIAN
				POSTAGRARRIAN
				PREINDUSTRIAL
				INDUSTRIAL
				POSTINDUSTRIAL
				MODERN / PRESPACER
				POSTSPACER / SCIFI
				FANTASTIC
			changable through RESEARCH
		IDEOLOGY
			used by CITIZEN, ASSET, REASEARCH
			impacts MORALE
		CITIZEN
			requires RESOURCE, ASSET
			examples:
				FOOD
				WATER
				HOUSING
			has MORALE, IDEOLOGY
		MILITARY
			controlled by COMMANDS
			requires RESOURCE, ASSET, TECH, IDEOLOGY, CITIZEN
			examples:
				EQUIPMENT
				BODIES as CITIZEN and RESOURCE
				TRAINING_CAMP
				WARRIOR_TECH
				RAIDER_IDEO
			has SPEED, ATTACK, DEFENSE, STRATEGEY, PREPERATIONVSOPPOSED
		ASSET
			requires RESOURCE, TECH, TERRAIN, IDEOLOGY
			has ANY