
from collections import defaultdict

## -- CONSTANT
class Constant():
  def __init__(self, value, vartype, vAddr):
    self.value = value
    self.vartype = vartype
    self.vAddr = vAddr

## -- VARIABLE
class Var():
  def __init__(self, name, vartype, dimensions, vAddr):
    self.name = name
    self.vartype = vartype
    self.dimensions = dimensions
    self.vAddr = vAddr


## -- FUNCTION
class Function():
  def __init__(self, name, returnType):
    self.name = name
    self.returnType = returnType
    self.quadStart = None
    self.varTable = None
    self.cteTable = None
    self.paramTable = []
    # self.tempCount = 0
    self.era = []

  ## GETTERS
  # Get variable
  def getVar(self, name):
    return self.varTable[name]

  def getCte(self, value):
    return self.cteTable[value]

  ## SETTERS
  # Set start of quad for function
  def setQuadStart(self, qs):
    self.quadStart = qs

  # # Set number of temporals used in function
  # def setTempCount(self, count):
  #   self.tempCount = count

  # Set "era" (local and temporary counters)
  def setEra(self, era):
    self.era = era

  ## PUSH/ADD
  # Add variable
  def addVar(self, name, vartype, dimensions, vAddr):
    self.varTable[name] = Var(name, vartype, dimensions, vAddr)

  # Add constant
  def addCte(self, value, vartype, vAddr):
    self.cteTable[value] = Constant(value, vartype, vAddr)

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
  def __init__(self):
    self.directory = dict()
    self.globalFunc = None
    self.currentFunc = None
    self.currentType = "void"
    self.paramCount = 0

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

  # Set start of quad for function
  def setQuadStart(self, qs):
    self.directory[self.currentFunc].setQuadStart(qs)

  # Set number of temporals used in function
  # def setTempCountForFunc(self, count):
  #   self.directory[self.currentFunc].setTempCount(count)

  # Set "era" for function
  def setEra(self, era):
    self.directory[self.currentFunc].setEra(era)

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

  # Returns virtual address of desired variable
  def getVAddr(self, name):
    ret = None
    if name in self.directory[self.currentFunc].varTable:     # First check local variables
      ret = self.directory[self.currentFunc].getVar(name)
    elif name in self.directory[self.globalFunc].varTable:    # Then check global variables
      ret = self.directory[self.globalFunc].getVar(name)
    # elif name in self.directory[self.getCurrentFunc].cteTable:    # Finally check the constants
    #   ret = self.directory[self.currentFunc].getCte(name)
    else:     # Else, raise an error
      return name   # NOTE: It's an address if it reaches here?
      # raise Exception(f'Variable "{name}" does not exist!')

    return ret.vAddr

  # Get current function in parser
  def getCurrentFunc(self):
    return self.currentFunc

  # Get currently used type in parser
  def getCurrentType(self):
    return self.currentType

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

  # Get param count of function
  def getParamCount(self):
    return self.paramCount

  # Get ERA of function
  def getEra(self, func):
    return self.directory[self.currentFunc].era

  ## PUSH/ADD
  # Adds function to the directory
  def addFunction(self, name):
    self.directory[name] = Function(name, self.currentType)
    self.currentFunc = name

  # Add parameters to current function
  def addFuncParam(self):
    self.directory[self.currentFunc].addParam(self.currentType)

  # Add variable to the current function's var table
  def addVar(self, name, dimensions, vAddr):
    self.directory[self.currentFunc].addVar(name, self.currentType, dimensions, vAddr)

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

  # Returns a boolean if variable exists in local or global function
  def varExists(self, var):
    if var in self.directory[self.currentFunc].varTable or var in self.directory[self.globalFunc].varTable:
      return True
    return False
