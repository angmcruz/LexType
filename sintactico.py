# REQUERIMIENTOS
# PRINTL
#INPUT
#PLUS MINUS TIMES DIVIDE MOD 
# LET EQUALS
# ARRAY LSBRACKET LBRACKET
#IF ELSE WHILE FOR IN
#FUNCTION

import ply.yacc as yacc
from tokens import tokens
errores = []


def p_programa(p):
    '''programa : cuerpo'''
    

# Cuerpo del programa (una o más sentencias)
def p_cuerpo(p):
    '''cuerpo : sentencia
              | sentencia cuerpo'''
    
# function prueba() {
#   let x = 5;          }
def p_funcion(p):
    '''funcion : FUNCTION ID LPAREN RPAREN LBRACE RBRACE
                | FUNCTION ID LPAREN RPAREN LBRACE body RBRACE'''
    print(f"Función: {p[2]}")


# let x = 5;
def p_body(p):
    '''body : sentencia
            | sentencia body'''
    
def p_sentencia(p):
    '''sentencia : asignacion
                 | declaracion
                 | impresion
                 | input_teclado
                 | sentencia_while
                 | sentencia_for
                 | sentencia_for_in
                 | funcion
                 | clase'''
   

# variable
def p_asignacion(p):
    '''asignacion : LET ID ASSIGN expresion SEMICOLON'''

def p_declaracion(p):
    '''declaracion : CONST ID ASSIGN expresion SEMICOLON'''
    print(f"Declaración constante: {p[2]}")

# console.log('fgh');
def p_impresion(p):
    '''impresion : ID PUNTO ID LPAREN STRING RPAREN SEMICOLON'''

# x teclado let x = prompt('fs');
def p_input_teclado(p):
    '''input_teclado : LET ID ASSIGN ID LPAREN STRING RPAREN SEMICOLON'''


# array
def p_elementos(p):
    '''elementos : elementos COMMA expresion
                 | expresion'''


# while (x < 5) { ... }
def p_sentencia_while(p):
    '''sentencia_while : WHILE LPAREN expresion RPAREN bloque'''
    print("While detectado")

def p_bloque(p):
    '''bloque : LBRACE cuerpo RBRACE'''
    pass


def p_expresion(p):
    '''expresion : NUMBER
                 | STRING
                 | ID
                 | LBRACKET elementos RBRACKET
                 | LPAREN expresion RPAREN'''
    p[0] = p[1]

# for for (let i = 0; i < 10; i++) {// cuerpo del for}
def p_sentencia_for(p):
    '''sentencia_for : FOR LPAREN inicializacion PUNTOCOMA condicion PUNTOCOMA incremento RPAREN bloque'''
    print("For detectado")

def p_inicializacion(p):
    '''inicializacion : LET ID ASSIGN expresion
                      | asignacion'''
    # No requiere acción especial aquí, se procesa como una asignación

def p_condicion(p):
    '''condicion : expresion'''
    pass

def p_incremento(p):
    '''incremento : ID PLUSPLUS
                  | ID MINUSMINUS
                  | ID ASSIGN expresion'''
    pass

#for_in for (let item in collection) { // código}
def p_sentencia_for_in(p):
    '''sentencia_for_in : FOR LPAREN LET ID IN ID RPAREN bloque'''
    print(f"For...in detectado: iterando {p[4]} en {p[6]}")

#clase 
def p_clase(p):
    '''clase : CLASS ID LBRACE cuerpo_clase RBRACE'''
    print(f"Clase definida: {p[2]}")

def p_cuerpo_clase(p):
    '''cuerpo_clase : cuerpo_clase elemento_clase
                    | elemento_clase'''
    

def p_elemento_clase(p):
    '''elemento_clase : funcion
                      | asignacion
                      | declaracion'''

def p_error(p):
    if p:
        mensaje = f"Error de sintaxis en '{p.value}' (línea {p.lineno})"
    else:
        mensaje = "Error de sintaxis al final del archivo"

    print(mensaje)
    errores.append(mensaje)

#operadores logicos 

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    p[0] = f"({p[1]} {p[2]} {p[3]})"

def p_expresion_negacion(p):
    '''expresion : NOT expresion'''
    p[0] = f"(!{p[2]})"

def p_expresion_relacional(p):
    '''expresion : expresion GT expresion
                 | expresion LT expresion
                 | expresion GTE expresion
                 | expresion LTE expresion
                 | expresion EQ expresion
                 | expresion NEQ expresion'''
    p[0] = f"({p[1]} {p[2]} {p[3]})"


# FUNCION
parser = yacc.yacc()