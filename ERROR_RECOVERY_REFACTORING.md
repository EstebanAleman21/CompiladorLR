# Error Recovery Refactoring: main.py → main_improved.py

## Overview

This document explains the refactoring of error recovery mechanisms in the Little Duck compiler, transitioning from 14 hardcoded error rules to 6 strategic rules that properly leverage PLY's built-in error recovery features.

## Background

The original implementation (`main.py`) contained 14 specific error recovery rules. While functional, the teacher mentioned that PLY (Python Lex-Yacc) library has built-in mechanisms to handle error recovery more elegantly. This refactoring investigates and applies PLY's recommended patterns.

## PLY's Error Recovery Mechanism

According to the official PLY documentation (`Ply_docs.md`), PLY provides:

1. **Special `error` Token**: A reserved token type that can be placed in grammar rules (line 23 in docs)
2. **`parser.errok()` Method**: Resets the parser's error state (lines 2001-2010 in docs)
3. **Synchronization Pattern**: Place `error` token followed by synchronization tokens (`;`, `}`, `)`, etc.)

### Key Documentation Reference

From PLY docs (lines 2001-2010):
```
- parser.errok(). This resets the parser state so it doesn't think it's in
  error-mode anymore. This will prevent an error token from being generated
  and will reset the internal error counters so that the next syntax error
  will call p_error() again.
```

## What Changed

### Summary of Changes

| Aspect | main.py (Original) | main_improved.py (Improved) |
|--------|-------------------|----------------------------|
| Number of error rules | 14 specific rules | 6 strategic rules |
| Approach | Hardcoded for each case | Strategic sync points |
| `p_error()` function | Simple fallback | Simple fallback (unchanged) |
| Error count on factorial.txt | 2 errors | 2 errors (maintained) |
| Code complexity | High (14 rules) | Low (6 rules) |
| PLY feature usage | Basic | Proper synchronization |

### Reduction in Rules: 14 → 6

**Original 14 Rules** (main.py):
1. `p_assign_error_expr` - Assignment expression errors
2. `p_assign_error_semicol` - Missing semicolon in assignment
3. `p_print_error_args` - Print argument errors
4. `p_print_error_semicol` - Missing semicolon in print
5. `p_condition_error_expr` - If condition expression errors
6. `p_condition_error_parens` - Missing parentheses in if
7. `p_condition_error_semicol` - Missing semicolon in if
8. `p_cycle_error_body` - Do-while body errors
9. `p_cycle_error_cond` - Do-while condition errors
10. `p_cycle_error_semicol` - Missing semicolon in do-while
11. `p_call_error_args` - Function call argument errors
12. `p_call_error_parens` - Missing parentheses in function call
13. `p_expression_error` - Expression errors
14. `p_factor_error_parens` - Factor parenthesis errors

**New 6 Strategic Rules** (main_improved.py):
1. `p_statement_error` - General statement errors (sync on `;`)
2. `p_body_error` - Code block errors (sync on `}`)
3. `p_factor_error` - Expression errors in parentheses (sync on `)`)
4. `p_print_error` - Print statement errors (2 variants)
5. `p_condition_error` - If statement errors (2 variants)
6. `p_cycle_error` - Do-while loop errors (2 variants)

## Detailed Rule Comparison

### 1. Statement-Level Errors

**Before (main.py)**: Multiple specific rules
```python
# Rule 1: Assignment expression error
def p_assign_error_expr(p):
    '''assign : ID OP_ASIGNA error SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en expresión de asignación a '{p[1]}' en línea {p.lineno(1)}"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('assign', p[1], ('error',))

# Rule 2: Assignment semicolon error
def p_assign_error_semicol(p):
    '''assign : ID OP_ASIGNA expression error'''
    msg = f"⚠️ RECUPERACIÓN: Se esperaba ';' después de asignación en línea {p.lineno(1)}"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('assign', p[1], p[3])
```

**After (main_improved.py)**: Single general rule
```python
# REGLA 1: Error general en statements - Sincroniza en ;
def p_statement_error(p):
    '''statement : error SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Statement inválido, sincronizando en ';'"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('error_stmt',)
```

