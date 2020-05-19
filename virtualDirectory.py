
class VirtualDirectory:
  def __init__(self):
    # TODO: Make booleans only constants
    # NOTE: Remember constants are distributed throughout the whole program
    # Virtual address ranges
    # (|| int || float || char || bool ||)
    # self.globalRanges = (1000, 4000, 6500, 7999, 7999)
    # self.localRanges = (8000, 12000, 15000, 16999, 16999)
    # self.tempRanges = (17000, 22000, 25000, 26999, 26999)
    # self.cteRanges = (27000, 28500, 30000, 31000, 32000)
    self.globalRanges = (1000, 4000, 6500, 8000, 8999)
    self.localRanges = (9000, 13000, 16000, 17000, 17999)
    self.tempRanges = (18000, 23000, 26000, 27000, 27999)
    self.cteRanges = (27000, 28500, 30000, 31000, 32000)

    # Variable counters
    # [int, float, char, bool]
    self.globalCounter = [0, 0, 0, 0]
    self.localCounter = [0, 0, 0, 0]
    self.tempCounter = [0, 0, 0, 0]
    self.cteCounter = [0, 0, 0, 0]

    # Total counter
    self.totalCounter = 0

  def getEra(self):
    return [self.localCounter, self.tempCounter]

  def resetLocalCounters(self):
    self.localCounter = [0, 0, 0, 0]
    self.tempCounter = [0, 0, 0, 0]

  def setSpace(self, scope, vartype, space):
    # Select variable type
    v = None
    if vartype == 'int':
      v = 0
    elif vartype == 'float':
      v = 1
    elif vartype == 'char':
      v = 2
    elif vartype == 'bool':
      v = 3

    # Check for invalid bool
    # if v == 3 and (scope in ['global', 'local', 'temp']):
    #   raise Exception(f"Can't set {vartype} in {scope}!")

    # Update total counter
    self.totalCounter += space

    # Select scope (with validation checks)
    if scope == 'global':   # Global
      if self.globalRanges[v] + self.globalCounter[v] + space >= self.globalRanges[v + 1]:
        raise Exception(f"Out of bounds! {vartype} in {scope}")
      self.globalCounter[v] += space
      return self.globalRanges[v] + self.globalCounter[v] - 1
    elif scope == 'temp':   # Temp
      if self.tempRanges[v] + self.tempCounter[v] + space >= self.tempRanges[v + 1]:
        raise Exception(f"Out of bounds! {vartype} in {scope}")
      self.tempCounter[v] += space
      return self.tempRanges[v] + self.tempCounter[v] - 1
    elif scope == 'cte':    # Constants
      if self.cteRanges[v] + self.cteCounter[v] + space >= self.cteRanges[v + 1]:
        raise Exception(f"Out of bounds! {vartype} in {scope}")
      self.cteCounter[v] += space
      return self.cteRanges[v] + self.cteCounter[v] - 1
    else:                   # Local (any local function)
      if self.localRanges[v] + self.localCounter[v] + space >= self.localRanges[v + 1]:
        raise Exception(f"Out of bounds! {vartype} in {scope}")
      self.localCounter[v] += space
      return self.localRanges[v] + self.localCounter[v] - 1

    raise Exception(f'Invalid vartype/scope?! -> {vartype}, {scope}')

  def generateVirtualAddress(self, scope, vartype):
    return self.setSpace(scope, vartype, 1)

  def makeSpaceForArray(self, scope, vartype, value):
    self.setSpace(scope, vartype, value)
