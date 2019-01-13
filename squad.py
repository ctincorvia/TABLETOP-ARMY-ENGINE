import copy


class Squad:
    def __init__(self, _name, _army, _priority, _original_size, _soldier_type):
        self.name = _name
        self.soldier_type = _soldier_type
        self.priority = _priority
        self.army = _army
        self.original_size = _original_size
        self.soldiers = list()
        self.kills = 0
        self.damage_done = 0
        self.depleted = False

    def __str__(self):
        return self.name
    __repr__ = __str__

    def report_status(self):
        print("----------------------------")
        print("Squad: " + self.name)
        kills = 0
        damage = 0
        dead = 0
        reserves = 0
        for soldier in self.soldiers:
            kills += soldier.kills
            damage += soldier.damage_done
            if soldier.health < 1:
                dead += 1
            else:
                reserves += 1
        print("Kills: " + str(kills))
        print("Damage: " + str(damage))
        print("Dead: " + str(dead))
        print("Reserves: " + str(reserves))

    def refresh(self):
        self.depleted = False
        soldier = self.army.soldier_types[self.soldier_type]
        self.soldiers = list()
        for i in range(0, self.original_size):
            self.soldiers.append(copy.copy(soldier))

    # attempt to send the requested number of soldiers, but we might not have enough
    def supply_troops(self, number_of_soldiers):
        available_soldiers = list()
        for soldier in self.soldiers:
            if not soldier.fielded:
                available_soldiers.append(soldier)
        if len(available_soldiers) <= number_of_soldiers:
            self.depleted = True
        soldiers_sent = list()
        for i in range(0, number_of_soldiers):
            if i >= len(available_soldiers):
                return soldiers_sent or []
            available_soldiers[i].fielded = True
            soldiers_sent.append(available_soldiers[i])
        return soldiers_sent

