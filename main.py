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

def mostrar_detalle(receta):
    ventana_detalle = tk.Toplevel(ventana)
    ventana_detalle.title(receta["nombre"])
    ventana_detalle.geometry("400x400")

    tk.Label(ventana_detalle, text=receta["nombre"], font=("Arial", 14, "bold")).pack(pady=5)
    tk.Label(ventana_detalle, text=f"Región: {receta['region']}").pack()
    tk.Label(ventana_detalle, text=f"Porciones: {receta['porciones']}").pack(pady=5)

    tk.Label(ventana_detalle, text="Ingredientes:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
    for ingrediente, cantidad in receta["ingredientes"].items():
        tk.Label(ventana_detalle, text=f"  - {cantidad} {ingrediente}").pack(anchor="w", padx=20)

    tk.Label(ventana_detalle, text="Pasos:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    for i, paso in enumerate(receta["pasos"], start=1):
        tk.Label(ventana_detalle, text=f"{i}. {paso}", wraplength=350, justify="left").pack(anchor="w", padx=20)

def buscar():
    ingrediente = entry_ingrediente.get().lower().strip()
    try:
        cantidad = float(entry_cantidad.get())
        personas = int(entry_personas.get())
    except ValueError:
        resultado_label.config(text="Cantidad y personas deben ser números")
        return

    # limpiar resultados anteriores
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    recetas = cargar_recetas()
    coincidencias = []

    for receta in recetas:
        ingredientes = receta["ingredientes"]
        if ingrediente in ingredientes:
            factor = personas / receta["porciones"]
            cantidad_necesaria = ingredientes[ingrediente] * factor
            if cantidad >= cantidad_necesaria:
                coincidencias.append(receta)

    if coincidencias:
        resultado_label.config(text="Podés hacer:")
        for receta in coincidencias:
            tk.Button(frame_resultados, text=receta["nombre"],
                      command=lambda r=receta: mostrar_detalle(r)).pack(pady=2)
    else:
        resultado_label.config(text="No hay recetas que alcancen con eso")

ventana = tk.Tk()
ventana.title("Recetas Bolivia")
ventana.geometry("400x400")

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

frame_resultados = tk.Frame(ventana)
frame_resultados.pack()

ventana.mainloop()