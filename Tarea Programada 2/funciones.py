import re
import tkinter as tk
from tkinter import messagebox
tiposSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")
baseDatos = []

def insertarDonador():
    ventanaInsertarDonador = tk.Toplevel()
    ventanaInsertarDonador.title("Insertar Donador")
    ventanaInsertarDonador.geometry("400x500")

    etiquetaCedula = tk.Label(ventanaInsertarDonador, text = "Cédula:")
    etiquetaCedula.pack()

    campoCedula = tk.Entry(ventanaInsertarDonador)
    campoCedula.pack()

    etiquetaNombre = tk.Label(ventanaInsertarDonador, text = "Nombre completo: ")
    etiquetaNombre.pack()

    campoNombre = tk.Entry(ventanaInsertarDonador)
    campoNombre.pack()

    etiquetaFecha = tk.Label(ventanaInsertarDonador, text = "Fecha de Nacimiento: ")
    etiquetaFecha.pack()

    campoFecha = tk.Entry(ventanaInsertarDonador)
    campoFecha.pack()

    tipoSangreVar = tk.StringVar()
    tipoSangreVar.set("O+")

    listaTipoSangre = tk.OptionMenu(ventanaInsertarDonador, tipoSangreVar, *tiposSangre)
    listaTipoSangre.pack()

    sexoVar = tk.BooleanVar()
    sexoVar.set(True)

    radioMasculino = tk.Radiobutton(ventanaInsertarDonador, text = "Masculino", variable = sexoVar, value = True)
    radioMasculino.pack()

    radioFemenino = tk.Radiobutton(ventanaInsertarDonador, text = "Femenino", variable = sexoVar, value = False)
    radioFemenino.pack() 

    etiquetaPeso = tk.Label(ventanaInsertarDonador, text = "Peso (kg): ")
    etiquetaPeso.pack()

    campoPeso = tk.Entry(ventanaInsertarDonador)
    campoPeso.pack()

    etiquetaTel = tk.Label(ventanaInsertarDonador, text = "Teléfono: ")
    etiquetaTel.pack()

    campoTel = tk.Entry(ventanaInsertarDonador)
    campoTel.pack()

    etiquetaCorreo = tk.Label(ventanaInsertarDonador, text = "Correo: ")
    etiquetaCorreo.pack()

    campoCorreo = tk.Entry(ventanaInsertarDonador)
    campoCorreo.pack()

    def pesoAux(peso):
        try:
            pesoFloat = float(peso)
            if pesoFloat > 50 and pesoFloat < 120:
                return True
            return False
        except ValueError:
            return False
        
    def registrar():
        cedula = campoCedula.get()
        fecha = campoFecha.get()
        tel = campoTel.get()
        correo = campoCorreo.get()
        peso = campoPeso.get()

        if not re.match(r'^[1-9]-\d{4}-\d{4}$', cedula):
            messagebox.showerror("Cédula inválida", "el primer dígito no puede ser 0, siga los parámetros (#-####-####).")
            return
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', fecha):
            messagebox.showerror("Fecha inválida", "siga los parámetros (DD/MM/AAAA).")
            return
        if not re.match(r'^[246789]\d{3}-\d{4}$', tel):
            messagebox.showerror("Teléfono inválido", "siga los parámetros(####-####).")
            return
        if not re.match(r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+(\.[a-zA-Z]+)?$', correo):
            messagebox.showerror("Correo inválido", "siga los parámetros")
            return
        if not pesoAux(peso):
            messagebox.showerror("Usted no puede donar sangre", "debe pesar entre 50 y 120 kg.")
            return
        
    def limpiar():
        campoCedula.delete(0, tk.END)
        campoNombre.delete(0, tk.END)
        campoFecha.delete(0, tk.END)
        tipoSangreVar.set("O+")
        sexoVar.set(True)
        campoPeso.delete(0, tk.END)
        campoTel.delete(0, tk.END)
        campoCorreo.delete(0, tk.END)
    
    botonRegistrar = tk.Button(ventanaInsertarDonador, text="Registrar", command=registrar)
    botonRegistrar.pack()

    botonLimpiar = tk.Button(ventanaInsertarDonador, text="Limpiar", command=limpiar)
    botonLimpiar.pack()

    botonRegresar = tk.Button(ventanaInsertarDonador, text="Regresar", command=ventanaInsertarDonador.destroy)
    botonRegresar.pack()


def generarDonadores():
    print()

def actualizarDatos():
    print()

def eliminarDonador():
    print()

def insertarLugar():
    print()

def reportes():
    print()

def salir():
    print()