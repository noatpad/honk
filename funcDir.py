from collections import defaultdict

class Var():
  def __init__(self, name, vartype):
    self.name = name
    self.vartype = vartype

class Function():
  def __init__(self, name, returnType):
    self.name = name
    self.returnType = returnType
    self.varTable = None

  def addVar(self, name, vartype):
    self.varTable[name] = Var(name,vartype)

  def getVar(self, name):
    return self.varTable[name]

  def deleteVarTable(self):
    self.varTable = None

  def hasVarTable(self):
    return self.varTable != None

  def makeVarTable(self):
    self.varTable = dict()

class FunctionDirectory():
  def __init__(self):
    self.directory = dict()
    self.currentFunc = None
    self.globalFunc = None

  def setGlobalFuncton(self, globalFunc):
    self.globalFunc = globalFunc

  def addFunction(self, name, returnType):
    self.directory[name] = Function(name, returnType)
    self.currentFunc = name

  def addVarTable(self):
    if self.directory[self.currentFunc].hasVarTable() is False:
      self.directory[self.currentFunc].makeVarTable()

  def addVar(self, name, vartype):
    self.directory[self.currentFunc].addVar(name, vartype)

  def getVar(self, name, depth):
    if name in self.directory[self.currentFunc].varTable:
      ret = self.directory[self.currentFunc].getVar(name)
    else:
      ret = self.directory[self.globalFunc].getVar(name)

    ret.vartype = (ret.vartype[0], ret.vartype[1] - depth)
    return ret

  def deleteVarTable(self):
    if self.directory[self.currentFunc].hasVarTable() is True:
      self.directory[self.currentFunc].makeVarTable()

  def findFunction(self, func):
    if func in self.directory:
      return True
    return False

  def findVar(self, var):
    if var in self.directory[self.currentFunc].varTable:
      return True
    return False
