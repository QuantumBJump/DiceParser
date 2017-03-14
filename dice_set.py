from dice import Dice


class ContainerEmptyError(Exception):
    """
    Raised whenever an operation is attempted on an empty container object
    which should only be attempted when the container is not empty
    """
    pass


class DiceSet:
    """
    A pool of dice. That can be rolled.
    """

    def __init__(self, dice=[]):
        """
        Instantiates the dice pool object.

        dice: A list of dice in the pool.
        """

        if not isinstance(dice, list):
            raise TypeError(
                'dice argument {} to DiceSet object should be a list, is {}'
                .format(str(dice), type(dice))
            )

        for d in dice:
            if not isinstance(d, Dice):
                raise TypeError(
                    'Element {} of dice argument to DiceSet object should be a Dice'
                    .format(str(d)))

        self.dice = dice

    def __repr__(self):
        return repr(self.dice)

    def __str__(self):
        return str(self.dice)

    def add_dice(self, dice):
        """Adds the dice to the pool. dice must be a Dice object"""

        if not isinstance(dice, Dice):
            raise TypeError('dice argument {} to add_dice() must be a Dice'
                            .format(str(dice)))

        self.dice.append(dice)

    def rem_dice(self, dice):
        """Removes one dice which is identical to the argument dice from the
        Dice Pool"""

        try:
            self.dice.remove(dice)
        except ValueError:
            raise ValueError('dice {} is not in the DiceSet, so can\'t be removed'
                             .format(str(dice)))

    def roll(self):
        """Returns a list of rolls of all the dice in the pool"""

        if not self.dice:
            raise ContainerEmptyError("DiceSet {} is empty, and can't be rolled"
                                      .format(str(self)))

        result = [die.roll() for die in self.dice]
        return result
