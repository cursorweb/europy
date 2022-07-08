from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from tokens import TType

from error.lf import LineInfo
from error.error import SyntaxError

SyntaxError(LineInfo('main.eo', 5, 6), 'you made an oopsie LMAO').display()