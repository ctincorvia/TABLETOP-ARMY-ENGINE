import unittest
from army import *
from battlefield import *


class BattlefieldTests(unittest.TestCase):
    def setUp(self):
        self.armies = dict()
        # Armies to pull infantry out of
        dwarves = Army("Dwarves", False, self.armies)
        dwarves.add_soldier_type("Hammer", 18, 59, 8, 5, 1, 13, 0, 0)
        dwarves.add_squad("Hammers", "Hammer", 19, 1)
        dwarves.add_squad("Hammers2", "Hammer", 19, 1)
        undead = Army("UndeadHorde", True, self.armies)
        undead.add_soldier_type("Zombie", 0, 1, 4, 2, 1, 6)
        undead.add_squad("Zombies", "Zombie", 500, 1)
        undead.add_squad("Zombies2", "Zombie", 500, 1)
        self.armies["dwarves"] = dwarves
        self.armies["undead"] = undead
        self.battlefield = Battlefield(dwarves, undead, 20)

    def test_armies_advance(self):
        self.assertEqual(len(self.battlefield.front1), 0)
        self.assertEqual(len(self.battlefield.front2), 0)
        self.battlefield.armies_advance()
        self.assertEqual(len(self.battlefield.front1), 20)
        self.assertEqual(len(self.battlefield.front2), 20)

    def test_armies_attack(self):
        self.battlefield.armies_advance()
        self.battlefield.armies_attack()
        for soldier in self.battlefield.front2:
            self.assertTrue(soldier.health < 1)

    def test_clear_corpses(self):
        self.battlefield.armies_advance()
        self.battlefield.armies_attack()
        self.battlefield.clear_corpses()
        self.assertEqual(len(self.battlefield.front2), 0)


if __name__ == '__main__':
    unittest.main()
