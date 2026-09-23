import tkinter as tk
import json

def cargar_recetas():
    try:
        archivo = open("recetas.json", "r", encoding="utf-8")
        recetas = json.load(archivo)
        archivo.close()
        return recetas
    except FileNotFoundError:
        return []

def buscar():
    ingrediente = entry_ingrediente.get().lower().strip()
    try:
        cantidad = float(entry_cantidad.get())
        personas = int(entry_personas.get())
    except ValueError:
        resultado_label.config(text="Cantidad y personas deben ser números")
        return

    recetas = cargar_recetas()
    coincidencias = []

    for receta in recetas:
        ingredientes = receta["ingredientes"]
        if ingrediente in ingredientes:
            factor = personas / receta["porciones"]
            cantidad_necesaria = ingredientes[ingrediente] * factor
            if cantidad >= cantidad_necesaria:
                coincidencias.append(receta["nombre"])

    if coincidencias:
        resultado_label.config(text="Podés hacer: " + ", ".join(coincidencias))
    else:
        resultado_label.config(text="No hay recetas que alcancen con eso")

ventana = tk.Tk()
ventana.title("Recetas Bolivia")
ventana.geometry("400x350")

tk.Label(ventana, text="Ingrediente:").pack(pady=5)
entry_ingrediente = tk.Entry(ventana)
entry_ingrediente.pack()

tk.Label(ventana, text="Cantidad disponible:").pack(pady=5)
entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack()

tk.Label(ventana, text="Cantidad de personas:").pack(pady=5)
entry_personas = tk.Entry(ventana)
entry_personas.pack()

tk.Button(ventana, text="Buscar", command=buscar).pack(pady=15)

resultado_label = tk.Label(ventana, text="", wraplength=350)
resultado_label.pack()

ventana.mainloop()