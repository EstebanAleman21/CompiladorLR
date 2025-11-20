##############################################
#   COMPILADOR SIMPLIFICADO
#   Solo asignaciones y condicionales
#   Con generación de cuádruplos
##############################################

import ply.lex as lex
import ply.yacc as yacc
import sys

# Palabras reservadas
reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'if': 'IF',
    'else': 'ELSE',
    'main': 'MAIN',
    'end': 'END',
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

def t_CONST_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_CONST_FLOAT(t):
    r'\d+\.\d+(?:[eE][\+\-]?\d+)?'
    t.value = float(t.value)
    return t

def t_CONST_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    error_msg = f"ERROR LEXICO en linea {t.lineno}: Caracter ilegal '{t.value[0]}'"
    lexer_errors.append(error_msg)
    print(error_msg)
    t.lexer.skip(1)

#LEXER

lexer = lex.lex()
print("Lexer construido correctamente")


# ESTRUCTURAS DE DATOS DEL COMPILADOR


symbol_table = {}
operand_stack = []
type_stack = []
operator_stack = []
quadruples = []
jump_stack = []
temp_counter = 1
memory_counter = 1000

semantic_cube = {
    '+': {
        'int': {'int': 'int', 'float': 'float', 'string': 'string'},
        'float': {'int': 'float', 'float': 'float', 'string': 'string'},
        'string': {'int': 'string', 'float': 'string', 'string': 'string'}
    },
    '-': {
        'int': {'int': 'int', 'float': 'float'},
        'float': {'int': 'float', 'float': 'float'}
    },
    '*': {
        'int': {'int': 'int', 'float': 'float', 'string': 'string'},
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
        'int': {'int': 'int'},
        'float': {'int': 'float', 'float': 'float'},
        'string': {'string': 'string', 'int': 'string', 'float': 'string'}
    }
}

def reset_compiler_structures():
    global symbol_table, operand_stack, type_stack, operator_stack
    global quadruples, jump_stack, temp_counter, memory_counter
    
    symbol_table = {}
    operand_stack = []
    type_stack = []
    operator_stack = []
    quadruples = []
    jump_stack = []
    temp_counter = 1
    memory_counter = 1000

def get_new_temp():
    global temp_counter
    temp = f"t{temp_counter}"
    temp_counter += 1
    return temp

def get_type_from_value(value):
    if isinstance(value, int):
        return 'int'
    elif isinstance(value, float):
        return 'float'
    else:
        return 'string'

def check_semantic_cube(operator, type1, type2):
    if operator in semantic_cube:
        if type1 in semantic_cube[operator]:
            if type2 in semantic_cube[operator][type1]:
                return semantic_cube[operator][type1][type2]
    return None

def add_quadruple(operator, operand1, operand2, result):
    quadruples.append((operator, operand1, operand2, result))

#OP BINARIAS

def generate_binary_operation_quad(operator):
    try:
        if len(operand_stack) < 2 or len(type_stack) < 2:
            error_msg = f"ERROR INTERNO: Faltan operandos para '{operator}'"
            parser_errors.append(error_msg)
            print(error_msg)
            operand_stack.append('error')
            type_stack.append('error')
            return
        
        right_operand = operand_stack.pop()
        right_type = type_stack.pop()
        left_operand = operand_stack.pop()
        left_type = type_stack.pop()
        
        result_type = check_semantic_cube(operator, left_type, right_type)
        
        if result_type is None:
            error_msg = f"ERROR SEMANTICO: Operacion '{operator}' no valida entre '{left_type}' y '{right_type}'"
            parser_errors.append(error_msg)
            print(error_msg)
            result_type = 'error'
            
            temp = get_new_temp()
            add_quadruple(operator, left_operand, right_operand, temp)
            operand_stack.append(temp)
            type_stack.append(result_type)
        else:
            temp = get_new_temp()
            add_quadruple(operator, left_operand, right_operand, temp)
            operand_stack.append(temp)
            type_stack.append(result_type)
    
    except Exception as e:
        error_msg = f"ERROR INTERNO generando cuádruplo '{operator}': {str(e)}"
        parser_errors.append(error_msg)
        print(error_msg)
        operand_stack.append('error')
        type_stack.append('error')

