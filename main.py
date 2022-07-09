from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from tokens import TType

from error.lf import LineInfo
from error import EoError

lexer = Lexer.from_repl('''
use io;
var a = 2 + 2; // sets a
io.println(a);
''')

try:
    for token in lexer.run():
        print(token.ttype, f"{token.data!r}" if token.data else '')
except EoError as e:
    e.display()