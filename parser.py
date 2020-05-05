
from collections import deque

from lexer import tokens
from funcDir import FunctionDirectory
from quadruple import Quadruple
from semanticCube import getDuoResultType

""" State variables (accessible in `p` within each production)
- funcDir -> Function directory
- currentType -> Currently-used type
- varDimensions -> Helper to determine number of dimensions when declaring a variable

- operands -> Stack of operands
- operators -> Stack of operators
- types -> Stack of vartypes
- quads -> Queue of Quadruples
- tempCount -> Temporary variable count
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
  p.operands = deque()
  p.operators = deque()
  p.types = deque()
  p.quads = deque()
  p.tempCount = 0

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

def p_func_params2(p):
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
  "statement : assignment"""
  pass

def p_assignment(p):
  "assignment : expr_var '=' found_expr_duo_op expr found_assignment_end ';'"
  pass

def p_found_assignment_end(p):
  "found_assignment_end : empty"
  right_op = p.operands.pop()
  right_type = p.types.pop()
  left_op = p.operands.pop()
  left_type = p.types.pop()
  operator = p.operators.pop()

  result_type = getDuoResultType(left_type, right_type, operator)
  if result_type:
    result = 't' + str(p.tempCount)
    p.quads.append(Quadruple(operator, left_op, right_op, result))
    p.operands.append(result)
    p.types.append(result_type)
    p.tempCount += 1

def p_expr_duo(p):
  """expr : expr found_expr_duo_expr '+' found_expr_duo_op expr found_expr_duo_expr
          | expr found_expr_duo_expr '-' found_expr_duo_op expr found_expr_duo_expr
          | expr found_expr_duo_expr '*' found_expr_duo_op expr found_expr_duo_expr
          | expr found_expr_duo_expr '/' found_expr_duo_op expr found_expr_duo_expr"""
  pass

def p_found_expr_duo_op(p):
  "found_expr_duo_op : empty"
  p.operators.append(p[-1])

def p_found_expr_duo_expr(p):
  "found_expr_duo_expr : empty"
  if p.operators and p.operators[-1] in "+-*/":
    right_op = p.operands.pop()
    right_type = p.types.pop()
    left_op = p.operands.pop()
    left_type = p.types.pop()
    operator = p.operators.pop()

    result_type = getDuoResultType(left_type, right_type, operator)
    if result_type:
      result = 't' + str(p.tempCount)
      p.quads.append(Quadruple(operator, left_op, right_op, result))
      p.operands.append(result)
      p.types.append(result_type)
      p.tempCount += 1

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
  p.operands.append(p[1])
  p.types.append(('int', 0))

def p_expr_var(p):
  "expr : expr_var"
  pass

def p_expr_var_mat_elem(p):
  "expr_var : ID '[' expr ']' '[' expr ']'"
  var = p.funcDir.getVar(p[1], 2)
  p.operands.append(var.name)
  p.types.append(var.vartype)

def p_expr_var_list_elem(p):
  "expr_var : ID '[' expr ']'"
  var = p.funcDir.getVar(p[1], 1)
  p.operands.append(var.name)
  p.types.append(var.vartype)

def p_expr_var_atom(p):
  "expr_var : ID"
  var = p.funcDir.getVar(p[1], 0)
  p.operands.append(var.name)
  p.types.append(var.vartype)

def p_empty(p):
  "empty :"
  pass

# Error handling
def p_error(p):
  raise Exception(f'({p.lineno}:{p.lexpos}) Syntax error at "{p.value}"')

def s_error(lineno, lexpos, msg):
  raise Exception(f'({lineno}:{lexpos} - {msg}')