# PARSER LR CON GRAMATICA

precedence = (
    ('left', 'OP_EQ', 'OP_NEQ', 'OP_LT', 'OP_GT', 'OP_LEQ', 'OP_GEQ'), 
    ('left', 'OP_SUMA', 'OP_RESTA'),
    ('left', 'OP_MULT', 'OP_DIV'),
)

start = 'program'

def p_program(p):
    '''program : PROGRAM ID SEMICOL vars MAIN body END'''
    p[0] = ('program', p[2], p[4], p[6])
    print("Programa parseado correctamente")

def p_vars_first(p):
    '''vars : VAR var_list'''
    p[0] = p[2]

def p_var_list_single(p):
    '''var_list : id_list COLON type SEMICOL'''
    global memory_counter
    var_type = p[3]
    for var_name in p[1]:
        if var_name in symbol_table:
            error_msg = f"ERROR SEMANTICO: Variable '{var_name}' ya declarada"
            parser_errors.append(error_msg)
            print(error_msg)
        else:
            symbol_table[var_name] = {
                'tipo': var_type,
                'direccion': memory_counter
            }
            memory_counter += 1
    p[0] = [('var_decl', p[1], p[3])]

def p_var_list_multiple(p):
    '''var_list : id_list COLON type SEMICOL var_list'''
    global memory_counter
    var_type = p[3]
    for var_name in p[1]:
        if var_name in symbol_table:
            error_msg = f"ERROR SEMANTICO: Variable '{var_name}' ya declarada"
            parser_errors.append(error_msg)
            print(error_msg)
        else:
            symbol_table[var_name] = {
                'tipo': var_type,
                'direccion': memory_counter
            }
            memory_counter += 1
    p[0] = [('var_decl', p[1], p[3])] + p[5]

def p_id_list_single(p):
    '''id_list : ID'''
    p[0] = [p[1]]

def p_id_list_multiple(p):
    '''id_list : ID COMMA id_list'''
    p[0] = [p[1]] + p[3]

def p_type_int(p):
    '''type : INT'''
    p[0] = 'int'

def p_type_float(p):
    '''type : FLOAT'''
    p[0] = 'float'

def p_type_string(p):
    '''type : STRING'''
    p[0] = 'string'

def p_body(p):
    '''body : LBRACE statements RBRACE'''
    p[0] = ('body', p[2])

def p_statements_empty(p):
    '''statements : empty'''
    p[0] = []

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statement_assign(p):
    '''statement : assign'''
    p[0] = p[1]

def p_statement_condition(p):
    '''statement : condition'''
    p[0] = p[1]

def p_assign(p):
    '''assign : ID OP_ASIGNA expression SEMICOL'''
    var_name = p[1]
    
    if var_name not in symbol_table:
        error_msg = f"ERROR SEMANTICO: Variable '{var_name}' no declarada"
        parser_errors.append(error_msg)
        print(error_msg)
        p[0] = ('assign', var_name, p[3])
        return
    
    if len(operand_stack) > 0 and len(type_stack) > 0:
        result_operand = operand_stack.pop()
        result_type = type_stack.pop()
        
        var_type = symbol_table[var_name]['tipo']
        checked_type = check_semantic_cube('=', var_type, result_type)
        
        if checked_type is None:
            error_msg = f"ERROR SEMANTICO: No se puede asignar '{result_type}' a variable '{var_name}' de tipo '{var_type}'"
            parser_errors.append(error_msg)
            print(error_msg)
        else:
            add_quadruple('=', result_operand, None, var_name)
    
    p[0] = ('assign', var_name, p[3])

