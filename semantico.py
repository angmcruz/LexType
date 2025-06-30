
# ==================== VERIFICACION DE OPERACIONES ====================

tabla_simbolos = {}

class ErrorSemantico(Exception):
    pass

def reiniciar_tabla():
    global tabla_simbolos
    tabla_simbolos = {}

def declarar_variable(nombre, tipo):
    if nombre in tabla_simbolos:
        raise ErrorSemantico(f"[Error] La variable '{nombre}' ya fue declarada.")
    tabla_simbolos[nombre] = tipo

def usar_variable(nombre):
    if nombre not in tabla_simbolos:
        raise ErrorSemantico(f"[Error] La variable '{nombre}' no ha sido declarada.")
    return tabla_simbolos[nombre]

def verificar_asignacion(nombre, tipo_valor):
    tipo_var = usar_variable(nombre)
    if tipo_var != tipo_valor:
        raise ErrorSemantico(f"[Error] Tipo incompatible en asignación a '{nombre}': se esperaba '{tipo_var}' pero se dio '{tipo_valor}'.")

def verificar_operacion(tipo1, operador, tipo2):
    if operador in ['+', '-', '*', '/']:
        if tipo1 == tipo2 == 'int':
            return 'int'
        elif tipo1 == tipo2 == 'float':
            return 'float'
        elif tipo1 == tipo2 == 'string' and operador == '+':
            return 'string'
        else:
            raise ErrorSemantico(f"[Error] Operación inválida: '{tipo1} {operador} {tipo2}'")
    
    elif operador in ['<', '>', '<=', '>=', '==', '!=']:
        if tipo1 == tipo2:
            return 'bool'
        else:
            raise ErrorSemantico(f"[Error] Comparación entre tipos incompatibles: '{tipo1}' y '{tipo2}'")

    elif operador in ['&&', '||']:
        if tipo1 == tipo2 == 'bool':
            return 'bool'
        else:
            raise ErrorSemantico(f"[Error] Operador lógico requiere booleanos, no '{tipo1}' y '{tipo2}'")
    
    else:
        raise ErrorSemantico(f"[Error] Operador desconocido: '{operador}'")
