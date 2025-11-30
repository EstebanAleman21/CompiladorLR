# Test Cases - Compilador Little Duck con Maquina Virtual

Este documento describe todos los casos de prueba del compilador Little Duck y que caracteristicas de la maquina virtual demuestran.

---

## Estructura de Carpetas

```
test_cases/
├── valid/      # Tests que deben COMPILAR Y EJECUTAR correctamente
├── errors/     # Tests que deben DETECTAR errores semanticos
└── runtime/    # Tests que deben FALLAR en tiempo de ejecucion
```

---

## Tests Validos (valid/)

Estos tests demuestran el correcto funcionamiento del compilador y la maquina virtual.

### 01_arithmetic.txt
**Caracteristica:** Operaciones aritmeticas y precedencia de operadores

| Prueba | Descripcion |
|--------|-------------|
| Precedencia | `5 + 3 * 2 = 11` (multiplicacion antes de suma) |
| Parentesis | `(5 + 3) * 2 = 16` (parentesis alteran precedencia) |
| Division | `10 / 4 = 2.5` (division siempre produce float) |

**Cuadruplos generados:** `+`, `-`, `*`, `/`

**Componente VM probado:** Cubo semantico para operaciones aritmeticas

---

### 02_conditionals.txt
**Caracteristica:** Estructuras condicionales if-else

| Prueba | Descripcion |
|--------|-------------|
| If-else basico | Ejecuta rama correcta segun condicion |
| If sin else | Salta correctamente cuando condicion es falsa |
| Operadores relacionales | `>`, `<`, `>=`, `<=`, `==`, `!=` |

**Cuadruplos generados:** `GOTOF`, `GOTO`

**Componente VM probado:** Saltos condicionales, evaluacion de expresiones booleanas

---

### 03_loops.txt
**Caracteristica:** Ciclos while y do-while

| Prueba | Descripcion |
|--------|-------------|
| While loop | Ejecuta mientras condicion sea verdadera |
| Do-while loop | Ejecuta al menos una vez |
| Cuerpo vacio | `do { } while (x > 5);` compila correctamente |

**Cuadruplos generados:** `GOTOF` (while), `GOTOT` (do-while), `GOTO`

**Componente VM probado:** Control de flujo con ciclos

---

### 04_functions.txt
**Caracteristica:** Definicion y llamada de funciones

| Prueba | Descripcion |
|--------|-------------|
| Funcion con parametros | `suma(5, 3)` ejecuta correctamente |
| Multiples tipos de parametros | int, float, string |
| Variables locales | Cada funcion tiene su propio scope |

**Cuadruplos generados:** `SUB`, `PARAM`, `GOSUB`, `ENDFUNC`

**Componente VM probado:** Call stack, paso de parametros, retorno de funciones

---

### 05_recursion.txt
**Caracteristica:** Funciones recursivas

| Prueba | Descripcion |
|--------|-------------|
| Countdown | Recursion simple con condicion de paro |
| Factorial | Recursion con acumulador |

**Cuadruplos generados:** `SUB`, `PARAM`, `GOSUB`, `ENDFUNC` (anidados)

**Componente VM probado:** Stack de llamadas recursivas, contextos locales multiples

---

### 06_print.txt
**Caracteristica:** Salida de datos

| Prueba | Descripcion |
|--------|-------------|
| Print simple | Imprime un valor |
| Print multiple | `print("x = ", x, " fin")` |
| Newline automatico | Cada print termina con `\n` |

**Cuadruplos generados:** `PRINT`

**Componente VM probado:** Salida formateada, manejo de strings

---

### 07_string_operations.txt
**Caracteristica:** Operaciones con strings

| Prueba | Descripcion |
|--------|-------------|
| Concatenacion | `"Hello" + " World" = "Hello World"` |
| Asignacion | Variables de tipo string |

**Cuadruplos generados:** `+` (con operandos string), `=`

**Componente VM probado:** Cubo semantico para strings, memoria de strings

---

### 08_comparisons.txt
**Caracteristica:** Todos los operadores de comparacion

| Operador | Ejemplo | Resultado |
|----------|---------|-----------|
| `>` | `5 > 3` | true |
| `>=` | `5 >= 3` | true |
| `<` | `3 < 5` | true |
| `<=` | `3 <= 5` | true |
| `==` | `2.5 == 2.5` | true |
| `!=` | `5 != 3` | true |

