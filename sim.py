import attacks
import copy

armies = dict()


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
        for soldier in self.army1.supply_troops(self.front_size - len(self.front1)):
            self.front1.add(soldier)
        for soldier in self.army2.supply_troops(self.front_size - len(self.front2)):
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

    # I feel like this isn't working correctly
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
                    process_commands(resolve.split())
        self.round += 1


class Army:
    def __init__(self, name, horde):
        self.name = name
        self.soldier_types = dict()
        self.squads = list()
        self.horde = horde
        armies[name] = self

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

    def set_defenses(self, offensive, defensive):
        for sqd in self.squads:
            sqd.set_defenses(offensive, defensive)

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
        if len(deploying_troops) == number_of_soldiers or len(deploying_troops) == 0:
            return deploying_troops or []
        else:
            # otherwise, look for lower priority troops to deploy
            return deploying_troops.extend(self.supply_troops(number_of_soldiers - len(deploying_troops))) or []

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
        return supplied_troops or []

    def supply_horde(self, deploying_squads, number_of_troops):
        return self.supply_army(deploying_squads, number_of_troops)


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

    def set_defenses(self, offensive, defensive):
        for soldier in self.soldiers:
            soldier.set_defenses(offensive, defensive)

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
        return soldiers_sent or []


class Infantry:
    def __init__(self, name, armor, hp, attack_mod, damage_mod, num_attacks, face_value, defensive=0, offensive=0):
        self.name = name
        self.health = hp
        self.max_health = copy.copy(hp)
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


testarmy = Army("Dwarves", False)
testarmy2 = Army("d2", False)
testarmy.add_soldier_type("Ironbreaker", 21, 59, 7, 4, 2, 8, 1, 0)
testarmy.add_squad("Ironbreakers", "Ironbreaker", 60, 1)
testarmy2.add_soldier_type("Hammer", 18, 59, 8, 5, 2, 13, 0, 0)
testarmy2.add_squad("Hammers", "Hammer", 60, 1)
testhorde = Army("UndeadHorde", True)
testhorde.add_soldier_type("Zombie", 8, 22, 4, 2, 1, 6)
testhorde.add_soldier_type("Doom Skeleton", 14, 11, 20, 2, 1, 8)
testhorde.add_squad("Zombies", "Zombie", 120, 1)
testhorde.add_squad("Doom Skeletons", "Doom Skeleton", 120, 1)
armies["dwarves"] = testarmy
armies["undead"] = testhorde


def process_commands(arguments):
    try:
        for i in range(0, len(arguments)):
            arguments[i] = arguments[i].lower()
        argument_number = len(arguments)
        if argument_number == 2 and arguments[0] == "army":
            new_army = Army(arguments[1], False)
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
    except:
        print("")
    print("I don't know that command or the army/unit doesn't exist. Double check the instructions and try again.\n")


while True:
    command = input("Names must be one word only\n"
                    "Create an army using army [army name]\n"
                    "Add a unit type to an army with [army] unit [unit name] [AC] [HP] [TO-HIT] [DAMAGE MOD] [ATTACKS] [DIE VALUE]\n"
                    "Create a squad of units and add them to an army with [army] add squad [squad name] [unit_name] [unit count] [unit priority]\n"
                    "Start a battle with '[army1] battle [army2] [front width]'\n\n")
    cmd_arguments = command.split(" ")
    process_commands(cmd_arguments)
