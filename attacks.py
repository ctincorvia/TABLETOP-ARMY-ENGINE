import random
import sys

ATTACK_STAT = 5
PROFICIENCY = 3
TO_HIT = ATTACK_STAT + PROFICIENCY
HUMANOID_BONUS = 2

horde = dict()
character = dict()

terms = {
        "humanoid": True,
        "h": True,
        "human": True,
        "nonhumanoid": False,
        "nonhuman": False,
        "n": False,
        "advantage": 1,
        "a": 1,
        "disadvantage": -1,
        "d": -1,
        "swing": "swing",
        "s": "swing",
        "t": "throw",
        "throw": "throw",
        "regular": 0,
        "r": 0,
        "spikes": "spikes",
        "spike growth": "spikes",
        "fireball": "fireball",
        "fb": "fireball",
        "lb": "fireball",
        "lightningbolt": "fireball",
        "attack": "attack",
        "horde": "horde",
        "program_horde": "program_horde",
        "program_character": "program_character"
    }


# swing, number of attacks, human, optional advantage
def process_commands(commandSet):
    if not commandSet[0] in terms:
        return
    if terms[commandSet[0]] == "swing":
        rakan_melee_attacks(int(commandSet[1]), terms[commandSet[2]], terms[commandSet[3]])
    if terms[commandSet[0]] == "throw":
        rakan_ranged_attacks(int(commandSet[1]), terms[commandSet[2]], terms[commandSet[3]])
    if terms[commandSet[0]] == "program_horde":
        program_horde(int(commandSet[1]), int(commandSet[2]), int(commandSet[3]), int(commandSet[4]))
    if terms[commandSet[0]] == "horde":
        horde_attacks(int(commandSet[1]), int(commandSet[2]), terms[commandSet[3]])
    if terms[commandSet[0]] == "program_character":
        program_attacks(int(commandSet[1]), int(commandSet[2]), int(commandSet[3]), int(commandSet[4]))
    if terms[commandSet[0]] == "attack":
        generic_attacks(terms[commandSet[1]])
    if terms[commandSet[0]] == "spikes":
        spike_growth(int(commandSet[1]))
    if terms[commandSet[0]] == "fireball":
        fireball()


# advantage is 1, nothing is 0, disadvantage is -1
def rakan_melee_attacks(attacks, humanoid, advantage=0):
    # attack rolls
    to_hit_list = list()
    damage_list = list()
    magic_bonus = 1
    humanoid_bonus = 0
    if humanoid:
        humanoid_bonus = HUMANOID_BONUS

    if advantage == 1:
        _dice = 1
        to_hit_list.append(attack_roll(TO_HIT + magic_bonus, 0))
        if to_hit_list[-1] == "C!":
            _dice = 2
        damage_list.append(damage_roll(_dice, 8, ATTACK_STAT + humanoid_bonus + magic_bonus))
        to_hit_list.append(attack_roll(TO_HIT + magic_bonus, 0))
        _dice = 1
        if to_hit_list[-1] == "C!":
            _dice = 2
        damage_list.append(damage_roll(_dice, 8, ATTACK_STAT + humanoid_bonus + magic_bonus))
        attacks = attacks - 1

    for i in range(0, attacks):
        _dice = 1
        # if rakan makes at least 3 attacks, the last one isn't with Crake
        if attacks > 2 and attacks == i-1:
            magic_bonus = 0;
        to_hit_list.append(attack_roll(TO_HIT + magic_bonus, advantage))
        if to_hit_list[i] == "C!":
            _dice = 2
        damage_list.append(damage_roll(_dice, 8, ATTACK_STAT + humanoid_bonus + magic_bonus))
    print_uniform_list(to_hit_list)
    print_uniform_list(damage_list)


def rakan_ranged_attacks(attacks, humanoid, advantage=0):
    # attack rolls
    crake_attacks = 2
    to_hit_list = list()
    damage_list = list()
    magic_bonus = 1
    humanoid_bonus = 0
    if humanoid:
        humanoid_bonus = HUMANOID_BONUS

    # handle Rakan's advantage mechanics
    if advantage == 1:
        _dice = 1
        to_hit_list.append(attack_roll(TO_HIT + magic_bonus, 0))
        if to_hit_list[-1] == "C!":
            _dice = 2
        damage_list.append(damage_roll(_dice, 8, ATTACK_STAT + humanoid_bonus + magic_bonus))
        to_hit_list.append(attack_roll(TO_HIT + magic_bonus, 0))
        _dice = 1
        if to_hit_list[-1] == "C!":
            _dice = 2
        damage_list.append(damage_roll(_dice, 8, ATTACK_STAT + humanoid_bonus + magic_bonus))
        attacks = attacks - 1
        crake_attacks = crake_attacks - 2

    for i in range(0, attacks):
        _dice = 1
        face = 8
        if crake_attacks < 1:
            face = 6
            magic_bonus = 0
        to_hit_list.append(attack_roll(TO_HIT + magic_bonus, advantage))
        if to_hit_list[i] == "C!":
            _dice = 2
        damage_list.append(damage_roll(_dice, face, ATTACK_STAT + humanoid_bonus + magic_bonus))
        crake_attacks = crake_attacks - 1
    print_uniform_list(to_hit_list)
    print_uniform_list(damage_list)


