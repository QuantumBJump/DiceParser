#! /usr/bin/env python3
"""Takes user input as a string and parses it as the result
of a dice roll."""

import sys
import re
import argparse
import roller

#####################
#       LEXER       #
#####################

# Token types
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ROLL, EOF = ('INTEGER', 'PLUS',
                                                             'MINUS', 'MUL',
                                                             'DIV', '(', ')',
                                                             'ROLL', 'EOF')



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
        type=self.type, value=repr(self.value))

  def __repr__(self):
    return self.__str__()


class Lexer(object):

  def __init__(self, text):
    self.text = text
    self.pos = 0
    self.current_char = self.text[self.pos]

  def error(self):
    raise Exception('Invalid character')

  def advance(self):
    """Advance 'pos' and set 'current_char'"""
    self.pos += 1
    if self.pos > len(self.text) - 1:
      self.current_char = None  # Indicates end of input
    else:
      self.current_char = self.text[self.pos]

  def skip_whitespace(self):
    """Ignore any number of whitespaces and progress to the next
    non-space character
    """
    while self.current_char is not None and self.current_char.isspace():
      self.advance()

  def introll(self):
    """Return either a (multidigit) integer consumed from the input, or a 
    string representing a dice roll
    """
    result = ''
    # pattern:
    #   [number]d[number] followed by any number of modifiers
    # modifiers:
    #   k[number][h|H|l|L]
    #   rr[number]
    pattern = re.compile(r'\d+[d|D]\d+(\s+(k\d+[h|H|l|L]|rr\d+))*')
    match = pattern.match(self.text[self.pos:])
    if match:  # matched the regex, this is a roll
      result = match.string[match.start():match.end()]
      for i in range(len(result)):
        self.advance()
      return Token(ROLL, result)
    else:  # didn't match the regex, therefore it's an integer
      while self.current_char is not None and self.current_char.isdigit():
        result += self.current_char
        self.advance()
      return Token(INTEGER, int(result))

  def get_next_token(self):
    """Lexical analyser (aka scanner/tokeniser)

    Responsible for splitting the input apart into tokens, one token
    at a time.
    """
    while self.current_char is not None:

      if self.current_char.isspace():
        self.skip_whitespace()
        continue

      if self.current_char.isdigit():
        return self.introll()

      if self.current_char == '+':
        self.advance()
        return Token(PLUS, '+')

      if self.current_char == '-':
        self.advance()
        return Token(MINUS, '-')

      if self.current_char == '*':
        self.advance()
        return Token(MUL, '*')

      if self.current_char == '/':
        self.advance()
        return Token(DIV, '/')

      if self.current_char == '(':
        self.advance()
        return Token(LPAREN, '(')

      if self.current_char == ')':
        self.advance()
        return Token(RPAREN, ')')

      self.error()

    return Token(EOF, None)


######################
#       PARSER       #
######################


class AST(object):
  pass


class BinOp(AST):

  def __init__(self, left, op, right):
    self.left = left
    self.token = self.op = op
    self.right = right


class UnaryOp(AST):

  def __init__(self, op, expr):
    self.token = self.op = op
    self.expr = expr


class Num(AST):

  def __init__(self, token):
    self.token = token
    self.value = token.value


class Roll(AST):

  def __init__(self, token):
    self.token = token
    self.roll = roller.Roll(token.value)
    self.value = self.roll.get_value()


class Parser(object):

  def __init__(self, lexer):
    self.lexer = lexer
    #set current token to first token taken from input
    self.current_token = self.lexer.get_next_token()

  def error(self):
    raise Exception('Invalid syntax')

  def eat(self, token_type):
    # compares current token type to passed token type.
    # if they match, 'eats' current token and moves forward
    # in file. If not, throws a tantrum.
    if self.current_token.type == token_type:
      # that was tasty, give me another
      self.current_token = self.lexer.get_next_token()
    else:  # eww, bad token
      self.error()

  def factor(self):
    """factor: (PLUS|MINUS) factor | INTEGER | LPAREN expr RPAREN | ROLL"""
    token = self.current_token  # what am I looking at
    if token.type == PLUS:
      self.eat(PLUS)
      node = UnaryOp(token, self.factor())
      return node
    elif token.type == MINUS:
      self.eat(MINUS)
      node = UnaryOp(token, self.factor())
    elif token.type == INTEGER:
      self.eat(INTEGER)
      return Num(token)
    elif token.type == ROLL:
      self.eat(ROLL)
      return Roll(token)
    elif token.type == LPAREN:
      self.eat(LPAREN)
      node = self.expr()
      self.eat(RPAREN)
      return node

  def term(self):
    """term: factor ((MUL | DIV) factor)*"""
    node = self.factor()

    while self.current_token.type in (MUL, DIV):
      token = self.current_token
      if token.type == MUL:
        self.eat(MUL)
      elif token.type == DIV:
        self.eat(DIV)

      node = BinOp(left=node, op=token, right=self.factor())
    return node

  def expr(self):
    """
    expr    : term ((PLUS | MINUS) term)*
    term    : factor ((MUL | DIV) factor)*
    factor  : (PLUS|MINUS)factor | INTEGER | LPAREN expr RPAREN | ROLL
    """
    node = self.term()

    while self.current_token.type in (PLUS, MINUS):
      token = self.current_token
      if token.type == PLUS:
        self.eat(PLUS)
      elif token.type == MINUS:
        self.eat(MINUS)

      node = BinOp(left=node, op=token, right=self.term())

    return node

  def parse(self):
    return self.expr()


###########################
#       INTERPRETER       #
###########################


class NodeVisitor(object):

  def visit(self, node):
    method_name = 'visit_' + type(node).__name__
    visitor = getattr(self, method_name, self.generic_visit)
    return visitor(node)

  def generic_visit(self, node):
    raise Exception('no visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):

  def __init__(self, parser):
    self.parser = parser
    self.rolls = []
    self.report = []

  def visit_BinOp(self, node):
    if node.op.type == PLUS:
      return self.visit(node.left) + self.visit(node.right)
    if node.op.type == MINUS:
      return self.visit(node.left) - self.visit(node.right)
    if node.op.type == MUL:
      return self.visit(node.left) * self.visit(node.right)
    if node.op.type == DIV:
      return self.visit(node.left) // self.visit(node.right)

  def visit_UnaryOp(self, node):
    op = node.op.type
    if op == PLUS:
      return +self.visit(node.expr)
    elif op == MINUS:
      return -self.visit(node.expr)

  def visit_Num(self, node):
    return node.value

  def visit_Roll(self, node):
    self.rolls.append(node.roll)
    self.report.append((node.roll.text, node.roll.results))
    return node.value

  def interpret(self, tree=None):
    if tree is None:
      tree = self.parser.parse()
    result = self.visit(tree)
    return self.rolls, self.report, result


class Result(object):

  def __init__(self, text):
    self.text = text
    self.lexer = Lexer(self.text)
    self.parser = Parser(self.lexer)
    self.interpreter = Interpreter(self.parser)
    self.rolls, self.report, self.result = self.interpreter.interpret()
    self._gen_repr()

  def _gen_repr(self):
    self.repr = self.text
    for roll in self.rolls:
      self.repr = self.repr.replace(roll.text, str(roll.value), 1)

  def pretty_print(self):
    print(self.text)
    for roll in self.rolls:
      print("Rolling: {}\n\t{}".format(roll.text, roll.results))
    print(self.repr)
    print("Result: {}".format(self.result))

def calculate(text):
  return Result(text)
