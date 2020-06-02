
from lexhonker import tokens
from functionDirectory import FunctionDirectory
from quadManager import QuadManager

funcDir = FunctionDirectory()
quads = QuadManager(funcDir)

# Parsing productions
# PROGRAMA
def p_program(p):
  "program : UNTITLED ID GAME found_program_name HONK vars functions main body"
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
  """vars : POND found_var var_declare
          | empty"""
  pass

def p_found_var(p):
  "found_var : empty"
  funcDir.createVarTable()

def p_var_declare(p):
  """var_declare : type var_name HONK var_declare
                 | type var_name HONK"""
  pass

def p_var_name(p):
  """var_name : variable_declare var_dims MOAR var_name
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
  """type : type_int
          | type_float
          | type_char
          | type_bool"""
  p[0] = p[1]
  funcDir.setCurrentType(p[0])

def p_type_int(p):
  "type_int : WHOLE GOOSE"
  p[0] = 'int'

def p_type_float(p):
  "type_float : PART GOOSE"
  p[0] = 'float'

def p_type_char(p):
  "type_char : LETTER GOOSE"
  p[0] = 'char'

def p_type_bool(p):
  "type_bool : DUCK OR GOOSE"
  p[0] = 'bool'

# FUNCTIONS
def p_functions(p):
  """functions : TASK func_type ID found_func_name func_dims HONK func_params HONK vars found_func_start body found_func_end functions
               | empty"""
  pass

def p_func_type(p):
  "func_type : type"
  pass

def p_func_void(p):
  "func_type : MY SOUL"
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
  "dim : OPEN BOX CTE_INT CLOSE BOX"
  if p[3] <= 0:
    s_error(f'Zero or negative indexes are not allowed! [{p[3]}]')
  p[0] = p[3]

def p_func_params(p):
  """func_params : func_param
                 | empty"""
  pass

def p_func_param(p):
  """func_param : type ID found_func_param param_dims MOAR func_param
                | type ID found_func_param param_dims"""
  pass

def p_found_func_param(p):
  "found_func_param : empty"
  param = p[-1]
  if funcDir.varAvailable(param):
    funcDir.setVarHelper(param)
    vAddr = quads.vDir.generateVirtualAddress(funcDir.currentFunc, funcDir.currentType)
    funcDir.addVar(param, vAddr)
    funcDir.addFuncParam(vAddr)
  else:
    s_error(f'Multiple declaration of "{param}"!')

def p_param_no_dims(p):
  "param_dims : empty"
  pass

def p_param_dims(p):
  """param_dims : dim dim
                | dim"""
  space = None
  if len(p) == 3:
    p[0] = [p[1], p[2]]
    space = p[1] * p[2]
  else:
    p[0] = [p[1]]
    space = p[1]

  funcDir.addFuncParamDims(p[0])
  funcDir.setVarDims(p[0])
  quads.vDir.makeSpaceForArray(funcDir.currentFunc, funcDir.currentType, space)

def p_found_func_start(p):
  "found_func_start : empty"
  funcDir.setQuadStart(quads.getQuadCount())

def p_found_func_end(p):
  "found_func_end : empty"
  quads.addEndFuncQuad()
  funcDir.deleteVarTable()

# MAIN
def p_main(p):
  "main : PRESS Y TO HONK_LOWERCASE"
  quads.completeMainQuad()

# BODY
def p_body(p):
  "body : OPEN FANCY GATE statements CLOSE FANCY GATE"
  pass

def p_statements(p):
  """statements : statement statements
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
               | while
               | break
               | empty"""
  pass

## ASSIGNMENT
def p_assignment(p):
  "assignment : expr_var AM found_assignment_op found_expr_duo_op expr found_assignment_end HONK"
  pass

def p_found_assignment_op(p):
  "found_assignment_op : empty"
  p[0] = '='

def p_found_assignment_end(p):
  "found_assignment_end : empty"
  quads.addAssignQuad()

## RETURN
def p_return(p):
  "return : GOT BELL OPEN GATE expr CLOSE GATE HONK"
  quads.addReturnQuad()

## READ
def p_read(p):
  "read : HO '-' read_params '-' ONK HONK"
  pass

def p_read_params(p):
  """read_params : expr_var found_read_param MOAR read_params
                 | expr_var found_read_param"""
  pass

def p_found_read_param(p):
  "found_read_param : empty"
  quads.addReadQuad()

## PRINT
def p_print(p):
  "print : SHOW ON TV OPEN GATE print_params CLOSE GATE HONK"
  pass

def p_print_params(p):
  """print_params : print_param MOAR print_params
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
  """if : HONK '?' OPEN GATE expr CLOSE GATE found_if_expr HONK '!' body
        | HONK '?' OPEN GATE expr CLOSE GATE found_if_expr HONK '!' body else"""
  quads.completeIfQuad()

def p_found_if_expr(p):
  "found_if_expr : empty"
  quads.addGoToFQuad()

## ELSE
def p_else(p):
  "else : BONK found_else body"
  pass

def p_found_else(p):
  "found_else : empty"
  quads.addElseQuad()

## FROM
def p_from(p):
  "from : INHALES OPEN GATE ID found_from_iterator AM expr found_from_start HOOOONK expr CLOSE GATE found_from_cond HOONK body"
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
  "while : HONK HONK found_while OPEN GATE expr CLOSE GATE found_while_expr HOONK body"
  quads.completeLoopQuad()

