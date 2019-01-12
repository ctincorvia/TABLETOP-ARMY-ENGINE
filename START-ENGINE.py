from army import *
from squad import *
from infantry import *
from battlefield import *


armies = dict()

# Armies to play with to lean how the program works
testarmy2 = Army("Dwarves", False, armies)
testarmy = Army("Dwarves2", False, armies)
testarmy.add_soldier_type("Ironbreaker", 21, 59, 7, 4, 2, 8, 1, 0)
testarmy.add_squad("Ironbreakers", "Ironbreaker", 60, 1)
testarmy2.add_soldier_type("Hammer", 18, 59, 8, 5, 2, 13, 0, 0)
testarmy2.add_squad("Hammers", "Hammer", 100, 1)
testhorde = Army("UndeadHorde", True, armies)
testhorde.add_soldier_type("Zombie", 8, 22, 4, 2, 1, 6)
testhorde.add_soldier_type("Blood Knight", 14, 11, 10, 8, 1, 8)
testhorde.add_squad("Zombies", "Zombie", 1000, 1)
testhorde.add_squad("Blood Knights", "Blood Knight", 200, 1)
armies["dwarves"] = testarmy2
armies["dwarves2"] = testarmy
armies["undead"] = testhorde


while True:
    command = input("Names must be one word only\n"
                    "Create an army using army [army name]\n"
                    "Add a unit type to an army with [army] unit [unit name] [AC] [HP] [TO-HIT] [DAMAGE MOD] [ATTACKS] [DIE VALUE]\n"
                    "Create a squad of units and add them to an army with [army] add squad [squad name] [unit_name] [unit count] [unit priority]\n"
                    "Start a battle with '[army1] battle [army2] [front width]'\n\n")
    cmd_arguments = command.split(" ")
    process_commands(cmd_arguments, armies)