# a generic attack macro without rakan's special stuff
def program_attacks(attacks, attack_stat, to_hit, face):
    character["attacks"] = attacks
    character["attack_stat"] = attack_stat
    character["to_hit"] = to_hit
    character["face"] = face


def generic_attacks(advantage=0):
    to_hit_list = list()
    damage_list = list()
    for i in range(0, character["attacks"]):
        _dice = 1
        face = character["face"]
        to_hit_list.append(attack_roll(character["to_hit"], advantage))
        if to_hit_list[i] == "C!":
            _dice = 2
        damage_list.append(damage_roll(_dice, face, character["attack_stat"]))
    print_uniform_list(to_hit_list)
    print_uniform_list(damage_list)


def program_horde(attacks, attack_stat, to_hit, face):
    horde["attacks"] = attacks
    horde["attack_stat"] = attack_stat
    horde["to_hit"] = to_hit
    horde["face"] = face


def horde_attacks(horde_size, ac, advantage):
    hits = 0
    crits = 0
    damage = 0
    for j in range(0, horde_size):
        for i in range(0, horde["attacks"]):
            _dice = 1
            face = horde["face"]
            roll = attack_roll(horde["to_hit"], advantage)
            if (roll != "F!") and (roll == "C!" or int(roll) >= ac):
                hits += 1
                if roll == "C!":
                    crits += 1
                    _dice = 2
                damage += int(damage_roll(_dice, face, horde["attack_stat"]))
    print ("Hits: " + str(hits))
    print ("Critical hits: " + str(crits))
    print ("Total damage: " + str(damage))


def attack_roll(modifier, advantage=0):
    return roll(1, 20, modifier, advantage)


def damage_roll(dice, face, modifier):
    return roll(dice, face, modifier)


def attack_roll_rakan(modifier, advantage=0):
    return roll_rakan(1, 20, modifier, advantage)


def damage_roll_rakan(dice, face, modifier):
    return roll_rakan(dice, face, modifier)


def roll_rakan(dice, face, modifier, advantage=0):
    roll1 = roll_helper_rakan(dice, face, modifier)
    roll2 = roll_helper_rakan(dice, face, modifier)
    result = ""
    if advantage == 0:
        result = roll1
    elif advantage == 1:
        result = max(roll1, roll2)
    elif advantage == -1:
        result = min(roll1, roll2)
    if face == 20 and result == face + modifier:
        result = "C!"
    if face == 20 and result == 1 + modifier:
        result = "F!"
    return str(result)


def roll(dice, face, modifier, advantage=0):
    roll1 = roll_helper(dice, face, modifier)
    roll2 = roll_helper(dice, face, modifier)
    result = ""
    if advantage == 0:
        result = roll1
    elif advantage > 0:
        result = max(roll1, roll2)
    elif advantage < 0:
        result = min(roll1, roll2)
    if face == 20 and result == face + modifier:
        result = "C!"
    if face == 20 and result == 1 + modifier:
        result = "F!"
    return str(result)


def roll_helper_rakan(dice, face, modifier):
    face_sum = 0
    for i in range(0,dice):
        face_value = random.randint(1, face);
        if (face == 6 or face == 8) and face_value == 1:
            face_value = random.randint(1, face);
        face_sum = face_sum + face_value
    return face_sum + modifier


def roll_helper(dice, face, modifier):
    face_sum = 0
    for i in range(0,dice):
        face_value = random.randint(1, face);
        face_sum = face_sum + face_value
    return face_sum + modifier


def print_uniform_list(raw_list):
    sys.stdout.write("|  ")
    for i in range(0, len(raw_list)):
        concat = ""
        if len(str(raw_list[i])) == 1:
            concat = " "
        sys.stdout.write(str(raw_list[i]) + concat + "  |  ")
    print ("")


def spike_growth(feet):
    d4s = (feet / 5) * 2
    print (damage_roll(d4s, 4, 0))


def fireball():
    print (damage_roll(8, 6, 0))


if __name__ == "__main__":
    while True:
        commands = input("Throw/Swing, # of attacks, Humanoid/Nonhuman, Advantage/Disadvantage \n"
                             "or use spell then parameters \n")
        commandSet = commands.split(" ")
        process_commands(commandSet)


