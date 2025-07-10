import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import sys
import io
from main import (
    ejecutar_analisis_lexico,
    ejecutar_analisis_sintactico,
    ejecutar_analisis_semantico,
    ejecutar_analisis_completo,
    procesar_algoritmo_predefinido
)

class StdoutRedirector(io.StringIO):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def write(self, text):
        self.callback(text)

    def flush(self):
        pass

class LexTypeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LexType - Analizador TypeScript")
        self.geometry("900x600")
        self.usuario = "usuario_gui"
        self.pantalla_inicio()

    def pantalla_inicio(self):
        for widget in self.winfo_children():
            widget.destroy()

        frame_inicio = tk.Frame(self)
        frame_inicio.pack(expand=True)

        tk.Label(frame_inicio, text="LEXTYPE ANALIZADOR DE TYPESCRIPT :)", font=("Helvetica", 18)).pack(pady=20)

        tk.Button(frame_inicio, text="Analizar algoritmos predefinidos", font=("Arial", 14),
                  command=self.cargar_algoritmo).pack(pady=10)

        tk.Button(frame_inicio, text="Analizar tu propio algoritmo", font=("Arial", 14),
                  command=self.analizar_manual).pack(pady=10)

    def cargar_algoritmo(self):
        self.pantalla_analisis()
        self.mostrar_codigo_predefinido()

    def analizar_manual(self):
        self.pantalla_analisis()

    def pantalla_analisis(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Muestra de Codigo", font=("Arial", 12)).pack()
        self.area_codigo = scrolledtext.ScrolledText(self, height=12, font=("Courier", 11))
        self.area_codigo.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(self, text="Salida de errores y aprobados", font=("Arial", 12)).pack()
        self.area_resultado = scrolledtext.ScrolledText(self, height=10, font=("Courier", 11), bg="#f0f0f0")
        self.area_resultado.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="léxico", width=15, command=self.analizar_lexico).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="sintáctico", width=15, command=self.analizar_sintactico).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="semántico", width=15, command=self.analizar_semantico).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="completo", width=15, command=self.analizar_completo).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="volver", width=15, command=self.pantalla_inicio).pack(side=tk.RIGHT, padx=5)

    def mostrar_codigo_predefinido(self):
        opcion = simpledialog.askinteger("Algoritmo", "Selecciona 1, 2 o 3")
        if opcion not in [1, 2, 3]:
            messagebox.showerror("Error", "Opción inválida")
            return

        codigo, usuario = procesar_algoritmo_predefinido(opcion)
        if codigo:
            self.usuario = usuario
            self.area_codigo.delete(1.0, tk.END)
            self.area_codigo.insert(tk.END, codigo)

    def obtener_codigo(self):
        return self.area_codigo.get("1.0", tk.END).strip()

    def redirigir_salida(self, funcion):
        self.area_resultado.delete(1.0, tk.END)
        original_stdout = sys.stdout
        sys.stdout = StdoutRedirector(lambda x: self.area_resultado.insert(tk.END, x))
        try:
            funcion()
        except Exception as e:
            self.area_resultado.insert(tk.END, f"Error: {e}")
        finally:
            sys.stdout = original_stdout

    def analizar_lexico(self):
        codigo = self.obtener_codigo()
        if codigo:
            self.redirigir_salida(lambda: ejecutar_analisis_lexico(codigo, self.usuario))

    def analizar_sintactico(self):
        codigo = self.obtener_codigo()
        if codigo:
            self.redirigir_salida(lambda: ejecutar_analisis_sintactico(codigo, self.usuario))

    def analizar_semantico(self):
        codigo = self.obtener_codigo()
        if codigo:
            self.redirigir_salida(lambda: ejecutar_analisis_semantico(codigo, self.usuario))

    def analizar_completo(self):
        codigo = self.obtener_codigo()
        if codigo:
            self.redirigir_salida(lambda: ejecutar_analisis_completo(codigo, self.usuario))


if __name__ == "__main__":
    app = LexTypeGUI()
    app.mainloop()
