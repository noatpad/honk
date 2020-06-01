
from collections import deque

from lexer import tokens
from functionDirectory import FunctionDirectory
from quadManager import QuadManager

funcDir = FunctionDirectory()
quads = QuadManager(funcDir)

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
def p_program(p):
  "program : PROGRAM ID found_program_name ';' vars functions main '(' ')' '{' body '}'"
  # Finish parsing
  quads.addEndQuad()
  p[0] = quads

  # Build .o
  quads.build()

# Make a GOTO quad to main()
def p_found_program_name(p):
  'found_program_name : empty'
  if quads.debug:
      print("\n|==|==|==|==|==|==|==|==| START DEBUG LOG |==|==|==|==|==|==|==|==|\n")

  funcDir.addFunction('main')
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
  """var_declare : type var_name ';' var_declare
                 | type var_name ';'"""
  pass

def p_var_name(p):
  """var_name : variable_declare var_dims ',' var_name
              | variable_declare var_dims"""
  pass

def p_variable_declare(p):
  "variable_declare : ID"
  var = p[1]
  if funcDir.varAvailable(var):
    funcDir.addVar(var, quads.vDir.generateVirtualAddress(funcDir.currentFunc, funcDir.currentType))
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
    funcDir.setVarDims([p[1], p[2]])
    p[0] = p[1] * p[2]
  else:
    funcDir.setVarDims([p[1]])
    p[0] = p[1]

  quads.vDir.makeSpaceForArray(funcDir.currentFunc, funcDir.currentType, p[0])

# TYPE
def p_type(p):
  """type : INT
          | FLOAT
          | CHAR
          | BOOL"""
  funcDir.setCurrentType(p[1])
  p[0] = p[1]

