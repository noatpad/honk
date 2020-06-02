
### Goose Dictionary ###
# = -> AM GOOSE
# + -> MORE GOOSE
# - -> LESS GOOSE
# * -> GOOSETIPLY
# / -> GOOSIVIDE
# % -> LEFTOVERS
# $ -> GOOSECOIN
# ! -> SURPRISE
# ? -> wh
# == -> AM GOOSE?
# != -> NOT GOOSE?!
# < -> INFERIOR
# <= -> INFERIOR maybe
# > -> SUPERIOR SPECIMEN
# >= -> SUPERIOR maybe
# & -> TOGETHER FOREVER
# | -> POLE
# () -> OPEN/CLOSE GATE
# [] -> OPEN/CLOSE BOX
# {} -> OPEN/CLOSE FANCY GATE
# . -> DOOT
# , -> MOAR
# ; -> HONK

# Program _____ -> Untitled _____ game
# var -> pond
# int -> WHOLE GOOSE
# float -> PART GOOSE
# char -> LETTER GOOSE
# bool -> DUCK OR GOOSE
# void -> my soul
# function -> task
# return -> GOT BELL
# main() -> Press y to honk
# read(x) -> HO x ONK HONK
# print(x) -> SHOW ON TV OPEN GATE x CLOSE GATE HONK
# while -> HONK HONK OPEN GATE expr CLOSE GATE HOONK
# from -> inhales ID AM GOOSE expr HOOOONK expr HOOONK
# break -> peace was never an option
# if -> HONK?
# then -> HONK!
# else -> BONK!
# Function call -> HOOONK func OPEN GATE params CLOSE GATE HONK
### H o n k ###

# Reserved words
reserved = {
  # Common
  'GOOSE': 'GOOSE',
  'HONK': 'HONK',
  'HOONK': 'HOONK',
  'HOOONK': 'HOOONK',
  'HOOOONK': 'HOOOONK',
  'HO': 'HO',
  'ONK': 'ONK',
  'BONK': 'BONK',
  # Operators
  'AM': 'AM',
  'MORE': 'MORE',
  'LESS': 'LESS',
  'GOOSETIPLY': 'GOOSETIPLY',
  'GOOSIVIDE': 'GOOSIVIDE',
  'LEFTOVERS': 'LEFTOVERS',
  'GOOSECOIN': 'GOOSECOIN',
  'SURPRISE': 'SURPRISE',
  'wh': 'WH',
  'NOT': 'NOT',
  'INFERIOR': 'INFERIOR',
  'SUPERIOR': 'SUPERIOR',
  'maybe': 'MAYBE',
  'TOGETHER': 'TOGETHER',
  'FOREVER': 'FOREVER',
  'POLE': 'POLE',
  # Brackets
  'OPEN': 'OPEN',
  'CLOSE': 'CLOSE',
  'BOX': 'BOX',
  'FANCY': 'FANCY',
  'GATE': 'GATE',
  # Punctuation
  'doot': 'DOOT',
  'MOAR': 'MOAR',

  # Untitled _____ game
  'Untitled': 'UNTITLED',
  'game': 'GAME',
  # Main
  'Press': 'PRESS',
  'y': 'Y',
  'to': 'TO',
  'honk': 'HONK_LOWERCASE',
  # Vars
  'pond': 'POND',
  'WHOLE': 'WHOLE',
  'PART': 'PART',
  'LETTER': 'LETTER',
  'DUCK': 'DUCK',
  'OR': 'OR',
  # Functions
  'my': 'MY',
  'soul': 'SOUL',
  'task': 'TASK',
  'GOT': 'GOT',
  'BELL': 'BELL',
  'SHOW': 'SHOW',
  'ON': 'ON',
  'TV': 'TV',
  'inhales': 'INHALES',
  'peace': 'PEACE',
  'was': 'WAS',
  'never': 'NEVER',
  'an': 'AN',
  'option': 'OPTION'
}

# Token list
tokens = [
  'ID', 'CTE_INT', 'CTE_FLOAT', 'CTE_CHAR', 'CTE_BOOL', 'STRING'
] + list(reserved.values())

literals = '?!-'

# String
t_STRING = r'\".*\"'

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
  r'(Goose|Duck)'
  t.value = (t.value == "Goose")
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
