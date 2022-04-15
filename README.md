# CODENAME-WARS
Warfare ASCII Replication Simulator, aka WARS, is a political/warfare/country simulation game. I'll try to build it to be silky smooth to mod, but no promises.
Written in Python, using Curses as a main library, but because I'm a little windows freak, I used this (https://pypi.org/project/windows-curses/#description) instead of the "real" thing.

## Todo

1. First and foremost, I need to relearn the tools. Its been a while since I've worked in Python, and I've never used JSON, but I think I understand it to a degree.
2. Secondarily, I need to build the engine before the content. Clearly I'm going to need some basic content to test my engine, but thats not what I mean.
3. Finally, after building the engine, I can build the content of the game. Unit and Building types, Reasearch, goodies galore.

So, what does that really look like?

### The Big Three

On the right of the screen, a log and psuedo-topbar-thing with constantly relevant or changing information, on the left, the Gameboard. Appearing only when needed, a contextual Menu that layers and displays relevent information. I call these the big three. I bring the concept from Dwarf Fortress and CDDA, although I'm sure many other games have used it.

It seems like a simple concept to back this game with.

### Content
Ideally, everything is somewhat connected; I like CDDA for that.

PLAYER controls FACTION, DECISCION
	FACTION controls LAND, RESOURCE, TECH, IDEOLOGY, CITIZEN, MILITARY, ASSET
		LAND
			changable through CONSTRUCTION
		RESOURCE
			used by CITIZEN, MILITARY, ASSET
		TECH
			required by CITIZEN, MILITARY, ASSET
				NEOLITHIC
				PREINDUSTRIAL
				INDUSTRIAL
				POSTINDUSTRIAL
				POSTMODERN
				FANTASTIC
			changable through RESEARCH
		IDEOLOGY
			used by CITIZEN, MILITARY, ASSET
			changable through DECISCION, TIME
		CITIZEN
			requires RESOURCE, ASSET
				FOOD
				WATER
				HOUSING
			has FEAROFLEADERSHIP, FEAROFOTHERS, JOY, PAIN
			impacted by IDEOLOGY
		MILITARY
			controlled by DECISCION
			requires RESOURCE, ASSET, TECH
				EQUIPMENT
				BODIES
				HOMEBASE
				*
			has SPEED, ATTACK, DEFENSE, STRATEGEY, PREPERATIONVSOPPOSED
			impacted by IDEOLOGY
		ASSET
			requires RESOURCE, TECH, LAND
			has PRODUCTION, HOMEBASE, CONSTRUCTION, RESEARCH, *
				PRODUCTION takes TIME
				CONSTRUCTION takes TIME
				RESEARCH takes TIME
				* takes time
			impacted by IDEOLOGY
			