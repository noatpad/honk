
from ply import lex, yacc
import lexer, parser

# TODO: Add file reading
data = """
Programa hi;
var
  int : a, b;
  float : f;
  int : c;

funcion void func()
var char : d;
{
  a = b + c;
  a = 1 + b;
}

principal() {
  a = (1 + 2) * 3;

  si (a > 3) entonces {
    b = 5 * 2;
  } sino {
    f = 5 / 2;
  }

  mientras (a > 3) haz {
    a = a - 1;
  }
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
