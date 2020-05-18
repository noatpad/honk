
from collections import deque
from semanticCube import getDuoResultType

# TODO: Add validation for dimensions
class QuadManager:
  def __init__(self):
    self.sOperands = deque()
    self.sOperators = deque()
    self.sTypes = deque()
    self.sJumps = deque()
    self.sFuncs = deque()
    self.quads = deque()
    self.quadCount = 0
    self.tempCount = 0

  # Get current quad counter
  def getQuadCount(self):
    return self.quadCount

  # Reset temporal counter
  def resetTemporals(self):
    self.tempCount = 0

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

  def getTopFunction(self):
    return self.sFuncs[-1]

  def popFunction(self):
    return self.sFuncs.pop()

  # Pop operator from stack
  def popOperator(self):
    return self.sOperators.pop()

  # Pop sTypes from stack
  def popType(self):
    return self.sTypes.pop()

  # General function to add quads
  def addQuad(self, quad):
    self.quads.append(quad)
    self.quadCount += 1

  # General function to complete quad
  def completeQuad(self, index, jump):
    quadToChange = list(self.quads[index])
    quadToChange[3] = jump
    self.quads[index] = tuple(quadToChange)

  # Append assignment quadruple
  def addAssignQuad(self):
    right_op = self.sOperands.pop()
    right_type = self.sTypes.pop()
    left_op = self.sOperands.pop()
    left_type = self.sTypes.pop()
    operator = self.sOperators.pop()

    result_type = getDuoResultType(left_type, right_type, operator)
    if result_type:
      self.addQuad((operator, right_op, None, left_op))
    else:
      raise Exception(f'Type mismatch! {left_type} {operator} {right_type}')

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

  # Prepare for `while` block
  def prepareWhile(self):
    self.sJumps.append(self.quadCount)

  # Append quadruple for `while` block
  # NOTE: It's practically identical to addIfQuad()
  def addWhileQuad(self):
    result_type = self.sTypes.pop()
    if result_type == 'bool':
      result = self.sOperands.pop()
      self.addQuad(('GoToF', result, None, None))
      self.sJumps.append(self.quadCount - 1)
    else:
      raise Exception(f'Type mismatch! {result_type} != bool')

  # Complete quadruple for `while` block
  def completeWhileQuad(self):
    end = self.sJumps.pop()
    ret = self.sJumps.pop()
    self.addQuad(('GoTo', None, None, ret))
    self.completeQuad(end, self.quadCount)

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
        result = 't' + str(self.tempCount)
        self.addQuad((operator, left_op, right_op, result))
        self.sOperands.append(result)
        self.sTypes.append(result_type)
        self.tempCount += 1
      else:
        raise Exception(f'Type mismatch! {left_type} {operator} {right_type}')

  # Append PARAM Quad
  def addParamQuad(self, target_param, k):
    argument = self.sOperands.pop()
    argument_type = self.sTypes.pop()
    if argument_type == target_param:
      self.addQuad(('PARAM', argument, None, k))
    else:
      raise Exception(f'Wrong param type! {argument_type} {target_param}')

  # Append ERA quad
  # TODO: Ask dafaq is this and where to get the size of said dafaq
  def addEraQuad(self):
    self.addQuad(('ERA', None, None, None))

  # Append EndFunc quad
  def addEndFuncQuad(self):
    self.addQuad(('EndFunc', None, None, None))

  # Append GOSUB quad
  def addGoSubQuad(self, func, qs):
    self.addQuad(('GOSUB', func, None, qs))

  # Append END Quad
  def addEndQuad(self):
    self.addQuad(('END', None, None, None))

  def printQuads(self):
    i = 0
    for q in self.quads:
      print(f'{i}:\t{q[0]}\t{q[1]}\t{q[2]}\t{q[3]}')
      i += 1
