### Example Content of parser.out Debug File

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This example illustrates the typical structure and content found within a `parser.out` file. It includes sections for unused terminals, grammar rules, lists of terminals and nonterminals with their associated rules, the parsing method used (e.g., LALR), and a detailed breakdown of each parsing state, showing transitions and reductions. This information is vital for diagnosing and resolving parser conflicts.

```Parser Output
    Unused terminals:


    Grammar

    Rule 1     expression -> expression PLUS expression
    Rule 2     expression -> expression MINUS expression
    Rule 3     expression -> expression TIMES expression
    Rule 4     expression -> expression DIVIDE expression
    Rule 5     expression -> NUMBER
    Rule 6     expression -> LPAREN expression RPAREN

    Terminals, with rules where they appear

    TIMES                : 3
    error                : 
    MINUS                : 2
    RPAREN               : 6
    LPAREN               : 6
    DIVIDE               : 4
    PLUS                 : 1
    NUMBER               : 5

    Nonterminals, with rules where they appear

    expression           : 1 1 2 2 3 3 4 4 6 0


    Parsing method: LALR


    state 0

        S' -> . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3
        LPAREN          shift and go to state 2


    state 1

        S' -> expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        PLUS            shift and go to state 6
        MINUS           shift and go to state 5
        TIMES           shift and go to state 4
        DIVIDE          shift and go to state 7


    state 2

        expression -> LPAREN . expression RPAREN
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3
        LPAREN          shift and go to state 2


    state 3

        expression -> NUMBER .

        $               reduce using rule 5
        PLUS            reduce using rule 5
        MINUS           reduce using rule 5
        TIMES           reduce using rule 5
        DIVIDE          reduce using rule 5
        RPAREN          reduce using rule 5


    state 4

        expression -> expression TIMES . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3
        LPAREN          shift and go to state 2


    state 5

        expression -> expression MINUS . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3
        LPAREN          shift and go to state 2


    state 6

        expression -> expression PLUS . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3
        LPAREN          shift and go to state 2


    state 7

        expression -> expression DIVIDE . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3
        LPAREN          shift and go to state 2


    state 8

        expression -> LPAREN expression . RPAREN
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        RPAREN          shift and go to state 13
        PLUS            shift and go to state 6
        MINUS           shift and go to state 5
        TIMES           shift and go to state 4
```

--------------------------------

### Setting the Starting Grammar Symbol via yacc() Argument (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to specify the starting grammar symbol when initializing the PLY parser using the `start` argument to the `yacc.yacc()` function. This provides a flexible way to parse subsets of a larger grammar, especially during development or debugging.

```Python
parser = yacc.yacc(start='foo')
```

--------------------------------

### Build PLY Lexer Instance

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This example shows the basic usage of `lex.lex()` to construct a lexer instance. The function uses Python reflection to automatically discover and incorporate regular expression rules defined in the calling context.

```Python
lexer = lex.lex()
```

--------------------------------

### Example: Tokenization with PLY's lex.py

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how PLY's `lex.py` module processes an input string, breaking it down into individual tokens. It demonstrates the transformation from a raw string to a sequence of named tokens and then to detailed type-value pairs, which are fundamental outputs for subsequent parsing.

```Input String
x = 3 + 42 * (s - t)
```

```Token Names Output
'ID','EQUALS','NUMBER','PLUS','NUMBER','TIMES',
'LPAREN','ID','MINUS','ID','RPAREN'
```

```Token Type-Value Pairs Output
('ID','x'), ('EQUALS','='), ('NUMBER','3'), 
('PLUS','+'), ('NUMBER','42'), ('TIMES','*'),
('LPAREN','('), ('ID','s'), ('MINUS','-'),
('ID','t'), ('RPAREN',')')
```

--------------------------------

### PLY Lexer Initialization and Token Stream Processing

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python example demonstrates the standard procedure for initializing a PLY lexer and processing input data. It shows how to feed a string to the lexer using `lexer.input()` and then iterate through the generated tokens using a `while` loop and `lexer.token()`, printing each token until the input is exhausted.

```Python
lexer = lex.lex()
data = "{}"

lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
```

--------------------------------

### Setting the Starting Grammar Symbol via 'start' Variable (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows how to explicitly define the starting grammar symbol for a PLY parser by assigning its name to a `start` variable in the parser specification file. This overrides the default behavior of using the first defined rule and is useful for debugging.

```Python
start = 'foo'

def p_bar(p):
    'bar : A B'

# This is the starting rule due to the start specifier above
def p_foo(p):
    'foo : bar X'
...
```

--------------------------------

### LR-Parsing Trace Example for `3 + 5 * (10 - 20)`

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates the step-by-step process of LR (shift-reduce) parsing for the expression `3 + 5 * (10 - 20)` using the previously defined arithmetic grammar. It shows the state of the symbol stack, remaining input tokens, and the action performed (shift or reduce) at each step, illustrating the bottom-up parsing technique.

```APIDOC
Step Symbol Stack           Input Tokens            Action
---- ---------------------  ---------------------   -------------------------------
1                           3 + 5 * ( 10 - 20 )$    Shift 3
2    3                        + 5 * ( 10 - 20 )$    Reduce factor : NUMBER
3    factor                   + 5 * ( 10 - 20 )$    Reduce term   : factor
4    term                     + 5 * ( 10 - 20 )$    Reduce expr : term
5    expr                     + 5 * ( 10 - 20 )$    Shift +
6    expr +                     5 * ( 10 - 20 )$    Shift 5
7    expr + 5                     * ( 10 - 20 )$    Reduce factor : NUMBER
8    expr + factor                * ( 10 - 20 )$    Reduce term   : factor
9    expr + term                  * ( 10 - 20 )$    Shift *
10   expr + term *                  ( 10 - 20 )$    Shift (
11   expr + term * (                  10 - 20 )$    Shift 10
12   expr + term * ( 10                  - 20 )$    Reduce factor : NUMBER
13   expr + term * ( factor              - 20 )$    Reduce term : factor
14   expr + term * ( term                - 20 )$    Reduce expr : term
15   expr + term * ( expr                - 20 )$    Shift -
16   expr + term * ( expr -                20 )$    Shift 20
17   expr + term * ( expr - 20                )$    Reduce factor : NUMBER
18   expr + term * ( expr - factor            )$    Reduce term : factor
19   expr + term * ( expr - term              )$    Reduce expr : expr - term
20   expr + term * ( expr                     )$    Shift )
21   expr + term * ( expr )                    $    Reduce factor : (expr)
22   expr + term * factor                      $    Reduce term : term * factor
```

--------------------------------

### Python: View Possible Next Productions with lr.lr_after

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

This example demonstrates the `lr.lr_after` attribute, which lists all `Production` instances that can legally appear immediately to the right of the dot (.). This attribute is crucial for understanding the possible branches a parse can take from the current position.

```Python
lr.lr_after
```

--------------------------------

### Python: Inspect an LRItem Instance

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

This snippet demonstrates how to inspect an `LRItem` instance, `lr`, which represents a specific stage in the parsing process. In this example, `lr` is shown immediately before an expression.

```Python
lr
```

--------------------------------

### Process Input and Extract Tokens with PLY Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python example demonstrates the fundamental process of feeding input to a `ply.lex` lexer and extracting tokens. It uses the `lexer.input()` method to provide the source text and then repeatedly calls `lexer.token()` within a `while` loop to retrieve each `LexToken` until the input is exhausted. The extracted tokens are then printed.

```Python
# Test it out
data = '''
3 + 4 * 10
  + -20 *2
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
```

--------------------------------

### Example: Parsing Nested C Code Blocks with Lexer States

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

A practical example demonstrating how to use an 'exclusive' lexer state to parse nested C code blocks enclosed by curly braces. It tracks brace levels to correctly identify the end of the code block, a task difficult with standard regex.

```Python
import ply.lex as lex

# Declare the states
states = (
  ('ccode','exclusive'),
)

# Match the first '{' Enter ccode state.
def t_ccode(t):
    r'\{'
    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
    t.lexer.level = 1                          # Initial brace level
    t.lexer.begin('ccode')                     # Enter 'ccode' state

# Rules for the 'ccode' state
def t_ccode_lbrace(t):     
    r'\{'
    t.lexer.level += 1                

def t_ccode_rbrace(t):
    r'\}'
    t.lexer.level -= 1

    # If closing brace, return the code fragment
    if t.lexer.level == 0:
```

--------------------------------

### PLY `p_expr` Rule Example and `p.grammar` Structure

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

This snippet illustrates a typical PLY `p_rule` function definition for an expression and shows how its corresponding grammar rules are structured and stored within the `p.grammar` attribute of a `ParserReflect` instance after processing.

```Python
def p_expr(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr'''
```

```Python
('p_expr', [ ('calc.py',10,'expr', ['expr','PLUS','expr']),
             ('calc.py',11,'expr', ['expr','MINUS','expr']),
             ('calc.py',12,'expr', ['expr','TIMES','expr']),
             ('calc.py',13,'expr', ['expr','DIVIDE','expr'])
           ])
```

--------------------------------

### Python: Inspect LR Items for a Production

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

This example shows how to view the LR items associated with a grammar production `p`. Each `LRItem` represents a specific stage of parsing, with the dot (.) indicating the current position within the production.

