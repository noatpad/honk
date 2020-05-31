
from collections import defaultdict

# Dual-operand type matching cube
dual_cube = {
  'int': {
    'int': {
      '=': 'int',
      '+': 'int',
      '-': 'int',
      '*': 'int',
      '/': 'int',
      '%': 'int',
      '.': 'int',
      '<': 'bool',
      '<=': 'bool',
      '>': 'bool',
      '>=': 'bool',
      '==': 'bool',
      '!=': 'bool'
    },
    'float': {
      '+': 'float',
      '-': 'float',
      '*': 'float',
      '/': 'float',
      '.': 'float',
      '<': 'bool',
      '<=': 'bool',
      '>': 'bool',
      '>=': 'bool',
      '==': 'bool',
      '!=': 'bool'
    }
  },
  'float': {
    'int': {
      '=': 'float',
      '+': 'float',
      '-': 'float',
      '*': 'float',
      '/': 'float',
      '.': 'float',
      '<': 'bool',
      '<=': 'bool',
      '>': 'bool',
      '>=': 'bool',
      '==': 'bool',
      '!=': 'bool'
    },
    'float': {
      '=': 'float',
      '+': 'float',
      '-': 'float',
      '*': 'float',
      '/': 'float',
      '.': 'float',
      '<': 'bool',
      '<=': 'bool',
      '>': 'bool',
      '>=': 'bool',
      '==': 'bool',
      '!=': 'bool'
    }
  },
  'char': {
    'char': {
      '=': 'char',
      '==': 'bool',
      '!=': 'bool'
    }
  },
  'bool': {
    'bool': {
      '=': 'bool',
      '&': 'bool',
      '|': 'bool',
      '==': 'bool',
      '!=': 'bool'
    }
  }
}

# Single-operand type matching table
mono_table = {
  'int': {
    '-': 'int',
    '$': 'int',
    '!': 'int',
    '?': 'float'
  },
  'float': {
    '-': 'float',
    '$': 'float',
    '!': 'float',
    '?': 'float'
  },
  'char': {
    '?': 'char'
  },
  'bool': {
    '?': 'bool'
  }
}

# Returns result type of a dual-operand operation
def getDuoResultType(left_type, right_type, operator):
  try:        # Return type from dual_cube
    return dual_cube[left_type][right_type][operator]
  except:     # If no entry exists for combination, return None
    return None

# Returns result type of a mono-operand operation
def getMonoResultType(vartype, operator):
  try:
    return mono_table[vartype][operator]
  except:
    return None
