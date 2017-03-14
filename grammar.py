#! /usr/bin/python3.5
from pyparsing import *


operand = OneOrMore(Word(nums))
operator = Word("*-/+", exact=1)
modifier = Literal("rr") + operand | Literal("k") + operand + Literal('h') | Literal('k') + operand + Literal('l')
roll = operand + CaselessLiteral('d') + operand
statement = Group(roll) + ZeroOrMore(Group(operator + operand)) + ZeroOrMore(Group(modifier))
sentence = statement + ZeroOrMore(Group(operator + statement))

result = sentence.parseString('5d8 + 4 k3h - 3d6')
print(result)
