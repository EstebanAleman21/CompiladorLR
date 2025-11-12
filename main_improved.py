#############################################
#   LEXER Y PARSER - VERSIÓN MEJORADA
#   Usando las mejores prácticas de PLY para error recovery
#   Combina: error token en gramática + p_error() inteligente
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

# Operadores
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

# VARS
def p_vars_empty(p):
    '''vars : empty'''
    p[0] = []

def p_vars_first(p):
    '''vars : VAR var_list'''
    p[0] = p[2]

def p_var_list_single(p):
    '''var_list : id_list COLON type SEMICOL'''
    p[0] = [('var_decl', p[1], p[3])]

def p_var_list_multiple(p):
    '''var_list : id_list COLON type SEMICOL var_list'''
    p[0] = [('var_decl', p[1], p[3])] + p[5]

# ID_LIST
def p_id_list_single(p):
    '''id_list : ID'''
    p[0] = [p[1]]

def p_id_list_multiple(p):
    '''id_list : ID COMMA id_list'''
    p[0] = [p[1]] + p[3]

# TYPES
def p_type_int(p):
    '''type : INT'''
    p[0] = 'int'

def p_type_float(p):
    '''type : FLOAT'''
    p[0] = 'float'

def p_type_string(p):
    '''type : STRING'''
    p[0] = 'string'

# FUNCS
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
    '''func : VOID ID LPAREN params RPAREN LBRACK func_vars body RBRACK SEMICOL'''
    p[0] = ('func_decl', p[2], p[4], p[7], p[8])

# FUNC_VARS
def p_func_vars_empty(p):
    '''func_vars : empty'''
    p[0] = []

def p_func_vars_first(p):
    '''func_vars : VAR func_var_list'''
    p[0] = p[2]

def p_func_var_list_single(p):
    '''func_var_list : id_list COLON type SEMICOL'''
    p[0] = [('var_decl', p[1], p[3])]

def p_func_var_list_multiple(p):
    '''func_var_list : id_list COLON type SEMICOL func_var_list'''
    p[0] = [('var_decl', p[1], p[3])] + p[5]

# PARAMS
def p_params_empty(p):
    '''params : empty'''
    p[0] = []

def p_params_list(p):
    '''params : param_list'''
    p[0] = p[1]

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

# STATEMENTS
def p_statements_empty(p):
    '''statements : empty'''
    p[0] = []

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

# STATEMENT
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

def p_rel_exp_tail_empty(p):
    '''rel_exp_tail : empty'''
    p[0] = None

def p_rel_exp_tail_rel(p):
    '''rel_exp_tail : rel_op exp'''
    p[0] = (p[1], p[2])

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

def p_exp_sum(p):
    '''exp : exp OP_SUMA termino'''
    p[0] = ('+', p[1], p[3])

def p_exp_sub(p):
    '''exp : exp OP_RESTA termino'''
    p[0] = ('-', p[1], p[3])

def p_exp_termino(p):
    '''exp : termino'''
    p[0] = p[1]

def p_termino_mul(p):
    '''termino : termino OP_MULT factor'''
    p[0] = ('*', p[1], p[3])

def p_termino_div(p):
    '''termino : termino OP_DIV factor'''
    p[0] = ('/', p[1], p[3])

def p_termino_factor(p):
    '''termino : factor'''
    p[0] = p[1]

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

def p_print_args_single(p):
    '''print_args : print_item'''
    p[0] = [p[1]]

def p_print_args_multiple(p):
    '''print_args : print_item COMMA print_args'''
    p[0] = [p[1]] + p[3]

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

def p_else_part_empty(p):
    '''else_part : empty'''
    p[0] = None

def p_else_part_else(p):
    '''else_part : ELSE body'''
    p[0] = p[2]

def p_f_call(p):
    '''f_call : ID LPAREN call_args RPAREN SEMICOL'''
    p[0] = ('call', p[1], p[3])

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

###############################################################
#  ERROR RECOVERY - MEJORES PRÁCTICAS DE PLY
#  Estrategia: Usar 'error' token en puntos de sincronización clave
###############################################################

