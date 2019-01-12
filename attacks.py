import random
import sys


def attack_roll(modifier, advantage=0):
    return roll(1, 20, modifier, advantage)


def damage_roll(dice, face, modifier):
    return roll(dice, face, modifier)


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
    return str(result)


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
    print("")


