
# Reserved words
reserved = {
  # Untitled _____ game
  'Untitled': 'UNTITLED',
  'game': 'GAME',
  # Program
  'Press y to honk': 'PRESS_Y',
  # Var, int, float, char, bool
  'Shop': 'SHOP',
  'WHOLE GOOSE': 'WHOLE_GOOSE',
  'PART GOOSE': 'PART_GOOSE',
  'LETTER GOOSE': 'LETTER_GOOSE',
  'GOOSE OR DUCK': 'GOOSE_OR_DUCK',
  # Function, void
  'task': 'TASK',
  'my soul': 'MY_SOUL',
  # Return
  'GOT BELL': 'GOT_BELL',
  # User input
  'HO-': 'HO',
  '-ONK': 'ONK',
  # Print
  'SHOW ON TV': 'SHOW_ON_TV',
  # While, do
  'HONK HONK': 'HONK_HONK',
  'HOONK': 'HOONK',
  # From, to
  'inhales...': 'INHALES',
  'HOOOONK': 'HOOOONK',
  # Break
  'peace was never an option': 'NO_PEACE',
  # . , ;
  'doot': 'doot',
  'MOAR': 'MOAR',
  'HONK': 'HONK',
}

# Token list
tokens = list(reserved.values()) + [
  'UNTITLED_GAME',
  'GOOSE_DOLLARS', 'SURPRISE', 'wh',
  'WE_GOOSE', 'MAYBE_GOOSE',
  'OPEN_GATE', 'CLOSE_GATE', 'OPEN_SQUARE_GATE', 'CLOSE_SQUARE_GATE', 'OPEN_FANCY_GATE', 'CLOSE_FANCY_GATE',
  'AM_GOOSE_QUESTION', 'AM_NOT_GOOSE', 'INFERIOR', 'INFERIOR_MAYBE', 'SUPERIOR', 'SUPERIOR_MAYBE',
  'AM_GOOSE', 'ADD_GOOSE', 'LESS_GOOSE', 'GOOSE_ARMY', 'GOOSE_PARTS', 'GOOSE_LEFTOVERS',
  'HONK_IF', 'HONK_THEN', 'BONK',
  'ID', 'CTE_INT', 'CTE_FLOAT', 'CTE_CHAR', 'CTE_BOOL', 'STRING'
]

# Simple tokens
# $!?
t_GOOSE_DOLLARS = r'GOOSE DOLLARS'
t_SURPRISE = r'SURPRISE'
t_wh = r'wh'

# &|
t_WE_GOOSE = r'WE GOOSE'
t_MAYBE_GOOSE = r'MAYBE GOOSE'

# ()[]{}
t_OPEN_GATE = r'OPEN GATE'
t_CLOSE_GATE = r'CLOSE GATE'
t_OPEN_SQUARE_GATE = r'OPEN SQUARE GATE'
t_CLOSE_SQUARE_GATE = r'CLOSE SQUARE GATE'
t_OPEN_FANCY_GATE = r'OPEN FANCY GATE'
t_CLOSE_FANCY_GATE = r'CLOSE FANCY GATE'

# == != < <= > >=
t_AM_GOOSE_QUESTION = r'AM GOOSE\?'
t_AM_NOT_GOOSE = r'AM NOT GOOSE\?!'
t_INFERIOR = r'INFERIOR'
t_INFERIOR_MAYBE = r'INFERIOR\.\.\.maybe'
t_SUPERIOR = r'SUPERIOR SPECIMEN'
t_SUPERIOR_MAYBE = r'SUPERIOR SPECIMEN\.\.\.maybe'
t_STRING = r'\".*\"'

# =+-*/%
t_AM_GOOSE = r'AM GOOSE'
t_ADD_GOOSE = r'ADD GOOSE'
t_LESS_GOOSE = r'LESS GOOSE'
t_GOOSE_ARMY = r'GOOSE ARMY'
t_GOOSE_PARTS = r'GOOSE PARTS'
t_GOOSE_LEFTOVERS = r'GOOSE LEFTOVERS'

# If, then, else
t_HONK_IF = r'HONK\?'
t_HONK_THEN = r'HONK!'
t_BONK = r'BONK!'

def t_CTE_FLOAT(t):
  r'\-?\d+\.\d+'
  t.value = float(t.value)
  return t

def t_CTE_INT(t):
  r'\-?\d+'
  t.value = int(t.value)
  return t

def t_CTE_CHAR(t):
  r'\'.\''
  t.value = t.value[1]
  return t

def t_CTE_BOOL(t):
  r'(true|false)'
  t.value = (t.value == "true")
  return t

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z0-9_]*'
  t.type = reserved.get(t.value, 'ID')
  return t

# Ignored characters and tokens
t_ignore = ' \t'
t_ignore_COMMENT = r'%%.*'

# Track line number
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
  # raise Exception(f'({t.lineno}:{t.lexpos}) Illegal character! -> {t.value[0]}')
  print(f'({t.lineno}:{t.lexpos}) Illegal character! -> {t.value[0]}')
  t.lexer.skip(1)