```Python
p.lr_items
```

--------------------------------

### Define and Parse Simple Expressions with PLY in Python

Source: https://github.com/dabeaz/ply/blob/master/README.md

This comprehensive example illustrates the use of PLY to build a lexer and parser for simple arithmetic expressions. It defines tokens, specifies regular expressions for token matching, implements grammar rules using docstrings for parser functions, and demonstrates how to build an Abstract Syntax Tree (AST) from the parsed input. It includes error handling for both lexical and syntax errors.

```Python
# -----------------------------------------------------------------------------
# example.py
#
# Example of using PLY To parse the following simple grammar.
#
#   expression : term PLUS term
#              | term MINUS term
#              | term
#
#   term       : factor TIMES factor
#              | factor DIVIDE factor
#              | factor
#
#   factor     : NUMBER
#              | NAME
#              | PLUS factor
#              | MINUS factor
#              | LPAREN expression RPAREN
#
# -----------------------------------------------------------------------------

from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = ( 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
           'NAME', 'NUMBER' )

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()
    
# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.
def p_expression(p):
    '''
    expression : term PLUS term
               | term MINUS term
    '''
    # p is a sequence that represents rule contents.
    #
    # expression : term PLUS term
    #   p[0]     : p[1] p[2] p[3]
    # 
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : factor TIMES factor
         | factor DIVIDE factor
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_number(p):
    '''
    factor : NUMBER
    '''
    p[0] = ('number', p[1])

def p_factor_name(p):
    '''
    factor : NAME
    '''
    p[0] = ('name', p[1])

def p_factor_unary(p):
    '''
    factor : PLUS factor
           | MINUS factor
    '''
    p[0] = ('unary', p[1], p[2])

def p_factor_grouped(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = ('grouped', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('2 * 3 + 4 * (5 - x)')
print(ast)
```

--------------------------------

### Configure Custom Logging for PLY Lexer and Parser Debugging

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Provides an example of setting up a custom Python `logging` object and passing it to `lex.lex()` and `yacc.yacc()` via the `debuglog` parameter. This allows for fine-grained control over debug output, including routing to files and custom formatting.

```Python
# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

lex.lex(debug=True,debuglog=log)
yacc.yacc(debug=True,debuglog=log)
```

--------------------------------

### Incorrect PLY Error Rule Placement Example

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates an example of an improperly defined error rule where the 'error' token is placed at the end. This configuration can lead to premature rule reduction upon the first bad token, making it difficult for the parser to recover if more errors immediately follow.

```Python
def p_statement_print_error(p):
        'statement : PRINT error'
        print("Syntax error in print statement. Bad expression")
```

--------------------------------

### PLY: Accessing Grammar Symbol Line and Lexing Spans

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows the usage of `p.linespan(num)` and `p.lexspan(num)` to obtain the start and end line numbers and lexing positions for grammar symbols, which are available when full tracking is enabled via `yacc.parse(tracking=True)`.

```Python
def p_expression(p):
    'expression : expression PLUS expression'
    p.lineno(1)        # Line number of the left expression
    p.lineno(2)        # line number of the PLUS operator
    p.lineno(3)        # line number of the right expression
    ...
    start,end = p.linespan(3)    # Start,end lines of the right expression
    starti,endi = p.lexspan(3)   # Start,end positions of right expression
```

--------------------------------

### PLY Parser State 10: Expression MINUS Reduction

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Outlines the actions and grammar rules for parser state 10, focusing on the reduction of `expression MINUS expression`. It includes shift actions for `TIMES` and `DIVIDE`, and reduction using rule 2 for other tokens, along with conflict resolution examples.

```PLY Parser Output
state 10

        expression -> expression MINUS expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        $               reduce using rule 2
        PLUS            reduce using rule 2
        MINUS           reduce using rule 2
        RPAREN          reduce using rule 2
        TIMES           shift and go to state 4
        DIVIDE          shift and go to state 7

      ! TIMES           [ reduce using rule 2 ]
      ! DIVIDE          [ reduce using rule 2 ]
      ! PLUS            [ shift and go to state 6 ]
      ! MINUS           [ shift and go to state 5 ]
```

--------------------------------

### Define Yacc Rule with Embedded Action (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This example shows how to execute code during intermediate parsing stages using an empty rule ('seen_A'). The embedded action 'seen_A' executes immediately after 'A' is parsed, allowing access to the preceding symbol via 'p[-1]' and returning a value via 'p[0]'.

```Python
def p_foo(p):
    "foo : A seen_A B C D"
    print("Parsed a foo", p[1],p[3],p[4],p[5])
    print("seen_A returned", p[2])

def p_seen_A(p):
    "seen_A :"
    print("Saw an A = ", p[-1])   # Access grammar symbol to left
    p[0] = some_value            # Assign value to seen_A
```

--------------------------------

### Add Grammar Productions in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

This snippet illustrates how to add new grammar rules (productions) to a `Grammar` object using `g.add_production()`. It shows examples with direct terminal names, character literals, and the `%prec` specifier for explicit precedence. If any error is detected, a `GrammarError` exception is raised.

```python
g.add_production('expr',['expr','PLUS','term'],func,file,line)
g.add_production('expr',['expr','"+"','term'],func,file,line)
g.add_production('expr',['MINUS','expr','%prec','UMINUS'],func,file,line)
```

--------------------------------

### Define PLY Lexer Rules using a Python Closure

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python example demonstrates defining PLY lexer rules within a closure. It shows how to encapsulate token definitions and rule functions inside a `MyLexer` function, providing an alternative to class-based or module-based definitions for organizing lexer components without a full class structure.

```Python
import ply.lex as lex

# List of token names.   This is always required
tokens = (
  'NUMBER',
  'PLUS',
  'MINUS',
  'TIMES',
  'DIVIDE',
  'LPAREN',
  'RPAREN',
)

def MyLexer():
    # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

    # A regular expression rule with some action code
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
```

--------------------------------

### PLY: Reporting Errors with Token Line Numbers

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Provides an example of reporting an error message using the line number of a specific token (e.g., 'LPAREN') within a grammar rule. This approach is often sufficient for error reporting without needing full position tracking.

```Python
def p_bad_func(p):
    'funccall : fname LPAREN error RPAREN'
    # Line number reported from LPAREN token
    print("Bad function call at line", p.lineno(2))
```

--------------------------------

### Use @TOKEN Decorator for PLY Token Rules

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This example demonstrates the use of the `@TOKEN` decorator from `ply.lex`. It shows how to attach a pre-defined complex regular expression variable (like `identifier`) to a token rule function, allowing `lex.py` to correctly associate the pattern with the token.

```Python
from ply.lex import TOKEN

@TOKEN(identifier)
def t_ID(t):
    ...
```

--------------------------------

### Handling Lexing Errors in PLY Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Provides an example of the `t_error()` function, which is automatically invoked when the PLY lexer encounters an illegal or unexpected character. This function typically reports the offending character and then skips it to allow lexing to continue.

```Python
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
```

--------------------------------

### PLY Grammar Rules with Derived Precedence and Associativity

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet illustrates how `yacc.py` automatically assigns precedence levels and associativity to grammar rules based on the `precedence` declaration. The rule's precedence is determined by the right-most terminal symbol, guiding conflict resolution during parsing.

```Python
expression : expression PLUS expression                 # level = 1, left
               | expression MINUS expression                # level = 1, left
               | expression TIMES expression                # level = 2, left
               | expression DIVIDE expression               # level = 2, left
               | LPAREN expression RPAREN                   # level = None (not specified)
               | NUMBER                                     # level = None (not specified)
```

--------------------------------

### Example Grammar Causing Reduce/Reduce Conflict in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This grammar snippet demonstrates a common scenario leading to a reduce/reduce conflict in PLY. The conflict arises because `NUMBER` can be reduced both as part of `assignment : ID EQUALS NUMBER` and as `expression : NUMBER`, making it ambiguous for the parser when encountering input like "a = 5".

```Grammar
assignment :  ID EQUALS NUMBER
           |  ID EQUALS expression

expression : expression PLUS expression
           | expression MINUS expression
           | expression TIMES expression
           | expression DIVIDE expression
           | LPAREN expression RPAREN
           | NUMBER
```

--------------------------------

### Yacc Grammar with Embedded Action Causing Shift/Reduce Conflict (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This example demonstrates how inserting an embedded action ('seen_AB') into one of the rules can introduce a shift-reduce conflict. The conflict arises because the parser faces ambiguity when the same symbol ('C') appears next in both the 'abcd' and 'abcx' rules, forcing a choice between shifting 'C' or reducing the empty 'seen_AB' rule.

```Python
def p_foo(p):
    """foo : abcd
               | abcx"""

def p_abcd(p):
    "abcd : A B C D"

def p_abcx(p):
    "abcx : A B seen_AB C X"

def p_seen_AB(p):
    "seen_AB :"
```

--------------------------------

### Build a PLY Lexer Instance

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows the basic function call to build a lexer using `lex.lex()` within the PLY framework. This function initializes the lexer based on the defined rules in the module.

```Python
# Build the lexer from my environment and return it
return lex.lex()
```

--------------------------------

### Change Lexer State using begin() Method

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to switch between lexing states using `t.lexer.begin('state_name')`. This method allows the lexer to transition to a new specified state or return to the 'INITIAL' state.

