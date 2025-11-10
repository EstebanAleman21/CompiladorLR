#############################################
#   LEXER Y PARSER COMPLETO PARA LITTLE DUCK
#   CON MANEJO DE ERRORES Y RECUPERACIÓN
#############################################

import ply.lex as lex
import ply.yacc as yacc
import sys

# Palabras reservadas
reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'print': 'PRINT',
    'main': 'MAIN',
    'end': 'END',
    'string': 'STRING'
}

# Tokens
tokens = [
    'CONST_INT',
    'CONST_FLOAT',
    'CONST_STRING',
    'ID',
    'OP_ASIGNA',
    'OP_SUMA',
    'OP_RESTA',
    'OP_MULT',
    'OP_DIV',
    'OP_EQ',
    'OP_NEQ',
    'OP_LEQ',
    'OP_GEQ',
    'OP_LT',
    'OP_GT',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACK',
    'RBRACK',
    'COMMA',
    'SEMICOL',
    'COLON',
] + list(reserved.values())

# Contador de errores global
lexer_errors = []
parser_errors = []

t_ignore = ' \t\r'

# Operadores (orden importante: más largos primero)
t_OP_EQ = r'=='
t_OP_NEQ = r'!='
t_OP_LEQ = r'<='
t_OP_GEQ = r'>='
t_OP_LT = r'<'
t_OP_GT = r'>'
t_OP_ASIGNA = r'='
t_OP_SUMA = r'\+'
t_OP_RESTA = r'-'
t_OP_MULT = r'\*'
t_OP_DIV = r'/'

# Delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMMA = r','
t_SEMICOL = r';'
t_COLON = r':'

