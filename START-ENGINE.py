from army import *
from squad import *
from infantry import *
from battlefield import *


armies = dict()

# Armies to play with to lean how the program works
dwarves = Army("Dwarves", False, armies)
reinforcements = Army("reinforcements", False, armies)
reinforcements.add_soldier_type("Ironbreaker", 21, 59, 7, 4, 2, 8, 1, 0)
reinforcements.add_squad("Ironbreakers", "Ironbreaker", 60, 1)
dwarves.add_soldier_type("Hammer", 18, 59, 8, 5, 2, 13, 0, 0)
dwarves.add_squad("Hammers", "Hammer", 100, 1)
undead = Army("UndeadHorde", True, armies)
undead.add_soldier_type("Zombie", 8, 22, 4, 2, 1, 6)
undead.add_soldier_type("Blood Knight", 14, 11, 10, 8, 1, 8)
undead.add_squad("Zombies", "Zombie", 500, 1)
undead.add_squad("Blood Knights", "Blood Knight", 200, 1)
armies["dwarves"] = dwarves
armies["reinforcements"] = reinforcements
armies["undead"] = undead

while True:
    command = input("Names must be one word only\n"
                    "Create an army using army [army name]\n"
                    "Add a unit type to an army with [army] unit [unit name] [AC] [HP] [TO-HIT] [DAMAGE MOD] [ATTACKS] [DIE VALUE]\n"
                    "Create a squad of units and add them to an army with [army] add squad [squad name] [unit_name] [unit count] [unit priority]\n"
                    "Start a battle with '[army1] battle [army2] [front width]'\n\n")
    cmd_arguments = command.split(" ")
    process_commands(cmd_arguments, armies)
