from datetime import datetime 
import ply.yacc as yacc
import os

# Variables globales
tabla_simbolos = {}
tabla_funciones = {} 
errores_semanticos = []

activar = True 
# uso de bandera porque el parser tiene reglas semanticas

class ErrorSemantico(Exception):
    pass

def reiniciar_tabla():
    """Reinicia la tabla de símbolos y errores"""
    global tabla_simbolos, tabla_funciones, errores_semanticos
    tabla_simbolos = {}
    tabla_funciones = {}
    errores_semanticos = []
    print("Tabla de símbolos y errores reiniciados")

def declarar_variable(nombre, tipo):
    """Declara una variable en la tabla de símbolos"""
    if not activar:
        return True
    if nombre in tabla_simbolos:
        registrar_error(f"La variable '{nombre}' ya fue declarada.")
        return False
    tabla_simbolos[nombre] = tipo
    print(f"✅ Variable declarada: {nombre} : {tipo}")
    return True

def declarar_funcion(nombre, parametros=None, tipo_retorno="void"):
    """Declara una función en la tabla de funciones"""
    if not activar:
        return True
    
    if parametros is None:
        parametros = []
    
    tabla_funciones[nombre] = {
        "parametros": parametros,
        "retorno": tipo_retorno
    }
    print(f"✅ Función declarada: {nombre}({len(parametros)} parámetros) -> {tipo_retorno}")
    return True

def usar_variable(nombre):
    """Verifica que una variable existe antes de usarla"""
    if not activar:
        return True
    if nombre not in tabla_simbolos:
        registrar_error(f"La variable '{nombre}' no ha sido declarada.")
        return "unknown"
    return tabla_simbolos[nombre]

def usar_funcion(nombre):
    """Verifica que una función existe antes de usarla"""
    if not activar:
        return True
    
    # Funciones built-in permitidas
    funciones_builtin = ["console", "prompt", "Math", "parseInt", "parseFloat", "toString"]
    
    if nombre in funciones_builtin:
        return "void"
    
    if nombre in tabla_funciones:
        return tabla_funciones[nombre]["retorno"]
    
    registrar_error(f"La función '{nombre}' no ha sido declarada.")
    return "unknown"

def verificar_asignacion(nombre, tipo_valor):
    """Verifica que la asignación sea compatible con el tipo declarado"""
    if not activar:
        return True
    if nombre not in tabla_simbolos:
        registrar_error(f"La variable '{nombre}' no ha sido declarada.")
        return False
    
    tipo_var = tabla_simbolos[nombre]
    if tipo_var != tipo_valor and tipo_valor != "unknown":
        registrar_error(f"Tipo incompatible en asignación a '{nombre}': se esperaba '{tipo_var}' pero se asignó '{tipo_valor}'.")
        return False
    return True

def verificar_operacion(tipo1, operador, tipo2):
    """Verifica que una operación sea válida entre dos tipos"""
    print(f"Verificando operación: {tipo1} {operador} {tipo2}")
    if not activar:
        return True
    
    # Manejar tipos unknown
    if tipo1 == "unknown" or tipo2 == "unknown":
        if operador in ['+', '-', '*', '/', '%']:
            return "number"
        elif operador in ['<', '>', '<=', '>=', '==', '!=', '!==', '===']:
            return "boolean"
        elif operador in ['&&', '||', 'AND', 'OR']:
            return "boolean"
        else:
            return "unknown"
    
    # Operaciones aritméticas
    if operador in ['+', '-', '*', '/', '%']:
        if tipo1 == "number" and tipo2 == "number":
            return "number"
        elif tipo1 == "string" and tipo2 == "string" and operador == '+':
            return "string"
        else:
            registrar_error(f"Operación aritmética '{operador}' inválida entre '{tipo1}' y '{tipo2}'")
            return "number"  # Asumimos number para continuar el análisis
    
    # Operaciones de comparación
    elif operador in ['<', '>', '<=', '>=', '==', '!=', '!==', '===']:
        return "boolean"  # Las comparaciones siempre devuelven boolean

    # Operaciones lógicas
    elif operador in ['&&', '||', 'AND', 'OR']:
        if tipo1 == "boolean" and tipo2 == "boolean":
            return "boolean"
        else:
            registrar_error(f"Operador lógico '{operador}' requiere operandos booleanos, recibió '{tipo1}' y '{tipo2}'")
            return "boolean"
    
    else:
        registrar_error(f"Operador desconocido: '{operador}'")
        return "unknown"

def verificar_funcion_existe(nombre_funcion):
    """Verifica si una función ha sido declarada"""
    if not activar:
        return True
    
    # Lista de funciones built-in
    funciones_builtin = ["console", "prompt", "Math", "parseInt", "parseFloat"]
    
    if nombre_funcion in funciones_builtin:
        return True
    
    if nombre_funcion in tabla_funciones:
        return True
    
    return False

