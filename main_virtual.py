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

# Pila de argumentos: lista de tuplas (dirección, tipo)
stack_args = []
jump_stack = []

# Contexto de llamada a función actual (para tracking de argumentos)
current_call = None  # (func_name, param_count, arg_addresses)

# Cuádruplos generados
quadruples = []

# Contadores
temp_counter = 1

# Scope actual
current_scope = 'global'
current_function = None

###############################################################
#              SISTEMA DE MEMORIA VIRTUAL
###############################################################

class MemorySegments:
    """Definición de rangos de direcciones de memoria virtual"""
    # Variables globales (1000 - 6999)
    GLOBAL_INT_BASE = 1000
    GLOBAL_INT_LIMIT = 1999
    GLOBAL_FLOAT_BASE = 2000
    GLOBAL_FLOAT_LIMIT = 2999
    GLOBAL_STRING_BASE = 3000
    GLOBAL_STRING_LIMIT = 3999
    GLOBAL_VOID_BASE = 4000
    GLOBAL_VOID_LIMIT = 4999

    # Variables locales (7000 - 11999)
    LOCAL_INT_BASE = 7000
    LOCAL_INT_LIMIT = 7999
    LOCAL_FLOAT_BASE = 8000
    LOCAL_FLOAT_LIMIT = 8999
    LOCAL_STRING_BASE = 9000
    LOCAL_STRING_LIMIT = 9999

    # Temporales (12000 - 16999)
    TEMP_INT_BASE = 12000
    TEMP_INT_LIMIT = 12999
    TEMP_FLOAT_BASE = 13000
    TEMP_FLOAT_LIMIT = 13999
    TEMP_BOOL_BASE = 14000
    TEMP_BOOL_LIMIT = 14999

    # Constantes (17000 - 19999)
    CONST_INT_BASE = 17000
    CONST_INT_LIMIT = 17999
    CONST_FLOAT_BASE = 18000
    CONST_FLOAT_LIMIT = 18999
    CONST_STRING_BASE = 19000
    CONST_STRING_LIMIT = 19999


