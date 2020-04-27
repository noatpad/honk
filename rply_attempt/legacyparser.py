
from rply import ParserGenerator

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
