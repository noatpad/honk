
class VirtualDirectory:
  def __init__(self):
    # Virtual address ranges
    # (|| int || float || char || bool ||)
    self.globalRanges = (1000, 4000, 7000, 8000, 9000)
    self.localRanges = (9000, 13000, 17000, 18500, 20000)
    self.tempRanges = (20000, 24000, 28000, 29500, 31000)
    self.cteRanges = (31000, 34000, 37000, 37500, 38000)

    # Variable counters
    # [int, float, char, bool]
    self.globalCounter = [0, 0, 0, 0]
    self.localCounter = [0, 0, 0, 0]
    self.tempCounter = [0, 0, 0, 0]
    self.cteCounter = [0, 0, 0, 0]

    # Total counter
    self.totalCounter = 0

  # Get a function's ERA
  def getEra(self):
    return [self.localCounter, self.tempCounter]

  # Get all ranges
  def getRanges(self):
    return [self.globalRanges, self.localRanges, self.tempRanges, self.cteRanges]

  # Reset local counters to 0
  def resetLocalCounters(self):
    self.localCounter = [0, 0, 0, 0]
    self.tempCounter = [0, 0, 0, 0]

  # Set space and counters based on a variable's needs
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

    # Update total counter
    self.totalCounter += space

    # Select scope (with validation checks)
    if scope == 'main':   # Global
      if self.globalRanges[v] + self.globalCounter[v] + space >= self.globalRanges[v + 1] - 1:
        raise Exception(f"Out of bounds! {vartype} in {scope}")
      self.globalCounter[v] += space
      return self.globalRanges[v] + self.globalCounter[v] - 1
    elif scope == 'temp':   # Temp
      if self.tempRanges[v] + self.tempCounter[v] + space >= self.tempRanges[v + 1] - 1:
        raise Exception(f"Out of bounds! {vartype} in {scope}")
      self.tempCounter[v] += space
      return self.tempRanges[v] + self.tempCounter[v] - 1
    elif scope == 'cte':    # Constants
      if self.cteRanges[v] + self.cteCounter[v] + space >= self.cteRanges[v + 1] - 1:
        raise Exception(f"Out of bounds! {vartype} in {scope}")
      self.cteCounter[v] += space
      return self.cteRanges[v] + self.cteCounter[v] - 1
    else:                   # Local (any local function)
      if self.localRanges[v] + self.localCounter[v] + space >= self.localRanges[v + 1] - 1:
        raise Exception(f"Out of bounds! {vartype} in {scope}")
      self.localCounter[v] += space
      return self.localRanges[v] + self.localCounter[v] - 1

    raise Exception(f'Invalid vartype/scope?! -> {vartype}, {scope}')

  # Generate virtual address for a variable
  def generateVirtualAddress(self, scope, vartype):
    return self.setSpace(scope, vartype, 1)

  # Make more room for array variables
  def makeSpaceForArray(self, scope, vartype, value):
    self.setSpace(scope, vartype, value - 1)