```Python
def t_begin_foo(t):
    r'start_foo'
    t.lexer.begin('foo')             # Starts 'foo' state

def t_foo_end(t):
    r'end_foo'
    t.lexer.begin('INITIAL')        # Back to the initial state
```

--------------------------------

### Instantiate PLY Lexer and Parser Objects

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to explicitly create and store lexer and parser objects using `lex.lex()` and `yacc.yacc()`, which is crucial for managing multiple instances in advanced parsing applications.

```Python
lexer  = lex.lex()       # Return lexer object
parser = yacc.yacc()     # Return parser object
```

--------------------------------

### Build and Test PLY Lexer from External Module

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This interactive Python session demonstrates how to build a PLY lexer by importing rules from a separate module (`tokrules`). It shows the `lex.lex(module=tokrules)` call and then inputs a string to tokenize, printing the resulting `LexToken` objects to illustrate the lexer's behavior.

```Python
import tokrules
lexer = lex.lex(module=tokrules)
lexer.input("3 + 4")
lexer.token()
LexToken(NUMBER,3,1,1,0)
lexer.token()
LexToken(PLUS,'+',1,2)
lexer.token()
LexToken(NUMBER,4,1,4)
lexer.token()
None
```

--------------------------------

### PLY Grammar Class API Reference

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

This section provides a detailed API reference for the `ply.yacc.Grammar` class, outlining its constructor and various methods. It includes parameter descriptions, return types, and usage notes for defining, validating, and analyzing grammar specifications.

```APIDOC
Grammar Class:
  Description: Used to hold and manipulate information about a grammar specification, encapsulating tokens, precedence rules, and grammar rules.

  __init__(terminals: list[str])
    Description: Creates a new grammar object.
    Parameters:
      terminals: A list of strings specifying the terminals for the grammar.

  set_precedence(term: str, assoc: str, level: int)
    Description: Sets the precedence level and associativity for a given terminal. Must be called prior to adding any productions.
    Parameters:
      term: The terminal name.
      assoc: The associativity, one of 'right', 'left', or 'nonassoc'.
      level: A positive integer representing the precedence level. Higher values indicate higher precedence.

  add_production(name: str, syms: list[str], func: callable = None, file: str = '', line: int = 0)
    Description: Adds a new grammar rule. The list of symbols in `syms` may include character literals and '%prec' specifiers. Raises `GrammarError` on error.
    Parameters:
      name: The name of the rule.
      syms: A list of symbols making up the right-hand side of the rule.
      func: The function to call when reducing the rule (optional).
      file: The filename of the rule (used for error messages, optional).
      line: The line number of the rule (used for error messages, optional).

  set_start(start: str = None)
    Description: Sets the starting rule for the grammar. If omitted, the first rule added with `add_production()` is used. Must be called after all productions are added.
    Parameters:
      start: A string specifying the name of the start rule (optional).

  find_unreachable() -> list[str]
    Description: Diagnostic function. Returns a list of all unreachable non-terminals defined in the grammar.

  infinite_cycle() -> list[str]
    Description: Diagnostic function. Returns a list of all non-terminals in the grammar that result in an infinite cycle (i.e., cannot expand to only terminal symbols).

  undefined_symbols() -> list[tuple[str, Production]]
    Description: Diagnostic function. Returns a list of tuples corresponding to undefined symbols.
    Returns:
      A list of `(name, prod)` tuples, where `name` is the undefined symbol and `prod` is a `Production` instance.

  unused_terminals() -> list[str]
    Description: Diagnostic function. Returns a list of terminals that were defined but never used in the grammar.

  unused_rules() -> list[Production]
    Description: Diagnostic function. Returns a list of `Production` instances corresponding to rules defined but never used.

  unused_precedence() -> list[tuple[str, str]]
    Description: Diagnostic function. Returns a list of tuples corresponding to precedence rules that were set but never used.
    Returns:
      A list of `(term, assoc)` tuples, where `term` is the terminal name and `assoc` is the associativity.

  compute_first() -> dict[str, list[str]]
    Description: Computes all of the first sets for all symbols in the grammar.
    Returns:
      A dictionary mapping symbol names to a list of their first symbols.

  compute_follow() -> dict[str, list[str]]
    Description: Computes all of the follow sets for all non-terminals in the grammar.
    Returns:
      A dictionary mapping non-terminal names to a list of symbols in their follow set.

  build_lritems()
    Description: Calculates all of the LR items for all productions in the grammar. This step is required before using the grammar for any kind of table generation.

  Attributes:
    Description: Attributes set by the above methods, assumed to be read-only.
```

--------------------------------

### Using an Empty Production Rule (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to incorporate an 'empty' production rule into a grammar, allowing for optional elements. The `optitem` rule can match either an `item` or nothing, making the `item` optional.

```Python
def p_optitem(p):
    'optitem : item'
    '        | empty'
    ...
```

--------------------------------

### PLY Lexer Control Methods

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This section documents the primary methods available on a built PLY lexer instance for controlling its input and token generation. It outlines their purpose, parameters, and return values.

```APIDOC
lexer.input(data)
  Purpose: Resets the lexer and stores a new input string.
  Parameters:
    data (str): The new input string for the lexer.
  Returns: None

lexer.token()
  Purpose: Returns the next token from the input.
  Returns:
    LexToken: A special LexToken instance on success.
    None: If the end of the input text has been reached.
```

--------------------------------

### APIDOC: LRItem Class Attributes and Methods

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

Comprehensive documentation for the `LRItem` class, detailing its attributes that hold information related to a specific stage of parsing in an LR-based parser. It also covers special methods like `__len__` and `__getitem__` and important usage constraints.

```APIDOC
LRItem:
  Attributes:
    lr.name: The name of the grammar rule (e.g., 'statement').
    lr.prod: A tuple of symbols representing the right-hand side of the production, including the special '.' character (e.g., ('ID','.','=','expr')).
    lr.number: An integer representing the production number in the grammar.
    lr.usyms: A set of unique symbols in the production. Inherited from the original Production instance.
    lr.lr_index: An integer representing the position of the dot (.).
    lr.lr_after: A list of all Production instances that can legally appear immediately to the right of the dot (.). Represents possible parse branches.
    lr.lr_before: The grammar symbol that appears immediately before the dot (.), or None if at the beginning of the parse.
    lr.lr_next: A link to the next LR item, representing the next stage of the parse. None if lr is the last LR item.
  Special Methods:
    __len__(): Returns the number of items in lr.prod including the dot (.).
    __getitem__(n): Returns lr.prod[n].
  Constraints:
    All attributes associated with LR items should be assumed to be read-only. Modifications are strongly discouraged.
```

--------------------------------

### LRParser Class API Reference

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

Documents the `LRParser` class, which implements the low-level LR parsing engine. It describes the constructor, the main `parse` method for running the parser, and a `restart` method to reset its state.

```APIDOC
LRParser:
  __init__(lrtab, error_func)
    lrtab: An instance of LRTable containing the LR production and state tables.
    error_func: The error function to invoke in the event of a parsing error.

  Methods:
    p.parse(input=None, lexer=None, debug=0, tracking=0)
      input: A string, which if supplied is fed into the lexer using its input() method.
      lexer: An instance of the Lexer class to use for tokenizing. If not supplied, the last lexer created with the lex module is used.
      debug: A boolean flag that enables debugging.
      tracking: A boolean flag that tells the parser to perform additional line number tracking.
      Purpose: Runs the parser.

    p.restart()
      Purpose: Resets the parser state for a parse already in progress.
```

--------------------------------

### Conceptual Parser Trace and Actions

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet illustrates a conceptual trace of a parser's actions, showing how grammar rules are recognized and reduced. It demonstrates the internal steps of a shift/reduce parser, including the reduction of expressions and the final success state, providing insight into the parser's decision-making process.

```Parser Trace
    23   expr + term                               $    Reduce expr : expr + term
    24   expr                                      $    Reduce expr
    25                                             $    Success!
```

--------------------------------

### Syntax-Directed Translation with Semantic Actions for a Calculator

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how semantic actions can be attached to BNF grammar rules to define the behavior of a simple calculator. Each rule specifies how to compute a 'val' attribute for the non-terminal based on the values of its components, demonstrating syntax-directed translation.

```APIDOC
Grammar                             Action
--------------------------------    -------------------------------------------- 
expression0 : expression1 + term    expression0.val = expression1.val + term.val
            | expression1 - term    expression0.val = expression1.val - term.val
            | term                  expression0.val = term.val

term0       : term1 * factor        term0.val = term1.val * factor.val
            | term1 / factor        term0.val = term1.val / factor.val
            | factor                term0.val = factor.val

factor      : NUMBER                factor.val = int(NUMBER.lexval)
            | ( expression )        factor.val = expression.val
```

--------------------------------

### Run PLY Lexer from Command Line

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet illustrates how to integrate `lex.runmain()` into a lexer script's main execution block. This allows the lexer to be run directly from the command line, tokenizing input from standard input or a specified file.

```Python
if __name__ == '__main__':
     lex.runmain()
```

--------------------------------

### Production Class API Reference (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

Documents the `Production` class in PLY, which represents individual grammar rules. It details attributes like name, symbols, number, associated function, and precedence, along with methods for binding reduction functions.

