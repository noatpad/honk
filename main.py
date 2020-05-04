
from ply import lex, yacc
import lexer, parser

# data = "1 + 2"
data = """
Programa hi;
var int : a, b;
float : c;

principal() {
  a = 1 + 2
}
"""
# data = """
# 1 + 2 / 3
# """

ducklexer = lex.lex(module=lexer)
ducklexer.input(data)

while True:
  token = ducklexer.token()
  if not token:
    break
  print(token)

duckparser = yacc.yacc(module=parser)
result = duckparser.parse(data)
# print(result)

for func in result.directory:
  print(f'{result.directory[func].name} -> {result.directory[func].returnType}')
  a = result.directory[func].varTable
  for var in result.directory[func].varTable:
    print(f'  {a[var].name} -> {a[var].vartype} = {a[var].value}')
