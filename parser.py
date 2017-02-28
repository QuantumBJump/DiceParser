#! /usr/bin/python3.4

# Import the various needed modules
import sys

if len(sys.argv) < 2:
    # they didn't add a string to be parsed
    if sys.argv[0] == 'parser.py':
        print("Usage: python parser.py [dice notation]")
        sys.exit()
    else:
        print("Usage: ./parser.py [dice notation]")
        sys.exit()

inputString = ' '.join(sys.argv[1:])
print(inputString)