def verificar_metodo_objeto(tipo_objeto, metodo):
    """Verifica si un método existe para un tipo de objeto"""
    if not activar:
        return True
    metodos_validos = {
        "string": ["length", "substring", "toUpperCase", "toLowerCase", "toString"],
        "array": ["push", "pop", "length"],
        "Map": ["set", "get", "has", "size", "values"],
        "Set": ["add", "has", "size", "delete"]
    }
    
    # Extraer tipo base
    tipo_base = tipo_objeto
    if isinstance(tipo_objeto, str):
        if tipo_objeto.endswith("[]"):
            tipo_base = "array"
        elif "Map" in tipo_objeto:
            tipo_base = "Map"
        elif "Set" in tipo_objeto:
            tipo_base = "Set"
    
    if tipo_base in metodos_validos:
        if metodo not in metodos_validos[tipo_base]:
            registrar_error(f"El método '{metodo}' no existe para el tipo '{tipo_objeto}'")
            return False
    
    return True

def registrar_error(mensaje):
    """Registra un error semántico"""
    error_completo = f"[ERROR SEMÁNTICO] {mensaje}"
    errores_semanticos.append(error_completo)
    print(f"❌ {error_completo}")

def obtener_errores():
    """Devuelve la lista de errores semánticos"""
    return errores_semanticos

def tiene_errores():
    """Verifica si hay errores semánticos"""
    return len(errores_semanticos) > 0

def guardar_log(usuario):
    """Guarda los errores semánticos en un archivo log"""
    # Crear directorio si no existe
    if not os.path.exists("SemLogs"):
        os.makedirs("SemLogs")
    
    fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")
    nombre_archivo = f"SemLogs/semantico-{usuario}-{fecha_hora}.txt"
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"=== ANÁLISIS SEMÁNTICO - {usuario} ===\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        if errores_semanticos:
            f.write("ERRORES SEMÁNTICOS ENCONTRADOS:\n")
            f.write("-" * 35 + "\n")
            for i, error in enumerate(errores_semanticos, 1):
                f.write(f"{i}. {error}\n")
        else:
            f.write("✅ No se encontraron errores semánticos\n")
        
        f.write(f"\nTotal de errores semánticos: {len(errores_semanticos)}\n")
        
        # Agregar tabla de símbolos
        f.write("\n" + "=" * 50 + "\n")
        f.write("TABLA DE SÍMBOLOS:\n")
        f.write("-" * 20 + "\n")
        if tabla_simbolos:
            for nombre, tipo in tabla_simbolos.items():
                f.write(f"{nombre} : {tipo}\n")
        else:
            f.write("(Vacía)\n")
        
        # Agregar tabla de funciones
        f.write("\n" + "=" * 50 + "\n")
        f.write("TABLA DE FUNCIONES:\n")
        f.write("-" * 20 + "\n")
        if tabla_funciones:
            for nombre, info in tabla_funciones.items():
                f.write(f"{nombre}({len(info['parametros'])} parámetros) -> {info['retorno']}\n")
        else:
            f.write("(Vacía)\n")
    
    return nombre_archivo

def mostrar_resumen():
    """Muestra un resumen del análisis semántico"""
    print("\n" + "=" * 50)
    print("RESUMEN DEL ANÁLISIS SEMÁNTICO")
    print("=" * 50)
    print(f"Variables declaradas: {len(tabla_simbolos)}")
    print(f"Funciones declaradas: {len(tabla_funciones)}")
    print(f"Errores encontrados: {len(errores_semanticos)}")
    
    if tabla_simbolos:
        print("\nVariables en tabla de símbolos:")
        for nombre, tipo in tabla_simbolos.items():
            print(f"   • {nombre} : {tipo}")
    
    if tabla_funciones:
        print("\nFunciones en tabla de símbolos:")
        for nombre, info in tabla_funciones.items():
            print(f"   • {nombre}({len(info['parametros'])} parámetros) -> {info['retorno']}")
    
    if errores_semanticos:
        print(f"\n❌ Errores semánticos ({len(errores_semanticos)}):")
        for i, error in enumerate(errores_semanticos, 1):
            print(f"   {i}. {error}")
    else:
        print("\n✅ No se encontraron errores semánticos")
    
    print("=" * 50)

# Análisis en dos pasadas
def analizar_en_dos_pasadas(codigo_ast):
    """Realiza análisis semántico en dos pasadas"""
    print("Iniciando análisis en dos pasadas...")
    
    # PRIMERA PASADA: Recolectar declaraciones de funciones
    print("Primera pasada: Recolectando declaraciones...")
    # Esta función sería llamada por el parser
    
    # SEGUNDA PASADA: Verificar uso de funciones y variables
    print("Segunda pasada: Verificando uso...")
    # Esta función sería llamada por el parser
