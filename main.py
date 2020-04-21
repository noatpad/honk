
from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox

# ----- LEXER -----

lg = LexerGenerator()
lg.add("PROGRAMA", r"Programa")
lg.add("FUNCION", r"funcion")
lg.add("ENTONCES", r"entonces")
lg.add("HACER",r"hacer")
lg.add("PRINCIPAL",r"principal")
lg.add("VOID",r"void")
lg.add("SINO",r"sino")
lg.add("VAR",r"var")
lg.add("REGRESA",r"regresa")
lg.add("MIENTRAS",r"mientras")
lg.add("INT",r"int")
lg.add("LEE",r"lee")
lg.add("HAZ",r"haz")
lg.add("FLOAT",r"float")
lg.add("ESCRIBE",r"escribe")
lg.add("DESDE",r"desde")
lg.add("CHAR",r"char")
lg.add("SI",r"si")
lg.add("HASTA",r"hasta")

lg.add("NUMERO", r"\d+")
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('ID', r"[a-zA-Z_][a-zA-Z0-9_]*")

lg.add('=', r'=')
lg.add('==', r'==')
lg.add('!=', r'!=')
lg.add('>=', r'>=')
lg.add('<=', r'<=')
lg.add('>', r'>')
lg.add('<', r'<')
lg.add('=', r'=')
lg.add('(', r'\(')
lg.add(')', r'\)')
lg.add('[', r'\[')
lg.add(']', r'\]')
lg.add('{', r'\{')
lg.add('}', r'\}')
lg.add('|', r'\|')
lg.add('.', r'\.')
lg.add(',', r',')
lg.add(':', r':')
lg.add(';', r';')
lg.add('NEWLINE', r'\n')

lg.add('MUL', r'\*')
lg.add('DIV', r'/')
lg.add('MOD', r'%')
lg.add('MAT_DETERMINANTE', r'\$')
lg.add('MAT_TRANSPUESTA', r'¡')
lg.add('MAT_INVERSA', r'\?')

lg.ignore(r"\s+")   # Ignore whitespace

l = lg.build()

# ----- PARSER -----

pg = ParserGenerator(
    ['PROGRAMA','FUNCION','ENTONCES','HACER','PRINCIPAL','VOID',
     'SINO','VAR','REGRESA','MIENTRAS','INT','FLOAT','CHAR',
     'LEE','HAZ','ESCRIBE','DESDE','SI',
     'HASTA','NUMERO','PLUS','MINUS','ID','(',')'
     ,'NEWLINE','=','==','!=','>=','<=','>','<','[',']','{','}'
     ,'|',',','.',':', ';','MUL','DIV','MOD'
     ,'MAT_DETERMINANTE','MAT_TRANSPUESTA','MAT_INVERSA']
     #todo, poner precedencia
)

dirFuncs = []

# TODO: Figure out how to make certain expressions optional

@pg.production("program : PROGRAMA ID ; vars functions PRINCIPAL ( ) { body }")
@pg.production("program : PROGRAMA ID ; vars PRINCIPAL ( ) { body }")
@pg.production("program : PROGRAMA ID ; functions PRINCIPAL ( ) { body }")
@pg.production("program : PROGRAMA ID ; PRINCIPAL ( ) { body }")
def expr_program(p):
  dirFuncs.append(funDir("global","void",[]))

# TODO: Implement arrays and matrixes
# TODO: Implement multiple variable declaration
@pg.production("vars : type : ID vars'")
def expr_vars(p):
  pass

@pg.production("vars' : , ID vars'")
def expr_vars2(p):
  pass

@pg.production("type : INT")
@pg.production("type : FLOAT")
@pg.production("type : CHAR")
def expr_type(p):
  pass

# TODO: Implement parameters
# TODO: Implement local variables
@pg.production("functions : FUNCION type ID ( ) { body }")
def expr_functions(p):
  pass

@pg.production("body : expr")
def expr_body(p):
  pass

@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
def expr_pm(p):
  lhs = p[0]
  op = p[1].gettokentype()
  rhs = p[2]

  if op == "PLUS":
    print(lhs + rhs)
    return lhs + rhs
  elif op == "MINUS":
    print(lhs - rhs)
    return lhs - rhs

@pg.production("expr : NUMERO")
def expr_num(p):
    return int(p[0].getstr())

# Error handling
@pg.error
def err_handler(token):
  raise ValueError("ERROR: %s -> Type: %s" % (token.getstr(), token.gettokentype()))

parser = pg.build()

class funDir:
  def __init__(self,nombre,tipo,variables):
    self.nombre = nombre
    self.tipo = tipo
    self.variables = variables


class varTable:
  def __init__(self,nombre,tipo,valor):
    self.nombre = nombre
    self.tipo = tipo
    self.valor = valor

# ----- MAIN -----

# testString = "1 + 2"
testString = """
Programa hi;

principal() {
  1 + 2 + 3
}
"""

for token in l.lex(testString):
  print(token)

parser.parse(l.lex(testString))