# REGLA 1: Error general en statements - Sincroniza en ; (MÁS IMPORTANTE)
# Según PLY docs: "Place error at the end, not beginning" para mejor recovery
def p_statement_error(p):
    '''statement : error SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Statement inválido, sincronizando en ';'"
    parser_errors.append(msg)
    print(msg)
    parser.errok()  # Reset error state
    p[0] = ('error_stmt',)

# REGLA 2: Error en bloques de código - Sincroniza en }
def p_body_error(p):
    '''body : LBRACE error RBRACE'''
    msg = f"⚠️ RECUPERACIÓN: Error en bloque de código"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('body', [])

# REGLA 3: Error en expresiones dentro de paréntesis
def p_factor_error(p):
    '''factor : LPAREN error RPAREN'''
    msg = f"⚠️ RECUPERACIÓN: Error en expresión entre paréntesis"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('error',)

# REGLA 4: Error en print - Sincroniza en ;
# PLY docs: "Good placement for error recovery"
def p_print_error(p):
    '''print_stmt : PRINT LPAREN error RPAREN SEMICOL
                  | PRINT error SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en print statement"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('print', [])

# REGLA 5: Error en condición if
def p_condition_error(p):
    '''condition : IF LPAREN error RPAREN body else_part SEMICOL
                 | IF error body else_part SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en condición if"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('if', ('error',), p[5] if len(p) == 8 else p[3], p[6] if len(p) == 8 else p[4])

# REGLA 6: Error en ciclo do-while
def p_cycle_error(p):
    '''cycle : DO error WHILE LPAREN expression RPAREN SEMICOL
             | DO body WHILE LPAREN error RPAREN SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en ciclo do-while"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    if len(p) == 8 and p[2] == 'error':
        p[0] = ('do_while', ('body', []), p[5])
    else:
        p[0] = ('do_while', p[2], ('error',))

# REGLA 7: Error en asignación - Sincroniza en ;
def p_assign_error(p):
    '''assign : ID OP_ASIGNA error SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en expresión de asignación a '{p[1]}'"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('assign', p[1], ('error',))

# REGLA 8: Error en llamada a función - Sincroniza en ;
def p_f_call_error(p):
    '''f_call : ID LPAREN error RPAREN SEMICOL
              | ID error SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en llamada a función '{p[1]}'"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    p[0] = ('call', p[1], [])

# REGLA 9: Error en función void - Sincroniza en ;
def p_func_error(p):
    '''func : VOID ID LPAREN error RPAREN LBRACK func_vars body RBRACK SEMICOL
            | VOID ID LPAREN params RPAREN LBRACK error RBRACK SEMICOL'''
    msg = f"⚠️ RECUPERACIÓN: Error en definición de función '{p[2]}'"
    parser_errors.append(msg)
    print(msg)
    parser.errok()
    if p[4] == 'error':
        p[0] = ('func_decl', p[2], [], p[7], p[8])
    else:
        p[0] = ('func_decl', p[2], p[4], [], ('body', []))

# MANEJO GLOBAL DE ERRORES (Fallback cuando las reglas no capturan)
def p_error(p):
    if p:
        # Detectar IDs similares a keywords
        similar = {
            'doe': 'do', 'iff': 'if', 'whilee': 'while',
            'printx': 'print', 'voide': 'void', 'programm': 'program',
            'maine': 'main', 'ende': 'end', 'intt': 'int', 'floatt': 'float'
        }

        if p.type == 'ID' and p.value in similar:
            error_msg = f"ERROR SINTÁCTICO en línea {p.lineno}: '{p.value}' no es válido (¿quisiste decir '{similar[p.value]}'?)"
        else:
            error_msg = f"ERROR SINTÁCTICO en línea {p.lineno}: Token inesperado '{p.value}' (tipo: {p.type})"

        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")

        # STRATEGY: When using grammar error rules (error token in productions),
        # DO NOT call parser.errok() here. Let the grammar rules handle it.
        # The parser enters "error mode" after p_error() and will look for
        # grammar rules with the 'error' token. When one matches and calls
        # parser.errok(), the parser exits error mode.
        # This is the recommended approach per PLY docs (line 2008).
    else:
        error_msg = "ERROR SINTÁCTICO: Fin inesperado del archivo"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")

###############################################################
#                    CONSTRUCCIÓN DEL PARSER
###############################################################

parser = yacc.yacc(write_tables=False, debug=False)
print("✅ Parser LR construido correctamente")
print("   📖 Usando error recovery híbrido (grammar rules + p_error)\n")

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

    # Análisis sintáctico
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
    print("COMPILADOR LITTLE DUCK - ERROR RECOVERY MEJORADO")
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
