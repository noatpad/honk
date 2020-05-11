from collections import defaultdict

# Variable class
class Var():
  def __init__(self, name, vartype, dimensions):
    self.name = name
    self.vartype = vartype
    self.dimensions = dimensions

# Function class
class Function():
  def __init__(self, name, returnType):
    self.name = name
    self.returnType = returnType
    self.varTable = None

  def addVar(self, name, vartype, dimensions):
    self.varTable[name] = Var(name, vartype, dimensions)

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
    self.currentType = "void"

  # Set name for global function
  def setGlobalFunction(self, globalFunc):
    self.globalFunc = globalFunc

  def setCurrentType(self, t):
    self.currentType = t

  # Adds function to the directory
  def addFunction(self, name):
    self.directory[name] = Function(name, self.currentType)
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
  def addVar(self, name, dimensions):
    self.directory[self.currentFunc].addVar(name, self.currentType, dimensions)

  # Returns desired variable
  def getVar(self, name, depth):
    ret = None
    if name in self.directory[self.currentFunc].varTable:     # First check local variables
      ret = self.directory[self.currentFunc].getVar(name)
    elif name in self.directory[self.globalFunc].varTable:    # Then check global variables
      ret = self.directory[self.globalFunc].getVar(name)
    else:     # Else, raise an error
      raise Exception(f'Variable "{name} does not exist!')

    if depth > ret.dimensions:
      raise Exception(f'{name} has {ret.dimensions} dimensions! (Trying to access depth {depth})')
    ret.dimensions = ret.dimensions - depth

    return ret

  # Returns a boolean if variable exists in local or global function
  def varExists(self, var):
    if var in self.directory[self.currentFunc].varTable or var in self.directory[self.globalFunc].varTable:
      return True
    return False
