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



def p_programa(p):
    '''programa : cuerpo'''
    pass

# Cuerpo del programa (una o más sentencias)
def p_cuerpo(p):
    '''cuerpo : sentencia
              | sentencia cuerpo'''
    pass
# function prueba() {
#   let x = 5;          }
def p_funcion(p):
    '''funcion : FUNCTION ID LPAREN RPAREN LBRACE RBRACE
                | FUNCTION ID LPAREN RPAREN LBRACE body RBRACE'''
    print(f"Función: {p[2]}")


# let x = 5;
def p_body(p):
    '''body : sentence
            | sentence body'''
    


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
    pass
    

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



# FUNCION
parser = yacc.yacc()