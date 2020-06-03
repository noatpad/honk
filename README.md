
# Honk
A barebones pseudo-compiler of a college final. It also can honk.

> The following guide is a preliminary guide on how to use Honk, which will likely change after I deliever this whole thing.

**Honk** is a rather peculiar language. It's able to most basic things in a language, as well as have a few "matrix operations". But it also has a second syntax...which is of course superior to anything else mankind has ever known.

## Usage
The only requirements to using Honk is to be running on Python 3.6+ and have `numpy` installed (yes, numpy). Once you have those, clone the repo, and get ready to honk.

When you have a file ready to run through the compiler, run the following script:
```py
python3 honk.py <your file>
```
The file will run through the regular lexer and parser as normal, _but if you input a `.honk` file, you'll be attempting to write in the superior syntax. You've been warned._

---

As mentioned before, there are 2 syntaxes. I recommend you try out the regular syntax to get you started, but if you dare, there is..._the goose syntax_. Read along...

## Regular syntax
The general structure of a program is as followed:
```
Program <program_name>;
<global variable declarations>
<function declarations>

%% Comments
main() {
  <statements>
}
```

All programs must start with a `Program <program_name>;` line to indicate the start of the program. Upon doing that, you can do declare global variables and then functions:

```
%% Variable declaration
var
  int a, b[2], c[7][4];
  float f;
  char ch;
  bool bb, b[10][10];
```

Variables are either global or local, depending when they were declared. Variables can be of type `int`, `float`, `char`, & `bool`, and can have up to 2 dimensions (in other words, you can have a regular variable, an array, or a matrix).

```
%% Function declaration
function <type> <name>(<params>)
<local variable declarations>
{
  <statements>
}
```
Functions can be of any type and also `void`. These functions can also return variables of any type & dimensions and receive parameters of any type & dimension.

### Statements
For statements, they can be any of the following:
- **Assignments**: `var = expression;`
- **Function call**: `func(<params>);` (must be void)
- **Read user input**: `read(<var>, ...);`
- **Print**: `print(<var>, ...);`
- **Conditionals**: `if (expression) then { <statements> } [else { <statements> }]`
- **Return**: `return(<var>);`
- **While loop**: `while (expression) do { <statements> }`
- **From loop**: `from (var = <x> to <y>) do { <statements> }`
- **Break**: `break;`

### Expressions
Expresions can be any kind of these operations:
- Arithmetic (+, -, *, /, %)
- Comparison (==, !=, <, <=, >, >=)
- Logic (&, |)
- Matrix operations on compatible matrixes (determinant - $, transpose - !, inverse - ? , dot product - .)
- Non-void function calls

A special characteristic about Honk is that besides doing matrix operations, you can also do "batch" operations using arrays and matrixes with some regular operators. The following functions/operators are batch-compatible:

- Every dual-operand operator (+, -, /, <, >, ==, %)
- '=' (you can assign an array to another array)
- Conditionals (they will act as AND gates with arrays and matrixes)
- print() (print a whole collection of data without a loop!)
- read() (input a whole collection without a loop!)

## Goose syntax

> you've been warned

The general structure of honk programs are:
```
Untitled <program_name> game HONK
<global variable declarations>
<function declarations>

%% Comments
Press y to honk
OPEN FANCY GATE
  <statements>
CLOSE FANCY GATE
```

```
%% Variable declaration
pond
  WHOLE GOOSE a, b OPEN BOX 2 CLOSE BOX 2 HONK
  PART GOOSE f HONK
  LETTER GOOSE ch HONK
  DUCK OR GOOSE bb OPEN BOX 10 CLOSE BOX OPEN BOX 10 CLOSE BOX HONK
```

```
%% Function declaration
task <type>/my soul <name> HONK <params> HONK
<local variable declarations>
OPEN FANCY GATE

CLOSE FANCY GATE
```

- **Assignments**: `var AM expression;`
- **Function call**: `HOOONK func OPEN GATE <params> CLOSE GATE HONK` (must be void)
- **Read user input**: `HO- x -ONK HONK`
- **Print**: `SHOW ON TV <var> HONK`
- **Conditionals**: `HONK? expression HOKN! OPEN FANCY GATE <statements> CLOSE FANCY GATE [BONK OPEN FANCY GATE <statements> CLOSE FANCY GATE]`
- **Return**: `GOT BELL <var> HONK`
- **While loop**: `HONK HONK expression HOONK OPEN FANCY GATE <statements> CLOSE FANCY GATE`
- **From loop**: `inhales var AM <x> HOOOONK <y>) HOOONK OPEN FANCY GATE <statements> CLOSE FANCY GATE`
- **Break**: `peace was never an option HONK`

### More cursed refs
- Addition: a MORE GOOSE b
- Substraction: a LESS GOOSE b
- Multiplication: a GOOSETIPLY b
- Division: a GOOSIVIDE b
- Modulo: a LEFTOVERS b
- Dot product: a doot b
- Determinant: c GOOSECOIN
- Transpose: c SURPRISE
- Inverse: c wh
- ==: AM GOOSE?
- !=: NOT GOOSE?!
- <: INFERIOR
- <=: INFERIOR maybe
- \>: SUPERIOR
- \>=: SUPERIOR maybe
- AND: TOGETHER FOREVER
- OR: POLE
