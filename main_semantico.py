#Jose Daniel Cantú Cantú A01284664
#Esteban Aleman A01285086
#Noviembre 20 2025
#   COMPILADOR LITTLE DUCK - ANÁLISIS SEMÁNTICO
#   Con generación de código intermedio (cuádruplos)

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
    t.value = t.value[1:-1]
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

lexer = lex.lex()
print("✅ Lexer construido correctamente")

###############################################################
#           ESTRUCTURAS DE DATOS SEMÁNTICAS
###############################################################

# Directorio de funciones: {func_name: {type, params: [(name, type)], vars: {}, start_quad}}
function_directory = {}

# Tabla de variables por scope (sin direcciones de memoria)
symbol_table = {}  # {scope: {var_name: tipo}}

# Pilas para análisis semántico
operand_stack = []
type_stack = []
operator_stack = []
jump_stack = []

# Cuádruplos generados
quadruples = []

# Contadores
temp_counter = 1

# Scope actual
current_scope = 'global'
current_function = None

# Cubo semántico expandido
semantic_cube = {
    '+': {
        'int': {'int': 'int', 'float': 'float'},
        'float': {'int': 'float', 'float': 'float'},
        'string': {'string': 'string', 'int': 'string', 'float': 'string'}
    },
    '-': {
        'int': {'int': 'int', 'float': 'float'},
        'float': {'int': 'float', 'float': 'float'}
    },
    '*': {
        'int': {'int': 'int', 'float': 'float'},
        'float': {'int': 'float', 'float': 'float'},
        'string': {'int': 'string'}
    },
    '/': {
        'int': {'int': 'float', 'float': 'float'},
        'float': {'int': 'float', 'float': 'float'}
    },
    '>': {
        'int': {'int': 'bool', 'float': 'bool'},
        'float': {'int': 'bool', 'float': 'bool'},
        'string': {'string': 'bool'}
    },
    '<': {
        'int': {'int': 'bool', 'float': 'bool'},
        'float': {'int': 'bool', 'float': 'bool'},
        'string': {'string': 'bool'}
    },
    '>=': {
        'int': {'int': 'bool', 'float': 'bool'},
        'float': {'int': 'bool', 'float': 'bool'},
        'string': {'string': 'bool'}
    },
    '<=': {
        'int': {'int': 'bool', 'float': 'bool'},
        'float': {'int': 'bool', 'float': 'bool'},
        'string': {'string': 'bool'}
    },
    '==': {
        'int': {'int': 'bool', 'float': 'bool'},
        'float': {'int': 'bool', 'float': 'bool'},
        'string': {'string': 'bool'}
    },
    '!=': {
        'int': {'int': 'bool', 'float': 'bool'},
        'float': {'int': 'bool', 'float': 'bool'},
        'string': {'string': 'bool'}
    },
    '=': {
        'int': {'int': 'int', 'float': 'error'},
        'float': {'int': 'float', 'float': 'float'},
        'string': {'string': 'string', 'int': 'string', 'float': 'string'}
    }
}

###############################################################
#              FUNCIONES AUXILIARES SEMÁNTICAS
###############################################################

def reset_compiler():
    global function_directory, symbol_table, operand_stack, type_stack
    global operator_stack, jump_stack, quadruples, temp_counter
    global current_scope, current_function
    
    function_directory = {}
    symbol_table = {'global': {}}
    operand_stack = []
    type_stack = []
    operator_stack = []
    jump_stack = []
    quadruples = []
    temp_counter = 1
    current_scope = 'global'
    current_function = None

def add_variable(var_name, var_type, scope=None):
    """Añade una variable a la tabla de símbolos (sin direcciones de memoria)"""
    if scope is None:
        scope = current_scope
    
    if scope not in symbol_table:
        symbol_table[scope] = {}
    
    if var_name in symbol_table[scope]:
        error_msg = f"ERROR SEMÁNTICO: Variable '{var_name}' ya declarada en scope '{scope}'"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return None
    
    symbol_table[scope][var_name] = var_type
    return var_name

