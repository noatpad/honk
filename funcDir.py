from collections import defaultdict

# Variable class
class Var():
  def __init__(self, name, vartype):
    self.name = name
    self.vartype = vartype

# Function class
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

  def createVarTable(self):
    self.varTable = dict()

# Function Directory class
class FunctionDirectory():
  def __init__(self):
    self.directory = dict()
    self.currentFunc = None
    self.globalFunc = None

  def setGlobalFunction(self, globalFunc):
    self.globalFunc = globalFunc

  def addFunction(self, name, returnType):
    self.directory[name] = Function(name, returnType)
    self.currentFunc = name

  def functionExists(self, func):
    if func in self.directory:
      return True
    return False

  def createVarTable(self):
    if self.directory[self.currentFunc].varTable is None:
      self.directory[self.currentFunc].createVarTable()

  def deleteVarTable(self):
    self.directory[self.currentFunc].deleteVarTable()
    self.currentFunc = self.globalFunc

  def addVar(self, name, vartype):
    self.directory[self.currentFunc].addVar(name, vartype)

  def getVar(self, name, depth):
    if name in self.directory[self.currentFunc].varTable:
      ret = self.directory[self.currentFunc].getVar(name)
    elif name in self.directory[self.globalFunc].varTable:
      ret = self.directory[self.globalFunc].getVar(name)
    else:
      raise Exception(f'Variable "{name} does not exist!')

    ret.vartype = (ret.vartype[0], ret.vartype[1] - depth)
    return ret

  def varExists(self, var):
    if var in self.directory[self.currentFunc].varTable:
      return True
    return False
