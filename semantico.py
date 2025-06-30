
# ==================== VERIFICACION DE OPERACIONES ====================
from datetime import datetime 
import os

tabla_simbolos = {}

errores_semanticos = []

class ErrorSemantico(Exception):
    pass

def reiniciar_tabla():
    global tabla_simbolos
    tabla_simbolos = {}

def declarar_variable(nombre, tipo):
    if nombre in tabla_simbolos:
        registrar_error(f"[Error] La variable '{nombre}' ya fue declarada.")
    tabla_simbolos[nombre] = tipo

def usar_variable(nombre):
    if nombre not in tabla_simbolos:
        registrar_error(f"[Error] La variable '{nombre}' no ha sido declarada.")
    return tabla_simbolos[nombre]

def verificar_asignacion(nombre, tipo_valor):
    tipo_var = usar_variable(nombre)
    if tipo_var != tipo_valor:
        registrar_error(f"[Error] Tipo incompatible en asignación a '{nombre}': se esperaba '{tipo_var}' pero se dio '{tipo_valor}'.")

def verificar_operacion(tipo1, operador, tipo2):
    if operador in ['+', '-', '*', '/']:
        if tipo1 == tipo2 == 'int':
            return 'int'
        elif tipo1 == tipo2 == 'float':
            return 'float'
        elif tipo1 == tipo2 == 'string' and operador == '+':
            return 'string'
        else:
            registrar_error(f"[Error] Operación inválida: '{tipo1} {operador} {tipo2}'")
    
    elif operador in ['<', '>', '<=', '>=', '==', '!=']:
        if tipo1 == tipo2:
            return 'bool'
        else:
            registrar_error(f"[Error] Comparación entre tipos incompatibles: '{tipo1}' y '{tipo2}'")

    elif operador in ['&&', '||']:
        if tipo1 == tipo2 == 'bool':
            return 'bool'
        else:
            registrar_error(f"[Error] Operador lógico requiere booleanos, no '{tipo1}' y '{tipo2}'")
    
    else:
        registrar_error(f"[Error] Operador desconocido: '{operador}'")


def registrar_error(mensaje):
    errores_semanticos.append("[Error Semántico] " + mensaje)

def guardar_log(usuario):
    if not errores_semanticos:
        return
    if not os.path.exists("SemLogs"):
        os.makedirs("SemLogs")
    fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")
    nombre_archivo = f"SemLogs/semantico-{usuario}-{fecha_hora}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        for e in errores_semanticos:
            f.write(e + "\n")
    print(f"Log guardado en: {nombre_archivo}")
