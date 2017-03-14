#! /usr/bin/python3.4

# Import the various needed modules
import sys
import re
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("notation",
                    help="the notation for which dice to roll",
                    nargs='+')
args = parser.parse_args()

inputString = ' '.join(args.notation)
dicePat = re.compile(r'(\d+)d(\d+)')


def roll(number, sides):
    """
    Rolls number dice, each with sides sides, returns the sum of them all
    """
    total = 0
    for i in range(int(number)):
        result = random.randint(1, int(sides))
        total += result
    return total


def parse(toParse):
    """
    Parses a string for RPG dice notation, and also rolls this dice pool
    """
    parsedString = dicePat.search(toParse)
    diceNo, sides = parsedString.groups()
    print("Rolling " + diceNo + ' dice with ' + sides + ' sides each.')
    print("Result: " + str(roll(diceNo, sides)))


parse(inputString)