def p_expression(p):
    '''expression : exp rel_exp_tail'''
    if p[2]:
        if len(operand_stack) >= 2 and len(type_stack) >= 2:
            right_operand = operand_stack.pop()
            right_type = type_stack.pop()
            left_operand = operand_stack.pop()
            left_type = type_stack.pop()
            operator = operator_stack.pop()
            
            result_type = check_semantic_cube(operator, left_type, right_type)
            if result_type is None:
                error_msg = f"ERROR SEMANTICO: Operacion '{operator}' no valida entre '{left_type}' y '{right_type}'"
                parser_errors.append(error_msg)
                print(error_msg)
                result_type = 'error'
            
            temp = get_new_temp()
            add_quadruple(operator, left_operand, right_operand, temp)
            
            operand_stack.append(temp)
            type_stack.append(result_type)
        
        p[0] = ('expr', p[1], p[2])
    else:
        p[0] = p[1]

def p_rel_exp_tail_empty(p):
    '''rel_exp_tail : empty'''
    p[0] = None

def p_rel_exp_tail_rel(p):
    '''rel_exp_tail : rel_op exp'''
    p[0] = (p[1], p[2])

def p_rel_op_gt(p):
    '''rel_op : OP_GT'''
    operator_stack.append('>')
    p[0] = '>'

def p_rel_op_lt(p):
    '''rel_op : OP_LT'''
    operator_stack.append('<')
    p[0] = '<'

def p_rel_op_neq(p):
    '''rel_op : OP_NEQ'''
    operator_stack.append('!=')
    p[0] = '!='

def p_rel_op_eq(p):
    '''rel_op : OP_EQ'''
    operator_stack.append('==')
    p[0] = '=='

def p_rel_op_geq(p):
    '''rel_op : OP_GEQ'''
    operator_stack.append('>=')
    p[0] = '>='

def p_rel_op_leq(p):
    '''rel_op : OP_LEQ'''
    operator_stack.append('<=')
    p[0] = '<='

def p_exp_sum(p):
    '''exp : exp OP_SUMA termino'''
    generate_binary_operation_quad('+')
    p[0] = ('+', p[1], p[3])

def p_exp_sub(p):
    '''exp : exp OP_RESTA termino'''
    generate_binary_operation_quad('-')
    p[0] = ('-', p[1], p[3])

def p_exp_termino(p):
    '''exp : termino'''
    p[0] = p[1]

def p_termino_mul(p):
    '''termino : termino OP_MULT factor'''
    generate_binary_operation_quad('*')
    p[0] = ('*', p[1], p[3])

def p_termino_div(p):
    '''termino : termino OP_DIV factor'''
    generate_binary_operation_quad('/')
    p[0] = ('/', p[1], p[3])

def p_termino_factor(p):
    '''termino : factor'''
    p[0] = p[1]

