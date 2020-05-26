
from collections import deque
from semanticCube import getDuoResultType
from virtualDirectory import VirtualDirectory

class QuadManager:
  def __init__(self, funcDir, debug):
    self.debug = debug
    self.funcDir = funcDir
    self.vDir = VirtualDirectory()
    self.quads = deque()
    self.sOperands = deque()
    self.sOperators = deque()
    self.sTypes = deque()
    self.sJumps = deque()
    self.sFuncs = deque()
    self.sDims = deque()
    self.quadCount = 0
    self.tempCount = 0
    self.returnCount = 0
    self.dimCount = 0

  ## GETTERS
  # Get operand from top of stack
  def getTopOperand(self):
    return self.sOperands[-1]

  # Get type from top of stack
  def getTopType(self):
    return self.sTypes[-1]

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
  # Push variable name and type to their respective stacks
  def pushVar(self, name, vartype):
    self.sOperands.append(name)
    self.sTypes.append(vartype)

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

  # Pop operand from stack
  def popOperand(self):
    return self.sOperands.pop()

  # Pop type from stack
  def popType(self):
    return self.sTypes.pop()

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
    right_op = self.sOperands.pop()
    right_type = self.sTypes.pop()
    left_op = self.sOperands.pop()
    left_type = self.sTypes.pop()
    operator = self.sOperators.pop()

    result_type = getDuoResultType(left_type, right_type, operator)
    if result_type:
      self.addQuad((operator, self.funcDir.getVAddr(right_op), None, self.funcDir.getVAddr(left_op)))
    else:
      raise Exception(f'Type mismatch! {left_type} {operator} {right_type}')

  # Append dual-operand operation quadruple
  def addDualOpQuad(self, ops):
    if self.sOperators and self.sOperators[-1] in ops:
      right_op = self.sOperands.pop()
      right_type = self.sTypes.pop()
      left_op = self.sOperands.pop()
      left_type = self.sTypes.pop()
      operator = self.sOperators.pop()

      result_type = getDuoResultType(left_type, right_type, operator)
      if result_type:
        result = self.vDir.generateVirtualAddress('temp', result_type)
        self.addQuad((operator, self.funcDir.getVAddr(left_op), self.funcDir.getVAddr(right_op), result))
        self.sOperands.append(result)
        self.sTypes.append(result_type)

        if self.debug:
          print(f'\t\t\t\t\t> TMP: t{self.tempCount} - {result_type} -> {result}')

        self.tempCount += 1
      else:
        raise Exception(f'Type mismatch! {left_type} {operator} {right_type}')

  # Append RETURN quadruple
  def addReturnQuad(self):
    vartype = self.sTypes.pop()
    returntype = self.funcDir.getCurrentFuncReturnType()

    if returntype is "void":
      raise Exception("There can't be return statements in non-void functions!")
    elif vartype != returntype:
      raise Exception(f"Returned variable doesn't match return type! -> {vartype} != {returntype}")

    var = self.sOperands.pop()
    self.addQuad(("RETURN", None, None, self.funcDir.getVAddr(var)))
    self.returnCount += 1

  # Append READ quadruple
  def addReadQuad(self):
    var = self.sOperands.pop()
    self.sTypes.pop()
    self.addQuad(('READ', None, None, self.funcDir.getVAddr(var)))

  # Append PRINT quadruple
  def addPrintQuad(self, string):
    if string:
      self.addQuad(('PRINT', None, None, string))
    else:
      var = self.sOperands.pop()
      self.sTypes.pop()
      self.addQuad(('PRINT', None, None, self.funcDir.getVAddr(var)))

  # Append quadruple for `if` statement
  def addIfQuad(self):
    result_type = self.sTypes.pop()
    if result_type == 'bool':
      result = self.sOperands.pop()
      self.addQuad(('GoToF', result, None, None))
      self.sJumps.append(self.quadCount - 1)
    else:
      raise Exception(f'Type mismatch! {result_type} != bool')

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
    result_type = self.sTypes.pop()
    if result_type == 'bool':
      result = self.sOperands.pop()
      self.addQuad(('GoToF', result, None, None))
      self.sJumps.append(self.quadCount - 1)
    else:
      raise Exception(f'Type mismatch! {result_type} != bool')

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
      self.pushVar(var, 'int')
      self.pushVar(var, 'int')
      self.pushVar(var, 'int')
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

    self.pushVar(self.getTopOperand(), self.getTopType())
    self.pushVar(self.getTopOperand(), self.getTopType())
    self.pushVar(one.vAddr, one.vartype)
    self.pushOperator('=')
    self.pushOperator('+')
    self.addDualOpQuad(['+'])
    self.addAssignQuad()
    self.completeLoopQuad()
    self.popOperand()
    self.popType()

  # Add necessary quads for array access
  def addArrQuads(self):
    aux = self.sDims[-1]
    dims = self.funcDir.getDimensionsOfVar(aux[0])
    self.addQuad(('VERIFY', self.sOperands[-1], None, dims[aux[1] - 1]))

    # Only do the following for first dimension and if a second dimension exists
    if len(dims) - aux[1] == 1:
      mul = self.upsertCte(dims[1], 'int')
      self.pushVar(mul.vAddr, mul.vartype)
      self.sOperators.append('*')
      self.addDualOpQuad(['*'])
    elif len(dims) == 2:     # NOTE: Hacky removal of useless constant for second dimension
      self.sOperands.pop()
      self.sTypes.pop()

    self.popOperator()

  def addBaseAddressQuad(self):
    self.sDims.pop()
    offset = self.sOperands.pop()
    self.sTypes.pop()
    arr = self.sOperands.pop()
    result_type = self.sTypes.pop()
    base = self.funcDir.getVAddr(arr)

    result = self.vDir.generateVirtualAddress('temp', result_type)
    self.addQuad(('+->', offset, base, result))
    self.sOperands.append((result,))
    self.sTypes.append(result_type)

    if self.debug:
      print(f'\t\t\t\t\t> PTR: t{self.tempCount} - {result_type} -> ({result})')

    self.tempCount += 1

  # Append PARAM Quad
  def addParamQuad(self, target_param, k):
    param = self.sOperands.pop()
    param_type = self.sTypes.pop()
    if param_type == target_param:
      self.addQuad(('PARAM', self.funcDir.getVAddr(param), None, k))
    else:
      raise Exception(f'Wrong param type! {param_type} {target_param}')

  # Append ERA quad
  def addEraQuad(self, func):
    self.addQuad(('ERA', None, None, func))

  # Append GOSUB quad
  def addGoSubQuad(self, func, qs):
    self.addQuad(('GoSub', func, None, qs))

  # Append EndFunc quad
  def addEndFuncQuad(self):
    if self.returnCount == 0 and self.funcDir.getCurrentFuncReturnType() != 'void':
      raise Exception("This function is missing a return statement!")

    self.funcDir.setEra(self.vDir.getEra())
    self.resetFuncCounters()
    self.addQuad(('EndFunc', None, None, None))

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
    if not self.funcDir.cteExists(value):
      vAddr = self.vDir.generateVirtualAddress('cte', vartype)
      self.funcDir.addCte(value, vartype, vAddr)
    return self.funcDir.getCte(value)

  # Print all quads
  def printQuads(self):
    i = 0
    for q in self.quads:
      print(f'{i}:\t{q[0]}\t{q[1]}\t{q[2]}\t{q[3]}')
      i += 1

  # Debug function
  def debugStep(self):
    print("\t - - - DEBUG - - - ")
    print("\tsOperands ->", list(self.sOperands))
    print("\tsOperators ->", list(self.sOperators))
    print("\tsTypes ->", list(self.sTypes))
    print("\tsJumps ->", list(self.sJumps))
    print("\tsFuncs ->", list(self.sJumps))
    print("\tsDims ->", list(self.sDims))
    print("\t- CTES")
    for c in self.funcDir.cteTable.values():
      print(c.value, c.vartype, c.vAddr)
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