**Why This Works**: By placing the error recovery at the statement level and synchronizing on `;`, we catch all statement-level errors (assignments, calls, etc.) without needing specific rules for each case.

### 2. Block-Level Errors

**Before (main.py)**: No specific block error rule

**After (main_improved.py)**: Strategic block recovery
```python
# REGLA 2: Error en bloques de código - Sincroniza en }
def p_body_error(p):
    '''body : LBRACE error RBRACE'''
    msg = f"⚠️ RECUPERACIÓN: Error en bloque de código"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('body', [])
```

**Why This Works**: When errors occur inside `{ }` blocks, the parser can discard everything until the closing `}` and continue parsing the next statement.

### 3. Expression-Level Errors

**Before (main.py)**:
```python
def p_expression_error(p):
    '''expression : error'''
    msg = f"⚠️ RECUPERACIÓN: Expresión inválida"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('error',)

def p_factor_error_parens(p):
    '''factor : LPAREN error'''
    msg = f"⚠️ RECUPERACIÓN: Error en expresión entre paréntesis, falta ')'"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('error',)
```

**After (main_improved.py)**:
```python
# REGLA 3: Error en expresiones entre paréntesis
def p_factor_error(p):
    '''factor : LPAREN error RPAREN'''
    msg = f"⚠️ RECUPERACIÓN: Error en expresión entre paréntesis"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('error',)
```

**Why This Works**: By requiring the closing `)`, we ensure proper synchronization. The original rule without `)` could leave the parser in an inconsistent state.

### 4. Print Statement Errors

**Before (main.py)**: Two separate rules
```python
def p_print_error_args(p):
    '''print_stmt : PRINT LPAREN error RPAREN SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en argumentos de print"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('print', [])

def p_print_error_semicol(p):
    '''print_stmt : PRINT LPAREN print_list RPAREN error'''
    msg = f"⚠️ RECUPERACIÓN: Se esperaba ';' después de print"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('print', p[3])
```

**After (main_improved.py)**: Combined with multiple patterns
```python
# REGLA 4: Error en print
def p_print_error(p):
    '''print_stmt : PRINT LPAREN error RPAREN SEMICOL
                  | PRINT error SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en print statement"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('print', [])
```

**Why This Works**: Multiple patterns in a single rule cover both cases (error in arguments and malformed print) while maintaining proper synchronization.

### 5. Conditional Statement Errors

**Before (main.py)**: Three separate rules
```python
def p_condition_error_expr(p):
    '''condition : IF LPAREN error RPAREN body else_part SEMICOL'''
    # ...

def p_condition_error_parens(p):
    '''condition : IF error body else_part SEMICOL'''
    # ...

def p_condition_error_semicol(p):
    '''condition : IF LPAREN expression RPAREN body else_part error'''
    # ...
```

**After (main_improved.py)**: Combined rule
```python
# REGLA 5: Error en condición if
def p_condition_error(p):
    '''condition : IF LPAREN error RPAREN body else_part SEMICOL
                 | IF error body else_part SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en condición if"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('condition', ('error',), p[len(p)-3], p[len(p)-2])
```

**Why This Works**: Two patterns cover the main error cases (bad condition expression and missing parentheses) while ensuring synchronization at the statement end (`;`).

### 6. Loop Errors

**Before (main.py)**: Three separate rules
```python
def p_cycle_error_body(p):
    '''cycle : DO error WHILE LPAREN expression RPAREN SEMICOL'''
    # ...

def p_cycle_error_cond(p):
    '''cycle : DO body WHILE LPAREN error RPAREN SEMICOL'''
    # ...

def p_cycle_error_semicol(p):
    '''cycle : DO body WHILE LPAREN expression RPAREN error'''
    # ...
```

**After (main_improved.py)**: Combined rule
```python
# REGLA 6: Error en ciclo do-while
def p_cycle_error(p):
    '''cycle : DO error WHILE LPAREN expression RPAREN SEMICOL
             | DO body WHILE LPAREN error RPAREN SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en ciclo do-while"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('cycle', ('error',), ('error',))
```

