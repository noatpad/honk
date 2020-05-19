from collections import defaultdict

## -- VARIABLE
class Var():
  def __init__(self, name, vartype, dimensions):
    self.name = name
    self.vartype = vartype
    self.dimensions = dimensions


## -- FUNCTION
class Function():
  def __init__(self, name, returnType):
    self.name = name
    self.returnType = returnType
    self.quadStart = None
    self.varTable = None
    self.paramTable = []
    self.tempCount = 0

  ## GETTERS
  # Get variable
  def getVar(self, name):
    return self.varTable[name]

  ## SETTERS
  # Set start of quad for function
  def setQuadStart(self, qs):
    self.quadStart = qs

  # Set number of temporals used in function
  def setTempCount(self, count):
    self.tempCount = count

  ## PUSH/ADD
  # Add variable
  def addVar(self, name, vartype, dimensions):
    self.varTable[name] = Var(name, vartype, dimensions)

  # Add parameter
  def addParam(self, vartype):
    self.paramTable.append(vartype)

  # Create var table
  def createVarTable(self):
    self.varTable = dict()

  # Delete var table
  def deleteVarTable(self):
    self.varTable = None



## -- FUNCTION DIRECTORY
class FunctionDirectory():
  def __init__(self):
    self.directory = dict()
    self.currentFunc = None
    self.globalFunc = None
    self.currentType = "void"
    self.paramCount = 0

  ## SETTERS
  # NOTE: `currentFunc` is set in addFunction()
  # Set name for global function
  def setGlobalFunction(self, globalFunc):
    self.globalFunc = globalFunc

  # Set name for current function
  def setCurrentFunction(self, currentFunc):
    self.currentFunc = currentFunc

  # Set current type used in parser
  def setCurrentType(self, t):
    self.currentType = t

  # Set start of quad for function
  def setQuadStart(self, qs):
    self.directory[self.currentFunc].setQuadStart(qs)

  # Set number of temporals used in function
  def setTempCountForFunc(self, count):
    self.directory[self.currentFunc].setTempCount(count)

  # Increment param count of function by 1
  def incrementParamCount(self):
    self.paramCount += 1

  ## GETTERS
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

  # Get parameter of function
  def getParamOfFunc(self, func):
    return self.directory[func].paramTable[self.paramCount]

  # Get quadStart of function
  def getQuadStartOfFunc(self, func):
    return self.directory[func].quadStart

  # Get param count of function
  def getParamCount(self):
    return self.paramCount

  ## PUSH/ADD
  # Adds function to the directory
  def addFunction(self, name):
    self.directory[name] = Function(name, self.currentType)
    self.currentFunc = name

  # Add parameters to current function
  def addFuncParam(self):
    self.directory[self.currentFunc].addParam(self.currentType)

  # Add variable to the current function's var table
  def addVar(self, name, dimensions):
    self.directory[self.currentFunc].addVar(name, self.currentType, dimensions)

  ## FUNCTIONS
  # Creates var table for current function
  def createVarTable(self):
    if self.directory[self.currentFunc].varTable is None:
      self.directory[self.currentFunc].createVarTable()

  # Deletes var table for current function
  def deleteVarTable(self):
    self.directory[self.currentFunc].deleteVarTable()
    self.currentFunc = self.globalFunc

  # Verify number of parameters of function
  def verifyParamCount(self, func):
    # print(self.paramCount, len(self.directory[func].paramTable))
    return (self.paramCount == len(self.directory[func].paramTable))

  # Return boolean if function exists
  def functionExists(self, func):
    if func in self.directory:
      return True
    return False

  # Returns a boolean if variable exists in local or global function
  def varExists(self, var):
    if var in self.directory[self.currentFunc].varTable or var in self.directory[self.globalFunc].varTable:
      return True
    return False
