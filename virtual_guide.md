
test = """7	17000			
3	17001			
2	17002	

global_int 2			
global_float 1			
global_str 0			
global_void 0			
local_int	 0			
local_float 0			
local_str	0			
temp_int	0			
temp_float 2			
temp_bool	0			
cte_int	3			
cte_float	0			
cte_str	0	

1	gotomain	-1	-1	2
2	= 	17000	-1	1000
3	=	17001	-1	1001
4	/	1000	1001	13001
5	+	13001	17002	13002
6	=	13002	-1	2001
7	print	2001	-1	-1
8	print  -1	-1	-1
"""


class Quad():
  op = -1
  arg1 = -1
  arg2 = -1
  destino = -1

  def __init__(self, lista):
    self.op = lista[1]
    self.arg1 = int(lista[2])
    self.arg2 = int(lista[3])
    self.destino = int(lista[4])


cte_dir = {}    
quads = {}      


regions = { "global_int"	  :	['1000']	,
      "global_float"	  :	['2000']	,
      "global_str"	  :	['3000']	,
      "global_void"	  :	['4000']	,
      "local_int"	  :	['7000']	,
      "local_float" :	['8000']	,
      "local_str"	  :	['9000']	,
      "temp_int"	  :	['12000']	,
      "temp_float"  :	['13000']	,
      "temp_bool"	  :	['14000']	,
      "cte_int"	  :	['17000']	,
      "cte_float"	  :	['18000']	,
      "cte_str"	  :	['19000']	 }

memo = {}

seccion = 0   # inicia en 0, avanza cada vez que aparezca una linea vacia
lineas = test.split("\n")
#print(lineas)
# dentifica de que linea se trata
#  constante: seccion 0, len 2
#  contadores de memoria :  seccion 1, len 2
#  quads: seccion 2, len 5

for i in lineas:
  linea  = i.split()
  longitud = len(linea)
  if longitud == 0:
    seccion += 1
  elif seccion == 0 and longitud == 2:
    print('const', linea)
    memo[int(linea[1])] = int(linea[0])
  elif seccion == 1 and longitud == 2:
    print('memo', linea)
    tipo = linea[0]
    regions[tipo].append(int(linea[1]))
  elif seccion == 2 and longitud == 5:
    print('quads', linea)
    quads[int(linea[0])] = Quad(linea)

  #print(linea)


# for k, v in quads.items():
#   print(k, v.op, v.arg1, v.arg2, v.destino)

current_q = 1
print_line_string = ""
# Por cada quad, identifica que es y realiza la operacion correcta
print("\n")

while current_q <= len(quads):
  q = quads[current_q]

  if q.op == 'gotomain':
    current_q = q.destino
    continue
  elif q.op == '=':
    memo[q.destino] = memo[q.arg1]
  elif q.op == '+':
    memo[q.destino] = memo[q.arg1] + memo[q.arg2]
  elif q.op == '/':
    memo[q.destino] = memo[q.arg1] / memo[q.arg2]
  elif q.op == 'print':
    if q.arg1 != -1:
      print_line_string += " " + str(memo[q.arg1])
    else:
      print("quack>", print_line_string, sep="")
      print_line_string = ""
  current_q += 1


print("\n\nMemory")
for m in memo:
  print(m, memo[m])