**Componente VM probado:** Operadores relacionales, comparacion int vs float

---

### 09_unary_minus.txt
**Caracteristica:** Operador unario menos

| Prueba | Descripcion |
|--------|-------------|
| Negacion de variable | `y = -x` donde x=5, y=-5 |
| Literal negativo | `f = -3.14` |
| En expresiones | `x + -3` |

**Cuadruplos generados:** `UMINUS`

**Componente VM probado:** Operador unario, preservacion de tipos

---

### 10_nested_control.txt
**Caracteristica:** Estructuras de control anidadas

| Prueba | Descripcion |
|--------|-------------|
| While anidado | `while { while { } }` |
| If anidado | `if { if { } else { } }` |
| While con if | Control mixto |

**Componente VM probado:** Stack de saltos, multiples niveles de anidacion

---

### 11_function_chain.txt
**Caracteristica:** Funciones que llaman a otras funciones

```
processNumber(x) -> doubleAndPrint(x) -> printValue(x)
```

| Prueba | Descripcion |
|--------|-------------|
| Cadena de llamadas | A llama a B, B llama a C |
| Contextos multiples | Cada funcion mantiene sus variables |

**Componente VM probado:** Stack de llamadas no recursivas, manejo de multiples contextos

---

### 12_complex_expressions.txt
**Caracteristica:** Expresiones aritmeticas complejas

| Expresion | Resultado |
|-----------|-----------|
| `2 + 3*4` | 14 |
| `(2+3)*4` | 20 |
| `((2+3)*4)/5` | 4.0 |
| `2*3 + 4*5 - 2*4` | 18 |

**Componente VM probado:** Precedencia correcta, temporales multiples

---

### 13_memory_segments.txt
**Caracteristica:** Segmentos de memoria virtual

| Segmento | Rango | Uso |
|----------|-------|-----|
| Global Int | 1000-1999 | Variables int globales |
| Global Float | 2000-2999 | Variables float globales |
| Global String | 3000-3999 | Variables string globales |
| Local Int | 7000-7999 | Variables int locales |
| Local Float | 8000-8999 | Variables float locales |
| Temp Int | 12000-12999 | Temporales int |
| Temp Float | 13000-13999 | Temporales float |
| Temp Bool | 14000-14999 | Resultados booleanos |
| Const Int | 17000-17999 | Constantes int |
| Const Float | 18000-18999 | Constantes float |
| Const String | 19000-19999 | Constantes string |

**Componente VM probado:** MemoryManager, asignacion de direcciones

---

### 14_deep_recursion.txt
**Caracteristica:** Recursion profunda (500 llamadas)

| Prueba | Descripcion |
|--------|-------------|
| 500 llamadas | Cerca del limite pero sin excederlo |
| Limpieza de stack | Memoria se libera correctamente |

**Componente VM probado:** Limite de recursion (1000), eficiencia del call stack

---

## Tests de Errores (errors/)

Estos tests verifican que el compilador detecta errores semanticos.

### 01_type_mismatch.txt
**Error detectado:** Incompatibilidad de tipos en asignacion

```
x : int = 3.14      // ERROR: float a int
s : string = 5/2.0  // ERROR: float a string
```

**Componente probado:** Cubo semantico para operador `=`

---

### 02_undeclared.txt
**Error detectado:** Variable no declarada

```
y = 10;    // ERROR: 'y' no declarada
print(z);  // ERROR: 'z' no declarada
```

**Componente probado:** Tabla de simbolos, `lookup_variable()`

---

### 03_scope.txt
**Error detectado:** Funcion intenta acceder a variable global

```
var globalVar : int;
void foo() [ { globalVar = 5; } ];  // ERROR: no puede acceder
```

**Componente probado:** Aislamiento de scope en funciones

---

### 04_param_type.txt
**Error detectado:** Tipo incorrecto en parametro de funcion

```
void foo(x : int, y : float) [ ... ];
foo(5, "hello");  // ERROR: string en lugar de float
```

**Componente probado:** Verificacion de tipos en llamadas a funciones

---

### 05_param_count.txt
**Error detectado:** Numero incorrecto de parametros

```
void twoParams(a : int, b : int) [ ... ];
twoParams(5);  // ERROR: espera 2, recibe 1
```

