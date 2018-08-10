import attacks


class Infantry:
    def __init__(self, name, armor, hp, attack_mod, damage_mod, num_attacks, face_value, defensive=0, offensive=0):
        self.name = name
        self.health = hp
        self.max_health = hp
        self.armor_class = armor
        self.damage_modifier = damage_mod
        self.to_hit = attack_mod
        self.attacks = num_attacks
        self.face = face_value
        self.damage_done = 0
        self.kills = 0
        self.offensive = offensive
        self.defensive = defensive
        self.fielded = False

    def __str__(self):
        return self.name
    __repr__ = __str__

    def set_defenses(self, offensive, defensive):
        self.offensive = offensive
        self.defensive = defensive

    def fight(self, other_soldier):
        for attack in range(0, self.attacks):
            attack = attacks.roll(1, 20, self.to_hit, self.offensive - other_soldier.defensive)
            if attack != "F!" and (attack == "C!" or int(attack) >= other_soldier.armor_class):
                damage = attacks.roll(1, self.face, self.damage_modifier)
                self.damage_done += int(damage)
                other_soldier.health -= int(damage)
                # this soldier got the killing blow
                # This is an approximation of switching targets after killing one
                if other_soldier.health < 1 and other_soldier.health + int(damage) > 0:
                    self.kills += 1
                    other_soldier.health = 0
