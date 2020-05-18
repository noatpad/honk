
from ply import lex, yacc
from sys import argv
from os import path
import lexer, parser

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
while True:
  token = ducklexer.token()
  if not token:
    break
  print(token)

# Parse file
duckparser = yacc.yacc(module=parser)
result = duckparser.parse(data)

# Print quad list
print("# QUADS")
result.printQuads()