```APIDOC
Production:
  Constructor:
    No public constructor. Instances should only be created by calling Grammar.add_production().
  Attributes:
    p.name: The name of the production (e.g., 'A' for 'A : B C D').
    p.prod: A tuple of symbols making up the right-hand side of the production (e.g., ('B','C','D')).
    p.number: Production number. An integer containing the index of the production in the grammar's Productions list.
    p.func: The name of the reduction function associated with the production.
    p.callable: The callable object associated with the name in p.func. None unless the production has been bound using bind().
    p.file: Filename associated with the production. Typically the file where the production was defined.
    p.lineno: Line number associated with the production. Typically the line number in p.file where the production was defined.
    p.prec: Precedence and associativity associated with the production. A tuple (assoc,level) where assoc is 'left', 'right', or 'nonassoc' and level is an integer.
    p.usyms: A list of all unique symbols found in the production.
    p.lr_items: A list of all LR items for this production. Meaningful if Grammar.build_lritems() has been called. Items are instances of LRItem.
    p.lr_next: The head of a linked-list representation of the LR items in p.lr_items. Meaningful if Grammar.build_lritems() has been called.
  Methods:
    p.bind(dict): Binds the production function name in p.func to a callable object in dict.
  Special Methods:
    __len__(): Returns the number of symbols in p.prod.
    __getitem__(n): Returns the nth symbol from p.prod (p[n]).
    __str__(): String representation of the production.
```

--------------------------------

### PLY Parser API: Position Tracking Methods

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

API documentation for methods available on the PLY production object (`p`) and the `yacc` module, used for tracking line numbers and lexing positions during parsing.

```APIDOC
PLY Production Object (p):
  lineno(num: int) -> int
    Description: Return the line number for symbol *num*.
    Parameters:
      num: The index of the symbol in the production rule (e.g., 1 for p[1]).
    Returns: The line number.

  lexpos(num: int) -> int
    Description: Return the lexing position (character offset) for symbol *num*.
    Parameters:
      num: The index of the symbol in the production rule.
    Returns: The lexing position.

  linespan(num: int) -> tuple[int, int]
    Description: Return a tuple (startline, endline) with the starting and ending line number for symbol *num*. Requires `tracking=True` in `yacc.parse()`.
    Parameters:
      num: The index of the symbol in the production rule.
    Returns: A tuple containing the start and end line numbers.

  lexspan(num: int) -> tuple[int, int]
    Description: Return a tuple (start, end) with the starting and ending lexing positions for symbol *num*. Requires `tracking=True` in `yacc.parse()`. Note: Returns range up to the start of the last grammar symbol.
    Parameters:
      num: The index of the symbol in the production rule.
    Returns: A tuple containing the start and end lexing positions.

  set_lineno(index: int, lineno: int) -> None
    Description: Sets the line number for a specific symbol in the production. Useful for selective propagation of line numbers.
    Parameters:
      index: The index of the symbol (e.g., 0 for p[0]).
      lineno: The line number to set.
    Returns: None.

yacc Module:
  parse(data: str, tracking: bool = False, ...) -> Any
    Description: Parses the input data. The `tracking` option enables automatic line number and position tracking for all grammar symbols.
    Parameters:
      data: The input string to parse.
      tracking: A boolean flag (default: False). If True, enables full position tracking.
    Returns: The result of the parsing operation.
```

--------------------------------

### PLY AST Construction: Tuple/List Based Nodes

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet demonstrates a minimal approach to constructing an Abstract Syntax Tree (AST) by propagating tuples or lists within grammar rule functions. Each rule assigns a tuple representing the node type and its children/values to `p[0]`, allowing for a simple, lightweight AST representation.

```Python
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = ('binary-expression',p[2],p[1],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ('group-expression',p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number-expression',p[1])
```

--------------------------------

### Python: Build LR Items and Access a Production

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

This snippet demonstrates how to initialize LR items for a grammar object and then retrieve a specific production rule for further inspection. It assumes `g` is an initialized `Grammar` object.

```Python
g.build_lritems()
p = g[1]
p
```

--------------------------------

### Separate Grammar Rules for Addition and Subtraction (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates defining distinct Python functions for simple arithmetic grammar rules (addition and subtraction) in PLY, where each function handles a single production. This approach can lead to more verbose code for similar rules.

```Python
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]
```

--------------------------------

### Manage Lexer States with Stack (push_state, pop_state)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows how to use `t.lexer.push_state()` to add a new state to the lexer's state stack and `t.lexer.pop_state()` to revert to the previous state. This approach is useful for managing nested lexing contexts.

```Python
def t_begin_foo(t):
    r'start_foo'
    t.lexer.push_state('foo')             # Starts 'foo' state

def t_foo_end(t):
    r'end_foo'
    t.lexer.pop_state()                   # Back to the previous state
```

--------------------------------

### LRTable Class API Reference

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

Documents the `LRTable` class, which represents constructed LR parsing tables on a grammar. It details the constructor, attributes for grammar, parsing method, production rules, action/goto tables, and conflict resolution, along with a method to bind callable functions.

```APIDOC
LRTable:
  __init__(grammar, log=None)
    grammar: An instance of Grammar.
    log: A logger object used to write debugging information (same as parser.out).

  Attributes:
    lr.grammar: A link to the Grammar object used to construct the parsing tables.
    lr.lr_method: The LR parsing method used (e.g., 'LALR').
    lr.lr_productions: A reference to grammar.Productions.
    lr.lr_action: The LR action dictionary that implements the underlying state machine. Keys are LR states.
    lr.lr_goto: The LR goto table that contains information about grammar rule reductions.
    lr.sr_conflicts: A list of tuples (state,token,resolution) identifying all shift/reduce conflicts.
      state: The LR state number where the conflict occurred.
      token: The token causing the conflict.
      resolution: A string describing the resolution taken ('shift' or 'reduce').
    lr.rr_conflicts: A list of tuples (state,rule,rejected) identifying all reduce/reduce conflicts.
      state: The LR state number where the conflict occurred.
      rule: The production rule that was selected (instance of Production).
      rejected: The production rule that was rejected (instance of Production).

  Methods:
    lrtab.bind_callables(dict)
      dict: A dictionary of callable objects to bind to function names used in productions.
      Purpose: Binds action function names (e.g., 'p_expr') to actual callable objects for parser execution. Always called prior to running a parser.
```

--------------------------------

### Define State-Specific Tokens and Rules in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows how to associate tokens and lexer rules with specific states by prefixing the token/rule name with the state name (e.g., `t_state_TOKEN`). Also illustrates defining tokens for multiple states or all states (`t_ANY_TOKEN`), and the default 'INITIAL' state.

```Python
t_foo_NUMBER = r'\d+'                      # Token 'NUMBER' in state 'foo'        
t_bar_ID     = r'[a-zA-Z_][a-zA-Z0-9_]*'   # Token 'ID' in state 'bar'

def t_foo_newline(t):
    r'\n'
    t.lexer.lineno += 1

t_foo_bar_NUMBER = r'\d+'         # Defines token 'NUMBER' in both state 'foo' and 'bar'

t_ANY_NUMBER = r'\d+'         # Defines a token 'NUMBER' in all states

t_NUMBER = r'\d+'
t_INITIAL_NUMBER = r'\d+'
```

--------------------------------

### PLY: Enabling Full Position Tracking in Yacc Parser

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to enable comprehensive line number and position tracking for all grammar symbols by passing the `tracking=True` option to `yacc.parse()`. Note that this extra processing can significantly slow down parsing.

```Python
yacc.parse(data,tracking=True)
```

--------------------------------

### Grammar Class API Reference (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

Documents the `Grammar` class in PLY, which manages the overall grammar structure. It provides attributes for accessing productions, terminals, nonterminals, and sets, along with special methods for debugging.

```APIDOC
Grammar:
  Attributes:
    g.Productions: A list of all productions added. The first entry is reserved for a production representing the starting rule. Objects are instances of the Production class.
    g.Prodnames: A dictionary mapping the names of nonterminals to a list of all productions of that nonterminal.
    g.Terminals: A dictionary mapping the names of terminals to a list of the production numbers where they are used.
    g.Nonterminals: A dictionary mapping the names of nonterminals to a list of the production numbers where they are used.
    g.First: A dictionary representing the first sets for all grammar symbols. Computed by the compute_first() method.
    g.Follow: A dictionary representing the follow sets for all grammar rules. Computed by the compute_follow() method.
    g.Start: Starting symbol for the grammar. Set by the set_start() method.
  Special Methods:
    __len__(): Returns the number of productions.
    __getitem__(n): Returns the nth production from the grammar (g[n]).
```

--------------------------------

### Enable Run-time Debugging for PLY Parser

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to enable run-time debugging for a PLY parser by passing a logging object to the `debug` option of the `parser.parse()` method. This allows for detailed inspection of the parsing process, including stack changes and rule reductions.

```Python
log = logging.getLogger()
parser.parse(input,debug=log)
```

--------------------------------

### Enable Debug Mode for PLY Lexer and Parser Creation

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows how to enable basic debugging output during the creation of lexer and parser objects. Setting the `debug=True` flag in `lex.lex()` and `yacc.yacc()` provides diagnostic information.

```Python
lex.lex(debug=True)
yacc.yacc(debug=True)
```