**Componente probado:** Conteo de argumentos en llamadas

---

### 06_duplicate_name.txt
**Error detectado:** Variable con mismo nombre que el programa

```
program DUPLICADO;
var DUPLICADO : int;  // ERROR: nombre duplicado
```

**Componente probado:** Validacion de nombres en `add_variable()`

---

### 07_non_boolean_condition.txt
**Error detectado:** Condicion no booleana en if/while

```
var x : int;
if (x) { ... }  // ERROR: condicion debe ser booleana
```

**Componente probado:** Verificacion de tipo en condiciones

---

## Tests de Runtime (runtime/)

Estos tests verifican errores detectados durante la ejecucion.

### 01_division_zero.txt
**Error runtime:** Division entre cero

```
result = x / y;  // donde y = 0
```

**Salida esperada:**
```
ERROR EN TIEMPO DE EJECUCION: Division entre cero
```

**Componente probado:** Validacion en operador `/` de la VM

---

### 02_stack_overflow.txt
**Error runtime:** Exceso de llamadas recursivas

```
void infiniteRecursion(n : int) [ { infiniteRecursion(n + 1); } ];
infiniteRecursion(1);  // Nunca termina
```

**Salida esperada:**
```
ERROR EN TIEMPO DE EJECUCION: Stack overflow: se excedio el limite de 1000 llamadas recursivas
```

**Componente probado:** Limite de recursion en `GOSUB`

---

### 03_memory_stress.txt
**Prueba de estres:** Uso intensivo de temporales

- 100 iteraciones de expresiones complejas
- Multiples temporales por iteracion
- Verifica que no hay memory leak

**Salida esperada:** Completa sin errores

**Componente probado:** Limpieza de temporales, estabilidad de memoria

---

## Resumen de Cobertura

### Componentes del Compilador

| Componente | Tests que lo prueban |
|------------|---------------------|
| Lexer | Todos (analisis lexico) |
| Parser | Todos (analisis sintactico) |
| Cubo Semantico | 01, 07, 08, errors/01 |
| Tabla de Simbolos | 04, 13, errors/02, errors/03 |
| Generacion de Cuadruplos | Todos |
| Directorio de Funciones | 04, 05, 11 |

### Componentes de la Maquina Virtual

| Componente | Tests que lo prueban |
|------------|---------------------|
| Operaciones Aritmeticas | 01, 09, 12 |
| Operaciones Relacionales | 02, 08 |
| Control de Flujo (GOTO) | 02, 03, 10 |
| Llamadas a Funciones | 04, 05, 11, 14 |
| Manejo de Memoria | 13, runtime/03 |
| Deteccion de Errores Runtime | runtime/01, runtime/02 |
| Print | 06, todos |

### Cuadruplos Probados

| Cuadruplo | Descripcion | Tests |
|-----------|-------------|-------|
| `+` | Suma | 01, 07, 12 |
| `-` | Resta | 01, 12 |
| `*` | Multiplicacion | 01, 12 |
| `/` | Division | 01, runtime/01 |
| `UMINUS` | Negacion | 09 |
| `>`, `<`, `>=`, `<=`, `==`, `!=` | Comparacion | 02, 08 |
| `=` | Asignacion | Todos |
| `GOTOMAIN` | Salto a main | Todos |
| `GOTO` | Salto incondicional | 02, 03 |
| `GOTOF` | Salto si falso | 02, 03 |
| `GOTOT` | Salto si verdadero | 03 (do-while) |
| `SUB` | Inicio llamada funcion | 04, 05, 11 |
| `PARAM` | Paso de parametro | 04, 05, 11 |
| `GOSUB` | Llamada a funcion | 04, 05, 11, 14 |
| `ENDFUNC` | Fin de funcion | 04, 05, 11 |
| `PRINT` | Imprimir | Todos |

---

## Como Ejecutar los Tests

### Test individual
```bash
python main_virtual.py test_cases/valid/01_arithmetic.txt
```

### Todos los tests validos
```bash
for f in test_cases/valid/*.txt; do
  echo "=== $f ==="
  python main_virtual.py "$f"
done
```

### Solo compilar (sin ejecutar)
```bash
python main_virtual.py test_cases/valid/01_arithmetic.txt --compile-only
```
