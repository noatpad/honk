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

  # Set name for global function
  def setGlobalFunction(self, globalFunc):
    self.globalFunc = globalFunc

  # Adds function to the directory
  def addFunction(self, name, returnType):
    self.directory[name] = Function(name, returnType)
    self.currentFunc = name

  # Return boolean if function exists
  def functionExists(self, func):
    if func in self.directory:
      return True
    return False

  # Creates var table for current function
  def createVarTable(self):
    if self.directory[self.currentFunc].varTable is None:
      self.directory[self.currentFunc].createVarTable()

  # Deletes var table for current function
  def deleteVarTable(self):
    self.directory[self.currentFunc].deleteVarTable()
    self.currentFunc = self.globalFunc

  # Add variable to the current function's var table
  def addVar(self, name, vartype):
    self.directory[self.currentFunc].addVar(name, vartype)

  # Returns desired variable
  def getVar(self, name, depth):
    if name in self.directory[self.currentFunc].varTable:     # First check local variables
      ret = self.directory[self.currentFunc].getVar(name)
    elif name in self.directory[self.globalFunc].varTable:    # Then check global variables
      ret = self.directory[self.globalFunc].getVar(name)
    else:     # Else, raise an error
      raise Exception(f'Variable "{name} does not exist!')

    ret.vartype = (ret.vartype[0], ret.vartype[1] - depth)
    return ret

  # Returns a boolean if variable exists in local or global function
  def varExists(self, var):
    if var in self.directory[self.currentFunc].varTable or var in self.directory[self.globalFunc].varTable:
      return True
    return False
