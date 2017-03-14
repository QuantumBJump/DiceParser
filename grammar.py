#! /usr/bin/python3.5
from pyparsing import *
import pprint

operand = OneOrMore(Word(nums))
operator = Word("*-/+", exact=1)
modifier = Literal("rr") + operand | Literal("k") + operand + Literal('h') | Literal('k') + operand + Literal('l')
#roll = operand + CaselessLiteral('d') + operand
#statement = Group(roll) + ZeroOrMore(Group(operator + operand)) + ZeroOrMore(Group(modifier))
#sentence = statement + ZeroOrMore(Group(operator + statement))

roll = Group(Group(operand + CaselessLiteral('d') + operand) + ZeroOrMore(Group(modifier)))
expr = infixNotation(roll | operand,
        [('-', 1, opAssoc.RIGHT),
        ('/', 2, opAssoc.LEFT),
        ('*', 2, opAssoc.LEFT),
        ('+', 2, opAssoc.LEFT),
        ('-', 2, opAssoc.LEFT)])



result = expr.parseString('5d8 k3h + 4 - 3d6')
print(result)
