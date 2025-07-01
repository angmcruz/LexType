from lexico import analizar_codigo
from sintactico import parser, errores, reiniciar_analisis
from lexico import lexer
import semantico
import datetime
import os


def mostrar_menu():
    """Muestra el menú principal de opciones"""
    print("\n" + "=" * 60)
    print("       ANALIZADOR LÉXICO Y SINTÁCTICO TYPESCRIPT")
    print("=" * 60)
    print("1. Analizar algoritmos predefinidos")
    print("2. Ingresar código personalizado por consola")
    print("3. Salir")
    print("-" * 60)


def mostrar_menu_algoritmos():
    """Muestra el menú de algoritmos predefinidos"""
    print("\n" + "=" * 50)
    print("        ALGORITMOS PREDEFINIDOS")
    print("=" * 50)
    print("1. Algoritmo 1 (Erick)")
    print("2. Algoritmo 2 (Melissa)")
    print("3. Algoritmo 3 (Javier)")
    print("4. Volver al menú principal")
    print("-" * 50)


def mostrar_menu_analisis():
    """Muestra el menú de tipo de análisis"""
    print("\n" + "=" * 40)
    print("     TIPO DE ANÁLISIS")
    print("=" * 40)
    print("1. Solo análisis léxico")
    print("2. Solo análisis sintáctico")
    print("3. Solo análisis semántico")
    print("4. Análisis completo (léxico + sintáctico + semántico)")
    print("5. Volver")
    print("-" * 40)


def leer_codigo_personalizado():
    """Lee código TypeScript ingresado por el usuario"""
    print("\n" + "=" * 60)
    print("         INGRESO DE CÓDIGO PERSONALIZADO")
    print("=" * 60)
    print("Ingresa tu código TypeScript línea por línea.")
    print("Para terminar, escribe 'FIN' en una línea separada.")
    print("Para cancelar, escribe 'CANCELAR'.")
    print("-" * 60)

    lineas = []
    numero_linea = 1

    while True:
        try:
            linea = input(f"{numero_linea:2d}| ")

            if linea.strip().upper() == 'FIN':
                break
            elif linea.strip().upper() == 'CANCELAR':
                return None

            lineas.append(linea)
            numero_linea += 1

        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            return None

    if not lineas:
        print("No se ingresó ningún código.")
        return None

    codigo = '\n'.join(lineas)

    print("\n" + "=" * 60)
    print("         CÓDIGO INGRESADO:")
    print("=" * 60)
    for i, linea in enumerate(lineas, 1):
        print(f"{i:2d}| {linea}")
    print("=" * 60)

    return codigo


def ejecutar_analisis_lexico(codigo, usuario):
    """Ejecuta el análisis léxico"""
    print(f"\n🔍 Ejecutando análisis léxico para {usuario}...")
    try:
        log_path = analizar_codigo(codigo, usuario)
        if log_path:
            print(f"✅ Análisis léxico completado. Log guardado en: {log_path}")
        else:
            print("❌ Error en el análisis léxico.")
    except Exception as e:
        print(f"❌ Error crítico en análisis léxico: {str(e)}")


