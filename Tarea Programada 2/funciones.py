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

infoSangre = {
    "O+": "El tipo de sangre más común, 1 de cada 3 personas (37.4%). Se recomienda donar glóbulos rojos dobles y sangre entera.",
    "O-": "Solo el 6.6% de la población. Donante universal. Se recomienda donar glóbulos rojos dobles y sangre entera.",
    "A+": "Segundo tipo más común (35.7%). Se recomienda donar sangre entera y plaquetas.",
    "A-": "El 6.3% de la población. Se recomienda donar sangre entera y glóbulos rojos dobles.",
    "B+": "El 8.5% de la población, o cada 1 de 12 personas tienen sangre tipo B+. Los donantes de sangre tipo B+ pueden lograr el mayor impacto con donaciones de sangre entera y de glóbulos rojos dobles.",
    "B-": "La sangre tipo B- se encuentra en 1 de cada 67 personas, formando el 1.5% de la población. Es un tipo de sangre menos común. A los donantes de sangre tipo Bse les recomienda que donen sangre entera o plaquetas.",
    "AB+": "AB+ es el tipo de sangre más raro deltipo ABO, con sólo 1 de cada 29 personas, o 3.4% de la población con este tipo. A los donantes AB+ se les recomienda hacer donaciones de plaquetas y de plasma.",
    "AB-": "El tipo de sangre más raro, el AB-, sólo lo tiene el 0.6% de la población, o 1 de cada 67 personas. A los donantes del tipo de sangre AB- se les recomienda donar plaquetas y plasma."
}

razones = {
    1: "Enfermedades Infecciosas/Crónicas: VIH, Hepatitis B o C, sífilis, tuberculosis, diabetes insulinodependiente.",
    2: "Conductas de Riesgo: nuevas parejas sexuales o más de una en los últimos 3 meses.",
    3: "Factores de Salud Física: hemoglobina bajo o alto, presión arterial inestable, fiebre.",
    4: "Procedimientos Médicos: transfusiones, trasplantes, cirugías, tatuajes, piercing recientes.",
    5: "Uso de Medicamentos: fármacos inyectables sin receta o ciertos medicamentos.",
    6: "Estilo de Vida y Viajes: drogas recreativas, alcohol en últimas 24 horas, viajes a zonas endémicas.",
    7: "Situaciones Específicas: embarazo, lactancia o menstruación."
}

compatibilidad = {
    "O-":  ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+":  ["O+", "A+", "B+", "AB+"],
    "A-":  ["A-", "A+", "AB-", "AB+"],
    "A+":  ["A+", "AB+"],
    "B-":  ["B-", "B+", "AB-", "AB+"],
    "B+":  ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"]
}

if os.path.exists("baseDatos.txt"):
    with open("baseDatos.txt", "rb") as archivo:
        baseDatos = pickle.load(archivo)


        
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
        

def cedulaExistente(cedula):
    for i in range(len(baseDatos)):
        if baseDatos[i][3] == cedula:
            return i
    return -1

def registrar(campoCedula, campoNombre, campoFecha, campoPeso, campoTel, campoCorreo, vTipoSangre, vSexo, ventanaInsertarDonador):
    cedula = campoCedula.get()
    fecha = campoFecha.get()
    tel = campoTel.get()
    correo = campoCorreo.get()
    peso = campoPeso.get()

    if not re.match(r'^[1-9]-\d{4}-\d{4}$', cedula):
        messagebox.showerror("Cédula inválida", "el primer dígito no puede ser 0, siga los parámetros (#-####-####).")
        return
    if cedulaExistente(cedula) != -1:
        messagebox.showerror("Error", "Esta cédula ya está registrada.")
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

    tipoActual = tiposSangre[indiceSangre]
    messagebox.showinfo("Tipo de sangre", infoSangre[tipoActual])

    if tipoActual == "A+" or tipoActual == "A-":
        messagebox.showinfo("Recomendación", 
            "Dado que su tipo de sangre es A+ o A-, le recomendamos ver el siguiente video:\nParticularidades de la sangre tipo A: Responde diferente al estrés según la ciencia.\nhttps://www.facebook.com/share/v/1GNXfvUBgd/")

