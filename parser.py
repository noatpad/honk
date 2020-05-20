
from collections import deque

from lexer import tokens
from functionDirectory import FunctionDirectory
from quadManager import QuadManager

# For debugging purposes
debug = True

funcDir = FunctionDirectory(debug)
quads = QuadManager(funcDir, debug)

# Precedence rules for arithmetic
precedence = (
  ('left', '|'),
  ('left', '&'),
  ('left', 'IS_EQUAL', 'IS_NOT_EQUAL', '<', 'LESS_THAN_OR_EQUAL', '>', 'MORE_THAN_OR_EQUAL'),
  ('left', '+', '-'),
  ('left', '*', '/', '%')
)

# Parsing productions
# PROGRAMA
def p_programa(p):
  "programa : PROGRAMA ID found_program_name ';' vars functions main '(' ')' '{' body '}'"
  quads.addEndQuad()
  quads.debugStep()
  p[0] = quads

# Make a GOTO quad to main()
def p_found_program_name(p):
  'found_program_name : empty'
  if quads.debug:
      print("\n|==|==|==|==|==|==|==|==| START DEBUG LOG |==|==|==|==|==|==|==|==|\n")

  funcDir.addFunction('global')
  funcDir.setGlobalFunction()
  quads.addMainQuad()

# VARS
def p_vars(p):
  """vars : VAR found_var var_declare
          | empty"""
  pass

def p_found_var(p):
  "found_var : empty"
  funcDir.createVarTable()

def p_var_declare(p):
  """var_declare : type ':' var_name ';' var_declare
                 | type ':' var_name ';'"""
  pass

def p_var_name(p):
  """var_name : variable_declare var_dims ',' var_name
              | variable_declare var_dims"""
  pass

def p_variable_declare(p):
  "variable_declare : ID"
  var = p[1]
  if funcDir.varAvailable(var):
    funcDir.addVar(var[0], quads.vDir.generateVirtualAddress(funcDir.currentFunc, funcDir.currentType))
    funcDir.setVarHelper(var)
  else:
    s_error(f'Variable "{var}" already exists!"')

def p_var_no_dims(p):
  "var_dims : empty"
  pass

def p_var_dims(p):
  """var_dims : dim dim
              | dim"""
  if len(p) == 3:
    p[0] = p[1] * p[2]
    funcDir.setMDimToVar(funcDir.varHelper, [p[2], 1])
  else:
    p[0] = p[1]
    funcDir.setMDimToVar(funcDir.varHelper, [1])

  quads.vDir.makeSpaceForArray(funcDir.currentFunc, funcDir.currentType, p[0] - 1)


def p_var_dim(p):
  "dim : '[' CTE_INT ']'"
  funcDir.addDimensionToVar(funcDir.varHelper, p[2])
  p[0] = p[2]

# TYPE
def p_type(p):
  """type : INT
          | FLOAT
          | CHAR
          | BOOL"""
  funcDir.setCurrentType(p[1])
  p[0] = p[1]

# FUNCTIONS
# TODO: Recursion?
def p_functions(p):
  """functions : FUNCION func_type ID found_func_name '(' func_params ')' vars found_func_start '{' body '}' found_func_end functions
               | empty"""
  pass

def p_func_type(p):
  """func_type : type
               | VOID"""
  if p[1] == 'void':
    funcDir.setCurrentType('void')

def p_found_func_name(p):
  "found_func_name : empty"
  func = p[-1]
  if funcDir.functionExists(func):
    s_error(f'Function "{func}" already exists!"')
  else:
    funcDir.addFunction(func)
    funcDir.createVarTable()

def p_func_params(p):
  """func_params : func_param
                 | empty"""
  pass

def p_func_param(p):
  """func_param : type ID found_func_param ',' func_param
                | type ID found_func_param"""
  pass

def p_found_func_param(p):
  "found_func_param : empty"
  param = p[-1]
  if funcDir.varAvailable(param):
    funcDir.addVar(param[0], quads.vDir.generateVirtualAddress(funcDir.currentFunc, funcDir.currentType))
    funcDir.addFuncParam()
  else:
    s_error(f'Multiple declaration of "{param}"!')

