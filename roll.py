#! /usr/bin/env python3
"""Takes user input as a string and parses it as the result
of a dice roll."""

import sys
from roller import Roller

#####################
#		LEXER		#
#####################

# Token types
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ROLL, EOF = (
	'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'ROLL', 'EOF'
	)

class Token(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __str__(self):
		"""String representation of the class instance

		Examples:
			Token(INTEGER, 3)
			Token(MUL, '*')
			Token(ROLL, 15)
		"""
		return 'Token({type}, {value})'.format(
			type=self.type,
			value=repr(self.value)
			)

	def __repr__(self):
		return self.__str__()


class Lexer(object):