class MemoryManager:
    """Administrador de memoria virtual para asignación de direcciones"""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia todos los contadores de memoria"""
        # Contadores globales
        self.global_int = MemorySegments.GLOBAL_INT_BASE
        self.global_float = MemorySegments.GLOBAL_FLOAT_BASE
        self.global_string = MemorySegments.GLOBAL_STRING_BASE

        # Contadores locales (se reinician por función)
        self.local_int = MemorySegments.LOCAL_INT_BASE
        self.local_float = MemorySegments.LOCAL_FLOAT_BASE
        self.local_string = MemorySegments.LOCAL_STRING_BASE

        # Contadores temporales
        self.temp_int = MemorySegments.TEMP_INT_BASE
        self.temp_float = MemorySegments.TEMP_FLOAT_BASE
        self.temp_bool = MemorySegments.TEMP_BOOL_BASE

        # Contadores de constantes
        self.const_int = MemorySegments.CONST_INT_BASE
        self.const_float = MemorySegments.CONST_FLOAT_BASE
        self.const_string = MemorySegments.CONST_STRING_BASE

    def get_global_address(self, var_type):
        """Asigna y retorna dirección para variable global"""
        if var_type == 'int':
            if self.global_int > MemorySegments.GLOBAL_INT_LIMIT:
                raise MemoryError("Desbordamiento de memoria global int")
            addr = self.global_int
            self.global_int += 1
            return addr
        elif var_type == 'float':
            if self.global_float > MemorySegments.GLOBAL_FLOAT_LIMIT:
                raise MemoryError("Desbordamiento de memoria global float")
            addr = self.global_float
            self.global_float += 1
            return addr
        elif var_type == 'string':
            if self.global_string > MemorySegments.GLOBAL_STRING_LIMIT:
                raise MemoryError("Desbordamiento de memoria global string")
            addr = self.global_string
            self.global_string += 1
            return addr

    def get_local_address(self, var_type):
        """Asigna y retorna dirección para variable local"""
        if var_type == 'int':
            if self.local_int > MemorySegments.LOCAL_INT_LIMIT:
                raise MemoryError("Desbordamiento de memoria local int")
            addr = self.local_int
            self.local_int += 1
            return addr
        elif var_type == 'float':
            if self.local_float > MemorySegments.LOCAL_FLOAT_LIMIT:
                raise MemoryError("Desbordamiento de memoria local float")
            addr = self.local_float
            self.local_float += 1
            return addr
        elif var_type == 'string':
            if self.local_string > MemorySegments.LOCAL_STRING_LIMIT:
                raise MemoryError("Desbordamiento de memoria local string")
            addr = self.local_string
            self.local_string += 1
            return addr

    def get_temp_address(self, temp_type):
        """Asigna y retorna dirección para temporal"""
        if temp_type == 'int':
            if self.temp_int > MemorySegments.TEMP_INT_LIMIT:
                raise MemoryError("Desbordamiento de memoria temporal int")
            addr = self.temp_int
            self.temp_int += 1
            return addr
        elif temp_type == 'float':
            if self.temp_float > MemorySegments.TEMP_FLOAT_LIMIT:
                raise MemoryError("Desbordamiento de memoria temporal float")
            addr = self.temp_float
            self.temp_float += 1
            return addr
        elif temp_type == 'bool':
            if self.temp_bool > MemorySegments.TEMP_BOOL_LIMIT:
                raise MemoryError("Desbordamiento de memoria temporal bool")
            addr = self.temp_bool
            self.temp_bool += 1
            return addr
        elif temp_type == 'string':
            # Strings temporales usan el rango de int temporales
            if self.temp_int > MemorySegments.TEMP_INT_LIMIT:
                raise MemoryError("Desbordamiento de memoria temporal")
            addr = self.temp_int
            self.temp_int += 1
            return addr

    def get_constant_address(self, const_type):
        """Asigna y retorna dirección para constante"""
        if const_type == 'int':
            if self.const_int > MemorySegments.CONST_INT_LIMIT:
                raise MemoryError("Desbordamiento de memoria constante int")
            addr = self.const_int
            self.const_int += 1
            return addr
        elif const_type == 'float':
            if self.const_float > MemorySegments.CONST_FLOAT_LIMIT:
                raise MemoryError("Desbordamiento de memoria constante float")
            addr = self.const_float
            self.const_float += 1
            return addr
        elif const_type == 'string':
            if self.const_string > MemorySegments.CONST_STRING_LIMIT:
                raise MemoryError("Desbordamiento de memoria constante string")
            addr = self.const_string
            self.const_string += 1
            return addr

    def reset_local_counters(self):
        """Reinicia contadores locales al entrar a nueva función"""
        self.local_int = MemorySegments.LOCAL_INT_BASE
        self.local_float = MemorySegments.LOCAL_FLOAT_BASE
        self.local_string = MemorySegments.LOCAL_STRING_BASE

    def reset_temp_counters(self):
        """Reinicia contadores temporales"""
        self.temp_int = MemorySegments.TEMP_INT_BASE
        self.temp_float = MemorySegments.TEMP_FLOAT_BASE
        self.temp_bool = MemorySegments.TEMP_BOOL_BASE

    def get_memory_usage(self):
        """Retorna contadores de uso de memoria por tipo"""
        return {
            'global': {
                'int': self.global_int - MemorySegments.GLOBAL_INT_BASE,
                'float': self.global_float - MemorySegments.GLOBAL_FLOAT_BASE,
                'string': self.global_string - MemorySegments.GLOBAL_STRING_BASE
            },
            'local': {
                'int': self.local_int - MemorySegments.LOCAL_INT_BASE,
                'float': self.local_float - MemorySegments.LOCAL_FLOAT_BASE,
                'string': self.local_string - MemorySegments.LOCAL_STRING_BASE
            },
            'temp': {
                'int': self.temp_int - MemorySegments.TEMP_INT_BASE,
                'float': self.temp_float - MemorySegments.TEMP_FLOAT_BASE,
                'bool': self.temp_bool - MemorySegments.TEMP_BOOL_BASE
            },
            'const': {
                'int': self.const_int - MemorySegments.CONST_INT_BASE,
                'float': self.const_float - MemorySegments.CONST_FLOAT_BASE,
                'string': self.const_string - MemorySegments.CONST_STRING_BASE
            }
        }


# Instancia global del administrador de memoria
memory_manager = MemoryManager()

# Tabla de constantes: {tipo: {valor: dirección}}
constants_table = {
    'int': {},
    'float': {},
    'string': {}
}

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
        'string': {'string': 'string'}
    }
}

###############################################################
#              FUNCIONES AUXILIARES SEMÁNTICAS
###############################################################

def reset_compiler():
    global function_directory, symbol_table, stack_args
    global jump_stack, quadruples, temp_counter
    global current_scope, current_function, constants_table, memory_manager
    global current_call

    function_directory = {}
    symbol_table = {'global': {}}
    stack_args = []
    jump_stack = []
    quadruples = []
    temp_counter = 1
    current_scope = 'global'
    current_function = None
    current_call = None

    # Reiniciar estructuras de memoria virtual
    constants_table = {'int': {}, 'float': {}, 'string': {}}
    memory_manager.reset()

def add_variable(var_name, var_type, scope=None):
    """Añade una variable a la tabla de símbolos con dirección de memoria virtual"""
    if scope is None:
        scope = current_scope

    if scope not in symbol_table:
        symbol_table[scope] = {}

    if var_name in symbol_table[scope]:
        error_msg = f"ERROR SEMÁNTICO: Variable '{var_name}' ya declarada en scope '{scope}'"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return None

    # Asignar dirección de memoria virtual según scope
    if scope == 'global':
        address = memory_manager.get_global_address(var_type)
    else:
        address = memory_manager.get_local_address(var_type)

    symbol_table[scope][var_name] = {
        'type': var_type,
        'address': address
    }
    return address

def lookup_variable(var_name):
    """Busca una variable y retorna (tipo, dirección) o (None, None) si no existe"""
    if current_scope in symbol_table and var_name in symbol_table[current_scope]:
        var_info = symbol_table[current_scope][var_name]
        return var_info['type'], var_info['address']
    elif 'global' in symbol_table and var_name in symbol_table['global']:
        var_info = symbol_table['global'][var_name]
        return var_info['type'], var_info['address']
    else:
        error_msg = f"ERROR SEMÁNTICO: Variable '{var_name}' no declarada"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return None, None


def register_constant(value, const_type):
    """Registra una constante y retorna su dirección (reutiliza si ya existe)"""
    if value in constants_table[const_type]:
        return constants_table[const_type][value]
    else:
        address = memory_manager.get_constant_address(const_type)
        constants_table[const_type][value] = address
        return address

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

def generate_temp(temp_type='int'):
    """Genera un temporal y retorna su dirección de memoria virtual"""
    return memory_manager.get_temp_address(temp_type)

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
    '''program : PROGRAM ID SEMICOL program_start program_vars program_funcs MAIN main_start program_body END'''
    print("✅ Programa compilado exitosamente")
    add_quadruple('END', None, None, None)

def p_program_start(p):
    '''program_start : '''
    # Generar GOTOMAIN al inicio para saltar a main (se llenará después)
    quad_index = add_quadruple('GOTOMAIN', None, None, None)
    jump_stack.append(quad_index)

def p_program_vars(p):
    '''program_vars : vars
                    | empty'''
    pass

def p_program_funcs(p):
    '''program_funcs : funcs
                     | empty'''
    pass

def p_main_start(p):
    '''main_start : '''
    # Llenar el GOTO inicial para saltar aquí (inicio de main)
    if len(jump_stack) > 0:
        goto_main = jump_stack.pop()
        fill_quadruple(goto_main, len(quadruples))

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
    # Reiniciar contadores de memoria local para nueva función
    memory_manager.reset_local_counters()

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
    param_address = add_variable(p[1], param_type)
    p[0] = [(p[1], param_type, param_address)]

def p_param_list_multiple(p):
    '''param_list : ID COLON type COMMA param_list'''
    param_type = p[3]
    param_address = add_variable(p[1], param_type)
    p[0] = [(p[1], param_type, param_address)] + p[5]

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

def p_statements_empty(p):
    '''statements : empty'''
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
    var_type, var_address = lookup_variable(p[1])
    if var_type and var_address is not None and len(stack_args) > 0:
        expr_address, expr_type = stack_args.pop()
        result_type = check_semantic_cube('=', var_type, expr_type)
        if result_type != 'error':
            add_quadruple('=', expr_address, None, var_address)

# CONDITION
def p_condition(p):
    '''condition : IF LPAREN expression RPAREN condition_check LBRACE statements RBRACE SEMICOL condition_end
                 | IF LPAREN expression RPAREN condition_check LBRACE statements RBRACE ELSE condition_else LBRACE statements RBRACE SEMICOL condition_end'''
    pass

def p_condition_check(p):
    '''condition_check : '''
    if len(stack_args) > 0:
        result, exp_type = stack_args.pop()
        if exp_type != 'bool':
            error_msg = f"ERROR SEMÁNTICO: La condición debe ser una expresión booleana, se recibió '{exp_type}'"
            parser_errors.append(error_msg)
            print(f"❌ {error_msg}")
            return
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
    if len(stack_args) > 0:
        result, exp_type = stack_args.pop()
        if exp_type != 'bool':
            error_msg = f"ERROR SEMÁNTICO: La condición del ciclo debe ser booleana, se recibió '{exp_type}'"
            parser_errors.append(error_msg)
            print(f"❌ {error_msg}")
            return
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
    if len(stack_args) > 0:
        result, exp_type = stack_args.pop()
        if exp_type != 'bool':
            error_msg = f"ERROR SEMÁNTICO: La condición del ciclo debe ser booleana, se recibió '{exp_type}'"
            parser_errors.append(error_msg)
            print(f"❌ {error_msg}")
            return
        return_addr = jump_stack.pop()
        add_quadruple('GOTOT', result, None, return_addr)

# FUNCTION CALL
def p_f_call(p):
    '''f_call : ID LPAREN f_call_start expression_list RPAREN SEMICOL f_call_end
              | ID LPAREN f_call_start RPAREN SEMICOL f_call_end'''
    pass

def p_f_call_start(p):
    '''f_call_start : '''
    global current_call
    func_name = p[-2]
    if func_name not in function_directory:
        error_msg = f"ERROR SEMÁNTICO: Función '{func_name}' no declarada"
        parser_errors.append(error_msg)
        print(f"❌ {error_msg}")
    else:
        add_quadruple('SUB', func_name, None, None)
        current_call = (func_name, 0, [])

def p_f_call_end(p):
    '''f_call_end : '''
    global current_call
    if current_call:
        func_name, param_count, arg_addresses = current_call
        if func_name in function_directory:
            expected_params = len(function_directory[func_name]['params'])
            if param_count != expected_params:
                error_msg = f"ERROR SEMÁNTICO: Función '{func_name}' espera {expected_params} parámetros, se pasaron {param_count}"
                parser_errors.append(error_msg)
                print(f"❌ {error_msg}")
            else:
                params = function_directory[func_name]['params']
                for i, arg_addr in enumerate(arg_addresses):
                    param_addr = params[i][2]
                    add_quadruple('PARAM', arg_addr, None, param_addr)
                add_quadruple('GOSUB', func_name, None, function_directory[func_name]['start_quad'])
        current_call = None

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
    global current_call
    if len(stack_args) > 0:
        operand_address, operand_type = stack_args.pop()
        if current_call:
            # Estamos en llamada a función - guardar argumento
            func_name, count, arg_addresses = current_call
            if func_name in function_directory:
                params = function_directory[func_name]['params']
                if count < len(params):
                    expected_type = params[count][1]
                    if operand_type and expected_type != operand_type and not (expected_type == 'float' and operand_type == 'int'):
                        error_msg = f"ERROR SEMÁNTICO: Parámetro {count+1} de '{func_name}' debe ser '{expected_type}', se pasó '{operand_type}'"
                        parser_errors.append(error_msg)
                        print(f"❌ {error_msg}")
            arg_addresses.append(operand_address)
            current_call = (func_name, count + 1, arg_addresses)
        else:
            # Estamos en print - generar cuádruplo PRINT
            add_quadruple('PRINT', None, None, operand_address)

# EXPRESSION
def p_expression(p):
    '''expression : exp
                  | exp relop exp'''
    if len(p) == 4:
        if len(stack_args) >= 2:
            right_address, right_type = stack_args.pop()
            left_address, left_type = stack_args.pop()
            operator = p[2]
            result_type = check_semantic_cube(operator, left_type, right_type)
            if result_type != 'error':
                temp_address = generate_temp(result_type)
                add_quadruple(operator, left_address, right_address, temp_address)
                stack_args.append((temp_address, result_type))

def p_relop(p):
    '''relop : OP_GT
             | OP_LT
             | OP_NEQ
             | OP_EQ
             | OP_GEQ
             | OP_LEQ'''
    p[0] = p[1]

def p_exp_single(p):
    '''exp : termino'''
    pass

def p_exp_add(p):
    '''exp : exp OP_SUMA termino
           | exp OP_RESTA termino'''
    if len(stack_args) >= 2:
        right_address, right_type = stack_args.pop()
        left_address, left_type = stack_args.pop()
        operator = p[2]
        result_type = check_semantic_cube(operator, left_type, right_type)
        if result_type != 'error':
            temp_address = generate_temp(result_type)
            add_quadruple(operator, left_address, right_address, temp_address)
            stack_args.append((temp_address, result_type))

def p_termino_single(p):
    '''termino : factor'''
    pass

def p_termino_mult(p):
    '''termino : termino OP_MULT factor
               | termino OP_DIV factor'''
    if len(stack_args) >= 2:
        right_address, right_type = stack_args.pop()
        left_address, left_type = stack_args.pop()
        operator = p[2]
        result_type = check_semantic_cube(operator, left_type, right_type)
        if result_type != 'error':
            temp_address = generate_temp(result_type)
            add_quadruple(operator, left_address, right_address, temp_address)
            stack_args.append((temp_address, result_type))

def p_factor_paren(p):
    '''factor : LPAREN expression RPAREN'''
    pass

def p_factor_unary_plus(p):
    '''factor : OP_SUMA var_cte'''
    pass

def p_factor_unary_minus(p):
    '''factor : OP_RESTA var_cte'''
    if len(stack_args) > 0:
        operand_address, operand_type = stack_args.pop()
        temp_address = generate_temp(operand_type)
        add_quadruple('UMINUS', operand_address, None, temp_address)
        stack_args.append((temp_address, operand_type))

def p_factor_var_cte(p):
    '''factor : var_cte'''
    pass

def p_var_cte_id(p):
    '''var_cte : ID'''
    var_type, var_address = lookup_variable(p[1])
    if var_type and var_address is not None:
        stack_args.append((var_address, var_type))

def p_var_cte_int(p):
    '''var_cte : CONST_INT'''
    address = register_constant(p[1], 'int')
    stack_args.append((address, 'int'))

def p_var_cte_float(p):
    '''var_cte : CONST_FLOAT'''
    address = register_constant(p[1], 'float')
    stack_args.append((address, 'float'))

def p_var_cte_string(p):
    '''var_cte : CONST_STRING'''
    address = register_constant(f'"{p[1]}"', 'string')
    stack_args.append((address, 'string'))

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
#                    MÁQUINA VIRTUAL
###############################################################

class VirtualMachine:
    """Máquina virtual para ejecutar cuádruplos de Little Duck"""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia el estado de la VM"""
        self.global_memory = {}
        self.local_memory_stack = [{}]  # Pila de marcos locales
        self.temp_memory = {}
        self.constant_memory = {}
        self.instruction_pointer = 0
        self.call_stack = []
        self.running = True
        self.output = []

    def load_program(self, quads, const_table, func_dir):
        """Carga el programa compilado en la VM"""
        self.quadruples = quads
        self.function_directory = func_dir
        self._load_constants(const_table)

    def _load_constants(self, const_table):
        """Carga las constantes en memoria"""
        for const_type, values in const_table.items():
            for value, address in values.items():
                self.constant_memory[address] = value

    def _get_memory_segment(self, address):
        """Determina a qué segmento de memoria pertenece una dirección"""
        if MemorySegments.GLOBAL_INT_BASE <= address <= MemorySegments.GLOBAL_VOID_LIMIT:
            return 'global'
        elif MemorySegments.LOCAL_INT_BASE <= address <= MemorySegments.LOCAL_STRING_LIMIT:
            return 'local'
        elif MemorySegments.TEMP_INT_BASE <= address <= MemorySegments.TEMP_BOOL_LIMIT:
            return 'temp'
        elif MemorySegments.CONST_INT_BASE <= address <= MemorySegments.CONST_STRING_LIMIT:
            return 'constant'
        else:
            raise RuntimeError(f"Dirección de memoria inválida: {address}")

    def _get_value(self, address):
        """Obtiene el valor de una dirección de memoria"""
        if address is None:
            return None

        # Si es un número menor a 1000, es un valor literal (para saltos)
        if isinstance(address, int) and address < 1000:
            return address

        # Si es un string (nombre de función), retornarlo directamente
        if isinstance(address, str):
            return address

        segment = self._get_memory_segment(address)

        if segment == 'global':
            if address not in self.global_memory:
                return self._get_default_value(address, 'global')
            return self.global_memory[address]

        elif segment == 'local':
            if not self.local_memory_stack:
                raise RuntimeError("No hay marco de memoria local activo")
            current_frame = self.local_memory_stack[-1]
            if address not in current_frame:
                return self._get_default_value(address, 'local')
            return current_frame[address]

        elif segment == 'temp':
            if address not in self.temp_memory:
                return self._get_default_value(address, 'temp')
            return self.temp_memory[address]

        elif segment == 'constant':
            if address not in self.constant_memory:
                raise RuntimeError(f"Constante no encontrada en dirección {address}")
            return self.constant_memory[address]

    def _get_default_value(self, address, segment_type):
        """Retorna valor por defecto según el rango de dirección"""
        if segment_type == 'global':
            if address < MemorySegments.GLOBAL_FLOAT_BASE:
                return 0
            elif address < MemorySegments.GLOBAL_STRING_BASE:
                return 0.0
            elif address < MemorySegments.GLOBAL_VOID_BASE:
                return ""
            else:
                return None  # void
        elif segment_type == 'local':
            if address < MemorySegments.LOCAL_FLOAT_BASE:
                return 0
            elif address < MemorySegments.LOCAL_STRING_BASE:
                return 0.0
            else:
                return ""
        elif segment_type == 'temp':
            if address < MemorySegments.TEMP_FLOAT_BASE:
                return 0
            elif address < MemorySegments.TEMP_BOOL_BASE:
                return 0.0
            else:
                return False

    def _set_value(self, address, value):
        """Almacena un valor en una dirección de memoria"""
        segment = self._get_memory_segment(address)

        if segment == 'global':
            self.global_memory[address] = value
        elif segment == 'local':
            if not self.local_memory_stack:
                self.local_memory_stack.append({})
            self.local_memory_stack[-1][address] = value
        elif segment == 'temp':
            self.temp_memory[address] = value
        elif segment == 'constant':
            raise RuntimeError("No se puede escribir en memoria de constantes")

    def run(self):
        """Ejecuta el programa cargado"""
        print("\n" + "="*70)
        print("EJECUCIÓN DEL PROGRAMA")
        print("="*70 + "\n")

        while self.running and self.instruction_pointer < len(self.quadruples):
            try:
                self._execute_instruction()
            except RuntimeError as e:
                print(f"\n❌ ERROR EN TIEMPO DE EJECUCIÓN en cuádruplo {self.instruction_pointer}:")
                print(f"   {e}")
                print(f"   Instrucción: {self.quadruples[self.instruction_pointer]}")
                self.running = False
                return False

        print("\n" + "="*70)
        print("FIN DE LA EJECUCIÓN")
        print("="*70)
        return True

    def _execute_instruction(self):
        """Ejecuta una instrucción (cuádruplo)"""
        quad = self.quadruples[self.instruction_pointer]
        operator, op1, op2, result = quad

        # ================== OPERACIONES ARITMÉTICAS ==================
        if operator == '+':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            # Manejo de concatenación de strings
            if isinstance(val1, str) or isinstance(val2, str):
                v1 = val1[1:-1] if isinstance(val1, str) and val1.startswith('"') else str(val1)
                v2 = val2[1:-1] if isinstance(val2, str) and val2.startswith('"') else str(val2)
                self._set_value(result, f'"{v1}{v2}"')
            else:
                self._set_value(result, val1 + val2)

        elif operator == '-':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            self._set_value(result, val1 - val2)

        elif operator == '*':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            # Manejo de repetición de strings
            if isinstance(val1, str) and isinstance(val2, int):
                inner = val1[1:-1] if val1.startswith('"') else val1
                self._set_value(result, f'"{inner * val2}"')
            else:
                self._set_value(result, val1 * val2)

        elif operator == '/':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            if val2 == 0:
                raise RuntimeError("División entre cero")
            self._set_value(result, val1 / val2)

        elif operator == 'UMINUS':
            val = self._get_value(op1)
            self._set_value(result, -val)

        # ================== ASIGNACIÓN ==================
        elif operator == '=':
            val = self._get_value(op1)
            self._set_value(result, val)

        # ================== OPERACIONES RELACIONALES ==================
        elif operator == '>':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            self._set_value(result, val1 > val2)

        elif operator == '<':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            self._set_value(result, val1 < val2)

        elif operator == '>=':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            self._set_value(result, val1 >= val2)

        elif operator == '<=':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            self._set_value(result, val1 <= val2)

        elif operator == '==':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            self._set_value(result, val1 == val2)

        elif operator == '!=':
            val1 = self._get_value(op1)
            val2 = self._get_value(op2)
            self._set_value(result, val1 != val2)

        # ================== CONTROL DE FLUJO ==================
        elif operator == 'GOTOMAIN':
            self.instruction_pointer = result
            return  # No incrementar IP

        elif operator == 'GOTO':
            self.instruction_pointer = result
            return  # No incrementar IP

        elif operator == 'GOTOF':
            condition = self._get_value(op1)
            if not condition:
                self.instruction_pointer = result
                return

        elif operator == 'GOTOT':
            condition = self._get_value(op1)
            if condition:
                self.instruction_pointer = result
                return

        # ================== LLAMADAS A FUNCIONES ==================
        elif operator == 'SUB':
            # Preparar registro de activación (crear nuevo marco local)
            pass  # El marco se crea con GOSUB

        elif operator == 'PARAM':
            # Pasar parámetro: copiar valor de op1 a dirección result
            val = self._get_value(op1)
            # Los parámetros se guardan temporalmente hasta GOSUB
            if not hasattr(self, '_pending_params'):
                self._pending_params = {}
            self._pending_params[result] = val

        elif operator == 'GOSUB':
            # Verificar límite de recursión (máximo 1000 llamadas)
            if len(self.call_stack) >= 1000:
                raise RuntimeError("Stack overflow: se excedió el límite de 1000 llamadas recursivas")
            # Guardar dirección de retorno
            self.call_stack.append(self.instruction_pointer + 1)
            # Crear nuevo marco local
            new_frame = {}
            # Copiar parámetros pendientes al nuevo marco
            if hasattr(self, '_pending_params'):
                for addr, val in self._pending_params.items():
                    new_frame[addr] = val
                self._pending_params = {}
            self.local_memory_stack.append(new_frame)
            # Limpiar temporales
            self.temp_memory = {}
            # Saltar a la función
            self.instruction_pointer = result
            return

        elif operator == 'ENDFUNC':
            # Restaurar marco local anterior
            if len(self.local_memory_stack) > 1:
                self.local_memory_stack.pop()
            # Retornar al llamador
            if self.call_stack:
                self.instruction_pointer = self.call_stack.pop()
                return

        # ================== ENTRADA/SALIDA ==================
        elif operator == 'PRINT':
            val = self._get_value(result)
            # Remover comillas de strings
            if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            print(val)
            self.output.append(str(val))

        # ================== TERMINACIÓN ==================
        elif operator == 'END':
            self.running = False
            return

        else:
            raise RuntimeError(f"Operador desconocido: {operator}")

        # Avanzar al siguiente cuádruplo
        self.instruction_pointer += 1


