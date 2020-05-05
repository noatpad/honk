
from collections import defaultdict

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

mono_cube = {
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

def getDuoResultType(left_type, right_type, operator):
  try:
    ret = dual_cube[left_type][right_type][operator]
    return ret
  except:
    return None