# FUNCTIONS
def p_functions(p):
  """functions : FUNCTION func_type ID found_func_name func_dims '(' func_params ')' vars found_func_start '{' body '}' found_func_end functions
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

def p_func_no_dims(p):
  "func_dims : empty"
  pass

def p_func_dims(p):
  """func_dims : dim dim
               | dim"""
  if len(p) == 3:
    funcDir.setReturnDims([p[1], p[2]])
  else:
    funcDir.setReturnDims([p[1]])

def p_dim(p):
  "dim : '[' CTE_INT ']'"
  if p[2] <= 0:
    s_error(f'Zero or negative indexes are not allowed! [{p[0]}]')
  p[0] = p[2]

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
    funcDir.addVar(param, quads.vDir.generateVirtualAddress(funcDir.currentFunc, funcDir.currentType))
    funcDir.addFuncParam()
  else:
    s_error(f'Multiple declaration of "{param}"!')

def p_found_func_start(p):
  "found_func_start : empty"
  funcDir.setQuadStart(quads.getQuadCount())

def p_found_func_end(p):
  "found_func_end : empty"
  quads.addEndFuncQuad()
  funcDir.deleteVarTable()

# PRINCIPAL
def p_principal(p):
  "main : MAIN"
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
               | from
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
  "return : RETURN '(' expr ')' ';'"
  quads.addReturnQuad()

## READ
def p_read(p):
  "read : READ '(' read_params ')' ';'"
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
  "print : PRINT '(' print_params ')' ';'"
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
  """if : IF '(' expr ')' found_if_expr THEN '{' body '}'
        | IF '(' expr ')' found_if_expr THEN '{' body '}' else"""
  quads.completeIfQuad()

def p_found_if_expr(p):
  "found_if_expr : empty"
  quads.addIfQuad()

## ELSE
def p_else(p):
  "else : ELSE found_else '{' body '}'"
  pass

def p_found_else(p):
  "found_else : empty"
  quads.addElseQuad()

## FROM
def p_from(p):
  "from : FROM '(' ID found_from_iterator '=' expr found_from_start TO expr ')' found_from_cond DO '{' body '}'"
  quads.addFromEndQuads()

def p_found_from_iterator(p):
  "found_from_iterator : empty"
  quads.addFromIteratorQuads(p[-1])


def p_found_from_start(p):
  "found_from_start : empty"
  quads.addFromStartQuad()

def p_found_from_cond(p):
  "found_from_cond : empty"
  quads.addFromCondQuads()

## WHILE
def p_while(p):
  "while : WHILE found_while '(' expr ')' found_while_expr DO '{' body '}'"
  quads.completeLoopQuad()

def p_found_while(p):
  "found_while : empty"
  quads.prepareLoop()

def p_found_while_expr(p):
  "found_while_expr : empty"
  quads.addLoopCondQuad()

# EXPRESSION -> Order of operator precedence:
# - Matrix operations ($, !, ?)
# - Factors (*, /, %, .)
# - Arithmetic (+, -)
# - Comparison (==, !=, <, <=, >, >=)
# - Logic (&, |)
def p_expr(p):
  "expr : expr_logic"
  pass

def p_expr_logic(p):
  "expr_logic : expr_compare found_expr_logic expr_logic2"
  pass

def p_found_expr_logic(p):
  "found_expr_logic : empty"
  quads.addDualOpQuad(['&', '|'])

def p_expr_logic2(p):
  """expr_logic2 : '&' found_expr_duo_op expr_logic
                 | '|' found_expr_duo_op expr_logic
                 | empty"""
  pass

def p_expr_compare(p):
  "expr_compare : expr_arith found_expr_compare expr_compare2"
  pass

def p_found_expr_compare(p):
  "found_expr_compare : empty"
  quads.addDualOpQuad(['==', '!=', '<', '<=', '>', '>='])

def p_expr_compare2(p):
  """expr_compare2 : IS_EQUAL found_expr_duo_op expr_compare
                   | IS_NOT_EQUAL found_expr_duo_op expr_compare
                   | '<' found_expr_duo_op expr_compare
                   | LESS_THAN_OR_EQUAL found_expr_duo_op expr_compare
                   | '>' found_expr_duo_op expr_compare
                   | MORE_THAN_OR_EQUAL found_expr_duo_op expr_compare
                   | empty"""
  pass

def p_expr_arith(p):
  "expr_arith : expr_factor found_expr_arith expr_arith2"
  pass

def p_found_expr_arith(p):
  "found_expr_arith : empty"
  quads.addDualOpQuad(['+', '-'])

def p_expr_arith2(p):
  """expr_arith2 : '+' found_expr_duo_op expr_arith
                 | '-' found_expr_duo_op expr_arith
                 | empty"""
  pass

def p_expr_factor(p):
  "expr_factor : expr_mono found_expr_factor expr_factor2"
  pass

def p_found_expr_factor(p):
  "found_expr_factor : empty"
  quads.addDualOpQuad(['*', '/', '%', '.'])

def p_expr_factor2(p):
  """expr_factor2 : '*' found_expr_duo_op expr_factor
                  | '/' found_expr_duo_op expr_factor
                  | '%' found_expr_duo_op expr_factor
                  | '.' found_expr_duo_op expr_factor
                  | empty"""
  pass

def p_found_expr_duo_op(p):
  "found_expr_duo_op : empty"
  quads.pushOperator(p[-1])

def p_expr_mono(p):
  "expr_mono : expr_atom expr_mono_op"
  pass

def p_expr_mono_op(p):
  """expr_mono_op : '!' found_expr_mono_op expr_mono_op
                  | '$' found_expr_mono_op expr_mono_op
                  | '?' found_expr_mono_op expr_mono_op
                  | empty"""
  pass

def p_found_expr_mono_op(p):
  "found_expr_mono_op : empty"
  quads.addMonoOpQuad(p[-1])

def p_expr_atom(p):
  """expr_atom : expr_group
               | expr_call_func
               | expr_var"""
  pass

def p_expr_group(p):
  "expr_group : '(' found_expr_duo_op expr ')'"
  quads.popOperator()

def p_expr_var(p):
  "expr_var : expr_var_name expr_var_dims"
  pass

def p_expr_var_name(p):
  "expr_var_name : ID"
  var = funcDir.getVar(p[1])
  funcDir.setVarHelper(var.name)
  quads.pushVar(var)

def p_expr_var_no_dims(p):
  "expr_var_dims : empty"
  pass

def p_expr_var_dims(p):
  """expr_var_dims : found_expr_var_dims expr_var_dim expr_var_dim
                   | found_expr_var_dims expr_var_dim"""
  quads.addBaseAddressQuad()

def p_found_expr_var_dims(p):
  "found_expr_var_dims : empty"
  quads.sDims.append((funcDir.varHelper, 0))

def p_expr_var_dim(p):
  "expr_var_dim : '[' expr_var_open_dim expr ']'"
  quads.addArrQuads()

def p_expr_var_open_dim(p):
  "expr_var_open_dim : empty"
  aux = quads.sDims.pop()
  if aux[1] + 1 > len(funcDir.getDimensionsOfVar(aux[0])):
    raise Exception(f'{aux[0]} has {len(funcDir.getDimensionsOfVar(aux[0]))} dimension(s)! -> {aux[1]}')

  quads.sDims.append((aux[0], aux[1] + 1))
  quads.sOperators.append('(')

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

  cte = quads.upsertCte(p[1], t)
  quads.pushCte(cte)

def p_expr_call_func(p):
  "expr_call_func : ID found_call_func_name '(' call_func_params ')' found_call_func_end"
  quads.addAssignFuncQuad()

## CALL_FUNCTION
def p_call_func(p):
  "call_func : ID found_call_func_name '(' call_func_params ')' found_call_func_end ';'"
  func = quads.popFunction()
  if quads.funcDir.getReturnTypeOfFunc(func) != 'void':
    raise Exception(f"This function is non-void, therefore it can't be used as an expression! -> {func}")

def p_found_call_func_name(p):
  "found_call_func_name : empty"
  func = p[-1]
  if funcDir.functionExists(func):
    quads.addEraQuad(func)
    quads.pushFunction(func)
    quads.sOperators.append('(')
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
    funcDir.resetParamCount()
    quads.addGoSubQuad(func, funcDir.getQuadStartOfFunc(func))
    quads.popOperator()
  else:
    raise Exception(f'Wrong number of parameters in {func}!')

def p_empty(p):
  "empty :"
  pass

# Error handling
def p_error(p):
  raise Exception(f'({p.lineno}) Syntax error at "{p.value}"')

# Manual error (line number & position are kinda broken...)
def s_error(msg):
  raise Exception(msg)