def limpiar(campoCedula, campoNombre, campoFecha, campoPeso, campoTel, campoCorreo, vTipoSangre, vSexo):
    campoCedula.delete(0, tk.END)
    campoNombre.delete(0, tk.END)
    campoFecha.delete(0, tk.END)
    vTipoSangre.set("O+")
    vSexo.set(True)
    campoPeso.delete(0, tk.END)
    campoTel.delete(0, tk.END)
    campoCorreo.delete(0, tk.END)


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
    
    botonRegistrar = tk.Button(ventanaInsertarDonador, text="Registrar", 
    command=lambda: registrar(campoCedula, campoNombre, campoFecha, campoPeso, campoTel, campoCorreo, vTipoSangre, vSexo, ventanaInsertarDonador))
    botonRegistrar.pack()

    botonLimpiar = tk.Button(ventanaInsertarDonador, text="Limpiar", command=lambda: limpiar(campoCedula, campoNombre, campoFecha, campoPeso, campoTel, campoCorreo, vTipoSangre, vSexo))
    botonLimpiar.pack()

    botonRegresar = tk.Button(ventanaInsertarDonador, text="Regresar", command=ventanaInsertarDonador.destroy)
    botonRegresar.pack()


def generarDonadores():
    print()

def actualizarDatos():
    print()

def buscar(campoCedula, ventanaEliminar):
    cedula = campoCedula.get()
    i  = cedulaExistente(cedula)

    if i == -1:
        messagebox.showerror("Error", f"La persona con cédula {cedula} no está registrada.")  
    else:
        vRazon = tk.StringVar()
        vRazon.set(list(razones.values())[0])

        listaRazones = tk.OptionMenu(ventanaEliminar, vRazon, *razones.values())
        listaRazones.pack()

        botonConfirmar = tk.Button(ventanaEliminar, text="Confirmar", command=lambda: confirmar(i, vRazon, ventanaEliminar))
        botonConfirmar.pack()
        botonCancelar = tk.Button(ventanaEliminar, text="Cancelar", command=cancelar)
        botonCancelar.pack()

def confirmar(i, vRazon,ventanaEliminar):
    for numRazones, descripcion in razones.items():
        if descripcion == vRazon.get():
            baseDatos[i][11] = numRazones
            break
    baseDatos[i][10] = 0
    with open("baseDatos.txt", "wb") as archivo:
        pickle.dump(baseDatos, archivo)
    messagebox.showinfo("Éxito", "Donador eliminado satisfactoriamente.")
    print(baseDatos)
    ventanaEliminar.destroy()

def cancelar():
    messagebox.showinfo("Cancelado", "Donador NO eliminado.")


def eliminarDonador():
    ventanaEliminar = tk.Toplevel()
    ventanaEliminar.title("Eliminar Donador")
    ventanaEliminar.geometry("400x500")

    etiquetaCedula = tk.Label(ventanaEliminar, text = "Cédula:")
    etiquetaCedula.pack()

    campoCedula = tk.Entry(ventanaEliminar)
    campoCedula.pack()
    
    botonBuscar = tk.Button(ventanaEliminar, text="Buscar", command=lambda: buscar(campoCedula, ventanaEliminar))
    botonBuscar.pack()

    botonRegresar = tk.Button(ventanaEliminar, text = "Regresar", command = ventanaEliminar.destroy)
    botonRegresar.pack()

def insertar(areaTexto, vProvincia):
    lugar = areaTexto.get("1.0", tk.END).strip()
    if not lugar:
        messagebox.showerror("Error", "El lugar no puede estar vacío.")
        return
    numProvincia = ""
    for num, nombre in nombresProvincia.items():
        if nombre == vProvincia.get():
            numProvincia = num
            break
    if lugar in lugaresDonacion[numProvincia]:
        messagebox.showerror("Error", "Este lugar ya está registrado en esa provincia.")
        return
    lugaresDonacion[numProvincia].append(lugar)
    messagebox.showinfo("Éxito", f"{lugar} agregado correctamente a {vProvincia.get()}.")
    areaTexto.delete("1.0", tk.END) 

