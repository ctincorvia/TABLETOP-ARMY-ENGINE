import unittest
import attacks


class TestAttacks(unittest.TestCase):

    def test_attack_roll(self):
        for i in range(0, 10):
            flat = int(attacks.attack_roll(i, 0))
            advantage = int(attacks.attack_roll(i, 1))
            disadvantage = int(attacks.attack_roll(i, -1))
            self.assertGreater(flat, i)
            self.assertGreater(advantage, i)
            self.assertGreater(disadvantage, i)
            self.assertGreater(21 + i, flat)
            self.assertGreater(21 + i, advantage)
            self.assertGreater(21 + i, disadvantage)

    def test_damage_roll(self):
        for i in range(4, 12):
            for j in range(0, 5):
                result = int(attacks.damage_roll(1, i, j))
                self.assertGreater(result, j)
                self.assertGreater(i + j + 1, result)


if __name__ == '__main__':
    unittest.main()
