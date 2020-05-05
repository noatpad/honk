
from ply import lex, yacc
import lexer, parser

# data = "1 + 2"
data = """
Programa hi;
var int : a, b;
int : c;

funcion void func()
var char : d;
{
  a = b + c;
  a = 1 + b;
}

principal() {
  a = 1 + 2;
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

print("# QUADS")
i = 1
for q in result.quads:
  print(f'{i} -> {q.operation} {q.operand_1} {q.operand_2} {q.result}')
  i += 1

print("# OPERANDS")
for op in result.operands: print(op)

print("# OPERATORS")
for op in result.operators: print(op)

# for func in result.directory:
#   print(f'{result.directory[func].name} -> {result.directory[func].returnType}')
#   table = result.directory[func].varTable
#   for var in table:
#     print(f'  {table[var].name} -> {table[var].vartype}')
