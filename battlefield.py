from army import *


class Battlefield:
    def __init__(self, army1, army2, front):
        self.army1 = army1
        self.army2 = army2
        self.front_size = front
        self.front1 = set()
        self.front2 = set()
        self.round = 0
        self.fast_resolve = False
        self.low_details = True
        self.all_armies = army1.armies

    def diagnostics(self):
        self.front_status(self.front1, self.army1)
        self.army1.status()
        if not self.low_details:
            self.army1.squad_statuses()
        self.front_status(self.front2, self.army2)
        self.army2.status()
        if not self.low_details:
            self.army2.squad_statuses()

    def front_status(self, front, army):
        print("----------------------------")
        print(army.name + " battle lines:")
        if len(front) < self.front_size:
            print("Battle line broken!")
        # organize the front in to unit types so we can do diagnostics on them
        front_soldiers = dict()
        for soldier in front:
            if soldier.name in front_soldiers:
                front_soldiers[soldier.name].append(soldier)
            else:
                front_soldiers[soldier.name] = list([soldier])

        for key in front_soldiers.keys():
            soldiers = front_soldiers[key]
            number_of_soldiers = len(soldiers)
            current_health = 0
            max_health = 0
            kills = 0
            for soldier in soldiers:
                current_health += soldier.health
                max_health += soldier.max_health
                kills += soldier.kills
            strength = current_health / max_health * 100
            print(str(number_of_soldiers) + " " + soldiers[0].name + "s at " + str(strength) + "% strength and " + str(
                kills) + " kills")

    def fight_battle(self):
        victory_achieved = False
        while not victory_achieved:
            victory_condition = self.fight_round()
            if victory_condition != "CONTINUE":
                victory_achieved = True
                print(victory_condition)

    def fight_round(self):
        # remove all of the dead troops from the front lines
        self.clear_corpses()
        # fill in any holes in the front lines of either roster
        self.armies_advance()
        # Battle Report once the dust has cleared
        self.battle_report()
        # declare a winner if everybody's dead or a tie
        if self.declare_victory() != "CONTINUE":
            return self.declare_victory()
        # ATTACK
        self.armies_attack()
        return "CONTINUE"

    def armies_advance(self):
        # both armies will attempt to fill the front
        soldiers1 = self.army1.supply_troops(self.front_size - len(self.front1))
        for soldier in soldiers1:
            self.front1.add(soldier)
        soldiers2 = self.army2.supply_troops(self.front_size - len(self.front2))
        for soldier in soldiers2:
            self.front2.add(soldier)
        # if either army cannot create a full battle line, fill the space with the other amy (if possible)
        if len(self.front1) < self.front_size or len(self.front2) < self.front_size:
            # Ignore if neither army can fill the front
            if not (len(self.front1) < self.front_size and len(self.front2) < self.front_size):
                if len(self.front1) > len(self.front2):
                    for soldier in self.army1.supply_troops(self.front_size - len(self.front2)):
                        self.front1.add(soldier)
                else:
                    for soldier in self.army2.supply_troops(self.front_size - len(self.front1)):
                        self.front2.add(soldier)

    def armies_attack(self):
        if len(self.front1) > len(self.front2):
            bigger_army = list(self.front1)
            smaller_army = list(self.front2)
        else:
            bigger_army = list(self.front2)
            smaller_army = list(self.front1)
        self._armies_attack(bigger_army, smaller_army)
        self.apply_overkill_damage()

    @staticmethod
    def _armies_attack(bigger_army, smaller_army):
        # there's a limit to how surrounded a given group of units can be
        max_attacks = min(len(bigger_army), (len(smaller_army) * 2) + 6)
        small_index = 0
        for big_index in range(0, max_attacks):
            if small_index == len(smaller_army):
                small_index = 0
            bigger_army[big_index].fight(smaller_army[small_index])
            small_index += 1
        for index in range(0, len(smaller_army)):
            smaller_army[index].fight(bigger_army[index])

    def apply_overkill_damage(self):
        self._apply_overkill_damage(list(self.front1))
        self._apply_overkill_damage(list(self.front2))

    def _apply_overkill_damage(self, overkill_front):
        overkill_attacks = list()
        for soldier in overkill_front:
            if soldier.health < 0:
                overkill_attacks.append(soldier.health)
                # zero health so they're not marked for overkill in the next pass
                soldier.health = 0
        if len(overkill_attacks) == 0:
            return
        front_index = 0
        dead_soldiers = 0
        while len(overkill_attacks) > 0 and dead_soldiers < len(overkill_front):
            if front_index >= len(overkill_front):
                front_index = 0
                dead_soldiers = 0
            victim = overkill_front[front_index]
            # overkill damage is negative, so we have to add it for this to make sense
            if victim.health > 0:
                victim.health += overkill_attacks.pop()
            if victim.health < 1:
                dead_soldiers += 1
            front_index += 1
        # do this until all damage is resolved
        self._apply_overkill_damage(overkill_front)

    def clear_corpses(self):
        front1dead = set()
        front2dead = set()
        for soldier in self.front1:
            if soldier.health < 1:
                front1dead.add(soldier)
        for soldier in self.front2:
            if soldier.health < 1:
                front2dead.add(soldier)
        for soldier in front1dead:
            self.front1.remove(soldier)
        for soldier in front2dead:
            self.front2.remove(soldier)

    def declare_victory(self):
        if len(self.front1) == 0 and len(self.front2) == 0:
            self.force_report()
            return "\nTIE\n"
        if len(self.front1) == 0:
            self.force_report()
            return "\n" + (str(self.army2.name)) + " win!\n"
        if len(self.front2) == 0:
            self.force_report()
            return "\n" + (str(self.army1.name)) + " win!\n"
        return "CONTINUE"

    def force_report(self):
        if self.fast_resolve:
            self.fast_resolve = False
            self.battle_report(True)

    # round by round analysis down here
    def battle_report(self, final_report=False):
        if not self.fast_resolve:
            print("########## Round " + str(self.round) + " ##########")
            self.diagnostics()
            if not final_report:
                resolve = str(input("")).lower()
                if resolve == "resolve":
                    self.fast_resolve = True
                elif resolve == "more":
                    self.low_details = False
                elif resolve == "less":
                    self.low_details = True
                elif resolve == "":
                    pass
                else:
                    process_commands(resolve.split(), self.all_armies)
        self.round += 1


