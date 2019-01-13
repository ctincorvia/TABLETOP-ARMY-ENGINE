from army import *
from infantry import *
from squad import *


class Army:
    def __init__(self, name, horde, armies):
        self.name = name
        self.soldier_types = dict()
        self.squads = list()
        self.horde = horde
        armies[name] = self
        self.armies = armies

    def __str__(self):
        return self.name
    __repr__ = __str__

    def living_soldiers(self):
        all_soldiers = list()
        for squad in self.squads:
            all_soldiers.extend(squad.soldiers)
        return len(all_soldiers)

    def status(self):
        all_soldiers = list()
        for squad in self.squads:
            all_soldiers.extend(squad.soldiers)
        dead = 0
        reserves = 0
        for soldier in all_soldiers:
            if not soldier.fielded:
                reserves += 1
            if soldier.health <= 0:
                dead += 1
        print("Total soldiers: " + str(len(all_soldiers)))
        print("Total dead: " + str(dead))
        print("In reserve: " + str(reserves))

    def absorb_army(self, other_army):
        self.squads.extend(other_army.squads)
        other_army.squads.clear()

    def squad_statuses(self):
        for squad in self.squads:
            squad.report_status()

    def refresh(self):
        for squad in self.squads:
            squad.refresh()

    def add_soldier_type(self, name, armor, hp, attack_mod, damage_mod, num_attacks, face_value, defensive=0,
                         offensive=0):
        soldier = Infantry(name, armor, hp, attack_mod, damage_mod, num_attacks, face_value, defensive, offensive)
        self.soldier_types[soldier.name] = soldier

    def add_squad(self, name, soldier_type, size, priority):
        sq = Squad(name, self, priority, size, soldier_type)
        sq.refresh()
        self.squads.append(sq)

    def supply_troops(self, number_of_soldiers):
        lowest_priority = 9999999
        for sqd in self.squads:
            if not sqd.depleted and sqd.priority < lowest_priority:
                lowest_priority = sqd.priority
        deploying_squads = list()
        for sqd in self.squads:
            if sqd.priority == lowest_priority and not sqd.depleted:
                deploying_squads.append(sqd)
        if self.horde:
            deploying_troops = self.supply_horde(deploying_squads, number_of_soldiers)
        else:
            deploying_troops = self.supply_army(deploying_squads, number_of_soldiers)
        # return if we've fulfilled the request or we can't deploy any more troops
        if len(deploying_troops) == number_of_soldiers:
            return deploying_troops
        if len(deploying_troops) == 0:
            return deploying_troops
        else:
            # otherwise, look for lower priority troops to deploy
            additional_troops = self.supply_troops(number_of_soldiers - len(deploying_troops))
            deploying_troops.extend(additional_troops)
            return deploying_troops

    @staticmethod
    def supply_army(deploying_squads, number_of_troops):
        if len(deploying_squads) == 0:
            return []
        if number_of_troops == 0:
            return []
        supplied_troops = list()
        soldiers_per_squad = number_of_troops // len(deploying_squads)
        remainder = number_of_troops % len(deploying_squads)
        for squad in deploying_squads:
            new_troops = squad.supply_troops(soldiers_per_squad)
            supplied_troops.extend(new_troops)
        supplied_troops.extend(deploying_squads[0].supply_troops(remainder))
        if len(supplied_troops) == 0:
            print("")
        return supplied_troops

    def supply_horde(self, deploying_squads, number_of_troops):
        return self.supply_army(deploying_squads, number_of_troops)
