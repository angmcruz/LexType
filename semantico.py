# ==================== ANÁLISIS SEMÁNTICO ====================
from datetime import datetime 
import os

# Variables globales
tabla_simbolos = {}
errores_semanticos = []

class ErrorSemantico(Exception):
    pass

def reiniciar_tabla():
    """Reinicia la tabla de símbolos y errores"""
    global tabla_simbolos, errores_semanticos
    tabla_simbolos = {}
    errores_semanticos = []
    print("Tabla de símbolos y errores reiniciados")

def declarar_variable(nombre, tipo):
    """Declara una variable en la tabla de símbolos"""
    if nombre in tabla_simbolos:
        registrar_error(f"La variable '{nombre}' ya fue declarada.")
        return False
    tabla_simbolos[nombre] = tipo
    print(f"✅ Variable declarada: {nombre} : {tipo}")
    return True

def usar_variable(nombre):
    """Verifica que una variable existe antes de usarla"""
    if nombre not in tabla_simbolos:
        registrar_error(f"La variable '{nombre}' no ha sido declarada.")
        return "unknown"
    return tabla_simbolos[nombre]

def verificar_asignacion(nombre, tipo_valor):
    """Verifica que la asignación sea compatible con el tipo declarado"""
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
    print(f"🔍 Verificando operación: {tipo1} {operador} {tipo2}")
    
    # Operaciones aritméticas
    if operador in ['+', '-', '*', '/', '%']:
        if tipo1 == "number" and tipo2 == "number":
            return "number"
        elif tipo1 == "string" and tipo2 == "string" and operador == '+':
            return "string"
        else:
            registrar_error(f"Operación aritmética '{operador}' inválida entre '{tipo1}' y '{tipo2}'")
            return None
    
    # Operaciones de comparación
    elif operador in ['<', '>', '<=', '>=', '==', '!=']:
        if tipo1 == tipo2 or (tipo1 == "unknown" or tipo2 == "unknown"):
            return "boolean"
        else:
            registrar_error(f"Comparación entre tipos incompatibles: '{tipo1}' y '{tipo2}'")
            return "boolean"  # Devolvemos boolean aunque haya error

    # Operaciones lógicas
    elif operador in ['&&', '||', 'AND', 'OR']:
        if tipo1 == "boolean" and tipo2 == "boolean":
            return "boolean"
        else:
            registrar_error(f"Operador lógico '{operador}' requiere operandos booleanos, recibió '{tipo1}' y '{tipo2}'")
            return "boolean"
    
    else:
        registrar_error(f"Operador desconocido: '{operador}'")
        return None

def verificar_funcion_existe(nombre_funcion):
    """Verifica si una función ha sido declarada"""
    # Lista de funciones built-in
    funciones_builtin = ["console", "prompt", "Math"]
    
    if nombre_funcion in funciones_builtin:
        return True
    
    # Aquí podrías verificar en una tabla de funciones declaradas
    return False

def verificar_metodo_objeto(tipo_objeto, metodo):
    """Verifica si un método existe para un tipo de objeto"""
    metodos_validos = {
        "string": ["length", "substring", "toUpperCase", "toLowerCase", "toString"],
        "array": ["push", "pop", "length"],
        "Map": ["set", "get", "has", "size", "values"],
        "Set": ["add", "has", "size", "delete"]
    }
    
    # Extraer tipo base
    tipo_base = tipo_objeto
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
    
    return nombre_archivo

def mostrar_resumen():
    """Muestra un resumen del análisis semántico"""
    print("\n" + "=" * 50)
    print("RESUMEN DEL ANÁLISIS SEMÁNTICO")
    print("=" * 50)
    print(f"Variables declaradas: {len(tabla_simbolos)}")
    print(f"Errores encontrados: {len(errores_semanticos)}")
    
    if tabla_simbolos:
        print("\nVariables en tabla de símbolos:")
        for nombre, tipo in tabla_simbolos.items():
            print(f"   • {nombre} : {tipo}")
    
    if errores_semanticos:
        print(f"\n❌ Errores semánticos ({len(errores_semanticos)}):")
        for i, error in enumerate(errores_semanticos, 1):
            print(f"   {i}. {error}")
    else:
        print("\n✅ No se encontraron errores semánticos")
    
    print("=" * 50)