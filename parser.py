
from collections import deque
from lexer import tokens
from funcDir import FunctionDirectory
from quadruple import Quadruple
from semanticCube import getBinopResultType

""" State variables (accessible in `p` within each production)
- funcDir -> Function directory
- currentType -> Currently-used type
- varDimensions -> Helper to determine number of dimensions when declaring a variable

- pOps -> Stack of operands
- pOpers -> Stack of operators
- pTypes -> Stack of vartypes
- quads -> Queue of Quadruples
- tempCount -> Temporary variable count
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
  p.sOps = deque()
  p.sOpers = deque()
  p.sTypes = deque()
  p.quads = deque()
  p.tempCount = 0

def p_found_program_name(p):
  'found_program_name : empty'
  p.funcDir.addFunction(p[-1], "void")
  p.funcDir.setGlobalFuncton(p[-1])

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
# TODO: Still buggy
def p_body(p):
  """body : statement body
          | statement"""
  pass

def p_statement(p):
  """statement : assignment"""

# ASSIGN
def p_assignment(p):
  "assignment : expr_var '=' found_binop_op expr found_binop_assign ';'"
  pass

def p_found_binop_assign(p):
  "found_binop_assign : empty"
  if p.sOpers and p.sOpers[-1] == '=':
    right_op = p.sOps.pop()
    right_type = p.sTypes.pop()
    left_op = p.sOps.pop()
    left_type = p.sTypes.pop()
    operator = p.sOpers.pop()

    result_type = getBinopResultType(left_type, right_type, operator)
    if result_type:
      result = 't' + str(p.tempCount)
      p.quads.append(Quadruple(operator, left_op, right_op, result))
      p.sOps.append(result)
      p.sTypes.append(result_type)
      print(f'{operator} {left_op} {right_op} {result}')
      p.tempCount += 1
    else:
      s_error(p.lineno, p.lexpos, f'Type mismatch! -> {left_type} {operator} {right_type}')

# EXPR
def p_expr_binop(p):
  """expr : expr '+' found_binop_op expr
          | expr '-' found_binop_op expr
          | expr '*' found_binop_op expr
          | expr '/' found_binop_op expr"""
  pass

def p_found_binop(p):
  "found_binop_op : empty"
  p.sOpers.append(p[-1])

def p_found_binop_expr(p):
  "found_binop_expr : empty"
  if p.sOpers and p.sOpers[-1] in "+-*/":
    right_op = p.sOps.pop()
    right_type = p.sTypes.pop()
    left_op = p.sOps.pop()
    left_type = p.sTypes.pop()
    operator = p.sOpers.pop()

    result_type = getBinopResultType(left_type, right_type, operator)
    if result_type:
      result = 't' + str(p.tempCount)
      p.quads.append(Quadruple(operator, left_op, right_op, result))
      p.sOps.append(result)
      p.sTypes.append(result_type)
      print(f'{operator} {left_op} {right_op} {result}')
      p.tempCount += 1
    else:
      s_error(p.lineno, p.lexpos, f'Type mismatch! -> {left_type} {operator} {right_type}')

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
  "expr : NUMBER found_binop_expr"
  p.sOps.append(p[1])
  p.sTypes.append(('int', 0))

def p_expr_var(p):
  "expr : expr_var found_binop_expr"
  pass

def p_expr_var_mat_elem(p):
  "expr_var : ID '[' NUMBER ']' '[' NUMBER ']'"
  var = p.funcDir.getVar(p[1], 2)
  p.sOps.append(var.name)
  p.sTypes.append(var.vartype)

def p_expr_var_list_elem(p):
  "expr_var : ID '[' NUMBER ']'"
  var = p.funcDir.getVar(p[1], 1)
  p.sOps.append(var.name)
  p.sTypes.append(var.vartype)

def p_expr_var_atom(p):
  "expr_var : ID"
  var = p.funcDir.getVar(p[1], 0)
  p.sOps.append(var.name)
  p.sTypes.append(var.vartype)

def p_empty(p):
  "empty :"
  pass

# Error handling
def p_error(p):
  raise Exception(f'({p.lineno}:{p.lexpos}) Syntax error at "{p.value}"')

def s_error(lineno, lexpos, msg):
  raise Exception(f'({lineno}:{lexpos} - {msg}')
