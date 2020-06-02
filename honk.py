
import config
from sys import argv
from os import path
import argparse
from ply import lex, yacc

# CLI Arguments
cli = argparse.ArgumentParser(description='h o n k')
cli.add_argument('-t', '--tokens', help='Print tokens', action='store_true')
cli.add_argument('-p', '--parser', help='Enable debug info for parsing', action='store_true')
cli.add_argument('-v', '--vm', help='Enable debug info for virtual machine', action='store_true')
cli.add_argument('file', help='Specify a file to run through')
args = cli.parse_args()

# Set configuration before importing lexer and parser
filepath = path.splitext(args.file)
config.objFilename = filepath[0]
config.debugParser = args.parser

# Import the brains and machines
if filepath[1] == '.honk':
  import lexhonker as lexer, parshonker as parser
else:
  import lexer, parser

from honkVM import honk

# Read file
data = ''
try:
  with open(args.file) as f:
    for line in f:
      data += line
except FileNotFoundError:
  raise Exception(f'{args.file} does not exist!')

# Scan file
ducklexer = lex.lex(module=lexer)
ducklexer.input(data)

# Print tokens when allowed
if args.tokens:
  while True:
    token = ducklexer.token()
    if not token:
      break
    print(token)

# Parse file and build .o file)
duckparser = yacc.yacc(module=parser)
resultQM = duckparser.parse(data)

# Read .o file
data = ''

try:
  with open(f'{config.objFilename}.o') as f:
    for line in f:
      data += line
except FileNotFoundError:
  raise Exception(f'{config.objFilename}.o does not exist!')

# Honk away
honk(data, args.vm)