**Why This Works**: Two patterns handle body errors and condition errors separately, synchronizing at proper boundaries.

## The Failed Approach: main_refactored.py

During the refactoring process, an intermediate version (`main_refactored.py`) was attempted that implemented aggressive token searching in `p_error()`:

```python
def p_error(p):
    if p:
        # ... error detection ...
        sync_tokens = {'SEMICOL', 'RBRACE', 'RPAREN', 'END'}
        while True:
            tok = parser.token()
            if not tok:
                break
            if tok.type in sync_tokens:
                parser.errok()
                return tok  # ← THIS CAUSES PROBLEMS
```

**Why It Failed**:
- This produced **27 cascading errors** instead of 2
- Returning unexpected tokens to the parser caused confusion
- The parser didn't expect the sync tokens in its current state

**Lesson Learned**: Let grammar rules with the `error` token handle recovery, not `p_error()`. The `p_error()` function should remain simple and just report the error.

## Key Principles Applied

### 1. Strategic Synchronization Points
Instead of trying to recover at every possible error point, we place recovery rules at natural synchronization boundaries:
- `;` for statements
- `}` for blocks
- `)` for parenthesized expressions

### 2. Error Token Placement
According to PLY docs, the correct pattern is:
```
rule : ... error SYNC_TOKEN ...
```

**NOT**:
```
rule : ... error
```

Without a sync token, the parser doesn't know where to resume.

### 3. Simple p_error() Function
Both versions keep `p_error()` simple:
```python
def p_error(p):
    if p:
        error_msg = f"ERROR SINTÁCTICO en línea {p.lineno}: Token inesperado '{p.value}' (tipo: {p.type})"
        parser_errors.append(error_msg)
        print(error_msg)
        parser.errok()
    else:
        print("ERROR SINTÁCTICO: Fin inesperado del archivo")
```

This provides a fallback for errors not caught by grammar rules.

## Results

### Test Case: factorial.txt

Both versions produce the same error count and quality:

```
ERROR SINTÁCTICO en línea 24: Token inesperado 'claude' (tipo: ID)
⚠️ RECUPERACIÓN: Statement inválido, sincronizando en ';'

=== ERRORES ENCONTRADOS ===
1. ERROR SINTÁCTICO en línea 24: Token inesperado 'claude' (tipo: ID)
2. ⚠️ RECUPERACIÓN: Statement inválido, sincronizando en ';'

Total de errores: 2
```

The refactored version achieves the same error detection with:
- **57% fewer rules** (6 vs 14)
- **Cleaner code organization**
- **Better adherence to PLY best practices**
- **Same error recovery quality**

## Verification Against PLY Documentation

The improved implementation correctly uses PLY's features as documented:

1. **`error` Token**: Special PLY token (docs line 23) ✓
2. **`parser.errok()`**: PLY's API to reset error state (docs lines 2001-2010) ✓
3. **Synchronization Pattern**: Error token followed by sync tokens (`;`, `}`, `)`) ✓
4. **Grammar Rule Approach**: Error handling in grammar rules, not just in `p_error()` ✓

## Conclusion

The refactoring from `main.py` to `main_improved.py` demonstrates that:

1. PLY's `error` token mechanism was already being used in the original code
2. The improvement comes from strategic placement rather than quantity of rules
3. Fewer, well-placed error recovery rules are more effective than many specific rules
4. Proper synchronization points are crucial for preventing cascading errors
5. The `p_error()` function should remain simple and serve as a fallback

The result is cleaner, more maintainable code that properly leverages PLY's built-in error recovery mechanisms while maintaining the same error detection quality.

## References

- PLY Documentation: `Ply_docs.md`
  - Error token definition: line 23
  - `parser.errok()` documentation: lines 2001-2010
- Original implementation: `main.py`
- Improved implementation: `main_improved.py`
- Failed intermediate attempt: `main_refactored.py`
- Test file: `factorial.txt`
