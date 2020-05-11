
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
  a = (1 + 2) * 3;
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
result.quads.printQuads()
