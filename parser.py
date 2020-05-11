
from collections import deque

from lexer import tokens
from funcDir import FunctionDirectory
from quads import Quads

""" State variables (accessible in `p` within each production)
- funcDir -> Function directory
- quads -> Quadruple handler
- currentType -> Currently-used type
- varDimensions -> Helper to determine number of dimensions when declaring a variable
"""

# Precedence rules for arithmetic
precedence = (
  ('left', '+', '-'),
  ('left', '*', '/')
)

# Parsing productions
# PROGRAMA
def p_programa(p):
  "programa : PROGRAMA found_program ID found_program_name ';' vars functions PRINCIPAL '(' ')' '{' body '}'"
  p[0] = p

def p_found_program(p):
  "found_program : empty"
  p.funcDir = FunctionDirectory()
  p.quads = Quads()

def p_found_program_name(p):
  'found_program_name : empty'
  p.funcDir.addFunction(p[-1], "void")
  p.funcDir.setGlobalFunction(p[-1])

# VARS
def p_vars(p):
  """vars : VAR found_var var_type
          | empty"""
  pass

def p_found_var(p):
  "found_var : empty"
  p.funcDir.createVarTable()

def p_var_type(p):
  """var_type : type ':' var_name ';' var_type
              | type ':' var_name ';'"""
  pass

def p_var_name(p):
  """var_name : variable p_found_var_name ',' var_name
              | variable p_found_var_name"""
  pass

def p_found_var_name(p):
  "p_found_var_name : empty"
  var = p[-1]
  if p.funcDir.varExists(var):
    s_error(p.lineno, p.lexpos, f'Variable "{var}" already exists!"')
  else:
    p.funcDir.addVar(var, (p.currentType, p.varDimensions))

def p_variable_mat(p):
  "variable : ID '[' NUMBER ']' '[' NUMBER ']'"
  p.varDimensions = 2
  p[0] = p[1]

def p_variable_list(p):
  "variable : ID '[' NUMBER ']'"
  p.varDimensions = 1
  p[0] = p[1]

def p_variable(p):
  "variable : ID"
  p.varDimensions = 0
  p[0] = p[1]

# TYPE
def p_type(p):
  """type : INT
          | FLOAT
          | CHAR
          | BOOL"""
  p.currentType = p[1]
  p[0] = p[1]

# FUNCTIONS
# TODO: Missing logic for functions parameters and their types
def p_functions(p):
  """functions : FUNCION func_type ID found_func_name '(' func_params ')' vars '{' body '}' found_func_end functions
               | empty"""
  pass

def p_func_type(p):
  """func_type : var_type
               | VOID"""
  if p[1] == 'void':
    p.currentType = 'void'

def p_found_func_name(p):
  "found_func_name : empty"
  func = p[-1]
  if p.funcDir.functionExists(func):
    s_error(p.lineno, p.lexpos, f'Function "{func}" already exists!"')
  else:
    p.funcDir.addFunction(func, p.currentType)
    p.funcDir.createVarTable()

def p_func_params(p):
  """func_params : func_param
                 | empty"""
  pass

def p_func_param(p):
  """func_param : var_type ID found_func_param ',' func_param
                | var_type ID found_func_param"""
  pass

def p_found_func_param(p):
  "found_func_param : empty"
  param = p[-1]
  if p.funcDir.varExists(param):
    s_error(p.lineno, p.lexpos, f'Multiple declaration of "{param}"!')
  else:
    p.funcDir.addVar(param, p.currentType)

def p_found_func_end(p):
  "found_func_end : empty"
  p.funcDir.deleteVarTable()

# BODY
# TODO: Missing functionality
def p_body(p):
  """body : statement body
          | statement"""
  pass

def p_statement(p):
  """statement : assignment
               | call_func
               | return
               | read
               | write
               | if
               | for
               | while"""
  pass

def p_assignment(p):
  "assignment : expr_var '=' found_expr_duo_op expr found_assignment_end ';'"
  pass

def p_found_assignment_end(p):
  "found_assignment_end : empty"
  p.quads.addAssignQuad()

# TODO: Missing logic for calling functions
def p_call_func(p):
  "call_func : ID '(' call_func_params ')' ';'"
  pass

def p_call_func_params(p):
  """call_func_params : call_func_param
                      | empty"""
  pass

def p_call_func_param(p):
  """call_func_param : expr ',' call_func_param
                     | expr"""
  pass

# TODO: Missing logic for return
def p_return(p):
  "return : REGRESA '(' expr ')' ';'"
  pass

# TODO: Missing logic for read
def p_read(p):
  "read : LEE '(' read_params ')' ';'"
  pass

def p_read_params(p):
  """read_params : expr_var ',' read_params
                 | expr_var"""
  pass

# TODO: Missing logic for write
def p_write(p):
  "write : ESCRIBE '(' write_params ')' ';'"
  pass

def p_write_params(p):
  """write_params : expr_var ',' write_params
                  | expr_var"""
  pass

# TODO: Missing logic for conditionals
def p_if(p):
  """if : SI '(' expr ')' ENTONCES '{' body '}'
        | SI '(' expr ')' ENTONCES '{' body '}' else"""
  pass

def p_else(p):
  "else : SINO '{' body '}'"
  pass

# TODO: Missing logic for 'for' loops
def p_for(p):
  "for : DESDE ID ':' expr HASTA expr HACER '{' body '}'"
  pass

# TODO: Missing logic for 'while' loops
def p_while(p):
  "while : MIENTRAS '(' expr ')' HAZ '{' body '}'"
  pass

def p_expr_duo(p):
  """expr : expr found_expr_duo_expr '+' found_expr_duo_op expr found_expr_duo_expr
          | expr found_expr_duo_expr '-' found_expr_duo_op expr found_expr_duo_expr
          | expr found_expr_duo_expr '*' found_expr_duo_op expr found_expr_duo_expr
          | expr found_expr_duo_expr '/' found_expr_duo_op expr found_expr_duo_expr"""
  pass

def p_found_expr_duo_op(p):
  "found_expr_duo_op : empty"
  p.quads.pushOperator(p[-1])

def p_found_expr_duo_expr(p):
  "found_expr_duo_expr : empty"
  p.quads.addDualOpQuad()

def p_expr_mono(p):
  """expr : '-' expr
          | '!' expr
          | '$' expr
          | '?' expr"""
  pass

def p_expr_group(p):
  "expr : '(' expr ')'"
  pass

def p_expr_num(p):
  "expr : NUMBER"
  p.quads.pushVar(p[1], ('int', 0))

def p_expr_var(p):
  "expr : expr_var"
  pass

def p_expr_var_mat_elem(p):
  "expr_var : ID '[' expr ']' '[' expr ']'"
  var = p.funcDir.getVar(p[1], 2)
  p.quads.pushVar(var.name, var.vartype)

def p_expr_var_list_elem(p):
  "expr_var : ID '[' expr ']'"
  var = p.funcDir.getVar(p[1], 1)
  p.quads.pushVar(var.name, var.vartype)

def p_expr_var_atom(p):
  "expr_var : ID"
  var = p.funcDir.getVar(p[1], 0)
  p.quads.pushVar(var.name, var.vartype)

def p_empty(p):
  "empty :"
  pass

# Error handling
def p_error(p):
  raise Exception(f'({p.lineno}:{p.lexpos}) Syntax error at "{p.value}"')

def s_error(lineno, lexpos, msg):
  raise Exception(f'({lineno}:{lexpos} - {msg}')
