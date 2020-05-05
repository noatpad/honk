
from lexer import tokens
from funcDir import FunctionDirectory

""" State variables (accessible in `p` within each production)
- funcDir -> Function directory
- currentType -> Currently-used type
- varDimensions -> Helper to determine number of dimensions when declaring a variable
"""

# Precedence rules for arithmetic
precedence = (
  ('left', '+', '-'),
  ('left', '*', '/'),
  ('right', '-', '$', '!', '?')
)

# Parsing productions
# PROGRAMA
def p_programa(p):
  "programa : PROGRAMA found_program ID found_program_name ';' vars functions PRINCIPAL '(' ')' '{' body '}'"
  p[0] = p.funcDir

def p_found_program(p):
  "found_program : empty"
  p.funcDir = FunctionDirectory()

def p_found_program_name(p):
  'found_program_name :'
  p.funcDir.addFunction(p[-1], "void")

# VARS
def p_vars(p):
  """vars : VAR found_var var_type
          | empty"""
  pass

def p_found_var(p):
  "found_var : empty"
  p.funcDir.addVarTable()

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
  if p.funcDir.findVar(var):
    s_error(p.lineno, p.lexpos, f'Variable "{var}" already exists!"')
  else:
    p.funcDir.addVar(var, (p.currentType, p.varDimensions))

def p_variable_mat(p):
  "variable : ID '[' expr ']' '[' expr ']'"
  p.varDimensions = 2
  p[0] = p[1]

def p_variable_list(p):
  "variable : ID '[' expr ']'"
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
  if p.funcDir.findFunction(func):
    s_error(p.lineno, p.lexpos, f'Function "{func}" already exists!"')
  else:
    p.funcDir.addFunction(func, p.currentType)
    p.funcDir.addVarTable()

def p_func_params(p):
  """func_params : func_params2
                 | empty"""
  pass

def p_func_params2(p):
  """func_params2 : var_type ID found_func_param ',' func_params2
                  | var_type ID found_func_param"""
  pass

def p_found_func_param(p):
  "found_func_param : empty"
  param = p[-1]
  if p.funcDir.findVar(param):
    s_error(p.lineno, p.lexpos, f'Multiple declaration of "{param}"!')
  else:
    p.funcDir.addVar(param, p.currentType)

def p_found_func_end(p):
  "found_func_end : empty"
  p.funcDir.deleteVarTable()

# BODY
# TODO: Change to statements
def p_body(p):
  """body : statement body
          | statement"""
  pass

def p_statement(p):
  """statement : assignment"""

# ASSIGN
def p_assignment(p):
  "assignment : variable '=' expr"
  pass

# EXPR
def p_expr_binop(p):
  """expr : expr '+' expr
          | expr '-' expr
          | expr '*' expr
          | expr '/' expr"""
  pass

def p_expr_uop(p):
  """expr : '-' expr
          | '$' expr
          | '!' expr
          | '?' expr"""
  pass

def p_expr_group(p):
  "expr : '(' expr ')'"
  pass

def p_expr_num(p):
  "expr : NUMBER"
  pass

def p_expr_var(p):
  """expr : ID
          | ID '[' NUMBER ']'
          | ID '[' NUMBER ']' '[' NUMBER ']'"""
  pass

def p_empty(p):
  "empty :"
  pass

# Error handling
def p_error(p):
  raise Exception(f'({p.lineno}:{p.lexpos}) Syntax error at "{p.value}"')

def s_error(lineno, lexpos, msg):
  raise Exception(f'({lineno}:{lexpos} - {msg}')
