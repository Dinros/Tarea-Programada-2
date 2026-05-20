from datetime import date
import os
import pickle
import re
import tkinter as tk
from tkinter import messagebox
tiposSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")
baseDatos = []
lugaresDonacion = {
    "1": ["El Banco Nacional de sangre", "Hospital México", "Hospital San Juan de Dios"],
    "2": ["Hospital San Rafael de Alajuela", "Hospital de San Ramón", "Hospital del Cantón Norteño"],
    "3": ["Hospital Max Peralta"],
    "4": ["Hospital San Vicente de Paúl"],
    "5": ["Hospital La Anexión en Nicoya", "Hospital Enrique Baltodano de Liberia"],
    "6": ["Hospital Monseñor Sanabria"],
    "7": ["Hospital Tony Facio", "Hospital de Guápiles"]
}

nombresProvincia = {
    "1": "San José",
    "2": "Alajuela", 
    "3": "Cartago",
    "4": "Heredia",
    "5": "Guanacaste",
    "6": "Puntarenas",
    "7": "Limón",
    "8": "Naturalizado"
}

if os.path.exists("baseDatos.txt"):
    with open("baseDatos.txt", "rb") as archivo:
        baseDatos = pickle.load(archivo)


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

    vTipoSangre = tk.StringVar() 
    vTipoSangre.set("O+")

    listaTipoSangre = tk.OptionMenu(ventanaInsertarDonador, vTipoSangre, *tiposSangre)
    listaTipoSangre.pack()

    vSexo = tk.BooleanVar()
    vSexo.set(True)

    radioMasculino = tk.Radiobutton(ventanaInsertarDonador, text = "Masculino", variable = vSexo, value = True)
    radioMasculino.pack()

    radioFemenino = tk.Radiobutton(ventanaInsertarDonador, text = "Femenino", variable = vSexo, value = False)
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
        
    def fechaAux(fechaTupla):
        hoy = date.today()
        annoNacimiento = fechaTupla[2]
        mesNacimiento = fechaTupla[1]

        if hoy.year - annoNacimiento > 18:
            puedeDonar = True
        elif hoy.year - annoNacimiento == 18:
            if hoy.month >= mesNacimiento:
                puedeDonar = True
            else:
                puedeDonar = False
        else:
            puedeDonar = False
        return puedeDonar
        
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
        if not re.match(r'^[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-zA-Z]+(\.[a-zA-Z]+)?$', correo):
            messagebox.showerror("Correo inválido", "siga los parámetros")
            return
        if not pesoAux(peso):
            messagebox.showerror("Usted no puede donar sangre", "debe pesar entre 50 y 120 kg.")
            return
        
        partesNombre = campoNombre.get().split()
        indiceSangre = tiposSangre.index(vTipoSangre.get())
        sexo = vSexo.get()
        partesFecha = fecha.split("/")
        fechaTupla = (int(partesFecha[0]), int(partesFecha[1]), int(partesFecha[2]))

        
        if len(partesNombre) != 3:
            messagebox.showerror("Nombre inválido", "Debe ingresar su nombre y dos apellidos.")
            return
        
        if not fechaAux(fechaTupla):
            messagebox.showerror("Edad", "Debido a que es menor de edad usted no puede donar.")
            return
        
        provincia = cedula[0]
        lugares = lugaresDonacion[provincia]
        lugaresTexto = "\n".join(lugares)
        messagebox.showinfo("Lugar de donación", f"Debido a que nació en {nombresProvincia[provincia]}, podría donar en:\n{lugaresTexto}")

            
        filaDonador = [partesNombre[0], partesNombre[1], partesNombre[2], cedula, indiceSangre, sexo, fechaTupla, float(peso), correo, tel, 1, 0]
        baseDatos.append(filaDonador)
        with open("baseDatos.txt", "wb") as archivo:
            pickle.dump(baseDatos, archivo)
        messagebox.showinfo("Éxito", "Donador registrado correctamente.")


        
    def limpiar():
        campoCedula.delete(0, tk.END)
        campoNombre.delete(0, tk.END)
        campoFecha.delete(0, tk.END)
        vTipoSangre.set("O+")
        vSexo.set(True)
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