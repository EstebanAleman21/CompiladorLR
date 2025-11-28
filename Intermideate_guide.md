import ply.yacc as yacc  # importa yacc
from vlexer import tokens, lexer  


def p_error(t):
	
	if t != None: 
		print("Syntax error at ", t.type, t.value, t.lineno, t.lexpos)
		
	else:
		print("Syntax error: unexpected EOF")

#--------------------------ESTRUCTURAS---------------------------------------
# todo lo que deba ser persistente debe ser OBJETO o DICCIONARIO, 
# si no se pierde en las funciones de la libreria 
class Persistent : 
	stack_args = ['none']

	nquads = 0			# contador de quads, para sus numeros de linea
	ntemps = 0	

	quad_list = [] 		# una lista de todos los quads

	def __init__(self):
		self.stack_args = [ ('none', 'none') ]
		self.nquads = 0
		self.ntemps = 0	



names = { }
names['main']  = {}

# cubo para validar semantica (recuerda extenderlo)
cubo = {
	('int','int', '+') : 'int',
	('float','float', '+') : 'float',
	('int','float', '+') : 'float',
	('float','int', '+') : 'float',

	('string','int', '/') : 'err',


	('int','int', '*') : 'int',
	('float','float', '*') : 'float',
	('int','float', '*') : 'float',
	('float','int', '*') : 'float',

	('int','int', '=') : 'true',
}

ds = Persistent();  # data structures

#------------------------------------------------------------------------------
#	genera quads de para operadores de 2 args
#	asi pe podra mandar llamar desde +, *, /, etc... 
def quad_gen_two_arg_ops( operator ): 
	
	# Ej. Al multiplicar 
	# operador es '*'
	# extrae argumento_L y tipo_L de la stack de operandos
	# extrae argumento_R y tipo_R de la stack de operandos
	# tipo_resultado = consulta el cubo
	
	# verifica si tipo_resultado no es error
	#	aumenta contadores
	# 	forma el nombre de una variable temporal
	#	la variable temporal y el tipo_resultado pasan a la stack
	# 	imprime
	op = operator
	arg_R, tipo_R = ds.stack_args.pop()
	arg_L, tipo_L = ds.stack_args.pop()

	tipo_res = cubo[tipo_L, tipo_R, op]

	if tipo_res != 'err':
		ds.nquads += 1
		ds.ntemps += 1
		temp = "t" + str(ds.ntemps)
		
		ds.stack_args.append( (temp, tipo_res) )

		new_quad = [ds.nquads, op, arg_L, arg_R, temp]
		ds.quad_list.append( new_quad )
		print(ds.nquads, op, arg_L, arg_R, temp)

	else: 
		print("Error de semantica blabla. . ." )


# -----------------------------------------------------------------------------

def p_statement_multi(t):
	"statement : statement asigna "

def p_statement(t):
	"statement : asigna "

def p_asigna(t):
	"asigna : ID OPASIGNA exp SEMICOL "
	#print( t[1], t[3])
	#names['main'][t[1]] = t[3]
	#t[0] = True

	# Verifica que el ID exista en la tabla de simbolos, y obten su tipo
	# 	significa revisar names[scope][name_id]
	# En este ejemplo la gramatica no tiene declaciones, asi que 
	# asumiremos que el ID existe y que es int

	
	# Despues de eso
	name_id = t[1] 
	type_id = 'int'   # en el ejemplo suponemos que sea int
	
	# operador es '='
	op = '='
	# extrae argumento y tipo de la stack
	arg, tipo = ds.stack_args.pop()
	
	# extrae type_res del cubo
	tipo_res = cubo[type_id, tipo, op]

	# Si type_res no es error
	if tipo_res != 'err':
		ds.nquads += 1
		ds.ntemps += 1
		
		new_quad = [ds.nquads, op, arg, "_", name_id ]
		
		print(ds.nquads, op, arg, "_", name_id)
		
		ds.quad_list.append(new_quad)

		# aumenta contadores
		# forma el quad:  nquad  =  arg  _ id
		# imprime el quad
		# agregalo a la lista de quads 
	


def p_exp_add(t):
	"exp : exp PLUS term "
	#print("exp -> exp + term")
	#print(t[1]+t[3])	
	#t[0] = t[1] + t[3]
	op = '+'
	quad_gen_two_arg_ops(op)
	

def p_exp(t):
	"exp : term"
	# print("exp -> term")
	# print(t[1])
	#t[0] = t[1]
	


def p_term_times( t):
	"term : term TIMES factor"
	#t[0] = t[1] * t[3]
	#print("term -> term * factor")	
	#print(t[0])
	
	op = '*'
	quad_gen_two_arg_ops(op)
	# sacar 2 operandos de la stack
	# arg_R, tipo_R = ds.stack_args.pop()
	# arg_L, tipo_L = ds.stack_args.pop()

	# tipo_res = cubo[tipo_L, tipo_R, op]

	# if tipo_res != 'err':
	# 	ds.nquads += 1
	# 	ds.ntemps += 1
	# 	temp = "t" + str(ds.ntemps)
		
	# 	ds.stack_args.append( (temp, tipo_res) )

	# 	new_quad = [ds.nquads, op, arg_L, arg_R, temp]
	# 	ds.quad_list.append( new_quad )
	# 	print(ds.nquads, op, arg_L, arg_R, temp)


	# else: 
	# 	print("Error de semantica blabla. . ." )

def p_term( t):
	"term : factor"

	
def p_factor_e(t):
	'factor : LPAREN exp RPAREN'


def p_factor_id(t):
	'factor : ID'
	# accede a la tabla de simbolos 
	# verifica que el id exista, y extrae su tipo
	# push (id, tipo) a la stack  ds.stack_args  
	


def p_factor_cons_float( t ):
	"factor : CONS_FLOAT"
	
	# push operando con tipo float 
	ds.stack_args.append( (t[1], 'float') )

def p_factor_cons_int( t ):
	"factor : CONS_INT"

	# push operando con tipo int 
	ds.stack_args.append( (t[1], 'int') )

	


s = """

b = 1 + 2 * 3;

a = 3 * 8;

"""


parser = yacc.yacc()
result = parser.parse(s)

for q in ds.quad_list : 
	print( q )


#print("\n\nFinal result:", result)
#print("Tabla simbols", names)