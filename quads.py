
from collections import deque
from semanticCube import getDuoResultType

class Quads:
  def __init__(self):
    self.sOperands = deque()
    self.sOperators = deque()
    self.sTypes = deque()
    self.sJumps = deque()
    self.quads = deque()
    self.quadCount = 0
    self.tempCount = 0

  # Push variable name and type to their respective stacks
  def pushVar(self, name, vartype):
    self.sOperands.append(name)
    self.sTypes.append(vartype)

  # Push operator to stack
  def pushOperator(self, op):
    self.sOperators.append(op)

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
      raise Exception("Type mismatch!")

  # Append if quadruple
  def addIfQuad(self):
    result_type = self.sTypes.pop()
    if result_type == ('bool', 0):
      result = self.sOperands.pop()
      self.addQuad(('GoToF', result, None, None))
      self.sJumps.append(self.quadCount - 1)
    else:
      raise Exception("Type mismatch!")

  # Prepare and append else quadruple
  def addElseQuad(self):
    self.addQuad(('GoTo', None, None, None))
    falseJump = self.sJumps.pop()
    self.sJumps.append(self.quadCount - 1)
    self.completeQuad(falseJump, self.quadCount)

  # Complete end of if quadruple
  def completeIfQuad(self):
    end = self.sJumps.pop()
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
        raise Exception("Type mismatch!")

  def printQuads(self):
    i = 0
    for q in self.quads:
      print(f'{i}:\t{q[0]} {q[1]} {q[2]} {q[3]}')
      i += 1