def lookup_variable(var_name):
    """Busca una variable en el scope actual y luego en global (retorna tipo)"""
    if current_scope in symbol_table and var_name in symbol_table[current_scope]:
        return symbol_table[current_scope][var_name]
    elif 'global' in symbol_table and var_name in symbol_table['global']:
        return symbol_table['global'][var_name]
    else:
        error_msg = f"ERROR SEMÁNTICO: Variable '{var_name}' no declarada"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return None

def add_function(func_name, return_type, params):
    """Añade una función al directorio"""
    if func_name in function_directory:
        error_msg = f"ERROR SEMÁNTICO: Función '{func_name}' ya declarada"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return False
    
    function_directory[func_name] = {
        'type': return_type,
        'params': params,
        'vars': {},
        'start_quad': len(quadruples)
    }
    return True

def check_semantic_cube(operator, type1, type2):
    """Verifica compatibilidad de tipos en el cubo semántico"""
    if operator in semantic_cube:
        if type1 in semantic_cube[operator]:
            if type2 in semantic_cube[operator][type1]:
                return semantic_cube[operator][type1][type2]
    
    error_msg = f"ERROR SEMÁNTICO: Operación '{operator}' no válida entre tipos '{type1}' y '{type2}'"
    parser_errors.append(error_msg)
    print(f"❌ {error_msg}")
    return 'error'

def generate_temp():
    """Genera un temporal y retorna su nombre"""
    global temp_counter
    temp_name = f"t{temp_counter}"
    temp_counter += 1
    return temp_name

def add_quadruple(operator, operand1, operand2, result):
    """Añade un cuádruple a la lista"""
    quadruples.append((operator, operand1, operand2, result))
    return len(quadruples) - 1

def fill_quadruple(quad_index, value):
    """Rellena el campo resultado de un cuádruple pendiente"""
    if quad_index < len(quadruples):
        op, op1, op2, _ = quadruples[quad_index]
        quadruples[quad_index] = (op, op1, op2, value)

###############################################################
#                    PARSER CON SEMÁNTICA
###############################################################

precedence = (
    ('left', 'OP_EQ', 'OP_NEQ', 'OP_LT', 'OP_GT', 'OP_LEQ', 'OP_GEQ'), 
    ('left', 'OP_SUMA', 'OP_RESTA'),
    ('left', 'OP_MULT', 'OP_DIV'),
)

start = 'program'

def p_program(p):
    '''program : PROGRAM ID SEMICOL program_vars program_funcs MAIN program_body END'''
    print("✅ Programa compilado exitosamente")
    add_quadruple('END', None, None, None)

def p_program_vars(p):
    '''program_vars : vars
                    | empty'''
    pass

def p_program_funcs(p):
    '''program_funcs : funcs
                     | empty'''
    pass

def p_program_body(p):
    '''program_body : body'''
    pass

# VARS
def p_vars_empty(p):
    '''vars : empty'''
    pass

def p_vars_first(p):
    '''vars : VAR var_list'''
    pass

def p_var_list_single(p):
    '''var_list : id_list COLON type SEMICOL'''
    var_type = p[3]
    for var_name in p[1]:
        add_variable(var_name, var_type)

def p_var_list_multiple(p):
    '''var_list : id_list COLON type SEMICOL var_list'''
    var_type = p[3]
    for var_name in p[1]:
        add_variable(var_name, var_type)

def p_id_list_single(p):
    '''id_list : ID'''
    p[0] = [p[1]]