def p_factor_group(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_factor_id(p):
    '''factor : ID'''
    var_name = p[1]
    
    if var_name not in symbol_table:
        error_msg = f"ERROR SEMANTICO: Variable '{var_name}' no declarada"
        parser_errors.append(error_msg)
        print(error_msg)
        operand_stack.append(var_name)
        type_stack.append('error')
    else:
        operand_stack.append(var_name)
        type_stack.append(symbol_table[var_name]['tipo'])
    
    p[0] = ('id', p[1])

def p_factor_int(p):
    '''factor : CONST_INT'''
    operand_stack.append(p[1])
    type_stack.append('int')
    p[0] = ('int', p[1])

def p_factor_float(p):
    '''factor : CONST_FLOAT'''
    operand_stack.append(p[1])
    type_stack.append('float')
    p[0] = ('float', p[1])

def p_factor_string(p):
    '''factor : CONST_STRING'''
    operand_stack.append(f'"{p[1]}"')
    type_stack.append('string')
    p[0] = ('string', p[1])

def p_condition(p):
    '''condition : IF LPAREN expression RPAREN if_action body else_part SEMICOL'''
    if p[7] is None:
        if len(jump_stack) > 0:
            false_jump = jump_stack.pop()
            quadruples[false_jump] = ('GOTOF', quadruples[false_jump][1], None, len(quadruples) + 1)
    else:
        if len(jump_stack) > 0:
            end_jump = jump_stack.pop()
            quadruples[end_jump] = ('GOTO', None, None, len(quadruples) + 1)
    
    p[0] = ('if', p[3], p[6], p[7])

def p_if_action(p):
    '''if_action : empty'''
    if len(operand_stack) > 0 and len(type_stack) > 0:
        condition = operand_stack.pop()
        cond_type = type_stack.pop()
        
        if cond_type != 'bool' and cond_type != 'error':
            error_msg = f"ERROR SEMANTICO: La condicion debe ser bool, no '{cond_type}'"
            parser_errors.append(error_msg)
            print(error_msg)
        
        quad_index = len(quadruples)
        add_quadruple('GOTOF', condition, None, -1)
        jump_stack.append(quad_index)

def p_else_part_empty(p):
    '''else_part : empty'''
    p[0] = None

def p_else_part_else(p):
    '''else_part : ELSE else_action body'''
    p[0] = p[3]

def p_else_action(p):
    '''else_action : empty'''
    if len(jump_stack) > 0:
        false_jump = jump_stack.pop()
        
        quad_index = len(quadruples)
        add_quadruple('GOTO', None, None, -1)
        
        quadruples[false_jump] = ('GOTOF', quadruples[false_jump][1], None, len(quadruples) + 1)
        
        jump_stack.append(quad_index)

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        error_msg = f"ERROR SINTACTICO en linea {p.lineno}: Token inesperado '{p.value}' (tipo: {p.type})"
    else:
        error_msg = "ERROR SINTACTICO: Fin inesperado del archivo"
    
    parser_errors.append(error_msg)
    print(error_msg)

parser = yacc.yacc(write_tables=False, debug=False)
print("Parser LR construido correctamente")

# FUNCIONES PARA IMPRIMIR RESULTADOS

def print_symbol_table():
    print("\n" + "="*70)
    print("TABLA DE SIMBOLOS")
    print("="*70)
    print(f"{'Variable':<15} {'Tipo':<10} {'Direccion':<10}")
    print("-"*70)
    for var_name, info in symbol_table.items():
        print(f"{var_name:<15} {info['tipo']:<10} {info['direccion']:<10}")
    print("-"*70)

def print_quadruples():
    start_index = 0
    for i, quad in enumerate(quadruples):
        operator, op1, op2, result = quad
        if operator == '=' and isinstance(op1, (int, float)):
            continue
        elif operator == '=' and isinstance(op1, str) and op1.startswith('"'):
            continue
        else:
            start_index = i
            break
    
    print("\n" + "="*70)
    print("CUADRUPLOS GENERADOS (CON VARIABLES)")
    print("="*70)
    print(f"{'#':<5} {'Operador':<12} {'Operando1':<12} {'Operando2':<12} {'Resultado':<12} {'Tipo':<10}")
    print("-"*70)
    
    for i, quad in enumerate(quadruples, start=1):
        operator, op1, op2, result = quad
        
        result_type = ''
        if operator in ['=', '+', '-', '*', '/']:
            if isinstance(result, str) and result.startswith('t'):
                result_type = get_result_type(i-1)
            elif result in symbol_table:
                result_type = symbol_table[result]['tipo']
        elif operator in ['>', '<', '>=', '<=', '==', '!=']:
            result_type = 'bool'
        elif operator in ['GOTOF', 'GOTO']:
            result_type = '-'
        
        op1_str = str(op1) if op1 is not None else '-'
        op2_str = str(op2) if op2 is not None else '-'
        result_str = str(result) if result is not None else '-'
        
        print(f"{i:<5} {operator:<12} {op1_str:<12} {op2_str:<12} {result_str:<12} {result_type:<10}")
    
    print("-"*70)
    
    print("\n" + "="*70)
    print("CUADRUPLOS GENERADOS (SIN VARIABLES)")
    print("="*70)
    print(f"{'#':<5} {'Operador':<12} {'Operando1':<12} {'Operando2':<12} {'Resultado':<12} {'Tipo':<10}")
    print("-"*70)
    
    display_num = 1
    for i in range(start_index, len(quadruples)):
        quad = quadruples[i]
        operator, op1, op2, result = quad
        
        result_type = ''
        if operator in ['=', '+', '-', '*', '/']:
            if isinstance(result, str) and result.startswith('t'):
                result_type = get_result_type(i)
            elif result in symbol_table:
                result_type = symbol_table[result]['tipo']
        elif operator in ['>', '<', '>=', '<=', '==', '!=']:
            result_type = 'bool'
        elif operator in ['GOTOF', 'GOTO']:
            result_type = '-'
        
        op1_str = str(op1) if op1 is not None else '-'
        op2_str = str(op2) if op2 is not None else '-'
        
        if operator in ['GOTOF', 'GOTO'] and result is not None:
            adjusted_result = result - start_index
            result_str = str(adjusted_result)
        else:
            result_str = str(result) if result is not None else '-'
        
        print(f"{display_num:<5} {operator:<12} {op1_str:<12} {op2_str:<12} {result_str:<12} {result_type:<10}")
        display_num += 1
    
    print("-"*70)

def get_result_type(quad_index):
    if quad_index >= len(quadruples):
        return ''
    
    quad = quadruples[quad_index]
    operator, op1, op2, result = quad
    
    type1 = get_operand_type(op1)
    type2 = get_operand_type(op2)
    
    if operator in semantic_cube and type1 and type2:
        if type1 in semantic_cube[operator] and type2 in semantic_cube[operator][type1]:
            return semantic_cube[operator][type1][type2]
    
    return ''

def get_operand_type(operand):
    if operand is None:
        return None
    
    if operand in symbol_table:
        return symbol_table[operand]['tipo']
    
    if isinstance(operand, int):
        return 'int'
    if isinstance(operand, float):
        return 'float'
    
    if isinstance(operand, str) and operand.startswith('"') and operand.endswith('"'):
        return 'string'
    
    if isinstance(operand, str) and operand.startswith('t'):
        for quad in quadruples:
            if quad[3] == operand:
                return get_result_type(quadruples.index(quad))
    
    return None

# INTERPRETE DE CUADRUPLOS


def execute_quadruples():
    memory = {}
    
    for var_name in symbol_table.keys():
        memory[var_name] = 0
    
    ip = 0
    
    while ip < len(quadruples):
        operator, op1, op2, result = quadruples[ip]
        
        def get_value(operand):
            if operand is None:
                return None
            if isinstance(operand, (int, float)):
                return operand
            if isinstance(operand, str) and operand.startswith('"') and operand.endswith('"'):
                return operand[1:-1]
            if operand in memory:
                return memory[operand]
            if isinstance(operand, str):
                return operand
            return 0
        
        try:
            if operator == '=':
                memory[result] = get_value(op1)
            
            elif operator == '+':
                val1 = get_value(op1)
                val2 = get_value(op2)
                
                if isinstance(val1, str) or isinstance(val2, str):
                    memory[result] = str(val1) + str(val2)
                else:
                    memory[result] = val1 + val2
            
            elif operator == '-':
                memory[result] = get_value(op1) - get_value(op2)
            
            elif operator == '*':
                val1 = get_value(op1)
                val2 = get_value(op2)
                
                if isinstance(val1, str) and isinstance(val2, (int, float)):
                    memory[result] = val1 * int(val2)
                elif isinstance(val2, str) and isinstance(val1, (int, float)):
                    memory[result] = val2 * int(val1)
                else:
                    memory[result] = val1 * val2
            
            elif operator == '/':
                val2 = get_value(op2)
                if val2 == 0:
                    print(f"Advertencia: Division por cero en cuadruple {ip}")
                    memory[result] = 0
                else:
                    memory[result] = get_value(op1) / val2
            
            elif operator == '>':
                memory[result] = get_value(op1) > get_value(op2)
            
            elif operator == '<':
                memory[result] = get_value(op1) < get_value(op2)
            
            elif operator == '>=':
                memory[result] = get_value(op1) >= get_value(op2)
            
            elif operator == '<=':
                memory[result] = get_value(op1) <= get_value(op2)
            
            elif operator == '==':
                memory[result] = get_value(op1) == get_value(op2)
            
            elif operator == '!=':
                memory[result] = get_value(op1) != get_value(op2)
            
            elif operator == 'GOTOF':
                condition = get_value(op1)
                if not condition:
                    ip = result - 1
                    continue
            
            elif operator == 'GOTO':
                ip = result - 1
                continue
        
        except Exception as e:
            print(f"Error ejecutando cuadruple {ip}: {e}")
            memory[result] = None
        
        ip += 1
    
    return memory

def print_execution_results():
    print("\n" + "="*70)
    print("EJECUCION DE CUADRUPLOS")
    print("="*70)
    
    memory = execute_quadruples()
    
    print(f"{'Variable':<15} {'Valor Final':<15} {'Tipo':<10}")
    print("-"*70)
    
    for var_name in sorted(symbol_table.keys()):
        value = memory.get(var_name, 0)
        var_type = symbol_table[var_name]['tipo']
        
        if var_type == 'int':
            formatted_value = f"{int(value)}"
        elif var_type == 'float':
            formatted_value = f"{float(value):.2f}"
        elif var_type == 'string':
            formatted_value = str(value)
        else:
            formatted_value = str(value)
        
        print(f"{var_name:<15} {formatted_value:<15} {var_type:<10}")
    
    print("-"*70)

# FUNCION PRINCIPAL DE ANALISIS


def analizar_archivo(filename):
    global lexer_errors, parser_errors
    
    reset_compiler_structures()
    lexer_errors = []
    parser_errors = []

    print("="*70)
    print(f"ANALIZANDO ARCHIVO: {filename}")
    print("="*70)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"ERROR: No se encontro el archivo '{filename}'")
        return False
    except Exception as e:
        print(f"ERROR al leer archivo: {e}")
        return False

    print("\nCODIGO FUENTE:")
    print("-"*70)
    for i, linea in enumerate(codigo.split('\n'), 1):
        print(f"{i:3d} | {linea}")
    print("-"*70)

    file_lexer = lex.lex()
    file_lexer.lineno = 1

    print("\nANALISIS SINTACTICO Y SEMANTICO:")
    print("-"*70)
    
    resultado = parser.parse(codigo, lexer=file_lexer)

    print_symbol_table()
    print_quadruples()
    
    if len(parser_errors) == 0:
        print_execution_results()

    print("\n" + "="*70)
    print("REPORTE FINAL")
    print("="*70)

    total_errores = len(lexer_errors) + len(parser_errors)

    if total_errores == 0:
        print("PROGRAMA VALIDO")
        print(f"Total de cuadruplos generados: {len(quadruples)}")
        print(f"Variables declaradas: {len(symbol_table)}")
        return True
    else:
        print(f"Se encontraron {total_errores} errores:")
        print(f"   - Errores lexicos: {len(lexer_errors)}")
        print(f"   - Errores semanticos: {len(parser_errors)}")
        return False


# MAIN


if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPILADOR SIMPLIFICADO - ASIGNACIONES Y CONDICIONALES")
    print("="*70 + "\n")

    if len(sys.argv) < 2:
        print("ERROR: Debes proporcionar el nombre del archivo a analizar")
        print("\nUso: python3 compiler_assignments_conditionals.py <nombre_archivo>")
        sys.exit(1)
    
    nombre_archivo = sys.argv[1]
    analizar_archivo(nombre_archivo)