def ejecutar_analisis_sintactico(codigo, usuario):
    """Ejecuta el análisis sintáctico"""
    print(f"\n🔍 Ejecutando análisis sintáctico para {usuario}...")
    try:
        # Limpiar errores previos
        global errores
        errores.clear()
        
        # Reiniciar análisis
        reiniciar_analisis()

        # Ejecutar parser
        resultado = parser.parse(codigo, lexer)

        # Crear directorio de logs si no existe
        logs_dir = "SintaxLogs"
        os.makedirs(logs_dir, exist_ok=True)

        # Generar nombre de archivo con timestamp
        fecha_hora = datetime.datetime.now().strftime("%d%m%Y-%Hh%M")
        nombre_archivo = f"SintaxLogs/sintactico-{usuario}-{fecha_hora}.txt"

        # Escribir log
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(f"=== ANÁLISIS SINTÁCTICO - {usuario} ===\n")
            f.write(f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")

            if errores:
                f.write("ERRORES SINTÁCTICOS ENCONTRADOS:\n")
                f.write("-" * 32 + "\n")
                for i, error in enumerate(errores, 1):
                    f.write(f"{i}. {error}\n")
                print(f"❌ Se encontraron {len(errores)} errores sintácticos.")
            else:
                f.write("✅ No se encontraron errores sintácticos\n")
                print("✅ Código sintácticamente correcto.")

            f.write(f"\nTotal de errores sintácticos: {len(errores)}\n")

        print(f"Log sintáctico guardado en: {nombre_archivo}")

    except Exception as e:
        print(f"❌ Error crítico en análisis sintáctico: {str(e)}")


def ejecutar_analisis_semantico(codigo, usuario):
    """Ejecuta el análisis semántico"""
    print(f"\nEjecutando análisis semántico para {usuario}...")
    try:
        # Reiniciar análisis semántico
        semantico.reiniciar_tabla()
        
        # Ejecutar parser (que incluye las reglas semánticas)
        resultado = parser.parse(codigo, lexer)
        
        # Mostrar resumen
        semantico.mostrar_resumen()
        
        # Guardar log
        log_path = semantico.guardar_log(usuario)
        
        if semantico.tiene_errores():
            print(f"❌ Se encontraron {len(semantico.obtener_errores())} errores semánticos.")
        else:
            print("✅ Código semánticamente correcto.")
            
        return log_path

    except Exception as e:
        print(f"❌ Error crítico en análisis semántico: {str(e)}")
        return None


def ejecutar_analisis_completo(codigo, usuario):
    """Ejecuta análisis léxico, sintáctico y semántico"""
    print(f"\nEjecutando análisis completo para {usuario}...")
    print("=" * 60)
    
    # Análisis léxico
    ejecutar_analisis_lexico(codigo, usuario)
    
    # Análisis sintáctico y semántico (se hacen juntos)
    ejecutar_analisis_sintactico(codigo, usuario)
    ejecutar_analisis_semantico(codigo, usuario)
    
    print("\n✅ Análisis completo terminado.")
    print("=" * 60)


def procesar_algoritmo_predefinido(opcion_algoritmo):
    """Procesa un algoritmo predefinido según la opción seleccionada"""
    algoritmos = {
        1: ("algoritmo1.ts", "Erick"),
        2: ("algoritmo2.ts", "Melissa"),
        3: ("algoritmo3.ts", "Javier")
    }

    if opcion_algoritmo not in algoritmos:
        print("Opción inválida.")
        return

    ruta, usuario = algoritmos[opcion_algoritmo]

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            codigo = f.read()

        print(f"\nCargando {ruta} (Usuario: {usuario})")
        print("Contenido del archivo:")
        print("-" * 50)
        for i, linea in enumerate(codigo.split('\n'), 1):
            print(f"{i:2d}| {linea}")
        print("-" * 50)

        return codigo, usuario

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta}")
        return None, None
    except Exception as e:
        print(f"Error al leer el archivo {ruta}: {str(e)}")
        return None, None


def main():
    """Función principal con menú interactivo"""
    
    while True:
        mostrar_menu()

        try:
            opcion = input("Selecciona una opción (1-3): ").strip()

            if opcion == '1':
                # Analizar algoritmos predefinidos
                while True:
                    mostrar_menu_algoritmos()
                    sub_opcion = input("Selecciona un algoritmo (1-4): ").strip()

                    if sub_opcion == '4':
                        break

                    if sub_opcion in ['1', '2', '3']:
                        codigo, usuario = procesar_algoritmo_predefinido(int(sub_opcion))

                        if codigo and usuario:
                            # Menú de tipo de análisis
                            while True:
                                mostrar_menu_analisis()
                                tipo_analisis = input("Selecciona el tipo de análisis (1-5): ").strip()

                                if tipo_analisis == '5':
                                    break
                                elif tipo_analisis == '1':
                                    ejecutar_analisis_lexico(codigo, usuario)
                                elif tipo_analisis == '2':
                                    ejecutar_analisis_sintactico(codigo, usuario)
                                elif tipo_analisis == '3':
                                    ejecutar_analisis_semantico(codigo, usuario)
                                elif tipo_analisis == '4':
                                    ejecutar_analisis_completo(codigo, usuario)
                                else:
                                    print("Opción inválida. Intenta de nuevo.")
                        break
                    else:
                        print("Opción inválida. Intenta de nuevo.")

            elif opcion == '2':
                # Ingresar código personalizado
                codigo = leer_codigo_personalizado()

                if codigo:
                    usuario = input("\nIngresa tu nombre de usuario: ").strip()
                    if not usuario:
                        usuario = "usuario_personalizado"

                    # Menú de tipo de análisis para código personalizado
                    while True:
                        mostrar_menu_analisis()
                        tipo_analisis = input("Selecciona el tipo de análisis (1-5): ").strip()

                        if tipo_analisis == '5':
                            break
                        elif tipo_analisis == '1':
                            ejecutar_analisis_lexico(codigo, usuario)
                        elif tipo_analisis == '2':
                            ejecutar_analisis_sintactico(codigo, usuario)
                        elif tipo_analisis == '3':
                            ejecutar_analisis_semantico(codigo, usuario)
                        elif tipo_analisis == '4':
                            ejecutar_analisis_completo(codigo, usuario)
                        else:
                            print("Opción inválida. Intenta de nuevo.")
                        break

            elif opcion == '3':
                print("\n¡Gracias por usar el analizador! Hasta luego.")
                break

            else:
                print("Opción inválida. Por favor, selecciona 1, 2 o 3.")

        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario. ¡Adiós!")
            break
        except Exception as e:
            print(f"Error inesperado: {str(e)}")


if __name__ == "__main__":
    print("Iniciando Analizador Léxico, Sintáctico y Semántico TypeScript...")
    main()