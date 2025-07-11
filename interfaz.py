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
        self.usuario = "user"
        self.pantalla_inicio()

    def pantalla_inicio(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.configure(bg="#f0f4f8") 

        frame_inicio = tk.Frame(self, bg="#f0f4f8")
        frame_inicio.pack(expand=True)

        tk.Label(
        frame_inicio,
        text="LEXTYPE ANALIZADOR DE TYPESCRIPT 🙂",
        font=("Helvetica", 20, "bold"),
        bg="#f0f4f8",
        fg="#333"
            ).pack(pady=20)

        estilo_btn = {
        "font": ("Arial", 14),
        "bg": "#4a90e2",
        "fg": "white",
        "activebackground": "#357ABD",
        "activeforeground": "white",
        "width": 30,
        "bd": 0,
        "relief": tk.FLAT,
        "cursor": "hand2"
            }

        btn1 = tk.Button(frame_inicio, text="📁 Analizar algoritmos predefinidos",
                     command=self.cargar_algoritmo, **estilo_btn)
        btn1.pack(pady=10)

        btn2 = tk.Button(frame_inicio, text="✏️ Analizar tu propio algoritmo",
                     command=self.analizar_manual, **estilo_btn)
        btn2.pack(pady=10)

  
    def cargar_algoritmo(self):
        self.pantalla_analisis()
        self.mostrar_codigo_predefinido()

    def analizar_manual(self):
        self.pantalla_analisis()

    def pantalla_analisis(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.configure(bg="#f0f4f8")
        tk.Label(self, text="📄 Muestra de Código", font=("Arial", 14, "bold"), bg="#f0f4f8", fg="#333").pack(pady=(10, 0))
        self.area_codigo = scrolledtext.ScrolledText(
        self,
        height=12,
        font=("Courier", 11),
        bg="white",
        fg="#111",
        relief=tk.FLAT,
        bd=4,
        highlightbackground="#c4d7f2",
        highlightcolor="#4a90e2",
        highlightthickness=1,
        insertbackground="#000"
            )
        self.area_codigo.pack(padx=20, pady=5, fill=tk.BOTH, expand=False)

   
        tk.Label(self, text="✅ Salida de errores y aprobados", font=("Arial", 14, "bold"), bg="#f0f4f8", fg="#333").pack(pady=(15, 0))
        self.area_resultado = scrolledtext.ScrolledText(
        self,
        height=10,
        font=("Courier", 11),
        bg="#f7f7f7",
        fg="#111",
        relief=tk.FLAT,
        bd=4,
        highlightbackground="#d6e3f3",
        highlightcolor="#4a90e2",
        highlightthickness=1
        )
        self.area_resultado.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        frame_botones = tk.Frame(self, bg="#f0f4f8")
        frame_botones.pack(pady=15)

        estilo_btn = {
        "font": ("Arial", 11),
        "bg": "#4a90e2",
        "fg": "white",
        "activebackground": "#357ABD",
        "activeforeground": "white",
        "width": 12,
        "bd": 0,
        "relief": tk.FLAT,
        "cursor": "hand2",
        "padx": 5,
        "pady": 5
        }

        tk.Button(frame_botones, text="léxico", command=self.analizar_lexico, **estilo_btn).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="sintáctico", command=self.analizar_sintactico, **estilo_btn).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="semántico", command=self.analizar_semantico, **estilo_btn).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="completo", command=self.analizar_completo, **estilo_btn).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="volver", command=self.pantalla_inicio, **estilo_btn).pack(side=tk.RIGHT, padx=10)

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