def p_found_func_start(p):
  "found_func_start : empty"
  funcDir.setQuadStart(quads.getQuadCount())

def p_found_func_end(p):
  "found_func_end : empty"
  funcDir.deleteVarTable()
  quads.addEndFuncQuad()

# PRINCIPAL
def p_principal(p):
  "main : PRINCIPAL"
  quads.completeMainQuad()

# BODY
def p_body(p):
  """body : statement body
          | empty"""
  pass

def p_statement(p):
  """statement : assignment
               | call_func
               | return
               | read
               | print
               | if
               | for
               | while"""
  pass

## ASSIGNMENT
def p_assignment(p):
  "assignment : expr_var '=' found_expr_duo_op expr found_assignment_end ';'"
  pass

def p_found_assignment_end(p):
  "found_assignment_end : empty"
  quads.addAssignQuad()

## RETURN
def p_return(p):
  "return : REGRESA '(' expr ')' ';'"
  quads.addReturnQuad()

## READ
def p_read(p):
  "read : LEE '(' read_params ')' ';'"
  pass

def p_read_params(p):
  """read_params : expr_var found_read_param ',' read_params
                 | expr_var found_read_param"""
  pass

def p_found_read_param(p):
  "found_read_param : empty"
  quads.addReadQuad()

## PRINT
def p_print(p):
  "print : ESCRIBE '(' print_params ')' ';'"
  pass

def p_print_params(p):
  """print_params : print_param ',' print_params
                  | print_param"""
  pass

def p_print_param(p):
  "print_param : expr"
  quads.addPrintQuad(False)

def p_print_string(p):
  "print_param : STRING"
  quads.addPrintQuad(p[1])

## IF
def p_if(p):
  """if : SI '(' expr ')' found_if_expr ENTONCES '{' body '}'
        | SI '(' expr ')' found_if_expr ENTONCES '{' body '}' else"""
  quads.completeIfQuad()

def p_found_if_expr(p):
  "found_if_expr : empty"
  quads.addIfQuad()

## ELSE
def p_else(p):
  "else : SINO found_else '{' body '}'"
  pass

def p_found_else(p):
  "found_else : empty"
  quads.addElseQuad()

## FOR
# TODO: Add constant 1 to constants table
def p_for(p):
  "for : DESDE ID found_for_iterator ':' expr found_for_start HASTA expr found_for_cond HACER '{' body '}'"
  quads.pushVar(quads.getTopOperand(), quads.getTopType())
  quads.pushVar(quads.getTopOperand(), quads.getTopType())
  quads.pushVar(1, 'int')
  quads.pushOperator('=')
  quads.pushOperator('+')
  quads.addDualOpQuad(['+'])
  quads.addAssignQuad()
  quads.completeLoopQuad()
  quads.popOperand()
  quads.popType()

def p_found_for_iterator(p):
  "found_for_iterator : empty"
  var = p[-1]
  if not funcDir.varExists(var):
    funcDir.setCurrentType('int')
    funcDir.addVar(var, quads.vDir.generateVirtualAddress('temp', 'int'))
    quads.pushVar(var, 'int')
    quads.pushVar(var, 'int')
    quads.pushVar(var, 'int')
  else:
    s_error(f'Variable "{var}" already exists!"')

def p_found_for_start(p):
  "found_for_start : empty"
  quads.pushOperator('=')
  quads.addAssignQuad()
  quads.prepareLoop()

def p_found_for_cond(p):
  "found_for_cond : empty"
  quads.pushOperator('<=')
  quads.addDualOpQuad(['<='])
  quads.addLoopCondQuad()

## WHILE
def p_while(p):
  "while : MIENTRAS found_while '(' expr ')' found_while_expr HAZ '{' body '}'"
  quads.completeLoopQuad()

def p_found_while(p):
  "found_while : empty"
  quads.prepareLoop()

def p_found_while_expr(p):
  "found_while_expr : empty"
  quads.addLoopCondQuad()