--------------------------------

### Combining Simple Arithmetic Grammar Rules (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to combine multiple similar grammar rules (addition and subtraction) into a single Python function in PLY. This is achieved by using a multi-line docstring for the rules and conditional logic based on the operator token to perform the correct action.

```Python
def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
```

--------------------------------

### Define Simple PLY Token with Regular Expression

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to define a simple token in PLY using a string and a regular expression. The `t_` prefix indicates a token definition, and Python raw strings (`r'...'`) are recommended for regex patterns to avoid issues with backslashes.

```Python
t_PLUS = r'\+'
```

--------------------------------

### ParserReflect Class API Reference (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

Comprehensive API documentation for the `ParserReflect` class in PLY. This class is central to collecting and validating parser specification data from Python modules or objects, forming the basis for grammar construction.

```APIDOC
ParserReflect Class:
  Description: Used to collect parser specification data from a Python module or object. Implements most of the high-level PLY interface used by `yacc()`.
  Constructor:
    __init__(pdict, log=None)
      pdict: A dictionary containing parser specification data, typically a module or class dictionary of code implementing a PLY parser.
      log: A logger instance used to report error messages.
  Methods:
    get_all(): Collect and store all required parsing information.
    validate_all(): Validate all collected parsing information. This is a separate step for performance optimization. Sets `p.error` if validation errors occur and returns its value.
    signature(): Compute a signature representing the contents of the collected parsing data. The signature changes if the parser specification justifies table regeneration. Can be called after `get_all()` but before `validate_all()`.
  Attributes:
    start: The grammar start symbol, if specified (from `pdict['start']`).
    error_func: The error handling function (from `pdict['p_error']`) or `None`.
    tokens: The token list (from `pdict['tokens']`).
    prec: The precedence specifier (from `pdict['precedence']`).
    preclist: A parsed version of the precedence specification. A list of tuples of the form `(token, assoc, level)`.
    grammar: A list of tuples `(name, rules)` representing the grammar rules.
      name: The name of a Python function or method in `pdict` that starts with "p_".
      rules: A list of tuples `(filename, line, prodname, syms)` representing grammar rules found in the function's documentation string.
    pfuncs: A sorted list of tuples `(line, file, name, doc)` representing all found `p_` functions, sorted by line number.
    files: A dictionary holding all source filenames encountered during data collection (keys only have meaning).
    error: An attribute indicating whether critical errors occurred during validation. If set, further processing should not be performed.
```

--------------------------------

### API Documentation: Requirements for Hand-Written Lexers in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This API documentation outlines the essential interface requirements for a custom-built lexer to be compatible with PLY's `yacc.py` parser generator. It specifies that the lexer object must provide a `token()` method and that the returned token objects must have `type` and `value` attributes, with an optional `lineno` attribute for line tracking.

```APIDOC
Lexer Object Requirements for yacc.py:
  1. token() method:
       Returns: The next token or None if no more tokens are available.
  2. Token Object (returned by token() method):
       Attributes:
         type: The type of the token.
         value: The value of the token.
         lineno (optional): The line number if tracking is enabled.
```

--------------------------------

### BNF Grammar for Simple Arithmetic Expressions

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Defines the syntax for basic arithmetic operations (addition, subtraction, multiplication, division) and parenthesized expressions using Backus-Naur Form (BNF). It distinguishes between terminals (tokens like NUMBER, +, -, *, /) and non-terminals (grammar rules like expression, term, factor).

```APIDOC
expression : expression + term
             | expression - term
             | term

term       : term * factor
           | term / factor
           | factor

factor     : NUMBER
           | ( expression )
```

--------------------------------

### Handling Variable-Length Grammar Rules with len() (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to handle grammar rules with varying numbers of terms (e.g., binary vs. unary minus) within a single Python function in PLY. It uses `len(p)` to determine which production was matched and apply the appropriate action, though this can duplicate parser work.

```Python
def p_expressions(p):
    '''expression : expression MINUS expression
                  | MINUS expression'''
    if (len(p) == 4):
        p[0] = p[1] - p[3]
    elif (len(p) == 3):
        p[0] = -p[2]
```

--------------------------------

### Combining Multiple Binary Operator Grammar Rules (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows how to group several binary operator grammar rules (addition, subtraction, multiplication, division) into a single Python function in PLY. This approach uses a multi-line docstring for all rules and conditional logic to perform the correct action based on the operator.

```Python
def p_binary_operators(p):
    '''expression : expression PLUS term
                  | expression MINUS term
       term       : term TIMES factor
                  | term DIVIDE factor'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
```

--------------------------------

### Define and Build a Simple Arithmetic Expression Parser with PLY Yacc

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python code defines grammar rules for arithmetic expressions (addition, subtraction, multiplication, division, numbers, parentheses) using PLY's `yacc` module. Each function represents a grammar rule, with the docstring specifying the context-free grammar and the function body implementing semantic actions. It also includes an error rule and a loop to parse user input, demonstrating the full parser workflow.

```Python
# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
```

--------------------------------

### PLY: Accessing Token Line Number and Position

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to retrieve the line number and lexing position of a specific token within a grammar rule using `p.lineno(num)` and `p.lexpos(num)`, where 'num' is the token's index in the production.

```Python
def p_expression(p):
    'expression : expression PLUS expression'
    line   = p.lineno(2)        # line number of the PLUS token
    index  = p.lexpos(2)        # Position of the PLUS token
```

--------------------------------

### Enable parser.out Debug File Generation

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

To generate the `parser.out` debug file, the `debug` parameter must be set to `True` when calling the `yacc.yacc()` function. This creates the file in the current working directory, providing insights into the parser's behavior.

```Python
yacc.yacc(debug=True)
```

--------------------------------

### PLY Parser State 11: Expression PLUS Reduction

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Describes the actions and grammar rules for parser state 11, specifically for the reduction of `expression PLUS expression`. It lists shift actions for `TIMES` and `DIVIDE`, and reduction using rule 1 for various tokens, including conflict resolution.

```PLY Parser Output
state 11

        expression -> expression PLUS expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        $               reduce using rule 1
        PLUS            reduce using rule 1
        MINUS           reduce using rule 1
        RPAREN          reduce using rule 1
        TIMES           shift and go to state 4
        DIVIDE          shift and go to state 7

      ! TIMES           [ reduce using rule 1 ]
      ! DIVIDE          [ reduce using rule 1 ]
      ! PLUS            [ shift and go to state 6 ]
      ! MINUS           [ shift and go to state 5 ]
```

--------------------------------

### Enable Debugging Mode for PLY Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet shows how to activate debugging output when building a PLY lexer. Setting `debug=True` in `lex.lex()` causes the lexer to produce detailed information about added rules, master regular expressions, and generated tokens, aiding in development and troubleshooting.

```Python
lexer = lex.lex(debug=True)
```

--------------------------------

### High-Level Operation of PLY's `yacc()` Function

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

This section outlines the specific sequence of operations performed by PLY's `yacc()` function to create a grammar and parser. This sequence should be emulated when building alternative PLY interfaces.

```APIDOC
High-level operation of yacc():
1. A `ParserReflect` object is created and raw grammar specification data is collected.
2. A `Grammar` object is created and populated with information from the specification data.
3. An `LRTable` object is created to run the LALR algorithm over the `Grammar` object.
4. Productions in the `LRTable` are bound to callables using the `bind_callables()` method.
5. A `LRParser` object is created from the information in the `LRTable` object.
```

--------------------------------

### Defining an Empty Production Rule (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to define an 'empty' production rule in PLY using a function with a docstring containing only the rule name followed by a colon. This rule can then be used to represent optional grammar elements.

```Python
def p_empty(p):
    'empty :'
    pass
```

--------------------------------

### Define PLY Lexer Rules within a Python Class

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python class (`MyLexer`) encapsulates all lexer rules and methods, including token names, regex rules, and error handling. It also provides `build` and `test` methods for creating and testing the lexer instance, demonstrating a structured, object-oriented approach to lexer definition and usage.

```Python
import ply.lex as lex

class MyLexer(object):
    # List of token names.   This is always required
    tokens = (
       'NUMBER',
       'PLUS',
       'MINUS',
       'TIMES',
       'DIVIDE',
       'LPAREN',
       'RPAREN',
    )

    # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_NUMBER(self,t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: 
                 break
             print(tok)

# Build the lexer and try it out
m = MyLexer()
m.build()           # Build the lexer
m.test("3 + 4")     # Test it
```

--------------------------------

### Supply Custom Lexer to PLY Yacc Parser

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This code demonstrates how to provide an alternative tokenizer to `yacc.parse()` instead of relying on the default `lex.py`. The custom lexer object must minimally implement a `token()` method and an `input()` method if an input string is provided to `yacc.parse()`.

```Python
parser = yacc.parse(lexer=x)
```

--------------------------------

### PLY AST Construction: Custom Class Nodes

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This approach uses custom Python classes to represent different types of Abstract Syntax Tree (AST) nodes. Each grammar rule instantiates the appropriate class and assigns the object to `p[0]`, which makes it easier to attach more complex semantics, type checking, and code generation features directly to the node classes.

```Python
class Expr: pass

class BinOp(Expr):
    def __init__(self,left,op,right):
        self.left = left
        self.right = right
        self.op = op

class Number(Expr):
    def __init__(self,value):
        self.value = value

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = BinOp(p[1],p[2],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Number(p[1])
```

