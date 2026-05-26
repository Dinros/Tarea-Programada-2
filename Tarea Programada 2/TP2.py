import tkinter as tk
from funciones import *
ventana = tk.Tk()
ventana.title("Banco de Sangre")
ventana.geometry("400x300")

botonInsertarDonador = tk.Button(ventana, text = "Insertar donador", command = insertarDonador)
botonInsertarDonador .pack()
botonGenerarDonadores = tk.Button(ventana, text = "Generar donadores", command = generarDonadores)
botonGenerarDonadores.pack()
botonActualizarDatos = tk.Button(ventana, text = "Actualizar datos del donador", command = actualizarDatos)
botonActualizarDatos.pack()
botonEliminarDonador = tk.Button(ventana, text = "Eliminar donador", command = eliminarDonador)
botonEliminarDonador.pack()
botonInsertarLugar = tk.Button(ventana, text = "Insertar lugar de donación", command = insertarLugar)
botonInsertarLugar.pack()
botonReportes = tk.Button(ventana, text = "Reportes", command = reportes)
botonReportes.pack()
botonSalir = tk.Button(ventana, text="Salir", command = lambda: salir(ventana)) 
botonSalir.pack()

import os

# por defecto desactivar los botones 3, 4, 6
botonActualizarDatos.config(state="disabled")
botonEliminarDonador.config(state="disabled")
botonReportes.config(state="disabled")

# si existe la base de datos, activarlos todos
if os.path.exists("baseDatos.txt"):
    botonActualizarDatos.config(state="normal")
    botonEliminarDonador.config(state="normal")
    botonReportes.config(state="normal")

ventana.mainloop()
