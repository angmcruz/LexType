from tokens import lexer, errores
from datetime import datetime
import os


def analizar_codigo(algoritmo: str, usuario: str):
    lexer.input(algoritmo)
    resultados = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        resultados.append(f"Línea {tok.lineno}: Reconozco el símbolo '{tok.value}' como {tok.type}")
    
    for err in errores:
        resultados.append(err)

    logs_dir = "LexLogs"
    os.makedirs(logs_dir, exist_ok=True)


    fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    log_filename = f"lexico-{usuario}-{fecha_hora}.txt"
    log_path = os.path.join(logs_dir, log_filename)

    with open(log_path, "w", encoding="utf-8") as f:
        for linea in resultados:
            f.write(linea + "\n")

    return log_path

