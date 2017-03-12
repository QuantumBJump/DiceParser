import random


class Dice:
    """
    A dice. That you can roll. Can have arbitrary objects sides.
    """
    def __init__(self, sides):
        """
        Instantiates a Dice object.

        Arguments:
        sides: Either the number of sides of the dice or
        a list of the sides of the dice. Each object in this can be
        anything (an str, a list of str, etc). If this is a list,
        then the sides of the dice are set to this list. If this is
        a number, then the sides are set to [1, 2, ... sides]
        """

        if isinstance(sides, list):
            self.sides = sides[:]
        elif isinstance(sides, int):
            self.sides = range(1, sides)
        else:
            raise TypeError('sides argument {} to Dice object should be a list or a number'
                            ' (is {})'.format(repr(sides), str(type(sides))))


    def __str__(self):
        """Returns a nice string representation of the object."""
        return '{}'.format(str(self.sides))

    def __repr__(self):
        """Returns a representation of the object."""
        return "\'{}\'".format(self.__str__())

    def roll(self):
        """Returns the result of a roll of the Dice."""

        return random.choice(self.sides)
