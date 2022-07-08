from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from tokens import TType

from error.lf import LineInfo
from error import EoError

lexer = Lexer.from_repl('{{ ')

try:
    lexer.run()
except EoError as e:
    e.display()