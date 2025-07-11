import ply.yacc as yacc
import semantico
from tokens import tokens

errores = []

# ==================== TABLA DE SÍMBOLOS Y REGLAS SEMÁNTICAS ====================
# Tabla de símbolos global para análisis semántico
tabla_simbolos = {
    "variables": {},  # {nombre: tipo}
    "funciones": {},  # {nombre: {"parametros": [tipos], "retorno": tipo}}
    "tipos": {
        "string_funciones": ["length", "substring", "toUpperCase", "toLowerCase", "toString"],
        "array_funciones": ["push", "pop", "length"],
        "map_funciones": ["set", "get", "has", "size", "values"],
        "set_funciones": ["add", "has", "size", "delete"]
    }
}

# Variable para controlar análisis en dos pasadas
primera_pasada = True

def agregar_error_semantico(mensaje, lineno=None):
    """Función para agregar errores semánticos al módulo semántico"""
    if lineno:
        error = f"Línea {lineno}: {mensaje}"
    else:
        error = mensaje
    
    semantico.registrar_error(error)

def son_tipos_compatibles(tipo1, tipo2, operacion="asignacion"):
    """Verifica si dos tipos son compatibles para una operación"""
    if tipo1 == tipo2:
        return True
    
    # Operaciones aritméticas solo entre números
    if operacion == "aritmetica":
        return tipo1 == "number" and tipo2 == "number"
    
    # Para asignaciones, ser más estricto
    if operacion == "asignacion":
        return tipo1 == tipo2
    
    return False

def reiniciar_analisis():
    """Reinicia el estado del análisis sintáctico y semántico"""
    global errores, tabla_simbolos, primera_pasada
    errores.clear()
    semantico.errores_semanticos = []
    semantico.reiniciar_tabla()
    primera_pasada = True
    
    # Reiniciar tabla de símbolos
    tabla_simbolos = {
        "variables": {},
        "funciones": {},
        "tipos": {
            "string_funciones": ["length", "substring", "toUpperCase", "toLowerCase", "toString"],
            "array_funciones": ["push", "pop", "length"],
            "map_funciones": ["set", "get", "has", "size", "values"],
            "set_funciones": ["add", "has", "size", "delete"]
        }
    }

