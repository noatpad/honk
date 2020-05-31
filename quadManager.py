
from collections import deque
from semanticCube import getDuoResultType, getMonoResultType
from virtualDirectory import VirtualDirectory

class QVar:
  def __init__(self, name, vAddr, vartype, dims):
    self.name = name
    self.vAddr = vAddr
    self.vartype = vartype
    self.dims = dims

class QuadManager:
  def __init__(self, funcDir, debug):
    self.debug = debug
    self.funcDir = funcDir
    self.vDir = VirtualDirectory()
    self.quads = deque()
    self.sVars = deque()
    self.sOperators = deque()
    self.sJumps = deque()
    self.sFuncs = deque()
    self.sDims = deque()
    self.quadCount = 0
    self.tempCount = 0
    self.returnCount = 0
    self.dimCount = 0

  ## GETTERS
  # Get function from top of stack
  def getTopFunction(self):
    return self.sFuncs[-1]

  # Get current quad counter
  def getQuadCount(self):
    return self.quadCount

  # Get temporal counter
  def getTempCount(self):
    return self.tempCount

  ## PUSH
  # Push variable to var stack
  def pushVar(self, var):
    qvar = QVar(var.name, var.vAddr, var.vartype, var.dims)
    self.sVars.append(qvar)

  # Push constant to var stack
  def pushCte(self, cte):
    qvar = QVar(cte.value, cte.vAddr, cte.vartype, [])
    self.sVars.append(qvar)

  # Push temporary value to var stack
  def pushTemp(self, vAddr, vartype, dims):
    qvar = QVar(f't{self.tempCount}', vAddr, vartype, dims)
    self.sVars.append(qvar)

  # Push operator to stack
  def pushOperator(self, op):
    self.sOperators.append(op)

  # Push function name to stack
  def pushFunction(self, func):
    self.sFuncs.append(func)

  ## POP
  # Pop function from stack
  def popFunction(self):
    return self.sFuncs.pop()

  # Pop operator from stack
  def popOperator(self):
    return self.sOperators.pop()

  ## GENERAL QUAD FUNCTIONS
  # General function to add quads
  def addQuad(self, quad):
    if self.debug:
      print(f'{self.quadCount}:\t{quad[0]}\t{quad[1]}\t{quad[2]}\t{quad[3]}')
    self.quads.append(quad)
    self.quadCount += 1

  # General function to complete quad
  def completeQuad(self, index, jump):
    quadToChange = list(self.quads[index])
    quadToChange[3] = jump
    self.quads[index] = tuple(quadToChange)

    if self.debug:
      print(f'\t\t\t\t\t! Completed quad #{index} with jump to {jump}')

  ## QUAD FUNCTIONS
  # Append quad to go to main
  def addMainQuad(self):
    self.addQuad(('GoTo', None, None, None))
    self.sJumps.append(0)

  # Complete quad to go to main
  def completeMainQuad(self):
    ret = self.sJumps.pop()
    self.completeQuad(ret, self.quadCount)

    if self.debug:
      print(f'--- main')

  # Append assignment quadruple
  def addAssignQuad(self):
    right = self.sVars.pop()
    left = self.sVars.pop()
    operator = self.sOperators.pop()

    result_type = getDuoResultType(left.vartype, right.vartype, operator)
    if not result_type:
      raise Exception(f'Type mismatch! {left.vartype} {operator} {right.vartype}')

    if not self.areCompatibleDims(left.dims, right.dims):
      raise Exception(f'Dimension mismatch! {left.dims} != {right.dims}')

    if left.dims:
      self.addMatQuad(left.dims)

    self.addQuad((operator, right.vAddr, None, left.vAddr))

  # Append dual-operand operation quad
  def addDualOpQuad(self, ops):
    # If operators stack is empty, stop here
    if not self.sOperators or self.sOperators[-1] not in ops:
      return

    # Special case for dot product operator ('.')
    if self.sOperators[-1] == '.':
      self.addDotProdQuad()
      return

    right = self.sVars.pop()
    left = self.sVars.pop()
    operator = self.sOperators.pop()

    result_type = getDuoResultType(left.vartype, right.vartype, operator)
    if not result_type:
      raise Exception(f'Type mismatch! {left.vartype} {operator} {right.vartype}')

    if not self.areCompatibleDims(left.dims, right.dims):
      raise Exception(f'Dimension mismatch! {left.dims} != {right.dims}')

    if left.dims:
      self.addMatQuad(left.dims)

    result = self.vDir.generateVirtualAddress('temp', result_type)
    self.addQuad((operator, left.vAddr, right.vAddr, result))
    self.pushTemp(result, result_type, left.dims)

    if self.debug:
      print(f'\t\t\t\t\t> TMP: t{self.tempCount} - {result_type} -> {result}')

    self.tempCount += 1

  # Append mono-operand operation quad
  def addMonoOpQuad(self, operator):
    mat = self.sVars.pop()
    if len(mat.dims) != 2:
      raise Exception(f'{mat.name} must be a matrix to use the {operator} operator!')

    result_type = getMonoResultType(mat.vartype, operator)
    if not result_type:
      raise Exception(f'Type mismatch! {mat.vartype} {operator}')

    # Error out if ['$', '?'] operator and not a square matrix
    if operator in ['$', '?'] and mat.dims[0] != mat.dims[1]:
      raise Exception(f'{mat.name} must be a square matrix to use the {operator} operator!')

    result_dims = mat.dims
    if operator == '$':     # '$' yields a single value
      result_dims = []
    elif operator == '!':   # '!' swaps the dimensions
      result_dims = [mat.dims[1], mat.dims[0]]

    result = self.vDir.generateVirtualAddress('temp', result_type)
    if self.debug:
      print(f'\t\t\t\t\t> TMP: t{self.tempCount} - {result_type} -> {result}')

    if result_dims:
      self.vDir.makeSpaceForArray('temp', result_type, result_dims[0] * result_dims[1])
      if self.debug:
        print(f'\t\t\t\t\t>> TMP: t{self.tempCount} - {result_type}{result_dims} -> {result} - {result + result_dims[0] * result_dims[1] - 1}')

    self.addMatQuad(mat.dims)
    self.addQuad((operator, mat.vAddr, None, result))
    self.pushTemp(result, result_type, result_dims)
    self.tempCount += 1

  # Append dot product quads
  def addDotProdQuad(self):
    right = self.sVars.pop()
    left = self.sVars.pop()
    operator = self.sOperators.pop()

    result_type = getDuoResultType(left.vartype, right.vartype, operator)
    if not result_type:
      raise Exception(f'Type mismatch! {left.vartype} {operator} {right.vartype}')

    if (len(left.dims) != 2) or (len(right.dims) != 2) or (left.dims[1] != right.dims[0]):
      raise Exception(f'Incompatible dimensions! {left.dims} {right.dims}')

    result_dims = [left.dims[0], right.dims[1]]
    result = self.vDir.generateVirtualAddress('temp', result_type)
    self.vDir.makeSpaceForArray('temp', result_type, result_dims[0] * result_dims[1])

    if self.debug:
      print(f'\t\t\t\t\t! Preparing dot product for dims {left.dims} · {right.dims}')

    self.addQuad(('MAT·', left.dims[0], left.dims[1], right.dims[1]))
    self.addQuad(('·', left.vAddr, right.vAddr, result))
    self.pushTemp(result, result_type, result_dims)
    self.tempCount += 1

  # Append MAT quadruple
  def addMatQuad(self, dims):
    if len(dims) == 1:
      rows = 1
      cols = dims[0]
    if len(dims) == 2:
      rows = dims[0]
      cols = dims[1]

    if self.debug:
      print(f'\t\t\t\t\t! Preparing for matrix of [{rows}][{cols}]')

    self.addQuad(('MAT', rows, cols, None))

  # Append RETURN quadruple
  def addReturnQuad(self):
    var = self.sVars.pop()
    return_type = self.funcDir.getCurrentFuncReturnType()

    if return_type is "void":
      raise Exception("There can't be return statements in non-void functions!")
    elif var.vartype != return_type:
      raise Exception(f"Returned variable doesn't match return type! -> {var.vartype} != {return_type}")
    if var.dims:    # NOTE: RETURN only allows atomic values
      raise Exception(f"Functions can only return atomic values, not arrays nor matrixes! -> ({var.vAddr}) - {var.dims}")

    if self.funcDir.getCurrentFuncReturnAddr() is None:
      self.funcDir.setReturnAddr(self.vDir.generateVirtualAddress(self.funcDir.currentFunc, return_type))
      if self.debug:
        print(f'\t\t\t\t\t! Set the function\'s return address to ({self.funcDir.getCurrentFuncReturnAddr()})')
    return_addr = self.funcDir.getCurrentFuncReturnAddr()

    self.addQuad(('=', var.vAddr, None, return_addr))
    self.addQuad(('RETURN', None, None, return_addr))
    self.returnCount += 1

  # Append READ quadruple
  def addReadQuad(self):
    var = self.sVars.pop()

    if var.dims:
      self.addMatQuad(var.dims)

    self.addQuad(('READ', None, None, var.vAddr))

  # Append PRINT quadruple
  def addPrintQuad(self, string):
    # Strings simply use this case and stop here
    if string:
      self.addQuad(('PRINT', None, None, string))
      return

    var = self.sVars.pop()

    if var.dims:
      self.addMatQuad(var.dims)

    self.addQuad(('PRINT', None, None, var.vAddr))

  # Append quadruple for `if` statement
  def addIfQuad(self):
    result = self.sVars.pop()

    if result.dims:
      self.addMatQuad(result.dims)

    if result.vartype == 'bool':
      self.addQuad(('GoToF', result.vAddr, None, None))
      self.sJumps.append(self.quadCount - 1)
    else:
      raise Exception(f'Type mismatch! {result.vartype} != bool')

  # Prepare and append quadruple for `else` statement
  def addElseQuad(self):
    self.addQuad(('GoTo', None, None, None))
    falseJump = self.sJumps.pop()
    self.sJumps.append(self.quadCount - 1)
    self.completeQuad(falseJump, self.quadCount)

  # Complete quadruple for `if` statement
  def completeIfQuad(self):
    end = self.sJumps.pop()
    self.completeQuad(end, self.quadCount)

  # Prepare for/while block
  def prepareLoop(self):
    self.sJumps.append(self.quadCount)

  # Append quadruple for `while` block
  # NOTE: It's practically identical to addIfQuad()
  def addLoopCondQuad(self):
    result = self.sVars.pop()

    if result.dims:
      self.addMatQuad(result.dims)

    if result.vartype == 'bool':
      self.addQuad(('GoToF', result.vAddr, None, None))
      self.sJumps.append(self.quadCount - 1)
    else:
      raise Exception(f'Type mismatch! {result.vartype} != bool')

  # Complete quadruple for `while` block
  def completeLoopQuad(self):
    end = self.sJumps.pop()
    ret = self.sJumps.pop()
    self.addQuad(('GoTo', None, None, ret))
    self.completeQuad(end, self.quadCount)

  # Add quads for when the iterator of a 'for' loop is found
  def addForIteratorQuads(self, var):
    if not self.funcDir.varExists(var):
      self.funcDir.setCurrentType('int')
      self.funcDir.addVar(var, self.vDir.generateVirtualAddress('temp', 'int'))
      iter_var = self.funcDir.getVar(var)
      self.pushVar(iter_var)
      self.pushVar(iter_var)
      self.pushVar(iter_var)
    else:
      raise Exception(f'Variable "{var}" already exists!"')

  # Add quads for a 'for' loop's initial assignment
  def addForStartQuad(self):
    self.pushOperator('=')
    self.addAssignQuad()
    self.prepareLoop()

  # Add quads for a 'for' loop's condition check
  def addForCondQuads(self):
    self.pushOperator('<=')
    self.addDualOpQuad(['<='])
    self.addLoopCondQuad()

  # Add quads for a 'for' loop's increment
  def addForEndQuads(self):
    # Get constant of 1
    one = self.upsertCte(1, 'int')

    self.pushVar(self.sVars[-1])
    self.pushVar(self.sVars[-1])
    self.pushCte(one)
    self.pushOperator('=')
    self.pushOperator('+')
    self.addDualOpQuad(['+'])
    self.addAssignQuad()
    self.completeLoopQuad()
    self.sVars.pop()

  # Add necessary quads for array access
  def addArrQuads(self):
    var = self.sVars[-1]
    if var.dims:
      raise Exception(f'Array indexes must be an atomic value! -> ({var.vAddr}) - {var.dims}')

    aux = self.sDims[-1]
    dims = self.funcDir.getDimensionsOfVar(aux[0])
    self.addQuad(('VERIFY', var.vAddr, None, dims[aux[1] - 1]))

    # Only do the following for first dimension and if a second dimension exists
    if len(dims) - aux[1] == 1:
      mul = self.upsertCte(dims[1], 'int')
      self.pushCte(mul)
      self.sOperators.append('*')
      self.addDualOpQuad(['*'])
    # Only do the following if in the second dimension
    elif len(dims) == 2:
      self.sOperators.append('+')
      self.addDualOpQuad(['+'])

    self.sOperators.pop()

  def addBaseAddressQuad(self):
    depth = self.sDims.pop()[1]
    offset = self.sVars.pop()
    arr = self.sVars.pop()

    result_type = arr.vartype
    result = self.vDir.generateVirtualAddress('temp', result_type)
    self.addQuad(('+->', offset.vAddr, arr.vAddr, result))
    self.pushTemp((result,), result_type, arr.dims[depth:])

    if self.debug:
      print(f'\t\t\t\t\t> PTR: t{self.tempCount} - {result_type} -> ({result})')

    self.tempCount += 1

  # Append ERA quad
  def addEraQuad(self, func):
    self.addQuad(('ERA', None, None, func))

  # Append PARAM Quad
  def addParamQuad(self, target_param, k):
    param = self.sVars.pop()

    if param.dims:    # NOTE: Function parameters can only be atomic values
      raise Exception(f'Function parameters must be atomic values -> ({param.vAddr}) - {param.dims}')

    if param.vartype == target_param:
      self.addQuad(('PARAM', param.vAddr, None, k))
    else:
      raise Exception(f'Wrong param type! {param.vartype} {target_param}')

  # Append GOSUB quad
  def addGoSubQuad(self, func, qs):
    self.addQuad(('GoSub', None, None, qs))

  # Append EndFunc quad
  def addEndFuncQuad(self):
    if self.returnCount == 0 and self.funcDir.getCurrentFuncReturnType() != 'void':
      raise Exception("This function is missing a return statement!")

    self.funcDir.setEra(self.vDir.getEra())
    self.resetFuncCounters()
    self.addQuad(('EndFunc', None, None, None))

  # Append an assignment quad for non-void function
  def addAssignFuncQuad(self):
    func = self.popFunction()
    return_type = self.funcDir.getReturnTypeOfFunc(func)
    if return_type == 'void':   # Error out if the function is void
      raise Exception(f'This function is void and cannot be used as an expression! -> {func}')

    result = self.vDir.generateVirtualAddress('temp', return_type)
    self.addQuad(('=>', None, None, result))
    self.pushTemp(result, return_type, [])    # NOTE: Functions can only return atomic variables

    if self.debug:
      print(f'\t\t\t\t\t> RET: t{self.tempCount} - {return_type} -> {result}')

    self.tempCount += 1

  # Append END Quad
  def addEndQuad(self):
    self.addQuad(('END', None, None, None))

  ## FUNCTIONS (PARSING)
  # Reset temporal counter
  def resetFuncCounters(self):
    self.tempCount = 0
    self.returnCount = 0
    self.vDir.resetLocalCounters()

  # Get a constant if it exists, otherwise create one and return it
  def upsertCte(self, value, vartype):
    if not self.funcDir.cteExists(value, vartype):
      vAddr = self.vDir.generateVirtualAddress('cte', vartype)
      self.funcDir.addCte(value, vartype, vAddr)
    return self.funcDir.getCte(value, vartype)

  # Check if two variables are "compatible" in dimensions
  def areCompatibleDims(self, left_dims, right_dims):
    if len(left_dims) == 0 and len(right_dims) == 0:
      return True
    elif len(left_dims) == 1 and len(right_dims) == 1:
      return left_dims[0] == right_dims[0]
    elif len(left_dims) == 2 and len(right_dims) == 2:
      return left_dims[0] == right_dims[0] and left_dims[1] == right_dims[1]
    return False

  # Print all quads
  def printQuads(self):
    i = 0
    for q in self.quads:
      print(f'{i}:\t{q[0]}\t{q[1]}\t{q[2]}\t{q[3]}')
      i += 1

  # Debug function
  def debugStep(self):
    operands = []
    vAddrs = []
    types = []
    dims = []
    for v in self.sVars:
      operands.append(v.name)
      vAddrs.append(v.vAddr)
      types.append(v.vartype)
      dims.append(v.dims)

    print("\t - - - DEBUG - - - ")
    print("\t sOperators ->", list(self.sOperators))
    print("\t sVars:")
    print("\t  operands ->", operands)
    print("\t  vAddrs ->", vAddrs)
    print("\t  types ->", types)
    print("\t  dims ->", dims)
    print("\t sJumps ->", list(self.sJumps))
    print("\t sFuncs ->", list(self.sJumps))
    print("\t sDims ->", list(self.sDims))
    print("\t - CTES")
    for c in self.funcDir.cteTable.values():
      print("\t ", c.value, c.vartype, c.vAddr)
    print("\t - - - DEBUG END - - - ")

  ## FUNCTIONS (BUILDING)
  # Build .o file
  def build(self):
    filename = 'quack.o'

    if self.debug:
      print(f'> Building {filename}...')

    f = open(filename, 'w')
    # Write ranges
    f.write('-> RANGES START\n')
    for r in self.vDir.getRanges():
      f.write(f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\n')
    f.write('->| RANGES END\n')
    # Write constants
    f.write('-> CTES START\n')
    for cte in self.funcDir.cteTable.values():
      f.write(f'{cte.value}\t{cte.vartype}\t{cte.vAddr}\n')
    f.write('->| CTES END\n')
    # Write ERAs
    f.write('-> ERAS START\n')
    for func in self.funcDir.directory.values():
      # Skip global since it has no ERA
      if func.name == 'global':
        continue
      era = self.funcDir.getEra(func.name)
      localCounts = '\t'.join([str(x) for x in era[0]])
      tempCounts = '\t'.join([str(x) for x in era[1]])
      f.write(f'{func.name}\t{localCounts}\t{tempCounts}\n')
    f.write('->| ERAS END\n')
    # Write quads
    f.write('-> QUADS START\n')
    for q in self.quads:
      f.write(f'{q[0]}\t{q[1]}\t{q[2]}\t{q[3]}\n')
    f.write('->| QUADS END\n')

    if self.debug:
      print(f'> Done!')
