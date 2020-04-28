
from lexer import tokens
from funcDir import FunctionDirectory

# TODO: Add semantic actions for function declarations and local variables

""" State variables (accessible in `p` within each production)
- funcDir -> Function directory
- currentType -> Currently-used type
"""

# Precedence rules for arithmetic
precedence = (
  ('left', '+', '-'),
  ('left', '*', '/')
)

# Parsing productions
def p_programa(p):
  "programa : PROGRAMA found_program ID found_program_name ';' vars functions PRINCIPAL '(' ')' '{' body '}'"
  p[0] = p.funcDir

def p_found_program(p):
  "found_program :"
  p.funcDir = FunctionDirectory()

def p_found_program_name(p):
  'found_program_name :'
  p.funcDir.addFunction(p[-1], "void")

def p_vars(p):
  """vars : VAR found_var var_type
          | empty"""
  pass

def p_found_var(p):
  "found_var :"
  p.funcDir.addVarTable()

def p_var_type(p):
  """var_type : type ':' var_declare ';' var_type
              | type ':' var_declare ';'"""
  pass

def p_var_declare(p):
  """var_declare : variable p_found_var_declare ',' var_declare
                 | variable p_found_var_declare"""
  pass

def p_found_var_declare(p):
  "p_found_var_declare :"
  var = p[-1]
  if p.funcDir.findVar(var):
    s_error(p.lineno, p.lexpos, f'Variable "{var}" already exists!"')
  else:
    p.funcDir.addVar(var, p.currentType)

def p_variable(p):
  """variable : ID '[' expr ']' '[' expr ']'
              | ID '[' expr ']'
              | ID"""
  p[0] = p[1]

def p_type(p):
  """type : INT
          | FLOAT
          | CHAR"""
  p.currentType = p[1]
  p[0] = p[1]

def p_functions(p):
  """functions : func
               | empty"""
  pass

def p_func(p):
  """func : FUNCION func_type ID '(' params ')' vars '{' body '}'
          | FUNCION func_type ID '(' ')' vars '{' body '}'"""
  pass

def p_func_type(p):
  """func_type : var_type
                | VOID"""
  pass

def p_params(p):
  """params : var_type ID ',' params
            | var_type ID"""
  pass

def p_body(p):
  "body : assignment"
  pass

def p_assignment(p):
  "assignment : variable '=' expr"
  pass

def p_expr_binop(p):
  """expr : expr '+' expr
          | expr '-' expr
          | expr '*' expr
          | expr '/' expr"""
  pass

def p_expr_group(p):
  "expr : '(' expr ')'"
  pass

def p_expr_num(p):
  "expr : NUMBER"
  pass

def p_expr_var_elem(p):
  "expr : ID '[' NUMBER ']'"
  pass

def p_expr_var(p):
  "expr : ID"
  pass

def p_empty(p):
  "empty :"
  pass

def p_error(p):
  raise Exception(f'({p.lineno}:{p.lexpos}) Syntax error at "{p.value}"')

def s_error(lineno, lexpos, msg):
  raise Exception(f'({lineno}:{lexpos} - {msg}')
