import unittest
from army import *


class ArmyTests(unittest.TestCase):
    def setUp(self):
        self.armies = dict()
        # Armies to pull infantry out of
        dwarves = Army("Dwarves", False, self.armies)
        dwarves.add_soldier_type("Hammer", 18, 59, 8, 5, 1, 13, 0, 0)
        dwarves.add_squad("Hammers", "Hammer", 100, 1)
        undead = Army("UndeadHorde", True, self.armies)
        undead.add_soldier_type("Zombie", 8, 22, 4, 2, 1, 6)
        undead.add_squad("Zombies", "Zombie", 500, 1)
        undead.add_squad("Zombies2", "Zombie", 500, 1)
        self.armies["dwarves"] = dwarves
        self.armies["undead"] = undead

    def test_living_soldiers(self):
        self.assertEqual(self.armies["dwarves"].living_soldiers(), 100)
        self.assertEqual(self.armies["undead"].living_soldiers(), 1000)

    def test_refresh(self):
        army = self.armies["dwarves"]
        soldiers = army.supply_troops(100)
        for soldier in soldiers:
            soldier.health = -1
        army.refresh()
        soldiers = army.supply_troops(100)
        for soldier in soldiers:
            self.assertEqual(soldier.health, 59)

    def test_absorb_army(self):
        army = self.armies["dwarves"]
        army2 = self.armies["undead"]
        army.absorb_army(army2)
        self.assertEqual(army.living_soldiers(), 1100)
        self.assertEqual(army2.living_soldiers(), 0)

    def test_supply_troops_adequate(self):
        army = self.armies["dwarves"]
        soldiers1 = army.supply_troops(50)
        army = self.armies["dwarves"]
        soldiers2 = army.supply_troops(50)
        self.assertEqual(len(soldiers1), 50)
        self.assertEqual(len(soldiers2), 50)
        army.absorb_army(self.armies["undead"])
        soldiers3 = army.supply_troops(1000)
        self.assertEqual(len(soldiers3), 1000)

    def test_supply_troops_inadequate(self):
        army = self.armies["dwarves"]
        soldiers1 = army.supply_troops(150)
        self.assertEqual(len(soldiers1), 100)
        soldiers2 = army.supply_troops(100)
        self.assertEqual(len(soldiers2), 0)


if __name__ == '__main__':
    unittest.main()