def insertarLugar():
    ventanaInsertarLugar = tk.Toplevel()
    ventanaInsertarLugar.title("Insertar lugar")
    ventanaInsertarLugar.geometry("400x500")
    
    etiquetaProvincia = tk.Label(ventanaInsertarLugar, text = "Seleccione la provincia: ")
    etiquetaProvincia.pack()

    vProvincia = tk.StringVar()
    vProvincia.set("San José")

    listaProvincia = tk.OptionMenu(ventanaInsertarLugar,vProvincia, *nombresProvincia.values())
    listaProvincia.pack()

    etiquetaLugar = tk.Label(ventanaInsertarLugar, text = "Nuevo lugar de donación:")
    etiquetaLugar.pack()

    areaTexto = tk.Text(ventanaInsertarLugar, height = 3, width = 30)
    areaTexto.pack() 

    botonInsertar = tk.Button(ventanaInsertarLugar, text="Insertar", command=lambda: insertar(areaTexto, vProvincia))  # ← BIEN
    botonInsertar.pack()

    botonSalir = tk.Button(ventanaInsertarLugar, text="Salir", command=ventanaInsertarLugar.destroy)
    botonSalir.pack()



def reporteListaCompleta():
    from datetime import datetime
    ahora = datetime.now()
    fechaHora = ahora.strftime("%d-%m-%y-%H-%M-%S")
    nombreHTML = "reporteListaCompleta_" + fechaHora + ".html"

    datosOrdenados = sorted(baseDatos, key = lambda fila: fila[3][0])

    html = open(nombreHTML, "w", encoding = "utf-8")
    html.write("<!DOCTYPE html>\n<html>\n<body>\n")
    html.write("<h1>Lista Completa de Donadores</h1>\n")
    html.write(f"<h2>{fechaHora}</h2>\n")
    html.write("<table border='1'>\n")
    html.write("<tr><th>Cédula</th><th>Nombre</th><th>Tipo Sangre</th><th>Fecha Nac.</th><th>Peso</th><th>Sexo</th><th>Teléfono</th><th>Correo</th></tr>\n")

    for fila in datosOrdenados:
        nombre = fila[0] + " " + fila[1] + " " + fila[2]
        sangre = tiposSangre[fila[4]]
        fecha = f"{fila[6][0]}/{fila[6][1]}/{fila[6][2]}"
        sexo = "Masculino" if fila[5] else "Femenino"
        html.write(f"<tr><td>{fila[3]}</td><td>{nombre}</td><td>{sangre}</td><td>{fecha}</td><td>{fila[7]}</td><td>{sexo}</td><td>{fila[9]}</td><td>{fila[8]}</td></tr>\n")
     
    html.write("</table\n</body>\n</html>")
    html.close()
    messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")

def generarReporteQuienDonar(vTipo, ventana):
    from datetime import datetime
    ahora = datetime.now()
    fechaHora = ahora.strftime("%d-%m-%y-%H-%M-%S")
    nombreHTML = "reporteQuienDonar_" + fechaHora + ".html"
    
    tipoSeleccionado = vTipo.get()
    indiceTipo = tiposSangre.index(tipoSeleccionado)
    puedeDonarA = compatibilidad[tipoSeleccionado]
    
    html = open(nombreHTML, "w", encoding="utf-8")
    html.write("<!DOCTYPE html>\n<html>\n<body>\n")
    html.write("<h1>¿A quién puede donar?</h1>\n")
    html.write(f"<h2>{fechaHora}</h2>\n")
    html.write(f"<p>Tipo de sangre: {tipoSeleccionado} puede donar a: {', '.join(puedeDonarA)}</p>\n")
    html.write("<table border='1'>\n")
    html.write("<tr><th>Cédula</th><th>Nombre</th><th>Tipo Sangre</th><th>Teléfono</th><th>Correo</th></tr>\n")
    
    for fila in baseDatos:
        if fila[4] == indiceTipo and fila[10] == 1:
            nombre = fila[0] + " " + fila[1] + " " + fila[2]
            sangre = tiposSangre[fila[4]]
            html.write(f"<tr><td>{fila[3]}</td><td>{nombre}</td><td>{sangre}</td><td>{fila[9]}</td><td>{fila[8]}</td></tr>\n")
    
    html.write("</table>\n</body>\n</html>")
    html.close()
    messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")

