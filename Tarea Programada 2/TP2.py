import tkinter as tk
ventana = tk.Tk()
ventana.title("Banco de Sangre")
ventana.geometry("400x300")
ventana.mainloop()

boton = tk.Button(ventana, text = "Insertar donador", command = insertarDonador())
boton = tk.Button(ventana, text = "Generar donadores", command = generarDonadores())
boton = tk.Button(ventana, text = "Actualizar datos del donador", command = actualizarDatos())
boton = tk.Button(ventana, text = "Eliminar donador", command = eliminarDonador())
boton = tk.Button(ventana, text = "Insertar lugar de donación", command = insertarLugar())
boton = tk.Button(ventana, text = "Reportes", command = reportes())
boton = tk.Button(ventana, text = "Salir", command = salir()) 