def t_COMMENT_BLOCK(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    pass

def t_COMMENT(t):
    r'(//[^\n]*)|(\#[^\n]*)'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_CONST_FLOAT(t):
    r'\d+\.\d+(?:[eE][\+\-]?\d+)?'
    t.value = float(t.value)
    return t

def t_CONST_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CONST_STRING(t):
    r'"([^"\\]|\\.)*"'
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    error_msg = f"ERROR LÉXICO en línea {t.lineno}: Carácter ilegal '{t.value[0]}'"
    lexer_errors.append(error_msg)
    print(f"❌ {error_msg}")
    t.lexer.skip(1)

###############################################################
#                    CONSTRUCCIÓN DEL LEXER
###############################################################

lexer = lex.lex()
print("✅ Lexer construido correctamente")

###############################################################
#                    PARSER LR CON GRAMÁTICA
###############################################################

precedence = (
    ('left', 'OP_EQ', 'OP_NEQ', 'OP_LT', 'OP_GT', 'OP_LEQ', 'OP_GEQ'),
    ('left', 'OP_SUMA', 'OP_RESTA'),
    ('left', 'OP_MULT', 'OP_DIV'),
    ('right', 'UMINUS'),
)

start = 'program'

############### GRAMÁTICA LR ###############

def p_program(p):
    '''program : PROGRAM ID SEMICOL vars funcs MAIN body END'''
    p[0] = ('program', p[2], p[4], p[5], p[7])

# VARS - Reglas separadas
def p_vars_empty(p):
    '''vars : empty'''
    p[0] = []

def p_vars_multiple(p):
    '''vars : vars var'''
    p[0] = p[1] + [p[2]]

def p_var(p):
    '''var : VAR id_list COLON type SEMICOL'''
    p[0] = ('var_decl', p[2], p[4])

def p_vars_continuation(p):
    '''vars : vars id_list COLON type SEMICOL'''
    p[0] = p[1] + [('var_decl', p[2], p[4])]

# ID_LIST - Reglas separadas
def p_id_list_single(p):
    '''id_list : ID'''
    p[0] = [p[1]]

def p_id_list_multiple(p):
    '''id_list : ID COMMA id_list'''
    p[0] = [p[1]] + p[3]

# TYPES - Reglas separadas
def p_type_int(p):
    '''type : INT'''
    p[0] = 'int'

def p_type_float(p):
    '''type : FLOAT'''
    p[0] = 'float'

def p_type_string(p):
    '''type : STRING'''
    p[0] = 'string'

# FUNCS - Reglas separadas
def p_funcs_empty(p):
    '''funcs : empty'''
    p[0] = []

def p_funcs_single(p):
    '''funcs : func'''
    p[0] = [p[1]]

def p_funcs_multiple(p):
    '''funcs : funcs func'''
    p[0] = p[1] + [p[2]]

def p_func(p):
    '''func : VOID ID LPAREN params RPAREN LBRACK vars body RBRACK SEMICOL'''
    p[0] = ('func_decl', p[2], p[4], p[7], p[8])

# PARAMS - Reglas separadas
def p_params_empty(p):
    '''params : empty'''
    p[0] = []

def p_params_list(p):
    '''params : param_list'''
    p[0] = p[1]

# PARAM_LIST - Reglas separadas
def p_param_list_single(p):
    '''param_list : param'''
    p[0] = [p[1]]

def p_param_list_multiple(p):
    '''param_list : param COMMA param_list'''
    p[0] = [p[1]] + p[3]

def p_param(p):
    '''param : ID COLON type'''
    p[0] = ('param', p[1], p[3])

def p_body(p):
    '''body : LBRACE statements RBRACE'''
    p[0] = ('body', p[2])

# STATEMENTS - Reglas separadas
def p_statements_empty(p):
    '''statements : empty'''
    p[0] = []

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

# STATEMENT - Reglas separadas por tipo
def p_statement_assign(p):
    '''statement : assign'''
    p[0] = p[1]

def p_statement_condition(p):
    '''statement : condition'''
    p[0] = p[1]

def p_statement_cycle(p):
    '''statement : cycle'''
    p[0] = p[1]

def p_statement_call(p):
    '''statement : f_call'''
    p[0] = p[1]

def p_statement_print(p):
    '''statement : print_stmt'''
    p[0] = p[1]

def p_assign(p):
    '''assign : ID OP_ASIGNA expression SEMICOL'''
    p[0] = ('assign', p[1], p[3])

def p_expression(p):
    '''expression : exp rel_exp_tail'''
    p[0] = ('expr', p[1], p[2]) if p[2] else p[1]

# REL_EXP_TAIL - Reglas separadas
def p_rel_exp_tail_empty(p):
    '''rel_exp_tail : empty'''
    p[0] = None

def p_rel_exp_tail_rel(p):
    '''rel_exp_tail : rel_op exp'''
    p[0] = (p[1], p[2])

# REL_OP - Reglas separadas
def p_rel_op_gt(p):
    '''rel_op : OP_GT'''
    p[0] = '>'

def p_rel_op_lt(p):
    '''rel_op : OP_LT'''
    p[0] = '<'

def p_rel_op_neq(p):
    '''rel_op : OP_NEQ'''
    p[0] = '!='

def p_rel_op_eq(p):
    '''rel_op : OP_EQ'''
    p[0] = '=='

def p_rel_op_geq(p):
    '''rel_op : OP_GEQ'''
    p[0] = '>='

def p_rel_op_leq(p):
    '''rel_op : OP_LEQ'''
    p[0] = '<='

# EXP - Reglas separadas (left-recursive para LR)
def p_exp_sum(p):
    '''exp : exp OP_SUMA termino'''
    p[0] = ('+', p[1], p[3])

def p_exp_sub(p):
    '''exp : exp OP_RESTA termino'''
    p[0] = ('-', p[1], p[3])

def p_exp_termino(p):
    '''exp : termino'''
    p[0] = p[1]

# TERMINO - Reglas separadas (left-recursive para LR)
def p_termino_mul(p):
    '''termino : termino OP_MULT factor'''
    p[0] = ('*', p[1], p[3])

def p_termino_div(p):
    '''termino : termino OP_DIV factor'''
    p[0] = ('/', p[1], p[3])

def p_termino_factor(p):
    '''termino : factor'''
    p[0] = p[1]

# FACTOR - Reglas separadas
def p_factor_group(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_factor_sign(p):
    '''factor : OP_RESTA factor %prec UMINUS'''
    p[0] = ('uminus', p[2])

def p_factor_id(p):
    '''factor : ID'''
    p[0] = ('id', p[1])

def p_factor_int(p):
    '''factor : CONST_INT'''
    p[0] = ('int', p[1])

def p_factor_float(p):
    '''factor : CONST_FLOAT'''
    p[0] = ('float', p[1])

def p_factor_string(p):
    '''factor : CONST_STRING'''
    p[0] = ('string', p[1])

def p_print(p):
    '''print_stmt : PRINT LPAREN print_args RPAREN SEMICOL'''
    p[0] = ('print', p[3])

# PRINT_ARGS - Reglas separadas
def p_print_args_single(p):
    '''print_args : print_item'''
    p[0] = [p[1]]

def p_print_args_multiple(p):
    '''print_args : print_item COMMA print_args'''
    p[0] = [p[1]] + p[3]

# PRINT_ITEM - Reglas separadas
def p_print_item_expr(p):
    '''print_item : expression'''
    p[0] = p[1]

def p_print_item_string(p):
    '''print_item : CONST_STRING'''
    p[0] = ('string', p[1])

def p_cycle(p):
    '''cycle : DO body WHILE LPAREN expression RPAREN SEMICOL'''
    p[0] = ('do_while', p[2], p[5])

def p_condition(p):
    '''condition : IF LPAREN expression RPAREN body else_part SEMICOL'''
    p[0] = ('if', p[3], p[5], p[6])

# ELSE_PART - Reglas separadas
def p_else_part_empty(p):
    '''else_part : empty'''
    p[0] = None

def p_else_part_else(p):
    '''else_part : ELSE body'''
    p[0] = p[2]

def p_f_call(p):
    '''f_call : ID LPAREN call_args RPAREN SEMICOL'''
    p[0] = ('call', p[1], p[3])

# CALL_ARGS - Reglas separadas
def p_call_args_empty(p):
    '''call_args : empty'''
    p[0] = []

def p_call_args_single(p):
    '''call_args : expression'''
    p[0] = [p[1]]

def p_call_args_multiple(p):
    '''call_args : expression COMMA call_args'''
    p[0] = [p[1]] + p[3]

def p_empty(p):
    '''empty :'''
    pass

# MANEJO DE ERRORES CON RECUPERACIÓN
def p_error(p):
    if p:
        error_msg = f"ERROR SINTÁCTICO en línea {p.lineno}: Token inesperado '{p.value}' (tipo: {p.type})"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")

        # Estrategia de recuperación: saltar hasta el siguiente punto y coma
        while True:
            tok = parser.token()
            if not tok or tok.type == 'SEMICOL':
                break
        parser.restart()
    else:
        error_msg = "ERROR SINTÁCTICO: Fin inesperado del archivo"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")

###############################################################
#                    CONSTRUCCIÓN DEL PARSER
###############################################################

parser = yacc.yacc(write_tables=False, debug=False)
print("✅ Parser LR construido correctamente\n")

###############################################################
#              FUNCIONES PARA ANÁLISIS DE ARCHIVOS
###############################################################

def analizar_archivo(filename):
    """Lee y analiza un archivo .txt con código Little Duck"""
    global lexer_errors, parser_errors
    lexer_errors = []
    parser_errors = []

    print("="*70)
    print(f"📄 ANALIZANDO ARCHIVO: {filename}")
    print("="*70)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo '{filename}'")
        return False
    except Exception as e:
        print(f"❌ ERROR al leer archivo: {e}")
        return False

    print("\n📝 CÓDIGO FUENTE:")
    print("-"*70)
    for i, linea in enumerate(codigo.split('\n'), 1):
        print(f"{i:3d} | {linea}")
    print("-"*70)

    # Crear un NUEVO lexer para este análisis
    file_lexer = lex.lex()
    file_lexer.lineno = 1
    
    # Análisis léxico
    print("\n🔍 ANÁLISIS LÉXICO:")
    print("-"*70)
    file_lexer.input(codigo)
    tokens_list = []

    while True:
        tok = file_lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
        if tok.type not in ['COMMENT', 'COMMENT_BLOCK']:
            print(f"  Línea {tok.lineno:3d}: {tok.type:15s} = {repr(tok.value)[:40]}")

    print(f"\n✅ Total de tokens reconocidos: {len(tokens_list)}")

    if lexer_errors:
        print(f"\n⚠️  Se encontraron {len(lexer_errors)} errores léxicos")

    # Análisis sintáctico con el MISMO lexer
    print("\n🔍 ANÁLISIS SINTÁCTICO:")
    print("-"*70)
    
    # Reiniciar el lexer para el parser
    file_lexer.lineno = 1
    resultado = parser.parse(codigo, lexer=file_lexer)

    # Reporte final
    print("\n" + "="*70)
    print("📊 REPORTE FINAL")
    print("="*70)

    total_errores = len(lexer_errors) + len(parser_errors)

    if total_errores == 0:
        print("✅ ¡PROGRAMA VÁLIDO! No se encontraron errores")
        print(f"✅ Estructura del programa parseada correctamente")
        return True
    else:
        print(f"❌ Se encontraron {total_errores} errores en total:")
        print(f"   - Errores léxicos: {len(lexer_errors)}")
        print(f"   - Errores sintácticos: {len(parser_errors)}")
        print("\n📋 Lista de errores:")
        for err in lexer_errors + parser_errors:
            print(f"   • {err}")
        return False

def analizar_codigo_directo(codigo, nombre="código"):
    """Analiza código directamente sin archivo"""
    global lexer_errors, parser_errors
    lexer_errors = []
    parser_errors = []

    print("="*70)
    print(f"📄 ANALIZANDO: {nombre}")
    print("="*70)

    print("\n📝 CÓDIGO:")
    print("-"*70)
    print(codigo)
    print("-"*70)

    # Crear un NUEVO lexer para este análisis
    test_lexer = lex.lex()
    test_lexer.lineno = 1
    resultado = parser.parse(codigo, lexer=test_lexer)

    total_errores = len(lexer_errors) + len(parser_errors)

    if total_errores == 0:
        print("\n✅ ¡CÓDIGO VÁLIDO!")
        return True
    else:
        print(f"\n❌ Errores encontrados: {total_errores}")
        return False

###############################################################
#                    EJEMPLOS Y PRUEBAS
###############################################################

if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPILADOR LITTLE DUCK - LEXER Y PARSER LR")
    print("="*70 + "\n")

    # Ejemplos de prueba
    tests = [
        ("Programa simple", """program test;
var x:int;
main {
   x = 5 + 3 * 2;
}
end
"""),
        ("Programa con if-else", """program p;
var i:int;
main {
   if(3 < 2) { print("no"); } else { print("yes"); };
}
end
"""),
        ("Programa con función", """program p;
var a:int;
void f(n:int) [ var x:int; { print(n); } ];
main {
  a = 5;
  f(a);
}
end
"""),
        ("Programa con error léxico", """program test;
var x:int;
main {
   x = 5 @ 3;
}
end
"""),
        ("Programa con error sintáctico", """program test;
var x:int;
main {
   x = 5 +;
}
end
""")
    ]

    for nombre, codigo in tests:
        analizar_codigo_directo(codigo, nombre)
        print("\n")

    # Para analizar un archivo:
    analizar_archivo("factorial.txt")