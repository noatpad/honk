
from collections import defaultdict

# Dual-operand type matching cube
dual_cube = {
  ('int', 0): {
    ('int', 0): {
      '=': ('int', 0),
      '+': ('int', 0),
      '-': ('int', 0),
      '*': ('int', 0),
      '/': ('float', 0),
      '%': ('int', 0),
      '<': ('bool', 0),
      '<=': ('bool', 0),
      '>': ('bool', 0),
      '>=': ('bool', 0),
      '==': ('bool', 0),
      '!=': ('bool', 0)
    },
    ('float', 0): {
      '+': ('float', 0),
      '-': ('float', 0),
      '*': ('float', 0),
      '/': ('float', 0),
      '<': ('bool', 0),
      '<=': ('bool', 0),
      '>': ('bool', 0),
      '>=': ('bool', 0),
      '==': ('bool', 0),
      '!=': ('bool', 0)
    }
  },
  ('int', 1): {
    ('int', 1): {
      '=': ('int', 1),
      '+': ('int', 1),
      '-': ('int', 1),
      '*': ('int', 1),
      '/': ('float', 1),
      '%': ('int', 1),
    },
    ('float', 1): {
      '+': ('float', 1),
      '-': ('float', 1),
      '*': ('float', 1),
      '/': ('float', 1),
    }
  },
  ('int', 2): {
    ('int', 2): {
      '=': ('int', 2),
      '+': ('int', 2),
      '-': ('int', 2),
      '*': ('int', 2),
      '/': ('float', 2),
      '%': ('int', 2),
    },
    ('float', 2): {
      '+': ('float', 2),
      '-': ('float', 2),
      '*': ('float', 2),
      '/': ('float', 2),
    }
  },
  ('float', 0): {
    ('int', 0): {
      '+': ('float', 0),
      '-': ('float', 0),
      '*': ('float', 0),
      '/': ('float', 0),
      '<': ('bool', 0),
      '<=': ('bool', 0),
      '>': ('bool', 0),
      '>=': ('bool', 0),
      '==': ('bool', 0),
      '!=': ('bool', 0)
    },
    ('float', 0): {
      '=': ('float', 0),
      '+': ('float', 0),
      '-': ('float', 0),
      '*': ('float', 0),
      '/': ('float', 0),
      '<': ('bool', 0),
      '<=': ('bool', 0),
      '>': ('bool', 0),
      '>=': ('bool', 0),
      '==': ('bool', 0),
      '!=': ('bool', 0)
    }
  },
  ('float', 1): {
    ('int', 1): {
      '+': ('float', 1),
      '-': ('float', 1),
      '*': ('float', 1),
      '/': ('float', 1)
    },
    ('float', 1): {
      '=': ('float', 1),
      '+': ('float', 1),
      '-': ('float', 1),
      '*': ('float', 1),
      '/': ('float', 1)
    }
  },
  ('float', 2): {
    ('int', 2): {
      '+': ('float', 2),
      '-': ('float', 2),
      '*': ('float', 2),
      '/': ('float', 2)
    },
    ('float', 2): {
      '=': ('float', 2),
      '+': ('float', 2),
      '-': ('float', 2),
      '*': ('float', 2),
      '/': ('float', 2)
    }
  },
  ('char', 0): {
    ('char', 0): {
      '=': ('char', 0),
      '+': ('char', 1)
    }
  },
  ('char', 1): {
    ('char', 0): {
      '+': ('char', 1)
    },
    ('char', 1): {
      '=': ('char', 1),
      '+': ('char', 1)
    }
  },
  ('char', 2): {
    ('char', 2): {
      '=': ('char', 2)
    }
  },
  ('bool', 0): {
    ('bool', 0): {
      '=': ('bool', 0),
      '&': ('bool', 0),
      '|': ('bool', 0)
    }
  },
  ('bool', 1): {
    ('bool', 1): {
      '=': ('bool', 1)
    }
  },
  ('bool', 2): {
    ('bool', 2): {
      '=': ('bool', 2)
    }
  }
}

# Single-operand type matching table
mono_table = {
  ('int', 0): {
    '-': ('int', 0)
  },
  ('int', 2): {
    '$': ('int', 0),
    '!': ('float', 2),
    '?': ('int', 2)
  },
  ('float', 0): {
    '-': ('float', 0)
  },
  ('float', 2): {
    '$': ('float', 0),
    '!': ('float', 2),
    '?': ('float', 2)
  },
  ('char', 2): {
    '?': ('char', 2)
  },
  ('bool', 0): {
    '!': ('bool', 0)
  },
  ('bool', 2): {
    '?': ('bool', 2)
  }
}

# Returns result type of a dual-operand operation
def getDuoResultType(left_type, right_type, operator):
  try:        # Return type from dual_cube
    ret = dual_cube[left_type][right_type][operator]
    return ret
  except:     # If no entry exists for combination, return None
    return None
