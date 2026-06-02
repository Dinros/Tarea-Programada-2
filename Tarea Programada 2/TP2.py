#Elaborado por: Abigail Coto y Felipe Duran
#Fecha de creacion: 01/06/2026
#Ultima modificacion: 01/06/2026
#Version: 1.0

#Importa la librería gráfica tkinter
import tkinter as tk

#Importa todas las funciones del archivo funciones.py
from funciones import *

#Importa funciones del sistema operativo
import os

"""
Funcionamiento:
Programa principal del sistema Banco de Sangre.

Se encarga de:

- Crear la ventana principal.
- Crear los botones de acceso a cada opción.
- Activar o desactivar opciones según exista
  una base de datos guardada.
- Mantener la interfaz gráfica en ejecución.

Entradas:
Este módulo no recibe entradas directas.

Salidas:
Muestra la interfaz gráfica del sistema.
"""

# =====================================================
# CREACIÓN DE LA VENTANA PRINCIPAL
# =====================================================

#Crea la ventana principal
ventana = tk.Tk()

#Asigna el título de la ventana
ventana.title("Banco de Sangre")

#Define el tamaño de la ventana
ventana.geometry("400x300")

# =====================================================
# BOTONES DEL SISTEMA
# =====================================================

#Botón para insertar un nuevo donador
botonInsertarDonador = tk.Button(ventana,text="Insertar donador", command=insertarDonador)
#Muestra el botón en pantalla
botonInsertarDonador.pack()
#Botón para generar donadores automáticamente
botonGenerarDonadores = tk.Button(ventana,text="Generar donadores", command=generarDonadores)
#Muestra el botón
botonGenerarDonadores.pack()
#Botón para actualizar datos de un donador
botonActualizarDatos = tk.Button(ventana,text="Actualizar datos del donador", command=actualizarDatos)
#Muestra el botón
botonActualizarDatos.pack()
#Botón para eliminar un donador
botonEliminarDonador = tk.Button(ventana, text="Eliminar donador", command=eliminarDonador)
#Muestra el botón
botonEliminarDonador.pack()
#Botón para insertar lugares de donación
botonInsertarLugar = tk.Button(ventana, text="Insertar lugar de donación", command=insertarLugar)
#Muestra el botón
botonInsertarLugar.pack()
#Botón para acceder a reportes
botonReportes = tk.Button(ventana, text="Reportes", command=reportes)
#Muestra el botón
botonReportes.pack()
#Botón para cerrar la aplicación
botonSalir = tk.Button(ventana, text="Salir", command=lambda: salir(ventana))
#Muestra el botón
botonSalir.pack()

# =====================================================
# CONFIGURACIÓN INICIAL DE BOTONES
# =====================================================
#Desactiva la actualización de datos
botonActualizarDatos.config(state="disabled")
#Desactiva la eliminación de donadores
botonEliminarDonador.config(state="disabled")
#Desactiva los reportes
botonReportes.config(state="disabled")

# =====================================================
# VERIFICACIÓN DE BASE DE DATOS
# =====================================================

#Verifica si existe el archivo de base de datos
if os.path.exists("baseDatos.txt"):
    #Activa actualizar datos
    botonActualizarDatos.config(state="normal")
    #Activa eliminar donadores
    botonEliminarDonador.config(state="normal")
    #Activa reportes
    botonReportes.config(state="normal")

# =====================================================
# EJECUCIÓN DE LA INTERFAZ
# =====================================================

#Mantiene la ventana abierta y en funcionamiento
ventana.mainloop()
