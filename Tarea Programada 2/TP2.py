import funciones
import tkinter as tk
ventana = tk.Tk()
ventana.title("Banco de Sangre")
ventana.geometry("400x300")

botonInsertarDonador = tk.Button(ventana, text = "Insertar donador", command = insertarDonador)
botonGenerarDonadores = tk.Button(ventana, text = "Generar donadores", command = generarDonadores)
botonActualizarDatos = tk.Button(ventana, text = "Actualizar datos del donador", command = actualizarDatos)
botonEliminarDonador = tk.Button(ventana, text = "Eliminar donador", command = eliminarDonador)
botonInsertarLugar = tk.Button(ventana, text = "Insertar lugar de donación", command = insertarLugar)
botonReportes = tk.Button(ventana, text = "Reportes", command = reportes)
botonSalir = tk.Button(ventana, text = "Salir", command = salir) 

ventana.mainloop()