# EXPRESSION -> Order of operator precedence:
# - Factors (*, /, %)
# - Arithmetic (+, -)
# - Comparison (==, !=, <, <=, >, >=)
# - Logic (&, |)
def p_expr(p):
  "expr : expr_logic"
  pass

def p_expr_logic(p):
  "expr_logic : expr_compare found_expr_logic expr_logic2"
  pass

def p_expr_logic2(p):
  """expr_logic2 : '&' found_expr_duo_op expr_logic
                 | '|' found_expr_duo_op expr_logic
                 | empty"""
  pass

def p_found_expr_logic(p):
  "found_expr_logic : empty"
  quads.addDualOpQuad(['&', '|'])

def p_expr_compare(p):
  "expr_compare : expr_arith found_expr_compare expr_compare2"
  pass

def p_expr_compare2(p):
  """expr_compare2 : IS_EQUAL found_expr_duo_op expr_compare
                   | IS_NOT_EQUAL found_expr_duo_op expr_compare
                   | '<' found_expr_duo_op expr_compare
                   | LESS_THAN_OR_EQUAL found_expr_duo_op expr_compare
                   | '>' found_expr_duo_op expr_compare
                   | MORE_THAN_OR_EQUAL found_expr_duo_op expr_compare
                   | empty"""
  pass

def p_found_expr_compare(p):
  "found_expr_compare : empty"
  quads.addDualOpQuad(['==', '!=', '<', '<=', '>', '>='])

def p_expr_arith(p):
  "expr_arith : expr_factor found_expr_arith expr_arith2"
  pass

def p_expr_arith2(p):
  """expr_arith2 : '+' found_expr_duo_op expr_arith
                 | '-' found_expr_duo_op expr_arith
                 | empty"""
  pass

def p_found_expr_arith(p):
  "found_expr_arith : empty"
  quads.addDualOpQuad(['+', '-'])

def p_expr_factor(p):
  "expr_factor : expr_atom found_expr_factor expr_factor2"
  pass

def p_expr_factor2(p):
  """expr_factor2 : '*' found_expr_duo_op expr_factor
                  | '/' found_expr_duo_op expr_factor
                  | '%' found_expr_duo_op expr_factor
                  | empty"""
  pass

def p_found_expr_factor(p):
  "found_expr_factor : empty"
  quads.addDualOpQuad(['*', '/', '%'])

def p_found_expr_duo_op(p):
  "found_expr_duo_op : empty"
  quads.pushOperator(p[-1])

# TODO: Fix mono operator
def p_expr_atom(p):
  """expr_atom : expr_group
               | expr_var
               | expr_call_func"""
  pass

def p_expr_group(p):
  "expr_group : '(' found_expr_duo_op expr ')'"
  quads.popOperator()

def p_expr_mono_op(p):
  """expr_mono : '-'
               | '!'
               | '$'
               | '?'
               | empty"""
  pass

def p_expr_var(p):
  "expr_var : expr_var_name expr_var_dims"
  pass

def p_expr_var_name(p):
  "expr_var_name : ID"
  var = funcDir.getVar(p[1])
  quads.pushVar(var.name, var.vartype)

def p_expr_var_no_dims(p):
  "expr_var_dims : empty"
  pass

def p_expr_var_dims(p):
  """expr_var_dims : found_expr_var_dims expr_var_dim found_expr_var_dim_2 expr_var_dim
                   | found_expr_var_dims expr_var_dim"""
  quads.addArrEndQuad()

def p_found_expr_var_dims(p):
  "found_expr_var_dims : empty"
  arr = quads.popOperand()
  quads.popType()
  quads.dimCount = 0
  quads.sDims.append((arr, 0))
  quads.sOperators.append('(')

def p_expr_var_dim(p):
  "expr_var_dim : found_expr_var_dim '[' expr found_expr_var_dim_expr ']'"
  pass

