#! /usr/bin/env python3
"""Classes designed to take in a string of the form

[x]d[y] (modifier)*

and return an integer total"""

import re
import random


class Roller(object):

  def __init__(self, text=None):
    if text == None:
      self.number = 1
      self.sides = 1
      self.modifiers = []
    else:
      self.inputs = text.split(' ')
      self.number, self.sides = re.split('d|D', self.inputs[0])
      self.number = int(self.number)
      self.sides = int(self.sides)
      self.modifiers = self.inputs[1:]

  def roll(self, sides):
    """Rolls a die with 'sides' sides"""
    return random.randint(1, sides)

  def rolls(self, number, sides):
    """Rolls 'number' dice with 'sides' sides"""
    results = []
    for i in range(number):
      results.append(self.roll(sides))
    return results

  def reroll(self, rolls_in, number, sides):
    """Takes in a list of results, a number below which to reroll,
        and the number of sides of each die, and returns a list
        where low numbers have been rerolled."""
    result = rolls_in[:]
    for i in range(len(result)):
      if result[i] <= number:
        result[i] = self.roll(sides)
    return result

  def keep(self, rolls_in, number, end):
    """Takes in a list of results, a number of results to keep, and
        a side from which to start, and returns a smaller list."""
    if end == 'l' or end == 'L':
      result = sorted(rolls_in)
    elif end == 'h' or end == 'H':
      result = sorted(rolls_in, reverse=True)
    else:
      raise Exception('Keep() received invalid argument')

    result = result[:number]
    return result

  def total(self, rolls_in):
    """Takes in a list of rolls, totals them and returns that"""
    result = 0
    for i in range(len(rolls_in)):
      result += rolls_in[i]
    return result

  def evaluate(self, text=None):
    if text is not None:
      self.inputs = text.split(' ')
      self.number, self.sides = re.split('d|D', self.inputs[0])
      self.number = int(self.number)
      self.sides = int(self.sides)
      self.modifiers = self.inputs[1:]

    roll_results = self.rolls(self.number, self.sides)

    if self.modifiers != []:
      for i in range(len(self.modifiers)):
        if self.modifiers[i][0] == 'k':
          roll_results = self.keep(roll_results,
                                   int(self.modifiers[i][1:-1]),
                                   self.modifiers[i][-1])
        elif self.modifiers[i][0:2] == 'rr':
          roll_results = self.reroll(roll_results,
                                     int(self.modifiers[i][2:]), self.sides)

    total = self.total(roll_results)
    print(text + ': ')
    print(roll_results)
    return total


class Roll(object):

  def __init__(self, text=None):
    """
    Initialises the roll object.

    Starts out with a 0 value and no rolls.
    Args:
      text: a text representation of the roll. Defaults to 1d6
    """
    self.text = text
    if text is not None:
      self.inputs = text.split(' ')
      self.number, self.sides = re.split('d|D', self.inputs[0])
      self.number = int(self.number)
      self.sides = int(self.sides)
      self.modifiers = self.inputs[1:]
    else:
      self.number = 1
      self.sides = 6
      self.modifiers = []

    self.results, self.value = self._generate_results()

  def _single_roll(self):
    """Rolls a single die of x sides.

    Returns:
      int - result of the roll
    """
    return random.randint(1, self.sides)

  def _multi_roll(self):
    """Rolls several dice with a given number of sides.
    Returns:
      list of ints - the results of the roll
    """
    results = []
    for i in range(self.number):
      results.append(self._single_roll())
    return results

  def _modifier_keep(self, rolls_in, number, end):
    """Keeps a certain number of the highest or lowest results.

    Args:
      rolls_in: list of rolls to modify
      number: number of rolls to keep
      end: which end of the results to keep (H|h|L|l)

    Returns:
      list of ints - results after modification
    """
    if end == 'l' or end == 'L':
      result = sorted(rolls_in)
    elif end == 'h' or end == 'H':
      result = sorted(rolls_in, reverse=True)
    else:
      raise Exception("_modifier_keep() received invalid argument.")
    result = result[:number]
    return result

  def _modifier_reroll(self, rolls_in, number):
    """Rerolls all results below a certain number.

    Args:
      rolls_in: list of rolls to modify
      number: number below which to reroll

    Returns:
      list of ints - results after modification
    """
    result = rolls_in[:]
    for roll in result:
      if roll <= number:
        roll = self._single_roll(self.sides)
    return result

  def _total(self, rolls_in):
    """Returns the sum of integers in a list."""
    total = 0
    for roll in rolls_in:
      total += roll
    return total

  def get_value(self):
    """Returns the value of the roll.

    Returns:
      int - value of roll.
    """
    return self.value

  def get_rolls(self):
    """Returns the results of each individual dice roll.

    Returns:
      list of ints - the results of each die.
    """
    return self.results

  def _generate_results(self):
    """Generates a set of rolls based on the parameters of the roll.

    Returns:
      (results, value)
    """
    results = self._multi_roll()
    for modifier in self.modifiers:
      if modifier[0] == 'k':
        results = self._modifier_keep(results, int(modifier[1:-1]),
                                           modifier[-1])
      elif modifier[:2] == 'rr':
        self.results = self._modifier_reroll(results, int(modifier[2:]))
    value = self._total(results)
    return results, value
