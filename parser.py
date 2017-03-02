#! /usr/bin/python3.4

# Import the various needed modules
import sys, re, random

if len(sys.argv) < 2:
    # they didn't add a string to be parsed
    if sys.argv[0] == 'parser.py':
        print("Usage: python parser.py [dice notation]")
        sys.exit()
    else:
        print("Usage: ./parser.py [dice notation]")
        sys.exit()

inputString = ' '.join(sys.argv[1:])
dicePat = re.compile(r'(\d+)d(\d+)')

def roll(number, sides):
    total = 0
    for i in range(int(number)):
        result = random.randint(1, int(sides))
        total += result
    return total

def parse(toParse):
    parsedString = dicePat.search(toParse)
    diceNo, sides = parsedString.groups()
    print("Rolling " + diceNo + ' dice with ' + sides + ' sides each.')
    print("Result: " + str(roll(diceNo, sides)))

parse(inputString)
