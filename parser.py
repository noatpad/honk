
from lexer import tokens

# Precedence rules for arithmetic
precedence = (
  ('left', '+', '-'),
  ('left', '*', '/')
)

# Parsing productions
def p_programa(p):
  "programa : PROGRAMA ID ';' vars functions PRINCIPAL '(' ')' '{' body '}'"
  pass

def p_vars(p):
  """vars : VAR var_type
          | empty"""
  pass

def p_var_type(p):
  """var_type : type ':' var_declare ';' var_type
              | type ':' var_declare"""
  pass

def p_var_declare(p):
  """var_declare : variable ',' var_declare
                 | variable"""
  pass

def p_variable(p):
  """variable : ID '[' expr '] '[' expr ']'
              | ID '[' expr ']'
              | ID"""
  pass

def p_type(p):
  """type : INT
          | FLOAT
          | CHAR"""
  pass

def p_functions(p):
  """functions : func
               | empty"""
  pass

def p_func(p):
  """func : FUNCION func_type ID '(' params ')' vars '{' body '}'
          | FUNCION func_type ID '(' ')' vars '{' body '}'"""
  pass

def p_func_type(p):
  """func_type : var_type
                | VOID"""
  pass

def p_params(p):
  """params : var_type ID ',' params
            | var_type ID"""
  pass

def p_body(p):
  "body : assignment"
  pass

def p_assignment(p):
  "assignment : variable '=' expr"
  pass

def p_expr_binop(p):
  """expr : expr '+' expr
          | expr '-' expr
          | expr '*' expr
          | expr '/' expr"""
  pass

def p_expr_group(p):
  "expr : '(' expr ')'"
  pass

def p_expr_num(p):
  "expr : NUMBER"
  pass

def p_expr_var_elem(p):
  "expr : ID '[' NUMBER ']'"
  pass

def p_expr_var(p):
  "expr : ID"
  pass

def p_empty(p):
  "empty :"
  pass

def p_error(p):
  print(f'({p.lineno}:{p.lexpos}) Syntax error at "{p.value}"')
