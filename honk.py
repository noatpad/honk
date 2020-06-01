
from sys import argv
from os import path
from ply import lex, yacc
import lexer, parser
from honkVM import honk

# Default variables
filename = "test.txt"
data = ''

# Take 0-1 arguments from command line
if len(argv) == 2:    # Pass a filename into the process
  filename = argv[1]
elif len(argv) > 2:
  raise Exception("Command only takes 0 or 1 argument (filename)!")

# Read file
try:
  with open(filename) as f:
    for line in f:
      data += line
except FileNotFoundError:
  raise Exception(f'{filename} does not exist!')

# Scan file
ducklexer = lex.lex(module=lexer)
ducklexer.input(data)

# Print tokens
# while True:
#   token = ducklexer.token()
#   if not token:
#     break
#   print(token)

# Parse file and build .o file
duckparser = yacc.yacc(module=parser)
resultQM = duckparser.parse(data)

# Read .o file
data = ''

try:
  with open('quack.o') as f:
    for line in f:
      data += line
except FileNotFoundError:
  raise Exception('quack.o does not exist!')

# Honk away
honk(data, True)