def process_commands(arguments, armies):

    for i in range(0, len(arguments)):
        arguments[i] = arguments[i].lower()
    argument_number = len(arguments)
    if argument_number == 2 and arguments[0] == "army":
        new_army = Army(arguments[1], False, armies)
        print("Army " + new_army.name + " created.")
        return
    if argument_number == 9 and arguments[0] in armies and arguments[1] == "unit":
        army = armies[arguments[0]]
        army.add_soldier_type(arguments[2], int(arguments[3]), int(arguments[4]), int(arguments[5]),
                              int(arguments[6]),
                              int(arguments[7]), int(arguments[8]))
        print("Unit type " + arguments[2] + " added to army " + army.name + ".")
        return
    if argument_number == 11 and arguments[0] in armies and arguments[1] == "unit":
        army = armies[arguments[0]]
        army.add_soldier_type(arguments[2], int(arguments[3]), int(arguments[4]), int(arguments[5]),
                              int(arguments[6]),
                              int(arguments[7]), int(arguments[8]), int(arguments[9]), int(arguments[10]))
        print("Unit type " + arguments[2] + " added to army " + army.name + ".")
        return
    if argument_number == 7 and arguments[2] == "squad":
        army = armies[arguments[0]]
        army.add_squad(arguments[3], arguments[4], int(arguments[5]), int(arguments[6]))
        print("Squad " + arguments[3] + " added to army " + army.name + ".")
        return
    if argument_number == 4 and arguments[0] in armies and arguments[2] in armies:
        army1 = armies[arguments[0]]
        army2 = armies[arguments[2]]
        battlefield = Battlefield(army1, army2, int(arguments[3]))
        battlefield.fight_battle()
        return
    if argument_number == 3 and arguments[0] in armies and arguments[2] in armies and arguments[1] == "absorb":
        army1 = armies[arguments[0]]
        army2 = armies[arguments[2]]
        army1.absorb_army(army2)
        print(army1.name + " absorbed " + army2.name)
        return
    if argument_number == 2 and arguments[1] in armies and arguments[0] == "refresh":
        army = armies[arguments[1]]
        army.refresh()
        print(army.name + " refreshed.")
        return
    if argument_number == 2 and arguments[0] in armies and arguments[1] == "status":
        army = armies[arguments[0]]
        army.squad_statuses()
        return

    print("")
    print("I don't know that command or the army/unit doesn't exist. Double check the instructions and try again.\n")