--------------------------------

### Iterate Over PLY Lexer Tokens Using For Loop

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python snippet showcases a more idiomatic way to consume tokens from a `ply.lex` lexer by leveraging its support for the iteration protocol. Instead of explicit `while` loops and `token()` calls, a simple `for` loop directly iterates over the `lexer` object, yielding each `LexToken`. This simplifies token processing.

```Python
for tok in lexer:
    print(tok)
```

--------------------------------

### Clone a PLY Lexer Object

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to duplicate an existing PLY lexer object using its `clone()` method. Cloning creates an identical copy, including any input text and internal state, allowing separate input processing without regenerating internal tables.

```Python
lexer = lex.lex()
...
newlexer = lexer.clone()
```

--------------------------------

### PLY Lexer State: Global Variable Counter

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to maintain state, specifically a token count, using a global variable within a PLY lexer rule. While simple, this approach can lead to issues with multiple lexer instances or concurrent processing.

```Python
num_count = 0
def t_NUMBER(t):
    r'\d+'
    global num_count
    num_count += 1
    t.value = int(t.value)    
    return t
```

--------------------------------

### Grammar Rules with Character Literals (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates defining grammar rules in PLY using single character literals (e.g., '+', '-') directly in the docstring. This method requires these literals to be explicitly declared in the corresponding lexer file.

```Python
def p_binary_operators(p):
    '''expression : expression '+' term
                  | expression '-' term
       term       : term '*' factor
                  | term '/' factor'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
```

--------------------------------

### PLY AST Construction: Generic Node Structure

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

To simplify tree traversal and provide a flexible structure, this snippet illustrates using a single generic `Node` class for all parse tree nodes. The `Node` class stores the node type, a list of children, and an optional leaf value, allowing for a unified way to represent various AST elements.

```Python
class Node:
    def __init__(self,type,children=None,leaf=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = Node("binop", [p[1],p[3]], p[2])
```

--------------------------------

### Enable Debug Output for PLY Yacc Parser

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet shows how to activate extensive debugging output during the parsing process with PLY Yacc. By setting the `debug` parameter to `True` when calling `parser.parse()`, detailed information about the parser's state and actions will be printed.

```Python
parser.parse(input_text, debug=True)
```

--------------------------------

### PLY Lexer Rules for C-Code State and Tokenization

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python snippet defines a set of regular expression rules for a PLY lexer operating in a 'ccode' state. It includes patterns for C/C++ comments, strings, character literals, and general non-whitespace sequences. The initial part of the snippet, implicitly part of a `t_ccode_rbrace` rule, demonstrates how to capture a block of code, assign it a 'CCODE' type, update line numbers, and transition the lexer back to the 'INITIAL' state.

```Python
t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
t.type = "CCODE"
t.lexer.lineno += t.value.count('\n')
t.lexer.begin('INITIAL')           
return t

    # C or C++ comment (ignore)    
def t_ccode_comment(t):
    r'(/*(.|\n)*?\*/)|(//.*)'
    pass

    # C string
def t_ccode_string(t):
   r'\"([^\\\n]|(\\.))*?\"'

    # C character literal
def t_ccode_char(t):
   r'\'([^\\\n]|(\\.))*?\''

    # Any sequence of non-whitespace characters (not braces, strings)
def t_ccode_nonspace(t):
   r'[^\s\{\}\'\\\"]+'

    # Ignored characters (whitespace)
t_ccode_ignore = " \t\n"

    # For bad characters, we just skip over it
def t_ccode_error(t):
        t.lexer.skip(1)
```

--------------------------------

### Import PLY Lexer and Parser Modules in Python

Source: https://github.com/dabeaz/ply/blob/master/README.md

This snippet demonstrates how to import the `lex` and `yacc` modules from the `ply` package. After copying the `ply` directory into your project, these imports make the lexer and parser functionalities available for use in your Python application.

```Python
from .ply import lex
from .ply import yacc
```

--------------------------------

### PLY Parser State 13: Parenthesized Expression Reduction

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows the actions and grammar rules for parser state 13, focusing on the reduction of `LPAREN expression RPAREN`. It indicates reduction using rule 6 for all relevant tokens.

```PLY Parser Output
state 13

        expression -> LPAREN expression RPAREN .

        $               reduce using rule 6
        PLUS            reduce using rule 6
        MINUS           reduce using rule 6
        TIMES           reduce using rule 6
        DIVIDE          reduce using rule 6
        RPAREN          reduce using rule 6
```

--------------------------------

### PLY Parser Error Recovery API Reference

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This section provides documentation for key methods used in PLY's error recovery. `parser.errok()` resets the parser's error state, `parser.token()` retrieves the next input token, and `parser.restart()` clears the parsing stack and resets the parser to its initial state.

```APIDOC
parser.errok():
  This resets the parser state so it doesn't think it's in error-recovery mode. This will prevent an `error` token from being generated and will reset the internal error counters so that the next syntax error will call `p_error()` again.
parser.token():
  This returns the next token on the input stream.
parser.restart():
  This discards the entire parsing stack and resets the parser to its initial state.
```

--------------------------------

### Using Embedded Actions for Scope Control in Yacc (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet illustrates a practical application of embedded actions for managing parsing context, such as variable scoping. An embedded action ('new_scope') is used to create a new scope upon encountering an opening brace, while a corresponding action at the end of the block ('pop_scope()') reverts to the previous scope.

```Python
def p_statements_block(p):
    "statements: LBRACE new_scope statements RBRACE"""
    # Action code
    ...
    pop_scope()        # Return to previous scope

def p_new_scope(p):
    "new_scope :"
    # Create a new scope for local variables
    s = new_scope()
    push_scope(s)
    ...
```

--------------------------------

### Define Lexer Rules for Expression Evaluator (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python code defines a complete lexer using `ply.lex` for a simple arithmetic expression evaluator. It specifies token names, regular expression rules for operators and numbers, includes action code for type conversion, handles newlines, ignores whitespace, and provides an error handling mechanism. This forms the foundational structure for the tokenizer.

```Python
# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
```

--------------------------------

### PLY Lexer State: Class-Based Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows how to define a PLY lexer as a Python class to manage state. This approach encapsulates state within the class instance, making it suitable for applications requiring multiple independent lexer instances and better adhering to object-oriented principles.

```Python
class MyLexer:
    ...
    def t_NUMBER(self,t):
        r'\d+'
        self.num_count += 1
        t.value = int(t.value)    
        return t

    def build(self, **kwargs):
        self.lexer = lex.lex(object=self,**kwargs)

    def __init__(self):
        self.num_count = 0
```

--------------------------------

### Handle Reserved Words in PLY Lexer using a Lookup Dictionary

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows the recommended approach for handling reserved keywords. A dictionary maps keywords to their token types. A single `t_ID` rule matches all identifiers, and then a lookup in the `reserved` dictionary determines if the identifier is a reserved word or a generic ID. This method reduces the number of regex rules and improves performance.

```Python
reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   ...
}

tokens = ['LPAREN','RPAREN',...,'ID'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
```

--------------------------------

### Access Parser and Lexer Objects within PLY Parser Rule

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to access both the parser and lexer objects from within a parser rule function. The `p.parser` and `p.lexer` attributes provide direct references to the respective active instances.

```Python
def p_expr_plus(p):
   'expr : expr PLUS expr'
   ...
   print(p.parser)          # Show parser object
   print(p.lexer)           # Show lexer object
```

--------------------------------

### PLY Parser State 9: Expression TIMES Reduction

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Details the actions and grammar rules for parser state 9, where an `expression` followed by `TIMES expression` is reduced. It shows shift actions for other operators and reduction using rule 3 for various tokens, including conflict indicators.

```PLY Parser Output
state 9

        expression -> expression TIMES expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        $               reduce using rule 3
        PLUS            reduce using rule 3
        MINUS           reduce using rule 3
        TIMES           reduce using rule 3
        DIVIDE          reduce using rule 3
        RPAREN          reduce using rule 3

      ! PLUS            [ shift and go to state 6 ]
      ! MINUS           [ shift and go to state 5 ]
      ! TIMES           [ shift and go to state 4 ]
      ! DIVIDE          [ shift and go to state 7 ]
```

--------------------------------

### PLY Parser State 12: Expression DIVIDE Reduction

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Presents the actions and grammar rules for parser state 12, where `expression DIVIDE expression` is reduced. It details shift actions for other operators and reduction using rule 4 for various tokens, along with conflict indicators.

```PLY Parser Output
state 12

        expression -> expression DIVIDE expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        $               reduce using rule 4
        PLUS            reduce using rule 4
        MINUS           reduce using rule 4
        TIMES           reduce using rule 4
        DIVIDE          reduce using rule 4
        RPAREN          reduce using rule 4

      ! PLUS            [ shift and go to state 6 ]
      ! MINUS           [ shift and go to state 5 ]
      ! TIMES           [ shift and go to state 4 ]
      ! DIVIDE          [ shift and go to state 7 ]
```

--------------------------------

