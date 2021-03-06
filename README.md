# TABLETOP-ARMY-ENGINE

Use this for all of you gigantic tabletop game battle simulation needs. Add armies, merge armies, or add units in the middle of battles.
Have the master necromancer lead from the back, and the high paladin lead from the front.
Get real time diagnostics.  Have the same army fight other armies one after another with losses and other stats persisting.  Go crazy.

# Getting started
You'll need python 3 to run this.  It's available here: https://www.python.org/downloads/

Once you have python, run the the START-ENGINE file.  There are some basic instructions that will pop up..

Armies are made up of squads.  Squads are made up of soldiers.  A single squad is all one type of soldier, but an army can have any amount of squads and each squad might be made up of different units.  For example, you might have an army made up of a squad of people weilding swords and a squad of people weilding axes.

There are 3 pre-constructed armies for you to play with to get a feel for how the commands work - dwarves, reinforcements, and undead.
You can create an army and add any number of squads, and then face it off against any other army you've built.

# Advanced instructions
Squads with the same priority will go in to battle at the same time.  Otherwise, squads with the lowest priority will go in to battle first.

During a battle, type resolve to skip to the end of the battle.

During a battle, type more to increase the amount of data reported.

During a battle, type less to decrease the amount of data reported.

Anytime, type [army1] absorb [army2] to absorb one army in to another.

Anytime, type refresh [army] to erase all of it's casualties.

During the battle, the engine will allow you to start another battle, but the original battle won't continue until the secondary one resolves.

# Author
Charles Incorvia
