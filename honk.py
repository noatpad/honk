
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

    self.globalRanges = (lines.popleft().split('\t'))
    self.localRanges = (lines.popleft().split('\t'))
    self.tempRanges = (lines.popleft().split('\t'))
    self.cteRanges = (lines.popleft().split('\t'))

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
      self.memory[data[2]] = Address(data[0], data[1])

      self._debugMsg('Init', f'{data[0]} -> ({data[2]})')

    # Get and set quads
    self.quads = deque()

    if lines.popleft() != '-> QUADS START':
      self._ded()

    while True:
      line = lines.popleft()

      if line == '->| QUADS END':
        break

      self.quads.append(line.split('\t'))

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
      ret = self.memory[addr]
      return ret.value
    except:
      raise Exception(f"Value doesn't exist in memory?! -> ({addr}) from {quad}")

# Set a value and save it in memory
  def setValue(self, value, addr):
    self.memory[addr] = Address(value, None)

  # Execute virtual machine
  def execute(self):
    ip = 0

    while True:
      # Let it begin. The super-switch case
      quad = self.quads[ip]
      op = quad[0]

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
        self._debugMsg(ip, f'Jump -> {int(quad[3])}')
        ip = int(quad[3])
        continue
      # Go to # if false
      elif op == 'GoToF':
        boolean = self.getValue(quad[1], quad)
        if boolean:
          self._debugMsg(ip, f'Denied jump because true')
        else:
          self._debugMsg(ip, f'Allowed jump -> {int(quad[3])}')
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
          value = self.getValue(int(quad[3]), quad)
          self._debugMsg(ip, f'Printing value: {value} <- ({quad[3]})')
          print(str(value))
      # Read input
      elif op == 'READ':
        self._debugMsg(ip, f'Requesting input...')
        user_input = input("> ")


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
