import unittest
from army import *


class SquadTests(unittest.TestCase):
    def setUp(self):
        self.armies = dict()
        # Armies to pull infantry out of
        dwarves = Army("Dwarves", False, self.armies)
        dwarves.add_soldier_type("Hammer", 18, 59, 8, 5, 1, 13, 0, 0)
        dwarves.add_squad("Hammers", "Hammer", 100, 1)
        undead = Army("UndeadHorde", True, self.armies)
        undead.add_soldier_type("Zombie", 8, 22, 4, 2, 1, 6)
        undead.add_squad("Zombies", "Zombie", 500, 1)
        self.armies["dwarves"] = dwarves
        self.armies["undead"] = undead

    def test_refresh_troops(self):
        army = self.armies["dwarves"]
        soldiers = army.supply_troops(100)
        for soldier in soldiers:
            soldier.health = -1
        army.squads[0].refresh()
        soldiers = army.supply_troops(100)
        for soldier in soldiers:
            self.assertEqual(soldier.health, 59)

    def test_supply_troops_adequate(self):
        army = self.armies["dwarves"]
        soldiers1 = army.squads[0].supply_troops(50)
        army = self.armies["dwarves"]
        soldiers2 = army.squads[0].supply_troops(50)
        self.assertEqual(len(soldiers1), 50)
        self.assertEqual(len(soldiers2), 50)

    def test_supply_troops_inadequate(self):
        army = self.armies["dwarves"]
        soldiers1 = army.squads[0].supply_troops(150)
        self.assertEqual(len(soldiers1), 100)


if __name__ == '__main__':
    unittest.main()
