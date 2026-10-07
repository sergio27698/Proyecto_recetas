import tkinter as tk
import json
from tkinter import messagebox

def cargar_recetas():
    try:
        archivo = open("recetas.json", "r", encoding="utf-8")
        recetas = json.load(archivo)
        archivo.close()
        return recetas
    except FileNotFoundError:
        return []

def guardar_receta(nombre, region, porciones, ingredientes_texto, pasos_texto, ventana_admin):
    try:
        porciones_num = int(porciones)
    except ValueError:
        tk.messagebox.showerror("Error", "Porciones debe ser un número")
        return

    ingredientes = {}
    for linea in ingredientes_texto.strip().split("\n"):
        if "," in linea:
            nombre_ing, cantidad = linea.split(",")
            ingredientes[nombre_ing.strip().lower()] = float(cantidad.strip())

    pasos = [p.strip() for p in pasos_texto.strip().split("\n") if p.strip()]

    nueva_receta = {
        "nombre": nombre,
        "region": region,
        "porciones": porciones_num,
        "ingredientes": ingredientes,
        "pasos": pasos
    }

    recetas = cargar_recetas()
    recetas.append(nueva_receta)

    archivo = open("recetas.json", "w", encoding="utf-8")
    json.dump(recetas, archivo, indent=4, ensure_ascii=False)
    archivo.close()

    tk.messagebox.showinfo("Listo", "Receta agregada")
    ventana_admin.destroy()


def abrir_formulario_receta():
    ventana_admin = tk.Toplevel(ventana)
    ventana_admin.title("Agregar receta")
    ventana_admin.geometry("400x500")

    tk.Label(ventana_admin, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_admin)
    entry_nombre.pack()

    tk.Label(ventana_admin, text="Región:").pack()
    entry_region = tk.Entry(ventana_admin)
    entry_region.pack()

    tk.Label(ventana_admin, text="Porciones:").pack()
    entry_porciones = tk.Entry(ventana_admin)
    entry_porciones.pack()

    tk.Label(ventana_admin, text="Ingredientes (uno por línea: nombre,cantidad):").pack()
    text_ingredientes = tk.Text(ventana_admin, height=5)
    text_ingredientes.pack()

    tk.Label(ventana_admin, text="Pasos (uno por línea):").pack()
    text_pasos = tk.Text(ventana_admin, height=6)
    text_pasos.pack()

    tk.Button(ventana_admin, text="Guardar receta",
              command=lambda: guardar_receta(
                  entry_nombre.get(), entry_region.get(), entry_porciones.get(),
                  text_ingredientes.get("1.0", "end"), text_pasos.get("1.0", "end"),
                  ventana_admin
              )).pack(pady=10)


def login_admin():
    ventana_login = tk.Toplevel(ventana)
    ventana_login.title("Iniciar sesión")
    ventana_login.geometry("250x150")

    tk.Label(ventana_login, text="Usuario:").pack(pady=5)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()

    tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
    entry_clave = tk.Entry(ventana_login, show="*")
    entry_clave.pack()

    def verificar():
        if entry_usuario.get() == "Sergio" and entry_clave.get() == "00000":
            ventana_login.destroy()
            abrir_formulario_receta()
        else:
            tk.messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(ventana_login, text="Entrar", command=verificar).pack(pady=10)

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

    for widget in frame_resultados.winfo_children():
        widget.destroy()

    recetas = cargar_recetas()
    coincidencias = []
    mas_cercana = None
    menor_faltante = None

    for receta in recetas:
        ingredientes = receta["ingredientes"]
        if ingrediente in ingredientes:
            factor = personas / receta["porciones"]
            cantidad_necesaria = ingredientes[ingrediente] * factor

            if cantidad >= cantidad_necesaria:
                coincidencias.append(receta)
            else:
                faltante = cantidad_necesaria - cantidad
                if menor_faltante is None or faltante < menor_faltante:
                    menor_faltante = faltante
                    mas_cercana = receta

    if coincidencias:
        resultado_label.config(text="Podés hacer:")
        for receta in coincidencias:
            tk.Button(frame_resultados, text=receta["nombre"],
                      command=lambda r=receta: mostrar_detalle(r)).pack(pady=2)
    elif mas_cercana:
        resultado_label.config(
            text=f"No te alcanza para ninguna completa.\n"
                 f"La más cercana es '{mas_cercana['nombre']}', "
                 f"te faltan {menor_faltante:.1f} {ingrediente}"
        )
    else:
        resultado_label.config(text="Ninguna receta usa ese ingrediente")

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

tk.Button(ventana, text="Administrador", command=login_admin).pack(pady=5)

resultado_label = tk.Label(ventana, text="", wraplength=350)
resultado_label.pack()

frame_resultados = tk.Frame(ventana)
frame_resultados.pack()

ventana.mainloop()