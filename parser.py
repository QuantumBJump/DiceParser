#! /usr/bin/env python3

# Import the various needed modules
import sys
import re
import random
import argparse
import dice
import dice_set

def parse(toParse):
    """
    Parses a string for RPG dice notation, and also rolls this dice pool
    """
    dicePat = re.compile(r'(\d+)[d|D](\d+)')
    parsedString = dicePat.search(toParse)
    diceNo, sides = parsedString.groups()
    print("Rolling " + diceNo + ' dice with ' + sides + ' sides each.')
    # print("Result: " + str(roll(diceNo, sides)))

    sides = int(sides)
    diceNo = int(diceNo)

    diceList = [dice.Dice(sides) for i in range(diceNo)]

    dicePool = dice_set.DiceSet(diceList)
    result = dicePool.roll()
    print('{sum}: {result}'.format(sum=sum(result), result=result))


def roll(number, sides):
    """
    Rolls number dice, each with sides sides, returns the sum of them all
    """
    total = 0
    for i in range(int(number)):
        result = random.randint(1, int(sides))
        total += result
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notation",
                        help="the notation for which dice to roll",
                        nargs='+')
    args = parser.parse_args()

    inputString = ' '.join(args.notation)

    parse(inputString)

if __name__ == '__main__':
    main()
