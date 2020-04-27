
from ply import lex

class DuckLexer():
  # Reserved words
  reserved = {
    'Programa': 'PROGRAMA',
    'principal': 'PRINCIPAL',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'funcion': 'FUNCION',
    'void': 'VOID',
    'regresa': 'REGRESA',
    'lee': 'LEE',
    'escribe': 'ESCRIBE',
    'si': 'SI',
    'entonces': 'ENTONCES',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'haz': 'HAZ',
    'desde': 'DESDE',
    'hasta': 'HASTA',
    'hacer': 'HACER'
  }

  # Token list
  tokens = [
    'ID', 'NUMBER',
    # 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
    # 'MAT_DETERMINANT', 'MAT_TRANSPOSE', 'MAT_INVERSE',
    'COMMENT',
    'IS_EQUAL', 'IS_NOT_EQUAL', 'LESS_THAN_OR_EQUAL', 'MORE_THAN_OR_EQUAL'
  ] + list(reserved.values())

  # literals = "=<>()[]{}|.,:;"
  literals = "+-*/%$¡?=<>()[]{}|.,:;"

  # Simple tokens
  # t_PLUS = r'\+'
  # t_MINUS = r'-'
  # t_MUL = r'\*'
  # t_DIV = r'/'
  # t_MOD = r'%'
  # t_MAT_DETERMINANT = r'\$'
  # t_MAT_TRANSPOSE = r'¡'
  # t_MAT_INVERSE = r'\?'
  t_IS_EQUAL = r'=='
  t_IS_NOT_EQUAL = r'!='
  t_LESS_THAN_OR_EQUAL = r'<='
  t_MORE_THAN_OR_EQUAL = r'>='

  # Function tokens
  def t_ID(self, t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = self.reserved.get(t.value, 'ID')
    return t

  def t_NUMBER(self, t):
    r'\d+'
    t.value = int(t.value)
    return t

  # Ignored characters and tokens
  t_ignore = ' \t'
  t_ignore_COMMENT = r'%%.*'

  # Track line number
  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)

  # Error handling
  def t_error(self, t):
    raise Exception(f'({t.lineno}:{t.lexpos}) Illegal character! -> {t.value[0]}')
    # print('Illegal character! -> "%s"' % t.value[0])
    # t.lexer.skip(1)

  # Build lexer
  def build(self, **kwargs):
    self.lexer = lex.lex(module=self, **kwargs)

  # Tokenize input and print them
  def test(self, data):
    # Feed input to lexer
    self.lexer.input(data)

    # Each token prints its type, value, line number, & line position
    while True:
      token = self.lexer.token()
      if not token:
        break
      print(token)
