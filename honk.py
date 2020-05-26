
from collections import deque, defaultdict
import re

class Address:
  def __init__(self, value, vartype):
    self.value = value
    self.vartype = vartype

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

    # Get and set constants
    if lines.popleft() != '-> CTES START':
      self._ded()

    while True:
      line = lines.popleft()

      if line == '->| CTES END':
        break

      data = line.split('\t')
      self.memory[int(data[2])] = Address(int(data[0]), data[1])

      self._debugMsg('Init', f'{int(data[0])} -> ({int(data[2])})')

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
  # TODO: Add validation for ranges
  # TODO: Add missing functions
  # Get a value from an address
  def getValue(self, addr, quad):
    try:
      ret = self.memory[int(addr)]
      return ret.value
    except:
      raise Exception(f"Value doesn't exist in memory?! -> ({int(addr)}) from {quad}")

  # Set a value and save it in memory
  def setValue(self, value, addr):
    self.memory[int(addr)] = Address(value, None)

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

    while True:
      quad = self.quads[ip]
      op = quad[0]

      ## - Let it begin. The super-switch case
      # Dual-op operation
      if op in ['+', '-', '/', '*', '==', '!=', '<', '<=', '>', '>=']:
        left = self.getValue(quad[1], quad)
        right = self.getValue(quad[2], quad)
        result = eval(f'{left} {op} {right}')
        self.setValue(result, quad[3])
        self._debugMsg(ip, f'{left} {op} {right} = {result} -> ({quad[3]})')
      # Assignment
      elif op == '=':
        value = self.getValue(quad[1], quad)
        self.setValue(value, quad[3])
        self._debugMsg(ip, f'{value} -> ({quad[3]})')
      # Go to #
      elif op == 'GoTo':
        self._debugMsg(ip, f'Jump -> {quad[3]}')
        ip = int(quad[3])
        continue
      # Go to # if false
      elif op == 'GoToF':
        boolean = self.getValue(quad[1], quad)
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
          value = self.getValue(operand, quad)
          self._debugMsg(ip, f'Printing value: {value} <- ({operand})')
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
        index = self.getValue(quad[1], quad)
        limit = int(quad[3])
        self._debugMsg(ip, f'Verifying that {index} < {limit}...')

        if index >= limit:
          raise Exception(f'{index} is above the array\'s range of {limit}')
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