def p_found_while(p):
  "found_while : empty"
  quads.prepareLoop()

def p_found_while_expr(p):
  "found_while_expr : empty"
  quads.addGoToFQuad()

## BREAK
def p_break(p):
  "break : PEACE WAS NEVER AN OPTION HONK"
  quads.addBreakQuad()

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
  """expr_logic2 : and_op found_expr_duo_op expr_logic
                 | or_op found_expr_duo_op expr_logic
                 | empty"""
  pass

def p_and_op(p):
  "and_op : TOGETHER FOREVER"
  p[0] = '&'

def p_or_op(p):
  "or_op : POLE"
  p[0] = '|'

def p_expr_compare(p):
  "expr_compare : expr_arith found_expr_compare expr_compare2"
  pass

def p_found_expr_compare(p):
  "found_expr_compare : empty"
  quads.addDualOpQuad(['==', '!=', '<', '<=', '>', '>='])

def p_expr_compare2(p):
  """expr_compare2 : eq_op found_expr_duo_op expr_compare
                   | noeq_op found_expr_duo_op expr_compare
                   | less_op found_expr_duo_op expr_compare
                   | lesseq_op found_expr_duo_op expr_compare
                   | more_op found_expr_duo_op expr_compare
                   | moreeq_op found_expr_duo_op expr_compare
                   | empty"""
  pass

def p_eq_op(p):
  "eq_op : AM GOOSE '?'"
  p[0] = '=='

def p_noeq_op(p):
  "noeq_op : NOT GOOSE '?' '!'"
  p[0] = '!='

def p_less_op(p):
  "less_op : INFERIOR"
  p[0] = '<'

def p_lesseq_op(p):
  "lesseq_op : INFERIOR MAYBE"
  p[0] = '<='

def p_more_op(p):
  "more_op : SUPERIOR"
  p[0] = '>'

def p_moreeq_op(p):
  "moreeq_op : SUPERIOR MAYBE"
  p[0] = '>='

def p_expr_arith(p):
  "expr_arith : expr_factor found_expr_arith expr_arith2"
  pass

def p_found_expr_arith(p):
  "found_expr_arith : empty"
  quads.addDualOpQuad(['+', '-'])

def p_expr_arith2(p):
  """expr_arith2 : plus_op found_expr_duo_op expr_arith
                 | minus_op found_expr_duo_op expr_arith
                 | empty"""
  pass

def p_plus_op(p):
  "plus_op : MORE GOOSE"
  p[0] = '+'

def p_minus_op(p):
  "minus_op : LESS GOOSE"
  p[0] = '-'

def p_expr_factor(p):
  "expr_factor : expr_mono found_expr_factor expr_factor2"
  pass

def p_found_expr_factor(p):
  "found_expr_factor : empty"
  quads.addDualOpQuad(['*', '/', '%', '.'])

def p_expr_factor2(p):
  """expr_factor2 : mul_op found_expr_duo_op expr_factor
                  | div_op found_expr_duo_op expr_factor
                  | mod_op found_expr_duo_op expr_factor
                  | dot_op found_expr_duo_op expr_factor
                  | empty"""
  pass

def p_mul_op(p):
  "mul_op : GOOSETIPLY"
  p[0] = '*'

def p_div_op(p):
  "div_op : GOOSIVIDE"
  p[0] = '/'

def p_mod_op(p):
  "mod_op : LEFTOVERS"
  p[0] = '%'

def p_dot_op(p):
  "dot_op : DOOT"
  p[0] = '.'

def p_found_expr_duo_op(p):
  "found_expr_duo_op : empty"
  quads.pushOperator(p[-1])

def p_expr_mono(p):
  "expr_mono : expr_atom expr_mono_op"
  pass

def p_expr_mono_op(p):
  """expr_mono_op : det_op found_expr_mono_op expr_mono_op
                  | trans_op found_expr_mono_op expr_mono_op
                  | inv_op found_expr_mono_op expr_mono_op
                  | empty"""
  pass

def p_det_op(p):
  "det_op : GOOSECOIN"
  p[0] = '$'

def p_trans_op(p):
  "trans_op : SURPRISE"
  p[0] = '!'

def p_inv_op(p):
  "inv_op : WH"
  p[0] = '?'

def p_found_expr_mono_op(p):
  "found_expr_mono_op : empty"
  quads.addMonoOpQuad(p[-1])

def p_expr_atom(p):
  """expr_atom : expr_group
               | expr_call_func
               | expr_var"""
  pass

def p_expr_group(p):
  "expr_group : OPEN GATE found_expr_group found_expr_duo_op expr CLOSE GATE"
  quads.popOperator()

def p_found_expr_group(p):
  "found_expr_group : empty"
  p[0] = '('

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
  "expr_var_dim : OPEN BOX expr_var_open_dim expr CLOSE BOX"
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
  "expr_call_func : HOOONK ID found_call_func_name OPEN GATE call_func_params CLOSE GATE found_call_func_end"
  quads.addAssignFuncQuad()

## CALL_FUNCTION
def p_call_func(p):
  "call_func : HOOONK ID found_call_func_name OPEN GATE call_func_params CLOSE GATE found_call_func_end HONK"
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
  """call_func_param : expr func_single_step MOAR call_func_param
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
