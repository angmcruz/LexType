from lexico import analizar_codigo
from sintactico import parser, errores
from lexico import lexer
import datetime
import os



ruta1 = "algoritmo1.ts"
ruta2 = "algoritmo2.ts"
ruta3 = "algoritmo3.ts"

with open("prueba.ts", "r", encoding="utf-8") as f:
    codigo = f.read()

with open(ruta1, "r", encoding="utf-8") as f:
    codigo1 = f.read()

with open(ruta2, "r", encoding="utf-8") as f:
    codigo2 = f.read()

with open(ruta3, "r", encoding="utf-8") as f:
    codigo3 = f.read()

#PARA LEXICO 

#analizar_codigo(codigo1, "Erick")
#analizar_codigo(codigo2, "Melissa")
#analizar_codigo(codigo3, "Josue")


#SINTACTICO
parser.parse(codigo, lexer)


# LOGS DE SINTACTICO
os.makedirs("SintaxLogs", exist_ok=True)
fecha_hora = datetime.datetime.now().strftime("%d%m%Y-%Hh%M")
usuario = "user"  
nombre_archivo = f"logs/sintactico-{usuario}-{fecha_hora}.txt"

if errores:
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        for error in errores:
            f.write(error + "\n")
    print(f"Log guardado en: {nombre_archivo}")
else:
    print("No se imprimio log de errores sintacticos.")