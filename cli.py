#! /usr/bin/env python3
"""Takes user input as a string and returns the result."""

import sys
import argparse
import parser

def format_report(report):
  """Nicely formats the report returned by parser.py.

  Args:
    report: list of tuples (string, list of ints), representing the text of a
      roll and the result of that roll.

  Returns:
    A nicely formatted string representation.
  """
  formatted_report = ""
  for roll in report:
    formatted_report += "\nRolling: {}\n\t{}".format(roll[0], roll[1])
  return formatted_report

def main():
  argparser = argparse.ArgumentParser(
    description='Calculate the result of a dice roll in dice notation')
  argparser.add_argument('notation',
                         metavar='notation',
                         help="""The notation for which dice to roll.
  If your notation contains parentheses, you must enclose it in single or double
  quotes (" or ')""",
                         nargs='*')
  args = argparser.parse_args()
  if len(sys.argv) >= 2:
    inputString = ' '.join(args.notation)
    report, result = parser.calculate(inputString)
    print(format_report(report))
    print(result)
  else:
    while True:
      try:
        inputString = input('roll> ')
      except EOFError:
        break
      if not inputString:
        sys.exit()

      result = parser.calculate(inputString)
      result.pretty_print()

if __name__ == '__main__':
  main()
