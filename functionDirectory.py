
from collections import defaultdict

## -- CONSTANT
class Constant():
  def __init__(self, value, vartype, vAddr):
    self.value = value
    self.vartype = vartype
    self.vAddr = vAddr



## -- VARIABLE
class Var():
  def __init__(self, name, vartype, vAddr):
    self.name = name
    self.vartype = vartype
    self.dimensions = []
    self.mDim = None
    self.vAddr = vAddr



## -- FUNCTION
class Function():
  def __init__(self, name, returnType, debug):
    self.debug = debug
    self.name = name
    self.returnType = returnType
    self.quadStart = None
    self.varTable = None
    self.cteTable = None
    self.paramTable = []
    self.era = []

  ## GETTERS
  # Get variable
  def getVar(self, name):
    return self.varTable[name]

  def getCte(self, value):
    return self.cteTable[value]

  # Get dimensions of a specified variable
  def getDimensionsOfVar(self, name):
    return self.varTable[name].dimensions

  # Get mDim from a specified variable
  def getMdim(self, name):
    return self.varTable[name].mDim

  ## SETTERS
  # Set start of quad for function
  def setQuadStart(self, qs):
    self.quadStart = qs

  # Set "era" (local and temporary counters)
  def setEra(self, era):
    self.era = era

  # Set mDim of a specified var
  def setMDimToVar(self, name, mdim):
    self.varTable[name].mDim = mdim

  ## PUSH/ADD
  # Add variable
  def addVar(self, name, vartype, vAddr):
    self.varTable[name] = Var(name, vartype, vAddr)

    if self.debug:
      v = self.varTable[name]
      print(f'\t\t\t\t\t> VAR: {v.name} - {v.vartype} -> {v.vAddr}')

  # Add dimension to var
  def addDimensionToVar(self, var, dim):
    self.varTable[var].dimensions.append(dim)

    if self.debug:
      v = self.varTable[var]
      print(f'\t\t\t\t\t>> VAR: {v.name} - {v.vartype}{v.dimensions} -> {v.vAddr}')

  # Add constant
  def addCte(self, value, vartype, vAddr):
    self.cteTable[value] = Constant(value, vartype, vAddr)

    if self.debug:
      c = self.cteTable[value]
      print(f'\t\t\t\t\t> CTE: {c.value} - {c.vartype} -> {c.vAddr}')

  # Add parameter
  def addParam(self, vartype):
    self.paramTable.append(vartype)

  # Create var table
  def createVarTable(self):
    self.varTable = dict()
    self.cteTable = dict()

  # Delete var table
  def deleteVarTable(self):
    self.varTable = None
    self.cteTable = None



## -- FUNCTION DIRECTORY
class FunctionDirectory():
  def __init__(self, debug):
    self.debug = debug
    self.directory = dict()
    self.globalFunc = None
    self.currentFunc = None
    self.currentType = "void"
    self.paramCount = 0
    self.varHelper = None

  ## SETTERS
  # NOTE: `currentFunc` is set in addFunction()
  # Set name for global function
  def setGlobalFunction(self):
    self.globalFunc = 'global'

  # Set name for current function
  def setCurrentFunction(self, currentFunc):
    self.currentFunc = currentFunc

  # Set current type used in parser
  def setCurrentType(self, t):
    self.currentType = t

  # Set var helper used in parser
  def setVarHelper(self, var):
    self.varHelper = var

  # Set start of quad for function
  def setQuadStart(self, qs):
    self.directory[self.currentFunc].setQuadStart(qs)

  # Set "era" for function
  def setEra(self, era):
    self.directory[self.currentFunc].setEra(era)

  # Set mDim to a specified variable
  def setMDimToVar(self, name, mdim):
    self.directory[self.currentFunc].setMDimToVar(name, mdim)

  # Increment param count of function by 1
  def incrementParamCount(self):
    self.paramCount += 1

  ## GETTERS
  # TODO: Search through constants
  # TODO: Make a centralized variable getter (some functions won't work locally)
  # Returns desired variable
  def getVar(self, name):
    ret = None
    # Priority: Local -> Global -> Constants
    if name in self.directory[self.currentFunc].varTable:
      ret = self.directory[self.currentFunc].getVar(name)
    elif name in self.directory[self.globalFunc].varTable:
      ret = self.directory[self.globalFunc].getVar(name)
    else:     # Else, raise an error
      raise Exception(f'Variable "{name} does not exist!')

    return ret

  # Returns virtual address of desired variable
  def getVAddr(self, name):
    ret = None
    if name in self.directory[self.currentFunc].varTable:
      ret = self.directory[self.currentFunc].getVar(name)
    elif name in self.directory[self.globalFunc].varTable:
      ret = self.directory[self.globalFunc].getVar(name)
    else:
      return name   # NOTE: It's an address if it reaches here?

    return ret.vAddr

  # Get dimensions of a specified variable
  def getDimensionsOfVar(self, name):
    return self.directory[self.currentFunc].getDimensionsOfVar(name)

  # Get mDim from a specified variable
  def getMdim(self, name):
    return self.directory[self.currentFunc].getMdim(name)

  # Get parameter of function
  def getParamOfFunc(self, func):
    return self.directory[func].paramTable[self.paramCount]

  # Get quadStart of function
  def getQuadStartOfFunc(self, func):
    return self.directory[func].quadStart

  # Get a function's return type
  def getReturnTypeOfFunc(self, func):
    return self.directory[func].returnType

  # Get current function's return type
  def getCurrentFuncReturnType(self):
    return self.directory[self.currentFunc].returnType

  # Get ERA of function
  def getEra(self, func):
    return self.directory[self.currentFunc].era

  ## PUSH/ADD
  # Adds function to the directory
  def addFunction(self, name):
    self.directory[name] = Function(name, self.currentType, self.debug)
    self.currentFunc = name

    if self.debug:
      print(f'-- {self.currentFunc} - {self.currentType}')

  # Add parameters to current function
  def addFuncParam(self):
    self.directory[self.currentFunc].addParam(self.currentType)

  # Add variable to the current function's var table
  def addVar(self, name, vAddr):
    self.directory[self.currentFunc].addVar(name, self.currentType, vAddr)

  # Add dimension to a specified variable in the current scope
  def addDimensionToVar(self, var, dim):
    self.directory[self.currentFunc].addDimensionToVar(var, dim)

  # Add constant to the current function's constants table
  def addCte(self, value, vartype, vAddr):
    self.directory[self.currentFunc].addCte(value, vartype, vAddr)

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

  # Returns a boolean if variable exists in local or global scope
  def varExists(self, var):
    if var in self.directory[self.currentFunc].varTable or var in self.directory[self.globalFunc].varTable:
      return True
    return False

  # Returns a boolean if variable is available to declare in current context
  def varAvailable(self, var):
    if var not in self.directory[self.currentFunc].varTable:
      return True
    return False