def reporteQuienDonar():
    ventanaReporteQuienDonar = tk.Toplevel()
    ventanaReporteQuienDonar.title("¿A quién puede donar?")
    ventanaReporteQuienDonar.geometry("400x500")

    etiquetaTipo = tk.Label(ventanaReporteQuienDonar, text = "Seleccione el tipo de sangre: ")
    etiquetaTipo.pack()

    vTipo = tk.StringVar()
    vTipo.set("O+")

    listaTipo = tk.OptionMenu(ventanaReporteQuienDonar, vTipo, *tiposSangre)
    listaTipo.pack()

    botonGenerar = tk.Button(ventanaReporteQuienDonar, text = "Generar reporte", command = lambda: generarReporteQuienDonar(vTipo, ventanaReporteQuienDonar))
    botonGenerar.pack()

    botonRegresar = tk.Button(ventanaReporteQuienDonar, text="Regresar", command = ventanaReporteQuienDonar.destroy)
    botonRegresar.pack()

def reporteNoActivos():
    from datetime import datetime
    ahora = datetime.now()
    fechaHora = ahora.strftime("%d-%m-%y-%H-%M-%S")
    nombreHTML = "reporteNoActivos_" + fechaHora + ".html"

    html = open(nombreHTML, "w", encoding="utf-8")
    html.write("<!DOCTYPE html>\n<html>\n<body>\n")
    html.write("<h1>Donantes No Activos</h1>\n")
    html.write(f"<h2>{fechaHora}</h2>\n")
    html.write("<table border='1'>\n")
    html.write("<tr><th>Justificación</th><th>Cédula</th><th>Nombre</th><th>Tipo Sangre</th><th>Fecha Nac.</th><th>Peso</th><th>Sexo</th><th>Teléfono</th><th>Correo</th></tr>\n")

    for fila in baseDatos:
        if fila[10] == 0:  
            nombre = fila[0] + " " + fila[1] + " " + fila[2]
            sangre = tiposSangre[fila[4]]
            fecha = f"{fila[6][0]}/{fila[6][1]}/{fila[6][2]}"
            sexo = "Masculino" if fila[5] else "Femenino"
            justificacion = razones[fila[11]] 
            html.write(f"<tr><td>{justificacion}</td><td>{fila[3]}</td><td>{nombre}</td><td>{sangre}</td><td>{fecha}</td><td>{fila[7]}</td><td>{sexo}</td><td>{fila[9]}</td><td>{fila[8]}</td></tr>\n")
    
    html.write("</table>\n</body>\n</html>")
    html.close()
    messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")


def reportes():
    ventanaReportes = tk.Toplevel()
    ventanaReportes.title("Reportes")
    ventanaReportes.geometry("400x300")

    botonRangoEdad = tk.Button(ventanaReportes, text="Por rango de edad", command = reporteRangoEdad)
    botonRangoEdad.pack()

    botonListaCompleta = tk.Button(ventanaReportes, text="Lista completa", command = reporteListaCompleta)
    botonListaCompleta.pack()

    botonQuienDonar = tk.Button(ventanaReportes, text="¿A quién puede donar?", command = reporteQuienDonar)
    botonQuienDonar.pack()

    botonNoActivos = tk.Button(ventanaReportes, text="Donantes no activos", command = reporteNoActivos)
    botonNoActivos.pack()

    botonRegresar = tk.Button(ventanaReportes, text="Regresar", command = ventanaReportes.destroy)
    botonRegresar.pack()

def salir(ventana):
    messagebox.showinfo("Hasta luego", "Donar sangre, es donar vida")
    ventana.destroy()