### Illustrating `p` Sequence Indexing in PLY Yacc Semantic Actions

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet clarifies how the `p` argument within PLY yacc rule functions is indexed. `p[0]` is used to assign the result of the rule (the value of the left-hand side non-terminal), while `p[1]`, `p[2]`, and so on, access the values of the grammar symbols on the right-hand side of the rule.

```Python
def p_expression_plus(p):
    'expression : expression PLUS term'
    #   ^
    #  p[0]         p[1]     p[2] p[3]

    p[0] = p[1] + p[3]
```

--------------------------------

### Configuring PLY Lexer with `reflags` for Regex Options

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python snippet illustrates how to pass custom flags to the `re.compile()` function used internally by PLY when initializing the lexer. By setting the `reflags` option, developers can control regular expression behavior, such as enabling `re.UNICODE` and `re.VERBOSE` for more flexible pattern matching.

```Python
lex.lex(reflags=re.UNICODE | re.VERBOSE)
```

--------------------------------

### Yacc Grammar Without Shift/Reduce Conflicts (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet presents a simple Yacc grammar with two alternative rules ('abcd' and 'abcx') that do not introduce any shift/reduce conflicts. It serves as a baseline to compare against grammars where embedded actions might cause conflicts.

```Python
def p_foo(p):
    """foo : abcd
               | abcx"""

def p_abcd(p):
    "abcd : A B C D"

def p_abcx(p):
    "abcx : A B C X"
```

--------------------------------

### Parse with a Specific Lexer Object in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows how to pass a specific lexer object to the `parser.parse()` function. This ensures the parser uses the intended lexer instance, preventing issues where it might default to the last created lexer.

```Python
parser.parse(text,lexer=lexer)
```

--------------------------------

### Define Yacc Rule with End-of-Rule Action (PLY)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet illustrates a standard Yacc rule where the associated action code executes only after all symbols in the rule (A, B, C, D) have been successfully parsed. It demonstrates basic rule definition and accessing parsed values.

```Python
def p_foo(p):
    "foo : A B C D"
    print("Parsed a foo", p[1],p[2],p[3],p[4])
```

--------------------------------

### Defining PLY Lexer Literals

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates two ways to define single-character literal tokens in PLY's lexer: using a Python list or a string. Literals are checked after all regular expression rules and are returned 'as is' when encountered by the lexer.

```Python
literals = [ '+','-','*','/' ]
```

```Python
literals = "+-*/"
```

--------------------------------

### PLY Lexer State: Closure-Based Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Explains how to manage lexer state using Python closures. This method allows state to be maintained within the scope of the enclosing function, providing an alternative to classes or global variables for state management.

```Python
def MyLexer():
    num_count = 0
    ...
    def t_NUMBER(t):
        r'\d+'
        nonlocal num_count
        num_count += 1
        t.value = int(t.value)    
        return t
    ...
```

--------------------------------

### PLY Lexer Internal State Attributes Reference

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Provides a reference for the internal attributes available on a PLY Lexer object, detailing their purpose, type, and behavior. These attributes are crucial for advanced lexer control, debugging, and custom line number tracking.

```APIDOC
Lexer Object Attributes:
  lexer.lexpos:
    Type: integer
    Description: Current position within the input text. Modifying this value changes the result of the next call to token(). Within token rule functions, this points to the first character *after* the matched text. If modified within a rule, the next returned token will be matched at the new position.
  lexer.lineno:
    Type: integer
    Description: The current value of the line number attribute stored in the lexer. PLY only specifies that the attribute exists; it never sets, updates, or performs any processing with it. Users must add custom code to track line numbers.
  lexer.lexdata:
    Type: string
    Description: The current input text stored in the lexer. This is the string passed with the input() method. Modification is generally not recommended unless the user fully understands the implications.
  lexer.lexmatch:
    Type: re.Match object
    Description: The raw Match object returned by the Python re.match() function (used internally by PLY) for the current token. If a regular expression contains named groups, this can be used to retrieve those values. Note: This attribute is only updated when tokens are defined and processed by functions.
```

--------------------------------

### PLY Error Recovery: Synchronizing on a Specific Token

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This `p_error()` function demonstrates a recovery strategy where the parser reads ahead to find a specific terminating token, such as a semicolon (';'). It then uses `parser.errok()` to clear the error state and returns the found token to the parser as the next lookahead, allowing parsing to potentially resume from a known point.

```Python
def p_error(p):
    # Read ahead looking for a terminating ";"
    while True:
        tok = parser.token()             # Get the next token
        if not tok or tok.type == 'SEMI': break
    parser.errok()

    # Return SEMI to the parser as the next lookahead token
    return tok
```

--------------------------------

### Defining an Ambiguous Expression Grammar in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet presents a compact, yet ambiguous, context-free grammar for arithmetic expressions, as it would be defined within a `yacc.py` parser specification. It highlights how such definitions can lead to parsing conflicts without explicit precedence rules.

```Python
expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | LPAREN expression RPAREN
               | NUMBER
```

--------------------------------

### PLY: Selectively Propagating Line Numbers

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to selectively propagate line number information using `p.set_lineno()`. This method can improve parsing performance by avoiding the overhead of full position tracking when line numbers are only needed for specific grammar symbols.

```Python
def p_fname(p):
    'fname : ID'
    p[0] = p[1]
    p.set_lineno(0,p.lineno(1))
```

--------------------------------

### Define PLY Token with Action Function (Number Conversion)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates defining a token using a Python function. The regular expression is specified in the function's docstring. The function receives a `LexToken` object, allows modification of its `value` attribute (e.g., converting to an integer), and must return the token. If no value is returned, the token is discarded.

```Python
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
```

--------------------------------

### Access Attributes of PLY LexToken Objects

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python code illustrates how to access the various attributes of `LexToken` objects returned by the `ply.lex` lexer. It demonstrates retrieving `type` (token type), `value` (token value), `lineno` (line number), and `lexpos` (position in input) for each token. This allows for detailed analysis and processing of tokenized data.

```Python
# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok.type, tok.value, tok.lineno, tok.lexpos)
```

--------------------------------

### Incorrect Method for Defining Reserved Word Tokens (Avoid)

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet demonstrates an *incorrect* way to define reserved words. Defining them as separate string-based rules can lead to partial matches (e.g., 'for' matching 'forget' or 'printed'), which is usually not desired. This approach should be avoided in favor of the lookup dictionary method for reserved words.

```Python
t_FOR   = r'for'
t_PRINT = r'print'
```

--------------------------------

### Customize PLY Token Value with Additional Data

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Explains how to store custom data in a token's `value` attribute. Instead of just the matched text, the `value` can be assigned any Python object, such as a tuple containing the lexeme and symbol table information. This allows passing richer data to the parser, as `yacc.py` primarily exposes the `value` attribute.

```Python
def t_ID(t):
    ...
    # Look up symbol table information and return a tuple
    t.value = (t.value, symbol_lookup(t.value))
    ...
    return t
```

--------------------------------

### PLY Panic Mode Error Recovery: Discarding Tokens and Restarting Parser

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python `p_error()` function demonstrates a panic mode recovery strategy. It reads and discards tokens from the input stream until a closing '}' is found or the end of the file is reached. After discarding, it resets the parser to its initial state using `parser.restart()` to attempt recovery.

```Python
def p_error(p):
    print("Whoa. You are seriously hosed.")
    if not p:
        print("End of File!")
        return

    # Read ahead looking for a closing '}'
    while True:
        tok = parser.token()             # Get the next token
        if not tok or tok.type == 'RBRACE': 
            break
    parser.restart()
```

--------------------------------

### Decorator for PLY Docstring Compatibility with Python -OO Mode

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Provides a custom Python decorator that re-attaches docstrings to functions, making PLY compatible with Python's `-OO` interpreter mode. This mode typically strips docstrings, which PLY relies on for rule definitions.

```Python
def _(doc):
    def decorate(func):
        func.__doc__ = doc
        return func
    return decorate

@_("assignment : expr PLUS expr")
def p_assignment(p):
    ...
```

--------------------------------

### Discarding Tokens Using `ignore_` Prefix in PLY Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows an alternative, simpler method to discard tokens in PLY by prefixing the token declaration with `ignore_`. This approach is suitable for basic token discarding but offers less control over matching order compared to function-based rules.

```Python
t_ignore_COMMENT = r'\#.*'
```

--------------------------------

### Custom Actions for PLY Lexer Literal Tokens

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to define token functions for literal characters to perform additional actions. When using functions for literals, it is crucial to explicitly set the `t.type` attribute to the expected literal character before returning the token.

```Python
literals = [ '{', '}' ]

def t_lbrace(t):
    r'\{'
    t.type = '{'      # Set token type to the expected literal
    return t

def t_rbrace(t):
    r'\}'
    t.type = '}'      # Set token type to the expected literal
    return t
```

--------------------------------

### Define Required Token Names for PLY Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python snippet specifically shows the `tokens` list, which is a mandatory component for any `ply.lex` lexer definition. This list explicitly declares all possible token names that the lexer is designed to recognize and produce. It is used internally by PLY for validation and by `yacc.py` for parser definition.

```Python
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)
```

--------------------------------

### Configure Custom Logging for PLY Lexer and Parser Errors

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to direct PLY's error messages and warnings to a custom logging object. By passing a logger instance to the `errorlog` parameter in `lex.lex()` and `yacc.yacc()`, error handling can be centralized.

