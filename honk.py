
from collections import deque, defaultdict

class Address:
  def __init__(self, value, vartype):
    self.value = value
    self.vartype = vartype

class HonkVM:
  def __init__(self, obj):
    # Split lines and turned it into a queue
    lines = deque(obj.split('\n'))

    # Get and set ranges
    if lines.popleft() != '-> RANGES START':
      self._ded()

    self.globalRange = (lines.popleft().split('\t'))
    self.localRange = (lines.popleft().split('\t'))
    self.tempRange = (lines.popleft().split('\t'))
    self.cteRange = (lines.popleft().split('\t'))

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

    # Get and set quads
    self.quads = deque()

    if lines.popleft() != '-> QUADS START':
      self._ded()

    while True:
      line = lines.popleft()

      if line == '->| QUADS END':
        break

      self.quads.append(line.split('\t'))

  ## INIT FUNCTIONS
  # Error
  def _ded(self):
    raise Exception('quack has commit die')

  ## EXECUTION FUNCTIONS
  # Execute virtual machine
  def execute(self):
    for quad in self.quads:
      # Let it begin. The super-switch case
      print(quad)

    #   if (op in ['+', '-', '/', '*']):
    #     pass

def honk(obj):
  vm = HonkVM(obj)
  vm.execute()