def p_found_expr_var_dim(p):
  "found_expr_var_dim : empty"
  sdim = quads.sDims[-1]
  quads.dimCount += 1
  if quads.dimCount > len(funcDir.getDimensionsOfVar(sdim[0])):
    raise Exception(f'{sdim[0]} has {len(funcDir.getDimensionsOfVar(sdim[0]))} dimension(s)! -> {quads.dimCount}')

def p_found_expr_var_dim_2(p):
  "found_expr_var_dim_2 : empty"
  sdim = quads.sDims.pop()
  quads.sDims.append((sdim[0], quads.dimCount))

def p_found_expr_var_dim_expr(p):
  "found_expr_var_dim_expr : empty"
  quads.addArrQuads()


# TODO: Redo arrays and matrixes
# def p_expr_var_mat_elem(p):
#   "expr_var : ID '[' expr ']' '[' expr ']'"
#   var = funcDir.getVar(p[1])
#   quads.pushVar(var.name, var.vartype)

# def p_expr_var_list_elem(p):
#   "expr_var : ID '[' expr ']'"
#   var = funcDir.getVar(p[1])
#   quads.pushVar(var.name, var.vartype)

# def p_expr_var_atom(p):
#   "expr_var : ID"
#   var = funcDir.getVar(p[1])
#   quads.pushVar(var.name, var.vartype)

def p_cte(p):
  """expr_var : CTE_INT
              | CTE_FLOAT
              | CTE_BOOL
              | CTE_CHAR"""
  t = None
  if (type(p[1]) is int):
    t = 'int'
  elif (type(p[1]) is float):
    t = 'float'
  elif (type(p[1]) is str):
    t = 'char'
  elif (type(p[1] is bool)):
    t = 'bool'

  vAddr = None
  if funcDir.cteExists(p[1]):
    vAddr = funcDir.getCte(p[1]).vAddr
  else:
    vAddr = quads.vDir.generateVirtualAddress('cte', t)
    funcDir.addCte(p[1], t, vAddr)
  quads.pushVar(vAddr, t)

def p_expr_call_func(p):
  "expr_call_func : ID found_call_func_name '(' call_func_params ')' found_call_func_end"
  func = quads.popFunction()
  if quads.funcDir.getReturnTypeOfFunc(func) == 'void':
    raise Exception("This function is void and cannot be used as an expression!")

## CALL_FUNCTION
# NOTE: Ask teacher about how a "function is assigned to a variable"
def p_call_func(p):
  "call_func : ID found_call_func_name '(' call_func_params ')' found_call_func_end ';'"
  func = quads.popFunction()
  quads.pushVar('??', 'int')
  if quads.funcDir.getReturnTypeOfFunc(func) != 'void':
    raise Exception("This function is non-void, therefore it can't be used outside of an expression!")

def p_found_call_func_name(p):
  """found_call_func_name : empty"""
  func = p[-1]
  if funcDir.functionExists(func):
    quads.addEraQuad(func)
    quads.pushFunction(func)
  else:
    raise Exception(f'Function {func}() does not exist!')

def p_call_func_params(p):
  """call_func_params : call_func_param
                      | empty"""
  pass

def p_call_func_param(p):
  """call_func_param : expr func_single_step ',' call_func_param
                     | expr func_single_step"""
  pass

def p_func_single_step(p):
  "func_single_step : empty"
  target_param = funcDir.getParamOfFunc(quads.getTopFunction())
  quads.addParamQuad(target_param, funcDir.paramCount)
  funcDir.incrementParamCount()
  pass

def p_found_call_func_end(p):
  "found_call_func_end : empty"
  func = quads.getTopFunction()
  if funcDir.verifyParamCount(func):
    quads.addGoSubQuad(func, funcDir.getQuadStartOfFunc(func))
  else:
    raise Exception(f'Wrong number of parameters in {func}!')

def p_empty(p):
  "empty :"
  pass

# Error handling
def p_error(p):
  raise Exception(f'({p.lineno}:{p.lexpos}) Syntax error at "{p.value}"')

# Manual error (line number & position are kinda broken...)
def s_error(msg):
  raise Exception(f'{msg}')
