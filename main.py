from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from tokens import TType

from error import EoError

lexer = Lexer.from_file('test/playground.eo')

try:
    tokens = lexer.run()
    for token in lexer.run():
        print(token.ttype, f"{token.data!r}" if token.data else '')
except EoError as e:
    e.display()