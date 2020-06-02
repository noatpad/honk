
from collections import deque, defaultdict
import re
import numpy as np

class Var:
  def __init__(self, value, vartype):
    self.value = value
    self.vartype = vartype

  def getActualValue(self):
    if self.vartype == 'int':       # Return int value
      return int(self.value)
    elif self.vartype == 'float':   # Return float value
      return float(self.value)
    else:                           # Return bool or char value
      return self.value

class HonkVM:
  def __init__(self, obj, debug=False):
    # For debugging purposes
    self.debug = debug

    # Split lines and turn it into a queue
    lines = deque(obj.split('\n'))

    # Get and set ranges
    if lines.popleft() != '-> RANGES START':
      self._ded()

    self.globalRanges = (self._stringsToNumbers(lines.popleft().split('\t')))
    self.localRanges = (self._stringsToNumbers(lines.popleft().split('\t')))
    self.tempRanges = (self._stringsToNumbers(lines.popleft().split('\t')))
    self.cteRanges = (self._stringsToNumbers(lines.popleft().split('\t')))

    self._debugMsg('Init', f'Global ranges: {self.globalRanges}')
    self._debugMsg('Init', f'Local ranges: {self.localRanges}')
    self._debugMsg('Init', f'Temp ranges: {self.tempRanges}')
    self._debugMsg('Init', f'Cte ranges: {self.cteRanges}')

    if lines.popleft() != '->| RANGES END':
      self._ded()

    # Prepare memory
    self.memory = dict()

    # NOTE: Locals and temps are in their own "stacks" for function calls
    self.Globals = [None] * (self.globalRanges[4] - self.globalRanges[0])
    self.Locals = [[None] * (self.localRanges[4] - self.localRanges[0])]
    self.Temps = [[None] * (self.tempRanges[4] - self.tempRanges[0])]
    self.Ctes = [None] * (self.cteRanges[4] - self.cteRanges[0])

    self.LocalOffsets = [[0, 0, 0, 0]]
    self.TempOffsets = [[0, 0, 0, 0]]

    # Get and set constants
    if lines.popleft() != '-> CTES START':
      self._ded()

    while True:
      line = lines.popleft()

      if line == '->| CTES END':
        break

      data = line.split('\t')

      addr = int(data[2]) - self.cteRanges[0]
      self.Ctes[addr] = Var(data[0], data[1])
      self._debugMsg('Init', f'{data[0]} -> ({data[2]})')

    # Prepare ERAs
    self.eras = dict()

    # Get and set ERAs
    if lines.popleft() != '-> ERAS START':
      self._ded()

    while True:
      line = lines.popleft()

      if line == '->| ERAS END':
        break

      data = line.split('\t')
      func = data[0]
      local = self._stringsToNumbers(data[1:5])
      temp = self._stringsToNumbers(data[5:9])
      self.eras[func] = [local, temp]

      self._debugMsg('Init', f'ERA - {func} -> {[local, temp]}')

    # Get and set quads
    self.quads = deque()

    if lines.popleft() != '-> QUADS START':
      self._ded()

    while True:
      line = lines.popleft()

      if line == '->| QUADS END':
        break

      self.quads.append(line.split('\t'))

    # Prepare for function calls & matrix operations
    self.sCalls = deque()
    self.sReturns = deque()
    self.sParams = deque()
    self.localAux = [None]
    self.tempAux = [None]

    self.matHelper = (1, 1)

  # Covert array of strings into ints
  def _stringsToNumbers(self, arr):
    return [int(i) for i in arr]

  # VM init error
  def _ded(self):
    raise Exception('quack has commit die')

  # Debugger message
  def _debugMsg(self, quad, msg):
    if self.debug:
      if quad == 'Init':
        print(f'{quad}:\t{msg}')
      else:
        print(f'{quad}:\t{msg}')

  ## EXECUTION FUNCTIONS
  # Get matrix iterator for batch processes when needed
  def matIter(self):
    return self.matHelper[0] * self.matHelper[1]

  # Simple helper function to reset matHelper to 1,1
  def resetMatHelper(self):
    self.matHelper = (1, 1)

  # Check if address is a pointer (using regex)
  def isPointer(self, addr):
    return re.match(r'\(\d+,\)', str(addr))

  # Get type based on a memory range's address
  def getTypeByRange(self, addr, memRange):
    if self.isPointer(addr):
      ptr = addr[1:-2]
      self.getTypeByRange(self.getValue(ptr), memRange)
    elif addr < memRange[1]:
      return 'int'
    elif addr < memRange[2]:
      return 'float'
    elif addr < memRange[3]:
      return 'char'
    else:
      return 'bool'

  # Get type by address
  def getTypeByAddress(self, addr):
    if self.isPointer(addr):
      ptr = addr[1:-2]
      return self.getTypeByAddress(self.getValue(ptr))

    addr = int(addr)
    if addr < self.globalRanges[0] or addr >= self.localRanges[4]:
      raise Exception(f'Accessing prohibited memory! -> ({addr})')

    if addr < self.globalRanges[1]:
      return 'int'
    elif addr < self.globalRanges[2]:
      return 'float'
    elif addr < self.globalRanges[3]:
      return 'char'
    elif addr < self.globalRanges[4]:
      return 'bool'
    elif addr < self.localRanges[1]:
      return 'int'
    elif addr < self.localRanges[2]:
      return 'float'
    elif addr < self.localRanges[3]:
      return 'char'
    elif addr < self.localRanges[4]:
      return 'bool'

    raise Exception(f'How did we get here?? -> ({addr})')

  # Get index of memory for locals and temporary values
  def getLocalIndex(self, addr, memRange, offsets):
    i = -1
    for r in memRange[:-1]:
      if addr >= r:
        ret = addr - r
        i += 1
      if addr < r:
        break
    return ret + offsets[i]

  # Get a raw address
  def getVar(self, addr, matOffset=0):
    try:
      if self.isPointer(addr):
        ptr = addr[1:-2]
        return self.getVar(self.getValue(ptr), matOffset)

      addr = int(addr) + matOffset
      if addr < self.globalRanges[0] or addr >= self.cteRanges[4]:
        raise Exception(f'Getting from out of bounds! -> ({addr}{f" + {matOffset}" if matOffset else ""})')

      if addr < self.globalRanges[4]:
        return self.Globals[addr - self.globalRanges[0]]
      elif addr < self.localRanges[4]:
        rangeAddr = None
        if len(self.Locals) == 1:
          rangeAddr = addr - self.localRanges[0]
        else:
          rangeAddr = self.getLocalIndex(addr, self.localRanges, self.LocalOffsets[-1])
        return self.Locals[-1][rangeAddr]
      elif addr < self.tempRanges[4]:
        rangeAddr = None
        if len(self.Temps) == 1:
          rangeAddr = addr - self.tempRanges[0]
        else:
          rangeAddr = self.getLocalIndex(addr, self.tempRanges, self.TempOffsets[-1])
        return self.Temps[-1][rangeAddr]
      else:
        return self.Ctes[addr - self.cteRanges[0]]
    except:
      raise Exception(f'Var is not assigned in memory?! -> ({addr}{f" + {matOffset}" if matOffset else ""})')

  # Get a value from an address
  def getValue(self, addr, matOffset=0):
    try:
      return self.getVar(addr, matOffset).getActualValue()
    except AttributeError:
      raise AttributeError(f'Var is not assigned in memory?! -> ({addr}{f" + {matOffset}" if matOffset else ""})')

  # Set a value and save it in memory
  def setValue(self, value, addr, matOffset=0):
    if self.isPointer(addr):
      ptr = addr[1:-2]
      self.setValue(value, self.getValue(ptr, matOffset))
    else:
      addr = int(addr) + matOffset
      if addr < self.globalRanges[0] or addr >= self.tempRanges[4]:
        return Exception(f'Setting in invalid memory! -> ({addr}{f" + {matOffset}" if matOffset else ""})')

      elif addr < self.globalRanges[4]:
        rangeAddr = addr - self.globalRanges[0]
        self.Globals[rangeAddr] = Var(value, self.getTypeByRange(addr, self.globalRanges))
      elif addr < self.localRanges[4]:
        rangeAddr = None
        if len(self.Locals) == 1:
          rangeAddr = addr - self.localRanges[0]
        else:
          rangeAddr = self.getLocalIndex(addr, self.localRanges, self.LocalOffsets[-1])
        self.Locals[-1][rangeAddr] = Var(value, self.getTypeByRange(addr, self.localRanges))
      elif addr < self.tempRanges[4]:
        rangeAddr = None
        if len(self.Temps) == 1:
          rangeAddr = addr - self.tempRanges[0]
        else:
          rangeAddr = self.getLocalIndex(addr, self.tempRanges, self.TempOffsets[-1])
        self.Temps[-1][rangeAddr] = Var(value, self.getTypeByRange(addr, self.tempRanges))
      else:
        rangeAddr = addr - self.cteRanges[0]
        self.Ctes[rangeAddr] = Var(value, self.getTypeByRange(addr, self.cteRanges))

  # Reconstruct a matrix for matrix operations
  def constructMatrix(self, addr, offset=0):
    rows = self.matHelper[0 + offset]
    cols = self.matHelper[1 + offset]

    ret = []
    for i in range(rows):
      tmp = []
      for j in range(cols):
        tmp.append(self.getValue(addr, (i * cols) + j))
      ret.append(tmp)
    return ret

  # Allocate memory for function call
  def prepareERA(self, func):
    eraVals = self.eras[func]
    self.localAux = [None] * sum(eraVals[0])
    localEra = [0]
    for e in eraVals[0][:-1]:
      localEra.append(localEra[-1] + e)
    self.LocalOffsets.append(localEra)

    self.tempAux = [None] * sum(eraVals[1])
    tempEra = [0]
    for e in eraVals[1][:-1]:
      tempEra.append(tempEra[-1] + e)
    self.TempOffsets.append(tempEra)

    self.sParams.append([])

  # Pop out of function and return state as previously saved
  def popOutOfFunction(self):
    self.Locals.pop()
    self.Temps.pop()
    self.LocalOffsets.pop()
    self.TempOffsets.pop()
    return self.sCalls.pop()

  # Execute virtual machine
  def execute(self):
    ip = 0

    while True:
      quad = self.quads[ip]
      op = quad[0]

      ## - Let it begin. The super-switch case
      # Dual-op operation - Batch-compatible
      if op in ['+', '-', '/', '*', '%', '==', '!=', '<', '<=', '>', '>=', '&', '|']:
        for i in range(self.matIter()):
          left = self.getValue(quad[1], i)
          right = self.getValue(quad[2], i)

          result = None
          if op == '&':
            result = eval(f'{left} and {right}')
          elif op == '|':
            result = eval(f'{left} or {right}')
          else:
            result = eval(f'{left} {op} {right}')

          self.setValue(result, quad[3], i)
          self._debugMsg(ip, f'{left} {op} {right} = {result} -> ({quad[3]}{f" + {i}" if i else ""})')

      # Assignment - Batch-compatible
      elif op == '=':
        for i in range(self.matIter()):
          value = self.getValue(quad[1], i)
          self.setValue(value, quad[3], i)
          self._debugMsg(ip, f'{value} -> ({quad[3]}{f" + {i}" if i else ""})')

      # Matrix Determinant
      elif op == '$':
        mat = self.constructMatrix(quad[1])
        det = np.linalg.det(np.array(mat))
        self.setValue(det, quad[3])
        self._debugMsg(ip, f'Stored determinant value -> ({quad[3]})')

      # Matrix Transpose
      elif op == '!':
        mat = self.constructMatrix(quad[1])
        trans = np.array(mat).transpose().tolist()
        flat = [leaf for tree in trans for leaf in tree]

        for i in range(len(flat)):
          self.setValue(flat[i], quad[3], i)

        self._debugMsg(ip, f'Transposed matrix -> ({quad[3]} - {int(quad[3]) + len(flat) - 1})')

      # Matrix Inversion
      elif op == '?':
        mat = self.constructMatrix(quad[1])
        try:
          inv = np.linalg.inv(np.array(mat))
          flat = [leaf for tree in inv for leaf in tree]

          for i in range(len(flat)):
            self.setValue(flat[i], quad[3], i)

          self._debugMsg(ip, f'Inverted matrix -> ({quad[3]} - {int(quad[3]) + len(flat) - 1})')
        except:
          raise Exception(f'This matrix can\'t be inverted! -> ({quad[1]})')

      # Matrix helper
      elif op == 'MAT':
        rows = int(quad[1])
        cols = int(quad[2])
        self.matHelper = (rows, cols)

        self._debugMsg(ip, f'Preparing for matrix of size [{rows}][{cols}]')

      # Dot product
      elif op == '·':
        left = self.constructMatrix(quad[1])
        right = self.constructMatrix(quad[2], 1)
        dot = np.dot(np.array(left), np.array(right)).tolist()
        flat = [leaf for tree in dot for leaf in tree]

        for i in range(len(flat)):
          self.setValue(flat[i], quad[3], i)

        self._debugMsg(ip, f'Dot product -> ({quad[3]} - {int(quad[3]) + len(flat) - 1})')

      # Matrix helper specialized for dot products
      elif op == 'MAT·':
        m = int(quad[1])
        n = int(quad[2])
        p = int(quad[3])
        self.matHelper = (m, n, p)

        if self.debug:
          self._debugMsg(ip, f'Preparing for dot product {m}x{n} · {n}x{p}')

      # Go to #
      elif op == 'GoTo':
        self._debugMsg(ip, f'Jump -> {quad[3]}')
        ip = int(quad[3])
        continue

      # Go to # if false - Batch-compatible
      elif op == 'GoToF':
        boolean = True
        # If array/matrix, functions like an AND gate
        for i in range(self.matIter()):
          if not self.getValue(quad[1], i):
            boolean = False
            break

        if boolean:
          self._debugMsg(ip, f'Denied jump because true')
        else:
          self._debugMsg(ip, f'Allowed jump -> {quad[3]}')
          ip = int(quad[3])
          continue

      # Print - Batch-compatible
      elif op == 'PRINT':
        operand = quad[3]
        if re.match(r'\".*\"', operand):
          string = operand[1:-1]
          self._debugMsg(ip, f'Printing string: {string}')
          print(string)
        else:
          count = self.matIter()
          if count == 1:
            self._debugMsg(ip, f'Printing value: ({operand}) -> {value}')
            value = self.getValue(operand)
            print(str(value))
          else:
            self._debugMsg(ip, f'Printing array/matrix: ({operand} - {int(operand) + count - 1})')
            mat = self.constructMatrix(operand)

            if len(mat) == 1:
              print(mat[-1])
            else:
              print(mat)

      # Read input - Batch-compatible
      elif op == 'READ':
        addr = quad[3]
        input_type = self.getTypeByAddress(addr)
        for i in range(self.matIter()):
          self._debugMsg(ip, f'Requesting input for ({addr}{f" + {i}" if i else ""}), type: {input_type}...')

          # Repeat asking for input until correct
          while True:
            user_input = input("> ")
            try:
              value = None
              if input_type == 'int':
                value = int(user_input)
              elif input_type == 'float':
                value = float(user_input)
              elif input_type == 'bool':
                if value == 'True':
                  value = True
                elif value == 'False':
                  value = False
                else:
                  raise Exception("Invalid type!")
              elif input_type == 'char':
                value = user_input[0]
            except:
              print('! Invalid type! Try again...')
              continue
            else:
              self.setValue(value, addr, i)
              break


      # Verify matrix access dimension
      elif op == 'VERIFY':
        index = self.getValue(quad[1])
        limit = int(quad[3])
        self._debugMsg(ip, f'Verifying that {index} < {limit}...')

        if index < 0 or index >= limit:
          raise Exception(f'{index} is out of bounds of range 0-{limit - 1}')

      # Add a variable's base address to produce a pointer
      elif op == '+->':
        offset = self.getValue(quad[1])
        base = int(quad[2])
        self._debugMsg(ip, f'Creating pointer {offset} + {base} -> (({quad[3]}))')
        self.setValue(offset + base, quad[3])

      # ERA Preparation
      elif op == 'ERA':
        self.prepareERA(quad[3])
        self._debugMsg(ip, f'Preparing ERA for function -> {quad[3]}')

      # Send parameter to function call - Batch-compatible
      elif op == 'PARAM':
        for i in range(self.matIter()):
          param = self.getValue(quad[1], i)
          self.sParams[-1].append((param, quad[2], i))
          self._debugMsg(ip, f'Assigning value from ({quad[1]}{f" + {i}" if i else ""}) as parameter #{quad[3]}')

      # Go to function
      elif op == 'GoSub':
        self.sCalls.append(ip)
        self.Locals.append(self.localAux)
        self.Temps.append(self.tempAux)

        params = self.sParams.pop()
        for p in params:
          self.setValue(p[0], p[1], p[2])

        ip = int(quad[3])
        self._debugMsg(self.sCalls[-1], f'Jump to function: {self.sCalls[-1]} -> {ip}')
        continue

      # Pop back to original function after RETURN - Batch-compatible
      elif op == 'RETURN':
        ret = []
        for i in range(self.matIter()):
          self._debugMsg(ip, f'Return found! Assigning value -> ({quad[3]}{f" + {i}" if i else ""})')
          ret.append(self.getValue(quad[3], i))
        self.sReturns.append(ret)
        self._debugMsg(ip, f'Popping back! {ip} -> {self.sCalls[-1] + 1}')
        ip = self.popOutOfFunction()

      # Special quad to complete RETURN functionality - Batch-compatible
      elif op == '=>':
        ret = self.sReturns.pop()
        for i in range(len(ret)):
          self.setValue(ret[i], quad[3], i)
          self._debugMsg(ip, f'Assigned return value of {value} to address ({quad[3]}{f" + {i}" if i else ""})')

      # Pop back to original function after end of function
      elif op == 'EndFunc':
        self._debugMsg(ip, f'End of function found! Popping back! {ip} -> {self.sCalls[-1] + 1}')
        ip = self.popOutOfFunction()

      # Program End
      elif op == 'END':
        self._debugMsg(ip, 'HONK! (BYE!)')
        break
      else:
        self._debugMsg(ip, f'! -> {quad}')

      ip += 1
      if op not in ['MAT', 'MAT·']:
        self.resetMatHelper()

# # # # # # # # # # # # # # # # # # # # # # #
# # # # HECKING HONK LIKE NO TOMORROW # # # #
# # # # # # # # # # # # # # # # # # # # # # #
def honk(obj, debug=False):
  vm = HonkVM(obj, debug)
  vm.execute()
