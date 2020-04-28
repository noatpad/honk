
class Var():
  def __init__(self, name, vartype):
    self.name = name
    self.vartype = vartype
    self.value = None

# TODO: Implement binary search tree in place of list for var table
class Function():
  def __init__(self, name, returnType):
    self.name = name
    self.returnType = returnType
    self.varTable = None

  def hasVarTable(self):
    return self.varTable != None

  def makeVarTable(self):
    self.varTable = []

  def addVar(self, name, vartype):
    self.varTable.append(Var(name, vartype))

# TODO: Implement binary search tree in place of list for directory
class FunctionDirectory():
  def __init__(self):
    self.directory = []
    self.currentFunc = 0

  def addFunction(self, name, returnType):
    self.directory.append(Function(name, returnType))

  def addVarTable(self):
    if self.directory[self.currentFunc].hasVarTable() is False:
      self.directory[self.currentFunc].makeVarTable()

  def findVar(self, var):
    for i in self.directory[self.currentFunc].varTable:
      if var == i.name:
        return True
    return False

  def addVar(self, name, vartype):
    self.directory[self.currentFunc].addVar(name, vartype)