# Instancia global de la máquina virtual
virtual_machine = VirtualMachine()


###############################################################
#              FUNCIONES DE REPORTE Y SALIDA
###############################################################

def print_symbol_table():
    print("\n" + "="*70)
    print("TABLA DE SÍMBOLOS")
    print("="*70)
    for scope, variables in symbol_table.items():
        print(f"\nScope: {scope}")
        print(f"{'Variable':<15} {'Tipo':<10} {'Dirección':<10}")
        print("-"*70)
        for var_name, var_info in variables.items():
            var_type = var_info['type']
            var_addr = var_info['address']
            print(f"{var_name:<15} {var_type:<10} {var_addr:<10}")

def print_function_directory():
    print("\n" + "="*70)
    print("DIRECTORIO DE FUNCIONES")
    print("="*70)
    for func_name, func_info in function_directory.items():
        print(f"\nFunción: {func_name}")
        print(f"  Tipo retorno: {func_info['type']}")
        print(f"  Parámetros:")
        if func_info['params']:
            for param in func_info['params']:
                param_name = param[0]
                param_type = param[1]
                param_addr = param[2] if len(param) > 2 else 'N/A'
                print(f"    - {param_name}: {param_type} (dir: {param_addr})")
        else:
            print(f"    (ninguno)")
        print(f"  Variables internas:")
        if func_name in symbol_table and symbol_table[func_name]:
            param_names = [p[0] for p in func_info['params']]
            has_internal_vars = False
            for var_name, var_info in symbol_table[func_name].items():
                if var_name not in param_names:
                    print(f"    - {var_name}: {var_info['type']} (dir: {var_info['address']})")
                    has_internal_vars = True
            if not has_internal_vars:
                print(f"    (ninguna)")
        else:
            print(f"    (ninguna)")
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
    """Guarda el código intermedio en formato estructurado para la VM"""
    output_file = filename.replace('.txt', '_intermediate.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        # Sección de constantes
        f.write("%%CONSTANTS\n")
        for const_type in ['int', 'float', 'string']:
            if constants_table[const_type]:
                items = [f"{val}={addr}" for val, addr in constants_table[const_type].items()]
                f.write(f"{const_type}:{','.join(items)}\n")
        f.write("\n")

        # Sección de funciones
        f.write("%%FUNCTIONS\n")
        for func_name, func_info in function_directory.items():
            params_str = ""
            if func_info['params']:
                params_str = ";".join([f"{p[0]}:{p[1]}:{p[2]}" for p in func_info['params']])
            f.write(f"{func_name}:{func_info['type']}:{func_info['start_quad']}:{params_str}\n")
        f.write("\n")

        # Sección de cuádruplos
        f.write("%%QUADRUPLES\n")
        for i, (op, op1, op2, res) in enumerate(quadruples):
            op1_str = str(op1) if op1 is not None else '-'
            op2_str = str(op2) if op2 is not None else '-'
            res_str = str(res) if res is not None else '-'
            f.write(f"{i}:{op}:{op1_str}:{op2_str}:{res_str}\n")
        f.write("\n")

        # Sección de contadores de memoria
        f.write("%%MEMORY_COUNTERS\n")
        usage = memory_manager.get_memory_usage()
        f.write(f"global:int={usage['global']['int']},float={usage['global']['float']},string={usage['global']['string']}\n")
        f.write(f"local:int={usage['local']['int']},float={usage['local']['float']},string={usage['local']['string']}\n")
        f.write(f"temp:int={usage['temp']['int']},float={usage['temp']['float']},bool={usage['temp']['bool']}\n")
        f.write(f"const:int={usage['const']['int']},float={usage['const']['float']},string={usage['const']['string']}\n")
        f.write("\n")

        f.write("%%END\n")

    print(f"\n✅ Código intermedio guardado en: {output_file}")


def print_constants_table():
    """Imprime la tabla de constantes"""
    print("\n" + "="*70)
    print("TABLA DE CONSTANTES")
    print("="*70)
    for const_type, values in constants_table.items():
        if values:
            print(f"\nTipo: {const_type}")
            print(f"{'Valor':<20} {'Dirección':<10}")
            print("-"*30)
            for value, address in values.items():
                print(f"{str(value):<20} {address:<10}")

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
        print_constants_table()
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
#                  COMPILAR Y EJECUTAR
###############################################################

def compile_and_run(filename):
    """Compila el archivo fuente y lo ejecuta con la máquina virtual"""
    print("\n" + "="*70)
    print("FASE 1: COMPILACIÓN")
    print("="*70)

    success = analizar_archivo(filename)

    if not success:
        print("\n❌ La compilación falló. No se puede ejecutar.")
        return False

    print("\n" + "="*70)
    print("FASE 2: EJECUCIÓN")
    print("="*70)

    # Preparar y ejecutar la máquina virtual
    virtual_machine.reset()
    virtual_machine.load_program(quadruples, constants_table, function_directory)

    try:
        result = virtual_machine.run()
        return result
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        return False


###############################################################
#                           MAIN
###############################################################

if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPILADOR LITTLE DUCK - CON MÁQUINA VIRTUAL")
    print("="*70 + "\n")

    if len(sys.argv) > 1:
        archivo = sys.argv[1]

        # Verificar si se pasó la opción --compile-only
        if len(sys.argv) > 2 and sys.argv[2] == '--compile-only':
            analizar_archivo(archivo)
        else:
            compile_and_run(archivo)
    else:
        print("Uso: python main_virtual.py <archivo.txt> [--compile-only]")
        print("Ejemplo: python main_virtual.py factorial.txt")
        print("         python main_virtual.py factorial.txt --compile-only")