def p_id_list_multiple(p):
    '''id_list : ID COMMA id_list'''
    p[0] = [p[1]] + p[3]

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING'''
    p[0] = p[1].lower()

# FUNCS
def p_funcs_empty(p):
    '''funcs : empty'''
    pass

def p_funcs_multiple(p):
    '''funcs : func funcs'''
    pass

def p_func(p):
    '''func : VOID ID func_start LPAREN func_params RPAREN LBRACK func_vars func_body RBRACK SEMICOL func_end'''
    pass

def p_func_start(p):
    '''func_start : '''
    global current_scope, current_function
    func_name = p[-1]
    current_function = func_name
    current_scope = func_name
    symbol_table[current_scope] = {}

def p_func_end(p):
    '''func_end : '''
    global current_scope, current_function
    add_quadruple('ENDFUNC', None, None, None)
    current_scope = 'global'
    current_function = None

def p_func_params(p):
    '''func_params : param_list
                   | empty'''
    params = p[1] if p[1] else []
    func_name = current_function
    add_function(func_name, 'void', params)

def p_param_list_single(p):
    '''param_list : ID COLON type'''
    param_type = p[3]
    add_variable(p[1], param_type)
    p[0] = [(p[1], param_type)]

def p_param_list_multiple(p):
    '''param_list : ID COLON type COMMA param_list'''
    param_type = p[3]
    add_variable(p[1], param_type)
    p[0] = [(p[1], param_type)] + p[5]

def p_func_vars(p):
    '''func_vars : vars
                 | empty'''
    pass

def p_func_body(p):
    '''func_body : body'''
    pass

# BODY
def p_body(p):
    '''body : LBRACE statements RBRACE'''
    pass

def p_statements_single(p):
    '''statements : statement'''
    pass

def p_statements_multiple(p):
    '''statements : statement statements'''
    pass

def p_statement(p):
    '''statement : assign
                 | condition
                 | cycle
                 | f_call
                 | print_stmt'''
    pass

# ASSIGN
def p_assign(p):
    '''assign : ID OP_ASIGNA expression SEMICOL'''
    var_type = lookup_variable(p[1])
    if var_type and len(type_stack) > 0 and len(operand_stack) > 0:
        expr_type = type_stack.pop()
        expr_operand = operand_stack.pop()
        
        result_type = check_semantic_cube('=', var_type, expr_type)
        if result_type != 'error':
            add_quadruple('=', expr_operand, None, p[1])

# CONDITION
def p_condition(p):
    '''condition : IF LPAREN expression RPAREN condition_check LBRACE statements RBRACE SEMICOL condition_end
                 | IF LPAREN expression RPAREN condition_check LBRACE statements RBRACE ELSE condition_else LBRACE statements RBRACE SEMICOL condition_end'''
    pass

def p_condition_check(p):
    '''condition_check : '''
    if len(type_stack) > 0:
        exp_type = type_stack.pop()
        if exp_type != 'bool':
            error_msg = f"ERROR SEMÁNTICO: La condición debe ser una expresión booleana, se recibió '{exp_type}'"
            parser_errors.append(error_msg)
            print(f"❌ {error_msg}")
            return
        
        result = operand_stack.pop()
        quad_index = add_quadruple('GOTOF', result, None, None)
        jump_stack.append(quad_index)

def p_condition_else(p):
    '''condition_else : '''
    quad_index = add_quadruple('GOTO', None, None, None)
    false_jump = jump_stack.pop()
    fill_quadruple(false_jump, len(quadruples))
    jump_stack.append(quad_index)

def p_condition_end(p):
    '''condition_end : '''
    if len(jump_stack) > 0:
        end_jump = jump_stack.pop()
        fill_quadruple(end_jump, len(quadruples))

# CYCLE (WHILE)
def p_cycle_while(p):
    '''cycle : WHILE cycle_start LPAREN expression RPAREN cycle_check LBRACE statements RBRACE cycle_end SEMICOL'''
    pass

def p_cycle_start(p):
    '''cycle_start : '''
    jump_stack.append(len(quadruples))

def p_cycle_check(p):
    '''cycle_check : '''
    if len(type_stack) > 0:
        exp_type = type_stack.pop()
        if exp_type != 'bool':
            error_msg = f"ERROR SEMÁNTICO: La condición del ciclo debe ser booleana, se recibió '{exp_type}'"
            parser_errors.append(error_msg)
            print(f"❌ {error_msg}")
            return
        
        result = operand_stack.pop()
        quad_index = add_quadruple('GOTOF', result, None, None)
        jump_stack.append(quad_index)

def p_cycle_end(p):
    '''cycle_end : '''
    if len(jump_stack) >= 2:
        end_jump = jump_stack.pop()
        return_addr = jump_stack.pop()
        add_quadruple('GOTO', None, None, return_addr)
        fill_quadruple(end_jump, len(quadruples))

# CYCLE (DO-WHILE)
def p_cycle_do(p):
    '''cycle : DO cycle_do_start LBRACE statements RBRACE WHILE LPAREN expression RPAREN cycle_do_end SEMICOL'''
    pass

def p_cycle_do_start(p):
    '''cycle_do_start : '''
    jump_stack.append(len(quadruples))

def p_cycle_do_end(p):
    '''cycle_do_end : '''
    if len(type_stack) > 0:
        exp_type = type_stack.pop()
        if exp_type != 'bool':
            error_msg = f"ERROR SEMÁNTICO: La condición del ciclo debe ser booleana, se recibió '{exp_type}'"
            parser_errors.append(error_msg)
            print(f"❌ {error_msg}")
            return
        
        result = operand_stack.pop()
        return_addr = jump_stack.pop()
        add_quadruple('GOTOT', result, None, return_addr)

# FUNCTION CALL
def p_f_call(p):
    '''f_call : ID LPAREN f_call_start expression_list RPAREN SEMICOL f_call_end
              | ID LPAREN f_call_start RPAREN SEMICOL f_call_end'''
    pass

def p_f_call_start(p):
    '''f_call_start : '''
    func_name = p[-2]
    if func_name not in function_directory:
        error_msg = f"ERROR SEMÁNTICO: Función '{func_name}' no declarada"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")
    else:
        operator_stack.append(('CALL', func_name, 0))

def p_f_call_end(p):
    '''f_call_end : '''
    if len(operator_stack) > 0 and isinstance(operator_stack[-1], tuple) and operator_stack[-1][0] == 'CALL':
        _, func_name, param_count = operator_stack.pop()
        
        if func_name in function_directory:
            expected_params = len(function_directory[func_name]['params'])
            if param_count != expected_params:
                error_msg = f"ERROR SEMÁNTICO: Función '{func_name}' espera {expected_params} parámetros, se pasaron {param_count}"
                parser_errors.append(error_msg)
                print(f"❌ {error_msg}")
            else:
                add_quadruple('CALL', func_name, None, function_directory[func_name]['start_quad'])

# PRINT
def p_print_stmt(p):
    '''print_stmt : PRINT LPAREN expression_list RPAREN SEMICOL'''
    pass

def p_expression_list_single(p):
    '''expression_list : expression print_action'''
    p[0] = 1

def p_expression_list_multiple(p):
    '''expression_list : expression print_action COMMA expression_list'''
    p[0] = 1 + p[4]

def p_print_action(p):
    '''print_action : '''
    if len(operand_stack) > 0:
        operand = operand_stack.pop()
        if len(type_stack) > 0:
            type_stack.pop()
        add_quadruple('PRINT', None, None, operand)
    
    # Incrementar contador de parámetros si estamos en llamada a función
    if len(operator_stack) > 0 and isinstance(operator_stack[-1], tuple) and operator_stack[-1][0] == 'CALL':
        _, func_name, count = operator_stack.pop()
        operator_stack.append(('CALL', func_name, count + 1))
        
        # Validar tipo de parámetro
        if func_name in function_directory:
            params = function_directory[func_name]['params']
            if count < len(params):
                expected_type = params[count][1]
                if len(type_stack) > 0:
                    actual_type = type_stack[-1]
                    if expected_type != actual_type and not (expected_type == 'float' and actual_type == 'int'):
                        error_msg = f"ERROR SEMÁNTICO: Parámetro {count+1} de '{func_name}' debe ser '{expected_type}', se pasó '{actual_type}'"
                        parser_errors.append(error_msg)
                        print(f"❌ {error_msg}")

# EXPRESSION
def p_expression(p):
    '''expression : exp
                  | exp relop exp'''
    if len(p) == 4:
        if len(operand_stack) >= 2 and len(type_stack) >= 2:
            right_type = type_stack.pop()
            right_operand = operand_stack.pop()
            left_type = type_stack.pop()
            left_operand = operand_stack.pop()
            operator = operator_stack.pop()
            
            result_type = check_semantic_cube(operator, left_type, right_type)
            if result_type != 'error':
                temp_name = generate_temp()
                add_quadruple(operator, left_operand, right_operand, temp_name)
                operand_stack.append(temp_name)
                type_stack.append(result_type)

def p_relop(p):
    '''relop : OP_GT
             | OP_LT
             | OP_NEQ
             | OP_EQ
             | OP_GEQ
             | OP_LEQ'''
    operator_stack.append(p[1])

def p_exp_single(p):
    '''exp : termino'''
    pass

def p_exp_add(p):
    '''exp : termino OP_SUMA exp
           | termino OP_RESTA exp'''
    if len(operand_stack) >= 2 and len(type_stack) >= 2:
        right_type = type_stack.pop()
        right_operand = operand_stack.pop()
        left_type = type_stack.pop()
        left_operand = operand_stack.pop()
        operator = p[2]
        
        result_type = check_semantic_cube(operator, left_type, right_type)
        if result_type != 'error':
            temp_name = generate_temp()
            add_quadruple(operator, left_operand, right_operand, temp_name)
            operand_stack.append(temp_name)
            type_stack.append(result_type)

def p_termino_single(p):
    '''termino : factor'''
    pass

def p_termino_mult(p):
    '''termino : factor OP_MULT termino
               | factor OP_DIV termino'''
    if len(operand_stack) >= 2 and len(type_stack) >= 2:
        right_type = type_stack.pop()
        right_operand = operand_stack.pop()
        left_type = type_stack.pop()
        left_operand = operand_stack.pop()
        operator = p[2]
        
        result_type = check_semantic_cube(operator, left_type, right_type)
        if result_type != 'error':
            temp_name = generate_temp()
            add_quadruple(operator, left_operand, right_operand, temp_name)
            operand_stack.append(temp_name)
            type_stack.append(result_type)

def p_factor_paren(p):
    '''factor : LPAREN expression RPAREN'''
    pass

def p_factor_unary_plus(p):
    '''factor : OP_SUMA var_cte'''
    pass

def p_factor_unary_minus(p):
    '''factor : OP_RESTA var_cte'''
    if len(operand_stack) > 0 and len(type_stack) > 0:
        operand = operand_stack.pop()
        operand_type = type_stack.pop()
        temp_name = generate_temp()
        add_quadruple('UMINUS', operand, None, temp_name)
        operand_stack.append(temp_name)
        type_stack.append(operand_type)

def p_factor_var_cte(p):
    '''factor : var_cte'''
    pass

def p_var_cte_id(p):
    '''var_cte : ID'''
    var_type = lookup_variable(p[1])
    if var_type:
        operand_stack.append(p[1])
        type_stack.append(var_type)

def p_var_cte_int(p):
    '''var_cte : CONST_INT'''
    operand_stack.append(p[1])
    type_stack.append('int')

def p_var_cte_float(p):
    '''var_cte : CONST_FLOAT'''
    operand_stack.append(p[1])
    type_stack.append('float')

def p_var_cte_string(p):
    '''var_cte : CONST_STRING'''
    operand_stack.append(f'"{p[1]}"')
    type_stack.append('string')

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        error_msg = f"ERROR SINTÁCTICO en línea {p.lineno}: Token inesperado '{p.value}' (tipo: {p.type})"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")
    else:
        error_msg = "ERROR SINTÁCTICO: Fin inesperado del archivo"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")

parser = yacc.yacc(write_tables=False, debug=False)
print("✅ Parser con análisis semántico construido correctamente")

###############################################################
#              FUNCIONES DE REPORTE Y SALIDA
###############################################################

def print_symbol_table():
    print("\n" + "="*70)
    print("TABLA DE SÍMBOLOS")
    print("="*70)
    for scope, variables in symbol_table.items():
        print(f"\nScope: {scope}")
        print(f"{'Variable':<15} {'Tipo':<10}")
        print("-"*70)
        for var_name, var_type in variables.items():
            print(f"{var_name:<15} {var_type:<10}")

def print_function_directory():
    print("\n" + "="*70)
    print("DIRECTORIO DE FUNCIONES")
    print("="*70)
    for func_name, func_info in function_directory.items():
        print(f"\nFunción: {func_name}")
        print(f"  Tipo retorno: {func_info['type']}")
        print(f"  Parámetros: {func_info['params']}")
        print(f"  Cuádruplo inicial: {func_info['start_quad']}")

def print_quadruples():
    print("\n" + "="*70)
    print("CÓDIGO INTERMEDIO (CUÁDRUPLOS)")
    print("="*70)
    print(f"{'#':<5} {'Operador':<10} {'Operando1':<15} {'Operando2':<15} {'Resultado':<15}")
    print("-"*70)
    for i, (op, op1, op2, res) in enumerate(quadruples):
        op1_str = str(op1) if op1 is not None else '-'
        op2_str = str(op2) if op2 is not None else '-'
        res_str = str(res) if res is not None else '-'
        print(f"{i:<5} {op:<10} {op1_str:<15} {op2_str:<15} {res_str:<15}")

def save_intermediate_code(filename):
    """Guarda el código intermedio en un archivo"""
    output_file = filename.replace('.txt', '_intermediate.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("CÓDIGO INTERMEDIO - CUÁDRUPLOS\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"{'#':<5} {'Operador':<10} {'Operando1':<15} {'Operando2':<15} {'Resultado':<15}\n")
        f.write("-"*70 + "\n")
        for i, (op, op1, op2, res) in enumerate(quadruples):
            op1_str = str(op1) if op1 is not None else '-'
            op2_str = str(op2) if op2 is not None else '-'
            res_str = str(res) if res is not None else '-'
            f.write(f"{i:<5} {op:<10} {op1_str:<15} {op2_str:<15} {res_str:<15}\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("TABLA DE SÍMBOLOS\n")
        f.write("="*70 + "\n")
        for scope, variables in symbol_table.items():
            f.write(f"\nScope: {scope}\n")
            f.write(f"{'Variable':<15} {'Tipo':<10}\n")
            f.write("-"*70 + "\n")
            for var_name, var_type in variables.items():
                f.write(f"{var_name:<15} {var_type:<10}\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("DIRECTORIO DE FUNCIONES\n")
        f.write("="*70 + "\n")
        for func_name, func_info in function_directory.items():
            f.write(f"\nFunción: {func_name}\n")
            f.write(f"  Tipo retorno: {func_info['type']}\n")
            f.write(f"  Parámetros: {func_info['params']}\n")
            f.write(f"  Cuádruplo inicial: {func_info['start_quad']}\n")
    
    print(f"\n✅ Código intermedio guardado en: {output_file}")

###############################################################
#              FUNCIÓN PRINCIPAL DE ANÁLISIS
###############################################################

def analizar_archivo(filename):
    global lexer_errors, parser_errors
    
    reset_compiler()
    lexer_errors = []
    parser_errors = []

    print("="*70)
    print(f" ANALIZANDO ARCHIVO: {filename}")
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

    print("\n CÓDIGO FUENTE:")
    print("-"*70)
    for i, linea in enumerate(codigo.split('\n'), 1):
        print(f"{i:3d} | {linea}")
    print("-"*70)

    file_lexer = lex.lex()
    file_lexer.lineno = 1

    print("\n🔍 ANÁLISIS LÉXICO, SINTÁCTICO Y SEMÁNTICO:")
    print("-"*70)
    
    resultado = parser.parse(codigo, lexer=file_lexer)

    if len(parser_errors) == 0 and len(lexer_errors) == 0:
        print_function_directory()
        print_symbol_table()
        print_quadruples()
        save_intermediate_code(filename)

    print("\n" + "="*70)
    print("REPORTE FINAL")
    print("="*70)

    total_errores = len(lexer_errors) + len(parser_errors)

    if total_errores == 0:
        print("✅ ¡PROGRAMA VÁLIDO! Compilación exitosa")
        print(f"✅ Total de cuádruplos generados: {len(quadruples)}")
        print(f"✅ Variables declaradas: {sum(len(v) for v in symbol_table.values())}")
        print(f"✅ Funciones declaradas: {len(function_directory)}")
        return True
    else:
        print(f"❌ Se encontraron {total_errores} errores en total:")
        print(f"   - Errores léxicos: {len(lexer_errors)}")
        print(f"   - Errores semánticos: {len(parser_errors)}")
        return False

###############################################################
#                           MAIN
###############################################################

if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPILADOR LITTLE DUCK - ANÁLISIS SEMÁNTICO")
    print("="*70 + "\n")

    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        analizar_archivo(archivo)
    else:
        print("Uso: python main_semantico.py <archivo.txt>")
        print("Ejemplo: python main_semantico.py factorial.txt")
