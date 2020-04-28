
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
  print(f'{func.name} -> {func.returnType}')
  for var in func.varTable:
    print(f'  {var.name} -> {var.vartype} = {var.value}')
