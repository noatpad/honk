
from rply import LexerGenerator

class Lexer:
  def __init__(self):
    self.lexer = LexerGenerator()

  def _setup_tokens(self):
    self.lexer.add("PROGRAMA", r"Programa")
    self.lexer.add("FUNCION", r"funcion")
    self.lexer.add("ENTONCES", r"entonces")
    self.lexer.add("HACER",r"hacer")
    self.lexer.add("PRINCIPAL",r"principal")
    self.lexer.add("VOID",r"void")
    self.lexer.add("SINO",r"sino")
    self.lexer.add("VAR",r"var")
    self.lexer.add("REGRESA",r"regresa")
    self.lexer.add("MIENTRAS",r"mientras")
    self.lexer.add("INT",r"int")
    self.lexer.add("LEE",r"lee")
    self.lexer.add("HAZ",r"haz")
    self.lexer.add("FLOAT",r"float")
    self.lexer.add("ESCRIBE",r"escribe")
    self.lexer.add("DESDE",r"desde")
    self.lexer.add("CHAR",r"char")
    self.lexer.add("SI",r"si")
    self.lexer.add("HASTA",r"hasta")

    self.lexer.add("NUMERO", r"\d+")
    self.lexer.add('PLUS', r'\+')
    self.lexer.add('MINUS', r'-')
    self.lexer.add('ID', r"[a-zA-Z_][a-zA-Z0-9_]*")

    self.lexer.add('=', r'=')
    self.lexer.add('==', r'==')
    self.lexer.add('!=', r'!=')
    self.lexer.add('>=', r'>=')
    self.lexer.add('<=', r'<=')
    self.lexer.add('>', r'>')
    self.lexer.add('<', r'<')
    self.lexer.add('(', r'\(')
    self.lexer.add(')', r'\)')
    self.lexer.add('[', r'\[')
    self.lexer.add(']', r'\]')
    self.lexer.add('{', r'\{')
    self.lexer.add('}', r'\}')
    self.lexer.add('|', r'\|')
    self.lexer.add('.', r'\.')
    self.lexer.add(',', r',')
    self.lexer.add(':', r':')
    self.lexer.add(';', r';')
    self.lexer.add('NEWLINE', r'\n')

    self.lexer.add('MUL', r'\*')
    self.lexer.add('DIV', r'/')
    self.lexer.add('MOD', r'%')
    self.lexer.add('MAT_DETERMINANTE', r'\$')
    self.lexer.add('MAT_TRANSPUESTA', r'¡')
    self.lexer.add('MAT_INVERSA', r'\?')

    self.lexer.ignore(r"\s+")   # Ignore whitespace

  def get_lexer(self):
    self._setup_tokens()
    return self.lexer.build()
