from lexico import analizar_codigo

ruta1 = "algoritmo1.ts"
ruta2 = "algoritmo2.ts"
ruta3 = "algoritmo3.ts"


with open(ruta1, "r", encoding="utf-8") as f:
    codigo1 = f.read()

with open(ruta2, "r", encoding="utf-8") as f:
    codigo2 = f.read()

with open(ruta3, "r", encoding="utf-8") as f:
    codigo3 = f.read()

analizar_codigo(codigo1, "Erick")
analizar_codigo(codigo2, "Melissa")
analizar_codigo(codigo3, "Josue")


