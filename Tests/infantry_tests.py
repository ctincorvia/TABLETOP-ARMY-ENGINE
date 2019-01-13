import unittest
from army import *
from infantry import *


class InfantryTest(unittest.TestCase):

    def setUp(self):
        self.armies = dict()
        # Armies to pull infantry out of
        dwarves = Army("Dwarves", False, self.armies)
        dwarves.add_soldier_type("Hammer", 900, 59, 8, 5, 2, 13, 0, 0)
        dwarves.add_squad("Hammers", "Hammer", 100, 1)
        undead = Army("UndeadHorde", True, self.armies)
        undead.add_soldier_type("Zombie", 0, 22, 4, 2, 1, 6)
        undead.add_squad("Zombies", "Zombie", 500, 1)
        self.armies["dwarves"] = dwarves
        self.armies["undead"] = undead

    def test_infantry_can_take_hits(self):
        army1 = self.armies["undead"]
        soldier1 = army1.supply_troops(10)[0]

        army2 = self.armies["dwarves"]
        soldier2 = army2.supply_troops(10)[0]

        starting_hp = soldier1.max_health
        soldier2.fight(soldier1)
        self.assertGreater(starting_hp, soldier1.health)

    def test_infantry_can_miss(self):
        army1 = self.armies["undead"]
        soldier1 = army1.supply_troops(10)[0]

        army2 = self.armies["dwarves"]
        soldier2 = army2.supply_troops(10)[0]

        starting_hp = soldier2.max_health
        soldier1.fight(soldier2)
        self.assertEqual(starting_hp, soldier2.health)


if __name__ == '__main__':
    unittest.main()
