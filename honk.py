
from collections import deque, defaultdict
import re

class Address:
  def __init__(self, value, vartype):
    self.value = value
    self.vartype = vartype

  def getActualValue(self):
    if self.vartype == 'int':
      return int(self.value)
    elif self.vartype == 'float':
      return float(self.value)
    elif self.vartype == 'bool':
      return (self.value == 'True')
    else:
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

    self.Globals = [None] * (self.globalRanges[4] - self.globalRanges[0])
    self.Locals = [None] * (self.localRanges[4] - self.localRanges[0])
    self.Temps = [None] * (self.tempRanges[4] - self.tempRanges[0])
    self.Ctes = [None] * (self.cteRanges[4] - self.cteRanges[0])
    self.GlobalCount = 0
    self.LocalCount = 0
    self.TempCount = 0
    self.CteCount = 0

    # Get and set constants
    if lines.popleft() != '-> CTES START':
      self._ded()

    while True:
      line = lines.popleft()

      if line == '->| CTES END':
        break

      data = line.split('\t')
      # self.memory[int(data[2])] = Address(int(data[0]), data[1])
      # self._debugMsg('Init', f'{data[0]} -> ({data[2]})')

      addr = int(data[2]) - self.cteRanges[0]
      self.Ctes[addr] = Address(data[0], data[1])
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

  # Covert array of strings into ints
  def _stringsToNumbers(self, arr):
    return [int(i) for i in arr]

  # VM init error
  def _ded(self):
    raise Exception('quack has commit die')

  # Debugger message
  def _debugMsg(self, quad, msg):
    if self.debug:
      print(f'{quad}: {msg}')

  ## EXECUTION FUNCTIONS
  # Get type based on a memory range's address
  def getTypeByRange(self, addr, memRange):
    if addr < memRange[1]:
      return 'int'
    elif addr < memRange[2]:
      return 'float'
    elif addr < memRange[3]:
      return 'char'
    else:
      return 'bool'

  # Get a value from an address
  def getValue(self, addr):
    try:
      if re.match(r'\(\d+,\)', addr):
        ptr = addr[1:-2]
        return self.getValue(str(self.getValue(ptr)))

      addr = int(addr)
      if addr < self.globalRanges[0] or addr >= self.cteRanges[4]:
        raise Exception(f'Getting from out of bounds! -> ({addr})')

      if addr < self.globalRanges[4]:
        return self.Globals[addr - self.globalRanges[0]].getActualValue()
      elif addr < self.localRanges[4]:
        return self.Locals[addr - self.localRanges[0]].getActualValue()
      elif addr < self.tempRanges[4]:
        return self.Temps[addr - self.tempRanges[0]].getActualValue()
      else:
        return self.Ctes[addr - self.cteRanges[0]].getActualValue()
    except:
      raise Exception(f"Value doesn't exist in memory?! -> ({addr})")
    # try:
    #   if re.match(r'\(\d+,\)', addr):
    #     ptr = addr[1:-2]
    #     ret = self.memory[self.getValue(ptr)]
    #     return ret.value
    #   else:
    #     ret = self.memory[int(addr)]
    #     return ret.value
    # except:
    #   raise Exception(f"Value doesn't exist in memory?! -> ({addr})")

  # Set a value and save it in memory
  def setValue(self, value, addr):
    if re.match(r'\(\d+,\)', addr):
      ptr = addr[1:-2]
      self.setValue(value, str(self.getValue(ptr)))
    else:
      addr = int(addr)
      if addr < self.globalRanges[0] or addr >= self.tempRanges[4]:
        return Exception(f'Setting in invalid memory! -> ({addr})')

      elif addr < self.globalRanges[4]:
        rangeAddr = addr - self.globalRanges[0]
        self.Globals[rangeAddr] = Address(value, self.getTypeByRange(addr, self.globalRanges))
      elif addr < self.localRanges[4]:
        rangeAddr = addr - self.localRanges[0]
        self.Locals[rangeAddr] = Address(value, self.getTypeByRange(addr, self.localRanges))
      elif addr < self.tempRanges[4]:
        rangeAddr = addr - self.tempRanges[0]
        self.Temps[rangeAddr] = Address(value, self.getTypeByRange(addr, self.tempRanges))
      else:
        rangeAddr = addr - self.cteRanges[0]
        self.Ctes[rangeAddr] = Address(value, self.getTypeByRange(addr, self.cteRanges))

    # if re.match(r'\(\d+,\)', addr):
    #   ptr = addr[1:-2]
    #   self.memory[self.getValue(ptr)] = Address(value, None)
    # else:
    #   self.memory[int(addr)] = Address(value, None)

  # Get type by address
  def getTypeByAddress(self, addr):
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

  # Execute virtual machine
  def execute(self):
    ip = 0

    # TODO: Implement matrix operations
    while True:
      quad = self.quads[ip]
      op = quad[0]

      ## - Let it begin. The super-switch case
      # Dual-op operation
      if op in ['+', '-', '/', '*', '==', '!=', '<', '<=', '>', '>=']:
        left = self.getValue(quad[1])
        right = self.getValue(quad[2])
        result = eval(f'{left} {op} {right}')
        self.setValue(result, quad[3])
        self._debugMsg(ip, f'{left} {op} {right} = {result} -> ({quad[3]})')
      # Assignment
      elif op == '=':
        value = self.getValue(quad[1])
        self.setValue(value, quad[3])
        self._debugMsg(ip, f'{value} -> ({quad[3]})')
      # Go to #
      elif op == 'GoTo':
        self._debugMsg(ip, f'Jump -> {quad[3]}')
        ip = int(quad[3])
        continue
      # Go to # if false
      elif op == 'GoToF':
        boolean = self.getValue(quad[1])
        if boolean:
          self._debugMsg(ip, f'Denied jump because true')
        else:
          self._debugMsg(ip, f'Allowed jump -> {quad[3]}')
          ip = int(quad[3])
          continue
      # Print
      elif op == 'PRINT':
        operand = quad[3]
        if re.match(r'\".+\"', operand):
          string = operand[1:-1]
          self._debugMsg(ip, f'Printing string: {string}')
          print(string)
        else:
          value = self.getValue(operand)
          self._debugMsg(ip, f'Printing value: ({operand}) -> {value}')
          print(str(value))
      # Read input
      elif op == 'READ':
        addr = quad[3]
        input_type = self.getTypeByAddress(addr)
        self._debugMsg(ip, f'Requesting input for ({addr}), type: {input_type}...')

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
            self.setValue(value, addr)
            break
      # Verify matrix access dimension
      elif op == 'VERIFY':
        index = self.getValue(quad[1])
        limit = int(quad[3])
        self._debugMsg(ip, f'Verifying that {index} < {limit}...')

        if index >= limit:
          raise Exception(f'{index} is above the array\'s range of {limit}')
      # Add a variable's base address to produce a pointer
      elif op == '+->':
        offset = self.getValue(quad[1])
        base = int(quad[2])
        self._debugMsg(ip, f'Creating pointer {offset} + {base} -> (({quad[3]}))')
        self.setValue(offset + base, quad[3])
      # elif op == 'ERA':
      # elif op == 'GoSub':
      # elif op == 'PARAM':
      # elif op == 'RETURN':
      # elif op == 'EndFunc':
      # Program End
      elif op == 'END':
        break
      else:
        self._debugMsg(ip, f'! -> {quad}')

      ip += 1

# # # # # # # # # # # # # # # # # # # # # # #
# # # # HECKING HONK LIKE NO TOMORROW # # # #
# # # # # # # # # # # # # # # # # # # # # # #
def honk(obj, debug=False):
  vm = HonkVM(obj, debug)
  vm.execute()