```Python
lex.lex(errorlog=log)
yacc.yacc(errorlog=log)
```

--------------------------------

### PLY Error Recovery: Discarding Token and Signaling OK

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This `p_error()` function handles syntax errors by printing an error message and then using `parser.errok()` to reset the parser's error state. This effectively discards the problematic token and tells the parser to continue as if the error was resolved, preventing further error tokens from being generated immediately.

```Python
def p_error(p):
    if p:
         print("Syntax error at token", p.type)
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")
```

--------------------------------

### Define PLY Lexer Rules in a Separate Python Module

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python module (`tokrules.py`) defines the token names and regular expression rules for a simple arithmetic lexer. It includes rules for numbers, operators, ignored characters, newlines, and error handling, making it reusable for lexer construction in other parts of an application.

```Python
# module: tokrules.py
# This module just contains the lexing rules

# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
```

--------------------------------

### Declaring Operator Precedence and Associativity in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python snippet demonstrates how to define operator precedence and associativity using the `precedence` variable in a `yacc.py` grammar file. Tokens are listed from lowest to highest precedence, and their associativity ('left' or 'right') is specified to resolve shift/reduce conflicts.

```Python
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)
```

--------------------------------

### PLY Grammar Rule for Valid Print Statement

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Defines a standard PLY grammar rule for a print statement. It expects the 'PRINT' keyword, followed by an expression ('expr'), and terminated by a semicolon ('SEMI'). This rule represents the correct syntax for a print statement in the language.

```Python
def p_statement_print(p):
         'statement : PRINT expr SEMI'
         ...
```

--------------------------------

### Calculating Column Position from PLY Lexer Token

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Provides a utility function to compute the column number for a given token using its `lexpos` attribute and the original input string. This calculation is typically performed on demand, especially for error reporting, rather than for every token.

```Python
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
```

--------------------------------

### PLY Lexer State: Lexer Object Attribute Counter

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates storing state directly on the lexer object via the `t.lexer` attribute. This method is generally safer for multiple lexer instances than global variables, as each lexer instance can maintain its own independent state.

```Python
def t_NUMBER(t):
    r'\d+'
    t.lexer.num_count += 1     # Note the use of lexer attribute
    t.value = int(t.value)    
    return t

lexer = lex.lex()
lexer.num_count = 0            # Set the initial count
```

--------------------------------

### Define State-Specific Ignored Characters and Error Handlers

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to define state-specific `t_ignore` for characters to be ignored and `t_error()` functions for custom error handling within a particular lexing state, overriding the default behavior.

```Python
t_foo_ignore = " \t\n"       # Ignored characters for state 'foo'

def t_bar_error(t):          # Special error handler for state 'bar'
    pass
```

--------------------------------

### Define EOF Handling Rule in PLY Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet demonstrates how to implement the `t_eof()` function to manage end-of-file conditions in a PLY lexer. It shows how to prompt for and provide more input to the lexer or signal that no more data is available by returning `None`.

```Python
# EOF handling rule
def t_eof(t):
    # Get more input (Example)
    more = input('... ')
    if more:
        t.lexer.input(more)
        return t.lexer.token()
    return None
```

--------------------------------

### PLY Grammar Rule for Print Statement Error Recovery

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to implement syntax error recovery in PLY using the special 'error' token. This rule catches errors within a print statement's expression, allowing the parser to skip problematic tokens until a synchronization token (like 'SEMI') is encountered, enabling continued parsing.

```Python
def p_statement_print_error(p):
         'statement : PRINT error SEMI'
         print("Syntax error in print statement. Bad expression")
```

--------------------------------

### PLY Reduce/Reduce Conflict Warning Message

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet shows the warning message generated by `yacc()` when a reduce/reduce conflict is detected. It indicates the number of conflicts, how a specific conflict was resolved (by picking the first rule), and which rule was rejected, aiding in debugging grammar ambiguities.

```Log
WARNING: 1 reduce/reduce conflict
WARNING: reduce/reduce conflict in state 15 resolved using rule (assignment -> ID EQUALS NUMBER)
WARNING: rejected rule (expression -> NUMBER)
```

--------------------------------

### Implement Unary Minus Grammar Rule with %prec in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python snippet shows a grammar rule for a unary minus operator. It uses the `%prec UMINUS` qualifier to explicitly set the precedence of this rule to that of the `UMINUS` fictitious token defined in the precedence table, ensuring it's evaluated with higher priority.

```Python
def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]
```

--------------------------------

### Set Precedence for Terminals in PLY Grammar

Source: https://github.com/dabeaz/ply/blob/master/doc/internals.md

This snippet demonstrates how to set precedence levels and associativity for terminal symbols using the `g.set_precedence()` method of the `Grammar` class. Higher `level` values indicate higher precedence. This method must be called before adding any productions to the grammar.

```python
g.set_precedence('PLUS',  'left',1)
g.set_precedence('MINUS', 'left',1)
g.set_precedence('TIMES', 'left',2)
g.set_precedence('DIVIDE','left',2)
g.set_precedence('UMINUS','left',3)
```

--------------------------------

### PLY Production Rule: Manually Raising SyntaxError

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python production rule demonstrates how to manually force the PLY parser into error recovery mode by raising a `SyntaxError` exception. This mimics a syntax error detection, causing the last shifted symbol to be popped and an 'error' token to be set, initiating error recovery without calling `p_error()`.

```Python
def p_production(p):
    'production : some production ...'
    raise SyntaxError
```

--------------------------------

### Silence PLY Lexer and Parser Warnings

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows how to completely suppress warnings from PLY by passing `yacc.NullLogger()` (or `lex.NullLogger()`) to the `errorlog` parameter. This can be useful in production environments where warnings are not desired.

```Python
yacc.yacc(errorlog=yacc.NullLogger())
```

--------------------------------

### Declare Lexer States in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to declare custom lexing states ('exclusive' or 'inclusive') in PLY using the `states` tuple. Exclusive states completely override default lexer behavior, while inclusive states add to it.

```Python
states = (
   ('foo','exclusive'),
   ('bar','inclusive'),
)
```

--------------------------------

### Define Complex Regular Expressions for PLY Tokens

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet illustrates how complex regular expressions can be defined using Python variables. It highlights a scenario where these variables cannot be directly used as docstrings for token functions, setting the context for the `@TOKEN` decorator.

```Python
digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

def t_ID(t):
    # want docstring to be identifier above. ?????
    ...
```

--------------------------------

### Discarding Tokens by Returning No Value in PLY Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Demonstrates how to discard a token in PLY's lexer by defining a token rule function that explicitly returns no value. This method is useful for ignoring comments or other non-essential parts of the input stream, providing precise control over matching order.

```Python
def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded
```

--------------------------------

### PLY Parser Configuration: Disabling Defaulted States

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This Python snippet shows how to disable 'defaulted states' in a PLY parser. By setting `parser.defaulted_states` to an empty dictionary, you can prevent the parser from delaying error reporting by reducing grammar rules without reading the next input token, which can be useful in specific error handling scenarios.

```Python
parser = yacc.yacc()
parser.defaulted_states = {}
```

--------------------------------

### Access Lexer Object within PLY Lexer Rule

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to access the lexer object that triggered a rule from within a lexer rule function. The `t.lexer` attribute provides a reference to the active lexer instance.

```Python
def t_NUMBER(t):
   r'\d+'
   ...
   print(t.lexer)           ## Show lexer object
```

--------------------------------

### Declaring Character Literals in PLY Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Shows how to declare single character literals (e.g., '+', '-', '*', '/') in a PLY lexer file using the `literals` variable. This declaration is crucial when using character literals directly in grammar rules instead of named tokens.

```Python
# Literals should be placed in module given to lex()
literals = ['+','-','*','/']
```

--------------------------------

### Disable PLY Parser Debug Output

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to disable the generation of the `parser.out` debug file in PLY by passing `debug=False` to the `yacc.yacc` function. This is useful for production environments or when debug information is not needed.

```Python
yacc.yacc(debug=False)
```

--------------------------------

### Updating Line Numbers in PLY Lexer

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

Illustrates how to define a special rule (`t_newline`) to track and update line numbers within the PLY lexer. The `lineno` attribute of `t.lexer` is incremented based on the length of the matched newline characters, and the token is discarded as nothing is returned.

```Python
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
```

--------------------------------

### Define Operator Precedence with Unary Minus in PLY

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet demonstrates how to define operator precedence in PLY using a `precedence` tuple. It specifically shows how to introduce a 'fictitious token' like `UMINUS` to assign a higher precedence to the unary minus operator, overriding its default precedence relative to other operators like `TIMES`.

```Python
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),            # Unary minus operator
)
```

--------------------------------

### Define Non-Associative Operators in PLY Precedence

Source: https://github.com/dabeaz/ply/blob/master/doc/ply.md

This snippet illustrates how to specify non-associativity for operators in PLY's `precedence` table. By using `'nonassoc'`, it prevents chaining of operations like `a < b < c`, causing a syntax error for such constructs while allowing simple expressions like `a < b`.

```Python
precedence = (
    ('nonassoc', 'LESSTHAN', 'GREATERTHAN'),  # Nonassociative operators
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),            # Unary minus operator
)
```

=== COMPLETE CONTENT === This response contains all available snippets from this library. No additional content exists. Do not make further requests.