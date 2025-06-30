import ply.yacc as yacc
import semantico
from tokens import tokens
from datetime import datetime
import os

errores = []

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


# ==================== ASIGNACIÓN Y DECLARACIÓN ====================
def p_asignacion(p):
    '''asignacion : LET ID ASSIGN expresion SEMICOLON
                  | LET ID COLON tipo ASSIGN expresion SEMICOLON
                  | variable ASSIGN expresion SEMICOLON'''
    if len(p) == 6 and p[1] == 'let':
        print(f"Asignación: {p[2]}")
    elif len(p) == 8:  # LET ID : tipo = expresion ;
        print(f"Asignación tipada: {p[2]}")
    else:
        print("Asignación a variable")


def p_declaracion(p):
    '''declaracion : CONST ID ASSIGN expresion SEMICOLON
                   | CONST ID COLON tipo ASSIGN expresion SEMICOLON
                   | LET ID COLON tipo SEMICOLON
                   | declaracion_array
                   | declaracion_map_set'''
    if len(p) >= 5 and p[1] == 'const':
        print(f"Declaración constante: {p[2]}")
    elif len(p) == 5 and p[1] == 'let':
        print(f"Declaración variable: {p[2]}")


def p_declaracion_array(p):
    '''declaracion_array : LET ID COLON tipo_array ASSIGN expresion SEMICOLON'''
    print(f"Declaración de array: {p[2]}")


def p_declaracion_map_set(p):
    '''declaracion_map_set : LET ID COLON tipo_generico ASSIGN NEW ID LPAREN argumentos_constructor RPAREN SEMICOLON
                           | LET ID COLON tipo_generico ASSIGN NEW ID LPAREN RPAREN SEMICOLON'''
    print(f"Declaración de Map/Set: {p[2]}")


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


def p_tipo_primitivo(p):
    '''tipo_primitivo : STRING_TYPE
                      | NUMBER_TYPE
                      | BOOLEAN'''


def p_tipo_array(p):
    '''tipo_array : tipo_primitivo LBRACKET RBRACKET
                  | ID LBRACKET RBRACKET'''


def p_tipo_generico(p):
    '''tipo_generico : ID LT tipo GT
                     | ID LT tipo COMMA tipo GT'''


# ==================== VARIABLES Y ACCESO ====================
def p_variable(p):
    '''variable : ID
                | variable PUNTO ID
                | variable LBRACKET expresion RBRACKET'''


# ==================== LLAMADAS A FUNCIONES Y MÉTODOS ====================
def p_llamada_funcion(p):
    '''llamada_funcion : ID LPAREN argumentos RPAREN
                       | ID LPAREN RPAREN'''
    print(f"Llamada a función: {p[1]}")


def p_llamada_metodo(p):
    '''llamada_metodo : variable PUNTO ID LPAREN argumentos RPAREN
                      | variable PUNTO ID LPAREN RPAREN'''
    print("Llamada a método detectado")


def p_argumentos(p):
    '''argumentos : expresion
                  | argumentos COMMA expresion'''


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
    print("While detectado")


def p_sentencia_for(p):
    '''sentencia_for : FOR LPAREN inicializacion SEMICOLON condicion SEMICOLON incremento RPAREN bloque'''
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


# ==================== EXPRESIONES ====================
def p_expresion_binaria_aritmetica(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion MOD expresion'''


def p_expresion_unaria(p):
    '''expresion : MINUS expresion %prec UMINUS
                 | PLUS expresion %prec UPLUS'''


def p_expresion_relacional(p):
    '''expresion : expresion GT expresion
                 | expresion LT expresion
                 | expresion GTE expresion
                 | expresion LTE expresion
                 | expresion EQ expresion
                 | expresion NEQ expresion'''


def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''


def p_expresion_negacion(p):
    '''expresion : NOT expresion'''


def p_expresion_acceso(p):
    '''expresion : expresion PUNTO ID
                 | expresion LBRACKET expresion RBRACKET'''


def p_expresion_llamadas(p):
    '''expresion : llamada_funcion
                 | llamada_metodo'''


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


# ==================== ESTRUCTURAS DE DATOS ====================
def p_array_literal(p):
    '''array_literal : LBRACKET elementos RBRACKET
                     | LBRACKET RBRACKET'''
    print("Array detectado")


def p_elementos(p):
    '''elementos : expresion
                 | elementos COMMA expresion'''


def p_map_set_literal(p):
    '''map_set_literal : NEW ID LPAREN array_de_pares RPAREN
                       | NEW ID LPAREN argumentos RPAREN
                       | NEW ID LPAREN RPAREN'''
    print("Map/Set detectado")


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
    print(f"Función: {p[2]}")


def p_parametros(p):
    '''parametros : parametro
                  | parametros COMMA parametro'''


def p_parametro(p):
    '''parametro : ID
                 | ID COLON tipo
                 | ID COLON tipo_generico
                 | ID COLON tipo_array'''


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


# ==================== MÉTODOS ESPECIALES (para .has, .values, etc.) ====================
def p_expresion_metodos_especiales(p):
    '''expresion : variable PUNTO ID LPAREN RPAREN
                 | variable PUNTO ID LPAREN argumentos RPAREN
                 | variable PUNTO SIZE
                 | variable PUNTO LENGTH'''
    print("Método/Propiedad especial detectado")


# Agregar SIZE y LENGTH como tokens especiales
def p_expresion_propiedades(p):
    '''expresion : variable PUNTO ID'''
    if p[3] in ['size', 'length', 'values', 'has']:
        print(f"Propiedad/método {p[3]} detectado")


# ==================== EXPRESIONES ESPECIALES PARA MAP/SET ====================
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

        # Recuperación de errores mejorada
        parser.errok()
    else:
        mensaje = "Error de sintaxis: final de entrada inesperado"
        print(mensaje)
        errores.append(mensaje)


# ==================== FUNCIÓN PRINCIPAL DE ANÁLISIS ====================
def analizar_sintaxis(codigo: str, usuario: str):
    global errores
    errores = []

    try:
        resultado = parser.parse(codigo, debug=False)
        print("Análisis sintáctico completado")

        # Crear directorio de logs si no existe
        logs_dir = "SyntaxLogs"
        os.makedirs(logs_dir, exist_ok=True)

        # Generar nombre de archivo con timestamp
        fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")
        log_filename = f"sintactico-{usuario}-{fecha_hora}.txt"
        log_path = os.path.join(logs_dir, log_filename)

        # Escribir log
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"=== ANÁLISIS SINTÁCTICO - {usuario} ===\n")
            f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")

            if errores:
                f.write("ERRORES ENCONTRADOS:\n")
                for i, error in enumerate(errores, 1):
                    f.write(f"{i}. {error}\n")
            else:
                f.write("✓ No se encontraron errores sintácticos\n")

            f.write(f"\nTotal de errores: {len(errores)}\n")

        print(f"Log guardado en: {log_path}")
        return log_path, len(errores) == 0

    except Exception as e:
        error_msg = f"Error crítico en el análisis: {str(e)}"
        errores.append(error_msg)
        print(error_msg)
        return None, False


# ==================== FUNCIONES DE PRODUCCION ====================

def p_declaracion(p):
    'declaracion : LET ID EQUALS expresion'
    tipo = p[4]['tipo']
    semantico.declarar_variable(p[2], tipo)

def p_asignacion(p):
    'asignacion : ID EQUALS expresion'
    tipo_valor = p[3]['tipo']
    semantico.verificar_asignacion(p[1], tipo_valor)



# Crear el parser
parser = yacc.yacc(debug=False, write_tables=True)