# ==================== PRECEDENCIA MEJORADA ====================
precedence = (
    ('right', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'GT', 'LT', 'GTE', 'LTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'UMINUS', 'UPLUS'),
    ('left', 'PUNTO'),
    ('left', 'LBRACKET'),
    ('left', 'LPAREN'),
    ('right', 'ASSIGN'),
)

# ==================== PROGRAMA PRINCIPAL ====================
def p_programa(p):
    '''programa : cuerpo'''
    print("Programa analizado correctamente")

def p_cuerpo(p):
    '''cuerpo : sentencias
              | empty'''

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencias sentencia'''

# ==================== SENTENCIAS ====================
def p_sentencia(p):
    '''sentencia : asignacion
                 | declaracion
                 | impresion
                 | input_teclado
                 | sentencia_if
                 | sentencia_while
                 | sentencia_for
                 | sentencia_for_in
                 | funcion
                 | clase
                 | sentencia_return
                 | llamada_funcion_stmt
                 | sentencia_inc_dec
                 | bloque'''

def p_sentencia_return(p):
    '''sentencia_return : RETURN expresion SEMICOLON
                        | RETURN SEMICOLON'''
    print("Return detectado")

def p_llamada_funcion_stmt(p):
    '''llamada_funcion_stmt : llamada_funcion SEMICOLON
                            | llamada_metodo SEMICOLON'''

# ==================== ASIGNACIÓN Y DECLARACIÓN CON SEMÁNTICA ====================

def p_asignacion(p):
    '''asignacion : LET ID ASSIGN expresion SEMICOLON
                  | LET ID COLON tipo ASSIGN expresion SEMICOLON
                  | variable ASSIGN expresion SEMICOLON'''
    
    if len(p) == 6 and p[1] == 'let':  # LET ID = expresion
        nombre = p[2]
        tipo_expr = p[4] if p[4] else "unknown"
        
        # REGLA SEMÁNTICA 1: Registrar variable en tabla de símbolos
        semantico.declarar_variable(nombre, tipo_expr)
        tabla_simbolos["variables"][nombre] = tipo_expr
        print(f"Asignación: {nombre} = {tipo_expr}")
        
    elif len(p) == 8:  # LET ID : tipo = expresion
        nombre = p[2]
        tipo_declarado = p[4]
        tipo_expr = p[6] if p[6] else "unknown"
        # REGLA SEMÁNTICA 2: Verificar compatibilidad de tipos en asignación
        if not son_tipos_compatibles(tipo_declarado, tipo_expr, "asignacion"):
            agregar_error_semantico(f"Incompatibilidad de tipos: no se puede asignar {tipo_expr} a variable de tipo {tipo_declarado}")
        
        semantico.declarar_variable(nombre, tipo_declarado)
        tabla_simbolos["variables"][nombre] = tipo_declarado
        print(f"Asignación tipada: {nombre} : {tipo_declarado}")
        
    else:  # variable = expresion
        # REGLA SEMÁNTICA 1: Verificar que la variable existe antes de asignar
        if hasattr(p[1], 'id'):
            nombre = p[1].id
            tipo_expr = p[3] if p[3] else "unknown"
            semantico.verificar_asignacion(nombre, tipo_expr)
        print("Asignación a variable")
        
def p_declaracion(p):
    '''declaracion : CONST ID ASSIGN expresion SEMICOLON
                   | CONST ID COLON tipo ASSIGN expresion SEMICOLON
                   | LET ID COLON tipo SEMICOLON
                   | declaracion_array
                   | declaracion_map_set'''
    
    if len(p) >= 5 and p[1] == 'const':
        nombre = p[2]
        if len(p) == 6:  # CONST ID = expresion
            tipo_expr = p[4] if p[4] else "unknown"
        else:  # CONST ID : tipo = expresion
            tipo_declarado = p[4]
            tipo_expr = p[6] if p[6] else "unknown"
            
            # REGLA SEMÁNTICA 2: Verificar compatibilidad de tipos
            if not son_tipos_compatibles(tipo_declarado, tipo_expr, "asignacion"):
                agregar_error_semantico(f"Incompatibilidad de tipos en constante: no se puede asignar {tipo_expr} a {tipo_declarado}")
            tipo_expr = tipo_declarado
            
        tabla_simbolos["variables"][nombre] = tipo_expr
        semantico.declarar_variable(nombre, tipo_expr)
        print(f"Declaración constante: {nombre}")
        
    elif len(p) == 6 and p[1] == 'let':  # LET ID : tipo ;
        nombre = p[2]
        tipo = p[4]
        tabla_simbolos["variables"][nombre] = tipo
        semantico.declarar_variable(nombre, tipo)
        print(f"Declaración variable: {nombre}")

def p_declaracion_array(p):
    '''declaracion_array : LET ID COLON tipo_array ASSIGN expresion SEMICOLON'''
    nombre = p[2]
    tipo_array = f"{p[4]}[]"
    tabla_simbolos["variables"][nombre] = tipo_array
    semantico.declarar_variable(nombre, tipo_array)
    print(f"Declaración de array: {nombre}")

def p_declaracion_map_set(p):
    '''declaracion_map_set : LET ID COLON tipo_generico ASSIGN NEW ID LPAREN argumentos_constructor RPAREN SEMICOLON
                           | LET ID COLON tipo_generico ASSIGN NEW ID LPAREN RPAREN SEMICOLON'''
    nombre = p[2]
    tipo = p[4]
    tabla_simbolos["variables"][nombre] = tipo
    semantico.declarar_variable(nombre, tipo)
    print(f"Declaración de Map/Set: {nombre}")

def p_argumentos_constructor(p):
    '''argumentos_constructor : array_de_pares
                              | argumentos
                              | array_literal'''

# ==================== TIPOS ====================
def p_tipo(p):
    '''tipo : tipo_primitivo
            | tipo_array
            | tipo_generico
            | ID'''
    p[0] = p[1]

def p_tipo_primitivo(p):
    '''tipo_primitivo : STRING_TYPE
                      | NUMBER_TYPE
                      | BOOLEAN'''
    if p[1] == 'string':
        p[0] = "string"
    elif p[1] == 'number':
        p[0] = "number"
    elif p[1] == 'boolean':
        p[0] = "boolean"

def p_tipo_array(p):
    '''tipo_array : tipo_primitivo LBRACKET RBRACKET
                  | ID LBRACKET RBRACKET'''
    p[0] = f"{p[1]}[]"

def p_tipo_generico(p):
    '''tipo_generico : ID LT tipo GT
                     | ID LT tipo COMMA tipo GT'''
    if len(p) == 5:
        p[0] = f"{p[1]}<{p[3]}>"
    else:
        p[0] = f"{p[1]}<{p[3]},{p[5]}>"

# ==================== VARIABLES Y ACCESO CON SEMÁNTICA ====================
def p_variable(p):
    '''variable : ID
                | variable PUNTO ID
                | variable LBRACKET expresion RBRACKET'''
    
    if len(p) == 2:  # ID simple
        nombre = p[1]
        # REGLA SEMÁNTICA 1: Verificar que la variable existe
        tipo_var = semantico.usar_variable(nombre)
        # Crear un objeto simple para pasar el ID
        class Variable:
            def __init__(self, id, tipo):
                self.id = id
                self.tipo = tipo
        
        p[0] = Variable(nombre, tipo_var)
    else:
        p[0] = "unknown"

# ==================== LLAMADAS A FUNCIONES Y MÉTODOS CON SEMÁNTICA ====================
def p_llamada_funcion(p):
    '''llamada_funcion : ID LPAREN argumentos RPAREN
                       | ID LPAREN RPAREN'''
    
    nombre_funcion = p[1]
    
    # REGLA SEMÁNTICA 4: Verificar que la función existe
    tipo_retorno = semantico.usar_funcion(nombre_funcion)
    
    # También verificar en la tabla local
    if nombre_funcion in tabla_simbolos["funciones"]:
        func_info = tabla_simbolos["funciones"][nombre_funcion]
        num_params_esperados = len(func_info["parametros"])
        num_params_recibidos = 0 if len(p) == 4 else contar_argumentos(p[3])
        
        if num_params_esperados != num_params_recibidos:
            agregar_error_semantico(f"Función '{nombre_funcion}' espera {num_params_esperados} parámetros, pero recibió {num_params_recibidos}")
        
        p[0] = func_info["retorno"]
    else:
        p[0] = tipo_retorno
    
    print(f"Llamada a función: {nombre_funcion}")

def contar_argumentos(argumentos):
    """Función auxiliar para contar el número de argumentos en una lista"""
    if not argumentos:
        return 0
    
    # Si argumentos es una lista, devolver su longitud
    if isinstance(argumentos, list):
        return len(argumentos)
    
    # Si es un string simple, contar las comas + 1
    if isinstance(argumentos, str):
        return argumentos.count(',') + 1 if argumentos.strip() else 0
    
    # Por defecto, asumir 1 argumento si hay algo
    return 1

def p_llamada_metodo(p):
    '''llamada_metodo : variable PUNTO ID LPAREN argumentos RPAREN
                      | variable PUNTO ID LPAREN RPAREN'''
    
    metodo = p[3]
    tipo_objeto = p[1] if p[1] else "unknown"
    
    # REGLA SEMÁNTICA 3: Verificar que el método existe para el tipo
    if hasattr(tipo_objeto, 'tipo'):
        tipo_real = tipo_objeto.tipo
    else:
        tipo_real = str(tipo_objeto)
    
    semantico.verificar_metodo_objeto(tipo_real, metodo)
    
    print("Llamada a método detectado")
    p[0] = "unknown"

def p_argumentos(p):
    '''argumentos : expresion
                  | argumentos COMMA expresion'''    
    if len(p) == 2:  # expresion
        p[0] = [p[1]]
    else:  # argumentos COMMA expresion
        if isinstance(p[1], list):
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1], p[3]]

# ==================== IMPRESIÓN ====================
def p_impresion(p):
    '''impresion : console_log SEMICOLON'''
    print("Impresión detectada")

def p_console_log(p):
    '''console_log : ID PUNTO ID LPAREN lista_argumentos RPAREN'''

def p_lista_argumentos(p):
    '''lista_argumentos : argumentos
                        | string_especial
                        | lista_argumentos COMMA argumentos
                        | lista_argumentos COMMA string_especial
                        | empty'''

def p_string_especial(p):
    '''string_especial : STRING
                       | TEMPLATE_LITERAL
                       | LBRACE ID RBRACE'''

# ==================== INPUT TECLADO ====================
def p_input_teclado(p):
    '''input_teclado : LET ID ASSIGN llamada_funcion SEMICOLON'''
    print("Input de teclado detectado")

# ==================== ESTRUCTURAS DE CONTROL ====================
def p_sentencia_if(p):
    '''sentencia_if : IF LPAREN expresion RPAREN sentencia_ejecutable
                    | IF LPAREN expresion RPAREN sentencia_ejecutable ELSE sentencia_ejecutable'''
    
    # REGLA SEMÁNTICA 7: Verificar que la condición sea de tipo boolean
    tipo_condicion = p[3] if p[3] else "unknown"
    if tipo_condicion != "boolean" and tipo_condicion != "unknown":
        agregar_error_semantico(f"La condición del IF debe ser de tipo boolean, no {tipo_condicion}")
    
    print("Estructura IF detectada")

def p_sentencia_ejecutable(p):
    '''sentencia_ejecutable : bloque
                            | asignacion
                            | impresion
                            | input_teclado
                            | llamada_funcion_stmt
                            | sentencia_return
                            | sentencia_if
                            | sentencia_while
                            | sentencia_for'''

def p_sentencia_while(p):
    '''sentencia_while : WHILE LPAREN expresion RPAREN bloque'''
    
    # REGLA SEMÁNTICA 7: Verificar que la condición sea de tipo boolean
    tipo_condicion = p[3] if p[3] else "unknown"
    if tipo_condicion != "boolean" and tipo_condicion != "unknown":
        agregar_error_semantico(f"La condición del WHILE debe ser de tipo boolean, no {tipo_condicion}")
    
    print("While detectado")

def p_sentencia_for(p):
    '''sentencia_for : FOR LPAREN inicializacion SEMICOLON condicion SEMICOLON incremento RPAREN bloque'''
    
    # REGLA SEMÁNTICA 7: Verificar que la condición sea de tipo boolean
    if p[5]:  # Si hay condición
        tipo_condicion = p[5] if p[5] else "unknown"
        if tipo_condicion != "boolean" and tipo_condicion != "unknown":
            agregar_error_semantico(f"La condición del FOR debe ser de tipo boolean, no {tipo_condicion}")
    
    print("For detectado")

def p_sentencia_for_in(p):
    '''sentencia_for_in : FOR LPAREN LET ID IN expresion RPAREN bloque
                        | FOR LPAREN LET ID OF expresion RPAREN bloque'''
    print(f"For...in/of detectado: iterando {p[4]}")

def p_sentencia_inc_dec(p):
    '''sentencia_inc_dec : ID INC SEMICOLON
                            | ID DEC SEMICOLON
                            | INC ID SEMICOLON
                            | DEC ID SEMICOLON'''
    
    # REGLA SEMÁNTICA 5: Verificar que la variable para incremento/decremento sea numérica
    variable = p[1] if p[1] != '++' and p[1] != '--' else p[2]
    if variable in tabla_simbolos["variables"]:
        tipo_var = tabla_simbolos["variables"][variable]
        if tipo_var != "number":
            operador = "++" if "++" in p[1:] else "--"
            agregar_error_semantico(f"El operador '{operador}' solo se puede aplicar a variables de tipo number, no {tipo_var}")
    
    if len(p) == 4:
        if p[2] == '++':
            print(f"Post-incremento detectado: {p[1]}++")
        elif p[2] == '--':
            print(f"Post-decremento detectado: {p[1]}--")
        elif p[1] == '++':
            print(f"Pre-incremento detectado: ++{p[2]}")
        elif p[1] == '--':
            print(f"Pre-decremento detectado: --{p[2]}")

def p_inicializacion(p):
    '''inicializacion : LET ID ASSIGN expresion
                      | variable ASSIGN expresion
                      | LET ID COLON tipo
                      | empty'''

def p_condicion(p):
    '''condicion : expresion
                 | empty'''
    if len(p) == 2:
        p[0] = p[1]

def p_incremento(p):
    '''incremento : ID INC
                  | ID DEC
                  | INC ID
                  | DEC ID
                  | variable ASSIGN expresion
                  | empty'''

def p_bloque(p):
    '''bloque : LBRACE cuerpo RBRACE
              | LBRACE RBRACE'''

# ==================== EXPRESIONES CON SEMÁNTICA ====================
def p_expresion_binaria_aritmetica(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion MOD expresion'''
    
    tipo_izq = p[1] if p[1] else "unknown"
    tipo_der = p[3] if p[3] else "unknown"
    operador = p[2]
    
    # REGLA SEMÁNTICA 5: Verificar compatibilidad en operaciones aritméticas
    resultado_tipo = semantico.verificar_operacion(tipo_izq, operador, tipo_der)
    if not resultado_tipo:
        agregar_error_semantico(f"Operación aritmética '{operador}' no válida entre {tipo_izq} y {tipo_der}")
    
    p[0] = resultado_tipo if resultado_tipo else "number"

def p_expresion_unaria(p):
    '''expresion : MINUS expresion %prec UMINUS
                 | PLUS expresion %prec UPLUS'''
    tipo_expr = p[2] if p[2] else "unknown"
    
    # REGLA SEMÁNTICA 5: Operadores unarios solo para números
    if tipo_expr != "number" and tipo_expr != "unknown":
        operador = p[1]
        agregar_error_semantico(f"Operador unario '{operador}' no válido para tipo {tipo_expr}")
    
    p[0] = "number"

def p_expresion_relacional(p):
    '''expresion : expresion GT expresion
                 | expresion LT expresion
                 | expresion GTE expresion
                 | expresion LTE expresion
                 | expresion EQ expresion
                 | expresion NEQ expresion
                 | expresion IGU expresion'''
    
    tipo_izq = p[1] if p[1] else "unknown"
    tipo_der = p[3] if p[3] else "unknown"
    operador = p[2]
    
    resultado_tipo = semantico.verificar_operacion(tipo_izq, operador, tipo_der)
    p[0] = "boolean"

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    
    tipo_izq = p[1] if p[1] else "unknown"
    tipo_der = p[3] if p[3] else "unknown"
    operador = p[2]
    
    resultado_tipo = semantico.verificar_operacion(tipo_izq, operador, tipo_der)
    p[0] = "boolean"

def p_expresion_negacion(p):
    '''expresion : NOT expresion'''
    tipo_expr = p[2] if p[2] else "unknown"
    
    # REGLA SEMÁNTICA 7: NOT solo para booleanos
    if tipo_expr != "boolean" and tipo_expr != "unknown":
        agregar_error_semantico(f"Operador NOT solo válido para tipo boolean, no {tipo_expr}")
    
    p[0] = "boolean"

def p_expresion_acceso(p):
    '''expresion : expresion PUNTO ID
                 | expresion LBRACKET expresion RBRACKET'''

def p_expresion_llamadas(p):
    '''expresion : llamada_funcion
                 | llamada_metodo'''
    p[0] = p[1]

def p_expresion_basica(p):
    '''expresion : NUMBER
                 | STRING
                 | variable
                 | TRUE
                 | FALSE
                 | TEMPLATE_LITERAL
                 | LPAREN expresion RPAREN
                 | array_literal
                 | map_set_literal'''
    
    if p[1] == 'true' or p[1] == 'false':
        p[0] = "boolean"
    elif hasattr(p.slice[1], 'type'):
        if p.slice[1].type == 'NUMBER':
            p[0] = "number"
        elif p.slice[1].type == 'STRING' or p.slice[1].type == 'TEMPLATE_LITERAL':
            p[0] = "string"
        else:
            p[0] = "unknown"
    elif isinstance(p[1], str):
        p[0] = p[1]  # Si es un tipo retornado por variable o literal
    elif len(p) == 4:  # LPAREN expresion RPAREN
        p[0] = p[2]
    else:
        if hasattr(p[1], 'tipo'):
            p[0] = p[1].tipo
        else:
            p[0] = "unknown"

# ==================== ESTRUCTURAS DE DATOS ====================
def p_array_literal(p):
    '''array_literal : LBRACKET elementos RBRACKET
                     | LBRACKET RBRACKET'''
    print("Array detectado")
    p[0] = "unknown[]"

def p_elementos(p):
    '''elementos : expresion
                 | elementos COMMA expresion'''

def p_map_set_literal(p):
    '''map_set_literal : NEW ID LPAREN array_de_pares RPAREN
                       | NEW ID LPAREN argumentos RPAREN
                       | NEW ID LPAREN RPAREN'''
    print("Map/Set detectado")
    p[0] = p[2]

def p_array_de_pares(p):
    '''array_de_pares : LBRACKET pares RBRACKET'''

def p_pares(p):
    '''pares : par
             | pares COMMA par'''

def p_par(p):
    '''par : LBRACKET expresion COMMA expresion RBRACKET'''

# ==================== FUNCIONES CON TIPOS TYPESCRIPT ====================
def p_funcion(p):
    '''funcion : FUNCTION ID LPAREN parametros RPAREN LBRACE cuerpo RBRACE
               | FUNCTION ID LPAREN parametros RPAREN COLON tipo LBRACE cuerpo RBRACE
               | FUNCTION ID LPAREN RPAREN LBRACE cuerpo RBRACE
               | FUNCTION ID LPAREN RPAREN COLON tipo LBRACE cuerpo RBRACE'''
    
    nombre_funcion = p[2]
    
    # REGLA SEMÁNTICA 6: Registrar función en tabla de símbolos
    if len(p) == 9:  # FUNCTION ID LPAREN parametros RPAREN LBRACE cuerpo RBRACE - Con parámetros, sin tipo de retorno
        parametros_lista = p[4] if isinstance(p[4], list) else []
        tabla_simbolos["funciones"][nombre_funcion] = {
            "parametros": parametros_lista,
            "retorno": "void"
        }
        # Registrar también en el módulo semántico
        semantico.declarar_funcion(nombre_funcion, parametros_lista, "void")
        print(f"Función '{nombre_funcion}' declarada con {len(parametros_lista)} parámetros y sin tipo de retorno")
        
    elif len(p) == 11:  # FUNCTION ID LPAREN parametros RPAREN COLON tipo LBRACE cuerpo RBRACE - Con parámetros, con tipo de retorno
        parametros_lista = p[4] if isinstance(p[4], list) else []
        tipo_retorno = p[7]
        tabla_simbolos["funciones"][nombre_funcion] = {
            "parametros": parametros_lista,
            "retorno": tipo_retorno
        }
        # Registrar también en el módulo semántico
        semantico.declarar_funcion(nombre_funcion, parametros_lista, tipo_retorno)
        print(f"Función '{nombre_funcion}' declarada con {len(parametros_lista)} parámetros y tipo de retorno: {tipo_retorno}")
        
    elif len(p) == 8:  # FUNCTION ID LPAREN RPAREN LBRACE cuerpo RBRACE - Sin parámetros, sin tipo de retorno
        tabla_simbolos["funciones"][nombre_funcion] = {
            "parametros": [],
            "retorno": "void"
        }
        # Registrar también en el módulo semántico
        semantico.declarar_funcion(nombre_funcion, [], "void")
        print(f"Función '{nombre_funcion}' declarada sin parámetros y sin tipo de retorno")
        
    elif len(p) == 10:  # FUNCTION ID LPAREN RPAREN COLON tipo LBRACE cuerpo RBRACE - Sin parámetros, con tipo de retorno
        tipo_retorno = p[6]
        tabla_simbolos["funciones"][nombre_funcion] = {
            "parametros": [],
            "retorno": tipo_retorno
        }
        # Registrar también en el módulo semántico
        semantico.declarar_funcion(nombre_funcion, [], tipo_retorno)
        print(f"Función '{nombre_funcion}' declarada sin parámetros y tipo de retorno: {tipo_retorno}")
    
    print(f"Función registrada: {nombre_funcion}")

def p_parametros(p):
    '''parametros : parametro
                  | parametros COMMA parametro'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        if isinstance(p[1], list):
            p[0] = p[1] + [p[3]] if p[3] else p[1]
        else:
            p[0] = [p[1], p[3]] if p[1] and p[3] else ([p[1]] if p[1] else [p[3]] if p[3] else [])

def p_parametro(p):
    '''parametro : ID
                 | ID COLON tipo
                 | ID COLON tipo_generico
                 | ID COLON tipo_array'''
    if len(p) == 2:
        p[0] = "unknown"
    else:
        p[0] = p[3]

# ==================== CLASES ====================
def p_clase(p):
    '''clase : CLASS ID LBRACE cuerpo_clase RBRACE'''
    print(f"Clase definida: {p[2]}")

def p_cuerpo_clase(p):
    '''cuerpo_clase : elementos_clase
                    | empty'''

def p_elementos_clase(p):
    '''elementos_clase : elemento_clase
                       | elementos_clase elemento_clase'''

def p_elemento_clase(p):
    '''elemento_clase : funcion
                      | asignacion
                      | declaracion'''

# ==================== MÉTODOS ESPECIALES ====================
def p_expresion_metodos_especiales(p):
    '''expresion : variable PUNTO ID LPAREN RPAREN
                 | variable PUNTO ID LPAREN argumentos RPAREN
                 | variable PUNTO SIZE
                 | variable PUNTO LENGTH'''
    print("Método/Propiedad especial detectado")

def p_expresion_propiedades(p):
    '''expresion : variable PUNTO ID'''
    if p[3] in ['size', 'length', 'values', 'has']:
        print(f"Propiedad/método {p[3]} detectado")

def p_expresion_constructor_con_array(p):
    '''expresion : NEW ID LPAREN array_literal RPAREN'''
    print(f"Constructor {p[2]} con array detectado")

# ==================== UTILIDADES ====================
def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        mensaje = f"Error de sintaxis en token '{p.value}' (línea {p.lineno})"
        print(mensaje)
        errores.append(mensaje)
        parser.errok()
    else:
        mensaje = "Error de sintaxis: final de entrada inesperado. Falta ;"
        print(mensaje)
        errores.append(mensaje)

# Crear el parser
parser = yacc.yacc(debug=False, write_tables=True)