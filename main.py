
from lexer import DuckLexer

# data = "1 + 2"
data = """
Programa hi;

principal() {
  a = 1 + 2 + 3
  si (b <= 8) entonces { lee(5); }
}
"""

# data = """
# 1 + 2 / 3
# """

lexer = DuckLexer()
lexer.build()
lexer.test(data)

# parser.parse(l.lex(testString))
