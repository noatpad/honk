from collections import defaultdict

class Var():
  def __init__(self, name, vartype):
    self.name = name
    self.vartype = vartype
    self.value = None

class Function():
  def __init__(self, name, returnType):
    self.name = name
    self.returnType = returnType
    self.varTable = None

  def hasVarTable(self):
    return self.varTable != None

  def makeVarTable(self):
    self.varTable = dict()

  def addVar(self, name, vartype):
    self.varTable[name] = Var(name,vartype)
    #self.varTable.append(Var(name, vartype))

class FunctionDirectory():
  def __init__(self):
    self.directory = dict()
    self.currentFunc = None

  def addFunction(self, name, returnType):
    self.directory[name] = Function(name,returnType)
    self.currentFunc = name
    #self.directory.append(Function(name, returnType))

  def addVarTable(self):
    if self.directory[self.currentFunc].hasVarTable() is False:
      self.directory[self.currentFunc].makeVarTable()

  def findVar(self, var):
    if var in self.directory[self.currentFunc].varTable:
      return True
    return False
    #for i in self.directory[self.currentFunc].varTable:
    #  if var == i.name:
    #    return True
    #return False

  def addVar(self, name, vartype):
    self.directory[self.currentFunc].addVar(name, vartype)

  