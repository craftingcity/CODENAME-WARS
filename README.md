# CODENAME-WARS
Warfare ASCII Replication Simulator, aka WARS, is a political/warfare/country simulation game. I'll try to build it to be silky smooth to mod, but no promises.
Written in Python, using Curses (https://docs.python.org/3/library/curses.html) as a main library.

## Todo

1. First and foremost, I need to relearn the tools. Its been a while since I've worked in Python, and I've never used JSON, but I think I understand it to a degree.
2. Secondarily, I need to build the engine before the content. Clearly I'm going to need some basic content to test my engine, but thats not what I mean.
3. Finally, after building the engine, I can build the content of the game. Unit and Building types, Reasearch, goodies galore.

So, what does that really look like?

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

PLAYER controls FACTION, DECISCION
	DECISCION controls RESEARCH, CONSTRUCTION, IDEOLOGY, COMMAND
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
				MODERN / PRESPACER
				POSTSPACER / SCIFI
				FANTASTIC
			changable through RESEARCH
		IDEOLOGY
			used by CITIZEN, MILITARY, ASSET
			impacts MORALE
			changable through DECISCION, TIME
		CITIZEN
			requires RESOURCE, ASSET
				FOOD
				WATER
				HOUSING
			has MORALE
			impacted by IDEOLOGY
		MILITARY
			controlled by COMMAND
			requires RESOURCE, ASSET, TECH
				EQUIPMENT
				BODIES
				HOMEBASE
				*
			has SPEED, ATTACK, DEFENSE, STRATEGEY, PREPERATIONVSOPPOSED, MORALE
			impacted by IDEOLOGY, CITIZEN
		ASSET
			requires RESOURCE, TECH, LAND
			has PRODUCTION, HOMEBASE, CONSTRUCTION, RESEARCH, *
				PRODUCTION takes TIME
				CONSTRUCTION takes TIME
				RESEARCH takes TIME
				* takes TIME
			impacted by IDEOLOGY

*see default_mod.json*

We begin with the basics - metadata.

The "modid" is a unique identifer for this specific modpack. The "version" is, as you may have guessed, the version number. "author" seems similarly self explanitory. "content" stores the core of the gameplay information. For consistency and ease of access, each individual entry in this file has some common features; a unique "id", a major "catagory" and a more minor "subcatagory". Most entries also have a "name" and a "description" that would display if they were examined, but some do not.

Inside "content", each of the categories of data is sorted by its name. Lets look at "decision".

Decisions are meant to be one of the most flexable portions of this game. Decisions are how you interact with your opponents, allies, and those otherwise under your influence. They have a "cost", which is for now simply a number - representing a Political Power cost - but theoretically could be a list of costs to include other resources. They also have "consequences", each of whom get there own "id" and such, as well as a "duration" in game-ticks, a "target" variable they wish to impact. As this object type is yet unimplimented, I can only note that the operation to be done by "effect" and to "target" is perhaps decided by the "subcatagory" of the object, or it could perhaps simply be added.

Moving on, lets examine "terrain". Each object gets the full 5 basics as well as a "resources_list" list, an "assets_list" list, and a "move_speed_multiplier" value. The lists contain "resources" and "assets" available to be extracted or constructed in that "terrain". The "move_speed_multiplier" impacts a "unit"'s "move_speed".

Resources are currently extremely simple. They have no nonstandard values, and are currently being defined here in their simplest terms.

Technologies are an exciting batch for me - they seem like a fun game design thing. They each bare the big 5 as well as a "cost" in Science Points. They are required for some "asset".

Currently, the "citizen" and "ideology" catagories are quite interlinked and only bare binary options. Remember, this is still the beginning stages of this portion of the game. "ideology" is especially influenced by "decision" as well, specificially pointing to "testing_decision_impose_*".

Military is currently structured such that each "unit" has a "training_cost", "bodies_cost", and "equipment_cost" in game-ticks, "bodies_resource" and a list of other resources, as well as an "attack", "defence", "move_speed", "base_preperation" and a "strategy" which gets its own little object that contains lists of other strategies it is better or worse vs.

Assets get the big 5 as well as "cost", "required" "tech", what if anything they have in "production" and how much, as well as the "prod_speed" value arbitratily representing the base speed of the production. When "prod_speed" is 0, the intended outcome is a one time bonus when the construction is first completed (of note, I have been thinking of how this can be scum-proofed, but this is the system as it is invisioned).