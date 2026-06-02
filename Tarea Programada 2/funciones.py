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
    """
    Funcionamiento:
    Valida que el peso ingresado corresponda
    a un número válido y verifica si la persona
    cumple con los requisitos para donar sangre.
    Entradas:
    - peso(str): Peso ingresado por el usuario.
    Salidas:
    - Muestra mensajes informativos o de error
      mediante cuadros de diálogo.
    """
    #Intenta convertir el peso a decimal
    try:
        #Convierte el texto a número
        pesoFloat = float(peso)
        #Verifica si pesa menos de lo permitido
        if pesoFloat <= 50:
            messagebox.showerror("Peso", "Usted debe pesar más de 50 kgms para poder ser donador.")

        #Verifica si supera el máximo permitido
        elif pesoFloat >= 120:
            messagebox.showerror("Peso", "Dado su sobre peso, no es posible donar sangre.")
        #Indica que el peso es válido
        else:
            messagebox.showinfo("Peso", "Usted posee un peso adecuado para ser donador.")
    #Captura errores si no se ingresa un número
    except ValueError:
        messagebox.showerror( "Error", "El peso debe ser un número.")

def fechaAux(fechaTupla):
    """
    Funcionamiento:
    Determina si una persona cumple con la
    edad mínima requerida para donar sangre,
    verificando que tenga al menos 18 años.
    Entradas:
    - fechaTupla(tuple): Tupla que contiene
      día, mes y año de nacimiento.
    Salidas:
    - (bool): True si la persona puede donar.
    - (bool): False si es menor de edad.
    """
    #Obtiene la fecha actual
    hoy = date.today()
    #Obtiene el año de nacimiento
    annoNacimiento = fechaTupla[2]
    #Obtiene el mes de nacimiento
    mesNacimiento = fechaTupla[1]
    #Verifica si tiene más de 18 años
    if hoy.year - annoNacimiento > 18:
        puedeDonar = True
    #Verifica si tiene exactamente 18 años
    elif hoy.year - annoNacimiento == 18:
        #Comprueba si ya cumplió años este año
        if hoy.month >= mesNacimiento:
            puedeDonar = True
        else:
            puedeDonar = False
    #Es menor de edad
    else:
        puedeDonar = False
    #Retorna el resultado de la validación
    return puedeDonar

def cedulaExistente(cedula):
    """
    Funcionamiento:
    Busca una cédula dentro de la base de datos
    para determinar si ya existe un registro
    asociado a ella.
    Entradas:
    - cedula(str): Número de cédula que se desea
      buscar.
    Salidas:
    - (int): Posición donde se encuentra la cédula.
    - (int): -1 si la cédula no existe.
    """
    #Recorre toda la base de datos
    for i in range(len(baseDatos)):
        #Verifica si la cédula coincide
        if baseDatos[i][3] == cedula:
            #Retorna la posición encontrada
            return i
    #Retorna -1 si la cédula no existe
    return -1

def registrar(campoCedula, campoNombre, campoFecha, campoPeso, campoTel, campoCorreo, vTipoSangre, vSexo, ventanaInsertarDonador):
    """
    Funcionamiento:
    Obtiene los datos ingresados en el formulario,
    valida cada uno de ellos y registra un nuevo
    donador en la base de datos.

    Además, muestra información relacionada con
    el tipo de sangre, lugares de donación y
    recomendaciones específicas.

    Entradas:
    - campoCedula(Entry): Campo de cédula.
    - campoNombre(Entry): Campo de nombre.
    - campoFecha(Entry): Campo de fecha de nacimiento.
    - campoPeso(Entry): Campo de peso.
    - campoTel(Entry): Campo de teléfono.
    - campoCorreo(Entry): Campo de correo electrónico.
    - vTipoSangre(StringVar): Tipo de sangre seleccionado.
    - vSexo(BooleanVar): Sexo seleccionado.
    - ventanaInsertarDonador(Tk): Ventana actual.

    Salidas:
    - Registra un nuevo donador.
    - Guarda la información en la base de datos.
    - Muestra mensajes informativos y de error.
    """
    #Obtiene los valores ingresados en el formulario
    cedula = campoCedula.get()
    fecha = campoFecha.get()
    tel = campoTel.get()
    correo = campoCorreo.get()
    peso = campoPeso.get()
    #Valida el formato de la cédula
    if not re.match(r'^[1-9]-\d{4}-\d{4}$', cedula):
        messagebox.showerror("Cédula inválida", "El primer dígito no puede ser 0, siga los parámetros (#-####-####).")
        return
    #Verifica si la cédula ya existe
    if cedulaExistente(cedula) != -1:
        messagebox.showerror("Error", "Esta cédula ya está registrada.")
        return
    #Valida el formato de la fecha
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', fecha):
        messagebox.showerror( "Fecha inválida", "Siga los parámetros (DD/MM/AAAA).")
        return
    #Valida el formato del teléfono
    if not re.match(r'^[246789]\d{3}-\d{4}$', tel):
        messagebox.showerror("Teléfono inválido", "Siga los parámetros (####-####)." )
        return
    #Valida el correo electrónico
    if not re.match( r'^[a-zA-Z0-9.]+@(costarricense\.cr|racsa\.go\.cr|ccss\.sa\.cr|gmail\.com)$', correo):
        messagebox.showerror( "Correo inválido", "Solo permitimos correos:\n" "-costarricense.cr\n" "-racsa.go.cr\n" "-ccss.sa.cr\n" "-gmail.com")
        return
    #Valida el peso del donador
    if not pesoAux(peso):
        return
    #Separa nombre y apellidos
    partesNombre = campoNombre.get().split()
    #Obtiene la posición del tipo sanguíneo
    indiceSangre = tiposSangre.index(vTipoSangre.get())
    #Obtiene el sexo seleccionado
    sexo = vSexo.get()
    #Divide la fecha en día, mes y año
    partesFecha = fecha.split("/")
    #Convierte la fecha a tupla numérica
    fechaTupla = (int(partesFecha[0]), int(partesFecha[1]), int(partesFecha[2]))
    #Verifica que se ingresen nombre y dos apellidos
    if len(partesNombre) != 3:
        messagebox.showerror("Nombre inválido", "Debe ingresar su nombre y dos apellidos.")
        return
    #Valida la edad mínima para donar
    if not fechaAux(fechaTupla):
        messagebox.showerror("Edad", "Dado su fecha de nacimiento usted aún no puede ser donador." )
        return
    #Indica que puede donar
    messagebox.showinfo( "Edad", "Dado su fecha de nacimiento usted ya puede ser donador.")
    #Obtiene la provincia según la cédula
    provincia = cedula[0]
    #Obtiene los lugares de donación disponibles
    lugares = lugaresDonacion[provincia]
    #Convierte la lista a texto
    lugaresTexto = "\n".join(lugares)
    #Muestra lugares de donación recomendados
    messagebox.showinfo("Lugar de donación",f"Dado que usted nació en la provincia de: " f"{nombresProvincia[provincia]}, "f"usted podría donar en:\n{lugaresTexto}")
    #Crea la fila del nuevo donador
    filaDonador = [partesNombre[0], partesNombre[1], partesNombre[2], cedula, indiceSangre, sexo, fechaTupla, float(peso), correo, tel, 1, 0]
    #Agrega el donador a la base de datos
    baseDatos.append(filaDonador)
    #Guarda la base de datos actualizada
    with open("baseDatos.txt", "wb") as archivo:
        pickle.dump(baseDatos, archivo)
    #Confirma el registro
    messagebox.showinfo("Éxito", "Donador registrado correctamente.")
    #Obtiene el tipo sanguíneo del donador
    tipoActual = tiposSangre[indiceSangre]
    #Muestra información del tipo de sangre
    messagebox.showinfo("Tipo de sangre", infoSangre[tipoActual])
    #Muestra recomendación para sangre tipo A
    if tipoActual == "A+" or tipoActual == "A-":
        messagebox.showinfo("Recomendación","Dado que su tipo de sangre es A+ o A-, " "le recomendamos ver el siguiente video:\n" "Particularidades de la sangre tipo A.\n" "https://www.facebook.com/share/v/1GNXfvUBgd/")

def limpiar(campoCedula, campoNombre, campoFecha, campoPeso, campoTel, campoCorreo, vTipoSangre, vSexo):
    """
    Funcionamiento:
    Limpia todos los campos del formulario
    y restablece los valores predeterminados.
    Entradas:
    - campoCedula(Entry): Campo de cédula.
    - campoNombre(Entry): Campo de nombre.
    - campoFecha(Entry): Campo de fecha.
    - campoPeso(Entry): Campo de peso.
    - campoTel(Entry): Campo de teléfono.
    - campoCorreo(Entry): Campo de correo.
    - vTipoSangre(StringVar): Variable del tipo sanguíneo.
    - vSexo(BooleanVar): Variable del sexo.
    Salidas:
    Esta función no retorna valores.
    """
    #Limpia el campo de cédula
    campoCedula.delete(0, tk.END)
    #Limpia el campo de nombre
    campoNombre.delete(0, tk.END)
    #Limpia el campo de fecha
    campoFecha.delete(0, tk.END)
    #Restablece el tipo de sangre por defecto
    vTipoSangre.set("O+")
    #Restablece el sexo por defecto
    vSexo.set(True)
    #Limpia el campo de peso
    campoPeso.delete(0, tk.END)
    #Limpia el campo de teléfono
    campoTel.delete(0, tk.END)
    #Limpia el campo de correo
    campoCorreo.delete(0, tk.END)

def insertarDonador():
    """
    Funcionamiento:
    Crea una ventana secundaria que permite
    registrar un nuevo donador mediante una
    interfaz gráfica.
    La ventana contiene campos para ingresar
    la información personal del donador, así
    como botones para registrar, limpiar los
    datos o regresar al menú principal.
    Entradas:
    Esta función no recibe entradas.
    Salidas:
    - Muestra la ventana de registro.
    - Permite capturar la información del donador.
    - Ejecuta las funciones registrar() y limpiar().
    """
    #Crea una nueva ventana para registrar donadores
    ventanaInsertarDonador = tk.Toplevel()
    #Asigna el título de la ventana
    ventanaInsertarDonador.title("Insertar Donador")
    #Define el tamaño de la ventana
    ventanaInsertarDonador.geometry("400x500")
    #Etiqueta para la cédula
    etiquetaCedula = tk.Label(ventanaInsertarDonador, text = "Cédula:")
    etiquetaCedula.pack()
    #Campo para ingresar la cédula
    campoCedula = tk.Entry(ventanaInsertarDonador)
    campoCedula.pack()
    #Etiqueta para el nombre completo
    etiquetaNombre = tk.Label(ventanaInsertarDonador, text = "Nombre completo: ")
    etiquetaNombre.pack()
    #Campo para ingresar el nombre
    campoNombre = tk.Entry(ventanaInsertarDonador)
    campoNombre.pack()
    #Etiqueta para la fecha de nacimiento
    etiquetaFecha = tk.Label(ventanaInsertarDonador, text = "Fecha de Nacimiento: ")
    etiquetaFecha.pack()
    #Campo para ingresar la fecha
    campoFecha = tk.Entry(ventanaInsertarDonador)
    campoFecha.pack()
    #Variable que almacena el tipo de sangre seleccionado
    vTipoSangre = tk.StringVar()
    #Valor por defecto del tipo sanguíneo
    vTipoSangre.set("O+")
    #Lista desplegable con los tipos sanguíneos
    listaTipoSangre = tk.OptionMenu(ventanaInsertarDonador, vTipoSangre, *tiposSangre)
    listaTipoSangre.pack()
    #Variable que almacena el sexo seleccionado
    vSexo = tk.BooleanVar()
    #Valor por defecto para sexo masculino
    vSexo.set(True)
    #Botón de selección para masculino
    radioMasculino = tk.Radiobutton(ventanaInsertarDonador, text = "Masculino", variable = vSexo, value = True)
    radioMasculino.pack()
    #Botón de selección para femenino
    radioFemenino = tk.Radiobutton(ventanaInsertarDonador, text = "Femenino", variable = vSexo, value = False)
    radioFemenino.pack()
    #Etiqueta para el peso
    etiquetaPeso = tk.Label(ventanaInsertarDonador, text = "Peso (kg): ")
    etiquetaPeso.pack()
    #Campo para ingresar el peso
    campoPeso = tk.Entry(ventanaInsertarDonador)
    campoPeso.pack()
    #Etiqueta para el teléfono
    etiquetaTel = tk.Label(ventanaInsertarDonador, text = "Teléfono: ")
    etiquetaTel.pack()
    #Campo para ingresar el teléfono
    campoTel = tk.Entry(ventanaInsertarDonador)
    campoTel.pack()
    #Etiqueta para el correo electrónico
    etiquetaCorreo = tk.Label(ventanaInsertarDonador, text = "Correo: ")
    etiquetaCorreo.pack()
    #Campo para ingresar el correo
    campoCorreo = tk.Entry(ventanaInsertarDonador)
    campoCorreo.pack()

    #Botón que registra al donador en la base de datos
    botonRegistrar = tk.Button(ventanaInsertarDonador, text="Registrar", command=lambda: registrar(campoCedula, campoNombre, campoFecha, campoPeso, campoTel, campoCorreo, vTipoSangre, vSexo, ventanaInsertarDonador))
    botonRegistrar.pack()
    #Botón que limpia todos los campos del formulario
    botonLimpiar = tk.Button(ventanaInsertarDonador, text="Limpiar", command=lambda: limpiar(campoCedula, campoNombre, campoFecha, campoPeso, campoTel, campoCorreo, vTipoSangre, vSexo))
    botonLimpiar.pack()
    #Botón que cierra la ventana actual
    botonRegresar = tk.Button(ventanaInsertarDonador, text="Regresar", command=ventanaInsertarDonador.destroy)
    botonRegresar.pack()

def generarDonadores():
    ventanaGenerar = tk.Toplevel()
    ventanaGenerar.title("Generar Donadores")
    ventanaGenerar.geometry("350x150")
 
    etiquetaCantidad = tk.Label(ventanaGenerar, text="Cantidad de donadores a generar:")
    etiquetaCantidad.pack()
 
    campoCantidad = tk.Entry(ventanaGenerar)
    campoCantidad.pack()
 
    def generarAux():
        cantidad = campoCantidad.get()
        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Cantidad inválida", "Debe ingresar un número entero mayor a 0.")
            return
        if cantidad <= 0:
            messagebox.showerror("Cantidad inválida", "El dato ingresado debe ser mayor a 0.")
            return
 
        nombresAleatorios = ["Carlos", "María", "Luis", "Ana", "Jorge", "Laura", "Pedro", "Sofía",
                             "Andrés", "Valeria", "Diego", "Camila", "Roberto", "Isabella", "Miguel"]
        apellidosAleatorios = ["González", "Rodríguez", "Jiménez", "Mora", "Castro", "Vargas",
                               "Solano", "Rojas", "Chaves", "Alvarado", "Ramírez", "Badilla", "Núñez"]
 
        generados = 0
        for _ in range(cantidad):
            nombre = random.choice(nombresAleatorios)
            apellido1 = random.choice(apellidosAleatorios)
            apellido2 = random.choice(apellidosAleatorios)
            provincia = random.randint(1, 7)
            tomo = random.randint(1000, 9999)
            asiento = random.randint(1000, 9999)
            cedula = f"{provincia}-{tomo:04d}-{asiento:04d}"
            indiceSangre = random.randint(0, 7)
            sexo = random.choice([True, False])
            anio = random.randint(1950, 2010)
            mes = random.randint(1, 12)
            dia = random.randint(1, 28)
            fechaTupla = (dia, mes, anio)
            peso = round(random.uniform(40, 130), 1)
            correo = f"{nombre.lower()}{random.randint(1,99)}@gmail.com"
            tel = f"{random.choice([2,4,6,7,8,9])}{random.randint(100,999)}-{random.randint(1000,9999)}"
 
            if peso <= 50:
                estado = 0
                justificacion = 3
            elif peso >= 120:
                estado = 0
                justificacion = 3
            else:
                estado = 1
                justificacion = 0
 
            edad = obtenerEdad(fechaTupla)
            if edad < 18:
                estado = 0
                justificacion = 3
 
            filaDonador = [nombre, apellido1, apellido2, cedula, indiceSangre, sexo,
                           fechaTupla, peso, correo, tel, estado, justificacion]
            baseDatos.append(filaDonador)
            generados += 1
 
        guardarBaseDatos()
        messagebox.showinfo("Generación completada", f"Se generaron {generados} donadores correctamente.")
        ventanaGenerar.destroy()
 
    botonGenerar = tk.Button(ventanaGenerar, text="Generar", command=generarAux)
    botonGenerar.pack()
 
    botonRegresar = tk.Button(ventanaGenerar, text="Regresar", command=ventanaGenerar.destroy)
    botonRegresar.pack()
def actualizarDatos():
    ventanaBuscar = tk.Toplevel()
    ventanaBuscar.title("Actualizar Datos del Donador")
    ventanaBuscar.geometry("350x120")
 
    etiquetaCedula = tk.Label(ventanaBuscar, text="Ingrese el número de cédula:")
    etiquetaCedula.pack()
 
    campoCedula = tk.Entry(ventanaBuscar)
    campoCedula.pack()
 
    def buscar():
        cedula = campoCedula.get()
        indiceDonador = -1
        for i, donador in enumerate(baseDatos):
            if donador[3] == cedula:
                indiceDonador = i
                break
 
        if indiceDonador == -1:
            messagebox.showinfo("No encontrado",
                f"La persona con el número de cédula: {cedula} no está registrado en la base de datos del Banco de Sangre aún.")
            return
 
        ventanaBuscar.destroy()
        donador = baseDatos[indiceDonador]
        ventanaActualizar = tk.Toplevel()
        ventanaActualizar.title("Actualizar Datos del Donador")
        ventanaActualizar.geometry("400x520")
 
        etiquetaCedulaRO = tk.Label(ventanaActualizar, text="Cédula (solo lectura):")
        etiquetaCedulaRO.pack()
        campoCedulaRO = tk.Entry(ventanaActualizar, state="readonly")
        campoCedulaRO.pack()
        campoCedulaRO.config(state="normal")
        campoCedulaRO.insert(0, donador[3])
        campoCedulaRO.config(state="readonly")
 
        etiquetaNombre = tk.Label(ventanaActualizar, text="Nombre completo:")
        etiquetaNombre.pack()
        campoNombre = tk.Entry(ventanaActualizar)
        campoNombre.pack()
        campoNombre.insert(0, f"{donador[0]} {donador[1]} {donador[2]}")
 
        etiquetaFecha = tk.Label(ventanaActualizar, text="Fecha de Nacimiento (DD/MM/AAAA):")
        etiquetaFecha.pack()
        campoFecha = tk.Entry(ventanaActualizar)
        campoFecha.pack()
        dd, mm, aaaa = donador[6]
        campoFecha.insert(0, f"{dd:02d}/{mm:02d}/{aaaa}")
 
        vTipoSangre = tk.StringVar()
        vTipoSangre.set(tiposSangre[donador[4]])
        listaTipoSangre = tk.OptionMenu(ventanaActualizar, vTipoSangre, *tiposSangre)
        listaTipoSangre.pack()
 
        vSexo = tk.BooleanVar()
        vSexo.set(donador[5])
        radioMasculino = tk.Radiobutton(ventanaActualizar, text="Masculino", variable=vSexo, value=True)
        radioMasculino.pack()
        radioFemenino = tk.Radiobutton(ventanaActualizar, text="Femenino", variable=vSexo, value=False)
        radioFemenino.pack()
 
        etiquetaPeso = tk.Label(ventanaActualizar, text="Peso (kg):")
        etiquetaPeso.pack()
        campoPeso = tk.Entry(ventanaActualizar)
        campoPeso.pack()
        campoPeso.insert(0, str(donador[7]))
 
        etiquetaTel = tk.Label(ventanaActualizar, text="Teléfono:")
        etiquetaTel.pack()
        campoTel = tk.Entry(ventanaActualizar)
        campoTel.pack()
        campoTel.insert(0, donador[9])
 
        etiquetaCorreo = tk.Label(ventanaActualizar, text="Correo:")
        etiquetaCorreo.pack()
        campoCorreo = tk.Entry(ventanaActualizar)
        campoCorreo.pack()
        campoCorreo.insert(0, donador[8])
 
        def confirmar():
            fecha = campoFecha.get()
            tel = campoTel.get()
            correo = campoCorreo.get()
            peso = campoPeso.get()
 
            if not re.match(r'^\d{2}/\d{2}/\d{4}$', fecha):
                messagebox.showerror("Fecha inválida", "siga los parámetros (DD/MM/AAAA).")
                return
            if not re.match(r'^[246789]\d{3}-\d{4}$', tel):
                messagebox.showerror("Teléfono inválido", "siga los parámetros(####-####).")
                return
            if not re.match(r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+(\.[a-zA-Z]+)?$', correo):
                messagebox.showerror("Correo inválido", "siga los parámetros.")
                return
            if not pesoAux(peso):
                messagebox.showerror("Peso inválido", "debe pesar entre 50 y 120 kg.")
                return
 
            partesNombre = campoNombre.get().split()
            if len(partesNombre) != 3:
                messagebox.showerror("Nombre inválido", "Debe ingresar su nombre y dos apellidos.")
                return
 
            partesFecha = fecha.split("/")
            fechaTupla = (int(partesFecha[0]), int(partesFecha[1]), int(partesFecha[2]))
 
            baseDatos[indiceDonador][0] = partesNombre[0]
            baseDatos[indiceDonador][1] = partesNombre[1]
            baseDatos[indiceDonador][2] = partesNombre[2]
            baseDatos[indiceDonador][4] = tiposSangre.index(vTipoSangre.get())
            baseDatos[indiceDonador][5] = vSexo.get()
            baseDatos[indiceDonador][6] = fechaTupla
            baseDatos[indiceDonador][7] = float(peso)
            baseDatos[indiceDonador][8] = correo
            baseDatos[indiceDonador][9] = tel
 
            guardarBaseDatos()
            messagebox.showinfo("Actualización", "Datos actualizados correctamente.")
            ventanaActualizar.destroy()
 
        def rechazar():
            messagebox.showinfo("Actualización", "Datos No actualizados.")
 
        botonConfirmar = tk.Button(ventanaActualizar, text="Confirmar", command=confirmar)
        botonConfirmar.pack()
 
        botonRechazar = tk.Button(ventanaActualizar, text="Rechazar", command=rechazar)
        botonRechazar.pack()
 
        botonRegresar = tk.Button(ventanaActualizar, text="Regresar", command=ventanaActualizar.destroy)
        botonRegresar.pack()
 
    botonBuscar = tk.Button(ventanaBuscar, text="Buscar", command=buscar)
    botonBuscar.pack()
 
    botonRegresar = tk.Button(ventanaBuscar, text="Regresar", command=ventanaBuscar.destroy)
    botonRegresar.pack()

def buscar(campoCedula, ventanaEliminar):
    """
    Funcionamiento:
    Busca una cédula dentro de la base de datos.
    Si la persona existe, muestra las razones
    disponibles para eliminar al donador y crea
    los botones de confirmación o cancelación.
    Entradas:
    - campoCedula(Entry): Campo donde se ingresa
      la cédula del donador.
    - ventanaEliminar(Toplevel): Ventana utilizada
      para el proceso de eliminación.
    Salidas:
    - Muestra un mensaje de error si la cédula
      no existe.
    - Muestra las opciones para continuar con
      la eliminación del donador.
    """
    #Obtiene la cédula ingresada
    cedula = campoCedula.get()
    #Busca la posición del donador
    i  = cedulaExistente(cedula)
    #Verifica si la cédula no existe
    if i == -1:
        messagebox.showerror("Error", f"La persona con cédula {cedula} no está registrada.")
    else:
        #Variable para almacenar la razón seleccionada
        vRazon = tk.StringVar()
        #Selecciona la primera razón como valor por defecto
        vRazon.set(list(razones.values())[0])
        #Crea la lista desplegable de razones
        listaRazones = tk.OptionMenu(ventanaEliminar, vRazon, *razones.values())
        listaRazones.pack()
        #Botón para confirmar la eliminación
        botonConfirmar = tk.Button( ventanaEliminar, text="Confirmar", command=lambda: confirmar(i, vRazon, ventanaEliminar))
        botonConfirmar.pack()
        #Botón para cancelar la eliminación
        botonCancelar = tk.Button(ventanaEliminar, text="Cancelar", command = cancelar)
        botonCancelar.pack()

def confirmar(i, vRazon, ventanaEliminar):
    """
    Funcionamiento:
    Confirma la eliminación lógica de un donador,
    registra la razón seleccionada y actualiza
    la base de datos.
    Entradas:
    - i(int): Posición del donador dentro de la
      base de datos.
    - vRazon(StringVar): Razón seleccionada para
      la eliminación.
    - ventanaEliminar(Toplevel): Ventana utilizada
      para el proceso de eliminación.
    Salidas:
    - Actualiza la información del donador.
    - Guarda los cambios en la base de datos.
    - Muestra un mensaje de confirmación.
    """
    #Busca el número asociado a la razón seleccionada
    for numRazones, descripcion in razones.items():
        #Verifica la razón elegida
        if descripcion == vRazon.get():
            #Guarda el código de la razón
            baseDatos[i][11] = numRazones
            break
    #Marca al donador como inactivo
    baseDatos[i][10] = 0
    #Guarda los cambios en el archivo
    with open("baseDatos.txt", "wb") as archivo:
        pickle.dump(baseDatos, archivo)
    #Muestra mensaje de éxito
    messagebox.showinfo("Éxito", "Donador eliminado satisfactoriamente.")
    #Muestra la base de datos actualizada
    print(baseDatos)
    #Cierra la ventana de eliminación
    ventanaEliminar.destroy()

def cancelar():
    """
    Funcionamiento:
    Cancela el proceso de eliminación de un
    donador sin realizar cambios en la base
    de datos.
    Entradas:
    Esta función no recibe entradas.
    Salidas:
    - Muestra un mensaje indicando que la
      eliminación fue cancelada.
    """
    #Informa que la eliminación fue cancelada
    messagebox.showinfo("Cancelado", "Donador NO eliminado.")

def eliminarDonador():
    """
    Funcionamiento:
    Crea una ventana secundaria que permite
    eliminar un donador mediante la búsqueda
    de su cédula.
    Entradas:
    Esta función no recibe entradas.
    Salidas:
    - Muestra la ventana de eliminación.
    - Permite buscar un donador registrado.
    - Ejecuta la función buscar().
    """
    #Crea una nueva ventana para eliminar donadores
    ventanaEliminar = tk.Toplevel()
    #Asigna el título de la ventana
    ventanaEliminar.title("Eliminar Donador")
    #Define el tamaño de la ventana
    ventanaEliminar.geometry("700x300")
    #Etiqueta para la cédula
    etiquetaCedula = tk.Label(ventanaEliminar, text = "Cédula:")
    etiquetaCedula.pack()
    #Campo para ingresar la cédula
    campoCedula = tk.Entry(ventanaEliminar)
    campoCedula.pack()
    #Botón para buscar al donador
    botonBuscar = tk.Button(ventanaEliminar, text="Buscar", command=lambda: buscar(campoCedula, ventanaEliminar))
    botonBuscar.pack()
    #Botón para regresar y cerrar la ventana
    botonRegresar = tk.Button(ventanaEliminar, text="Regresar", command=ventanaEliminar.destroy)
    botonRegresar.pack()

def insertar(areaTexto, vProvincia):
    """
    Funcionamiento:
    Agrega un nuevo lugar de donación a la
    provincia seleccionada, verificando que
    el nombre no esté vacío ni repetido.
    Entradas:
    - areaTexto(Text): Área donde se ingresa
      el nombre del nuevo lugar.
    - vProvincia(StringVar): Provincia
      seleccionada.
    Salidas:
    - Agrega un nuevo lugar de donación.
    - Muestra mensajes de éxito o error.
    """
    #Obtiene el texto ingresado
    lugar = areaTexto.get("1.0", tk.END).strip()
    #Verifica que el campo no esté vacío
    if not lugar:
        messagebox.showerror("Error","El lugar no puede estar vacío.")
        return
    #Variable para almacenar el número de provincia
    numProvincia = ""
    #Busca el código asociado a la provincia
    for num, nombre in nombresProvincia.items():
        if nombre == vProvincia.get():
            numProvincia = num
            break
    #Verifica si el lugar ya existe
    if lugar in lugaresDonacion[numProvincia]:
        messagebox.showerror("Error", "Este lugar ya está registrado en esa provincia.")
        return
    #Agrega el nuevo lugar a la provincia
    lugaresDonacion[numProvincia].append(lugar)
    #Muestra mensaje de éxito
    messagebox.showinfo("Éxito", f"{lugar} agregado correctamente a {vProvincia.get()}.")
    #Limpia el área de texto
    areaTexto.delete("1.0", tk.END)

def insertarLugar():
    """
    Funcionamiento:
    Crea una ventana secundaria que permite
    registrar nuevos lugares de donación
    asociados a una provincia.
    Entradas:
    Esta función no recibe entradas.

    Salidas:
    - Muestra una ventana para agregar
      lugares de donación.
    - Ejecuta la función insertar().
    """
    #Crea una nueva ventana
    ventanaInsertarLugar = tk.Toplevel()
    #Asigna el título de la ventana
    ventanaInsertarLugar.title("Insertar lugar")
    #Define el tamaño de la ventana
    ventanaInsertarLugar.geometry("400x500")
    #Etiqueta para seleccionar la provincia
    etiquetaProvincia = tk.Label(ventanaInsertarLugar,text = "Seleccione la provincia: ")
    etiquetaProvincia.pack()
    #Variable para almacenar la provincia seleccionada
    vProvincia = tk.StringVar()
    #Provincia por defecto
    vProvincia.set("San José")
    #Lista desplegable de provincias
    listaProvincia = tk.OptionMenu(ventanaInsertarLugar,vProvincia,*nombresProvincia.values())
    listaProvincia.pack()
    #Etiqueta para el nuevo lugar
    etiquetaLugar = tk.Label(ventanaInsertarLugar,text = "Nuevo lugar de donación:")
    etiquetaLugar.pack()
    #Área de texto para ingresar el lugar
    areaTexto = tk.Text(ventanaInsertarLugar, height = 3, width = 30)
    areaTexto.pack()
    #Botón para insertar el nuevo lugar
    botonInsertar = tk.Button(ventanaInsertarLugar,text="Insertar",command=lambda: insertar(areaTexto, vProvincia))
    botonInsertar.pack()
    #Botón para cerrar la ventana
    botonSalir = tk.Button(ventanaInsertarLugar, text="Salir",command=ventanaInsertarLugar.destroy)
    botonSalir.pack()

def reporteListaCompleta():
    """
    Funcionamiento:
    Genera un reporte HTML con la lista completa
    de donadores registrados en la base de datos.

    El reporte muestra información personal,
    tipo sanguíneo, fecha de nacimiento, peso,
    sexo, teléfono y correo electrónico de
    cada donador.

    Entradas:
    Esta función no recibe entradas.

    Salidas:
    - Genera un archivo HTML.
    - Muestra un mensaje de confirmación.
    """
    #Importa la clase para obtener fecha y hora actual
    from datetime import datetime
    #Obtiene la fecha y hora actuales
    ahora = datetime.now()
    #Genera una cadena con la fecha y hora
    fechaHora = ahora.strftime("%d-%m-%y-%H-%M-%S")
    #Crea el nombre del archivo HTML
    nombreHTML = "reporteListaCompleta_" + fechaHora + ".html"
    #Ordena los datos por provincia según la cédula
    datosOrdenados = sorted(baseDatos, key = lambda fila: fila[3][0])
    #Abre el archivo HTML para escritura
    html = open(nombreHTML, "w", encoding = "utf-8")
    html.write("<!DOCTYPE html>\n<html>\n<body>\n")
    html.write("<h1>Lista Completa de Donadores</h1>\n")
    html.write(f"<h2>{fechaHora}</h2>\n")
    html.write("<table border='1'>\n")
    html.write("<tr><th>Cédula</th><th>Nombre</th><th>Tipo Sangre</th><th>Fecha Nac.</th><th>Peso</th><th>Sexo</th><th>Teléfono</th><th>Correo</th></tr>\n")
    #Recorre todos los donadores registrados
    for fila in datosOrdenados:
        #Construye el nombre completo
        nombre = fila[0] + " " + fila[1] + " " + fila[2]
        #Obtiene el tipo de sangre
        sangre = tiposSangre[fila[4]]
        #Convierte la fecha a formato texto
        fecha = f"{fila[6][0]}/{fila[6][1]}/{fila[6][2]}"
        #Convierte el sexo a texto legible
        sexo = "Masculino" if fila[5] else "Femenino"
        #Agrega la fila al reporte
        html.write(f"<tr><td>{fila[3]}</td><td>{nombre}</td><td>{sangre}</td><td>{fecha}</td><td>{fila[7]}</td><td>{sexo}</td><td>{fila[9]}</td><td>{fila[8]}</td></tr>\n")
    html.write("</table>\n</body>\n</html>")
    #Cierra el archivo
    html.close()
    #Muestra mensaje de éxito
    messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")

def generarReporteQuienDonar(vTipo, ventana):
    """
    Funcionamiento:
    Genera un reporte HTML que muestra los
    donadores activos de un tipo sanguíneo
    específico y la compatibilidad de dicho
    tipo de sangre.
    Entradas:
    - vTipo(StringVar): Tipo de sangre
      seleccionado por el usuario.
    - ventana(Toplevel): Ventana desde la cual
      se genera el reporte.
    Salidas:
    - Genera un archivo HTML.
    - Muestra un mensaje de confirmación.
    """
    #Importa la clase para obtener fecha y hora actual
    from datetime import datetime
    #Obtiene la fecha y hora actuales
    ahora = datetime.now()
    #Genera una cadena con la fecha y hora
    fechaHora = ahora.strftime("%d-%m-%y-%H-%M-%S")
    #Crea el nombre del archivo HTML
    nombreHTML = "reporteQuienDonar_" + fechaHora + ".html"
    #Obtiene el tipo sanguíneo seleccionado
    tipoSeleccionado = vTipo.get()
    #Obtiene la posición del tipo sanguíneo
    indiceTipo = tiposSangre.index(tipoSeleccionado)
    #Obtiene los tipos de sangre compatibles
    puedeDonarA = compatibilidad[tipoSeleccionado]
    #Abre el archivo HTML para escritura
    html = open(nombreHTML, "w", encoding="utf-8")
    html.write("<!DOCTYPE html>\n<html>\n<body>\n")
    html.write("<h1>¿A quién puede donar?</h1>\n")
    html.write(f"<h2>{fechaHora}</h2>\n")
    html.write(f"<p>Tipo de sangre: {tipoSeleccionado} puede donar a: {', '.join(puedeDonarA)}</p>\n")
    html.write("<table border='1'>\n")
    html.write("<tr><th>Cédula</th><th>Nombre</th><th>Tipo Sangre</th><th>Teléfono</th><th>Correo</th></tr>\n")
    #Recorre la base de datos
    for fila in baseDatos:
        #Verifica que el tipo de sangre coincida y que el donador esté activo
        if fila[4] == indiceTipo and fila[10] == 1:
            #Construye el nombre completo
            nombre = fila[0] + " " + fila[1] + " " + fila[2]
            #Obtiene el tipo de sangre
            sangre = tiposSangre[fila[4]]
            #Agrega la fila al reporte
            html.write(f"<tr><td>{fila[3]}</td><td>{nombre}</td><td>{sangre}</td><td>{fila[9]}</td><td>{fila[8]}</td></tr>\n")
    html.write("</table>\n</body>\n</html>")
    #Cierra el archivo
    html.close()
    #Muestra mensaje de éxito
    messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")

def reporteNoActivos():
    """
    Funcionamiento:
    Genera un reporte HTML con todos los
    donadores inactivos registrados en la
    base de datos, incluyendo la razón por
    la cual dejaron de ser donadores activos.
    Entradas:
    Esta función no recibe entradas.
    Salidas:
    - Genera un archivo HTML.
    - Muestra un mensaje de confirmación.
    """
    #Importa la clase para obtener fecha y hora actual
    from datetime import datetime
    #Obtiene la fecha y hora actuales
    ahora = datetime.now()
    #Genera una cadena con la fecha y hora
    fechaHora = ahora.strftime("%d-%m-%y-%H-%M-%S")
    #Crea el nombre del archivo HTML
    nombreHTML = "reporteNoActivos_" + fechaHora + ".html"
    #Abre el archivo HTML para escritura
    html = open(nombreHTML, "w", encoding="utf-8")
    #Escribe la estructura inicial del documento
    html.write("<!DOCTYPE html>\n<html>\n<body>\n")
    #Escribe el título del reporte
    html.write("<h1>Donantes No Activos</h1>\n")
    #Escribe la fecha de generación
    html.write(f"<h2>{fechaHora}</h2>\n")
    #Crea la tabla principal
    html.write("<table border='1'>\n")
    #Escribe los encabezados de la tabla
    html.write("<tr><th>Justificación</th><th>Cédula</th><th>Nombre</th><th>Tipo Sangre</th><th>Fecha Nac.</th><th>Peso</th><th>Sexo</th><th>Teléfono</th><th>Correo</th></tr>\n")
    #Recorre todos los registros de la base de datos
    for fila in baseDatos:
        #Verifica que el donador esté inactivo
        if fila[10] == 0:
            #Construye el nombre completo
            nombre = fila[0] + " " + fila[1] + " " + fila[2]
            #Obtiene el tipo sanguíneo
            sangre = tiposSangre[fila[4]]
            #Convierte la fecha a formato texto
            fecha = f"{fila[6][0]}/{fila[6][1]}/{fila[6][2]}"
            #Convierte el sexo a texto legible
            sexo = "Masculino" if fila[5] else "Femenino"
            #Obtiene la justificación de inactividad
            justificacion = razones[fila[11]]
            #Agrega la fila al reporte
            html.write(f"<tr><td>{justificacion}</td><td>{fila[3]}</td><td>{nombre}</td><td>{sangre}</td><td>{fecha}</td><td>{fila[7]}</td><td>{sexo}</td><td>{fila[9]}</td><td>{fila[8]}</td></tr>\n")
    html.write("</table>\n</body>\n</html>")
    #Cierra el archivo
    html.close()
    #Muestra mensaje de éxito
    messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")

def validarEdadInicial(event, campoEdadInicial, campoEdadFinal):
    """
    Funcionamiento:
    Valida que la edad inicial ingresada se
    encuentre dentro del rango permitido para
    donadores y habilita o deshabilita el campo
    de edad final.
    Entradas:
    - event(Event): Evento generado por Tkinter.
    - campoEdadInicial(Entry): Campo de edad inicial.
    - campoEdadFinal(Entry): Campo de edad final.
    Salidas:
    - Habilita o deshabilita el campo de edad final.
    """
    #Obtiene la edad inicial ingresada
    edadInicial = campoEdadInicial.get()
    #Verifica que se hayan ingresado únicamente números
    if edadInicial.isdigit():
        #Convierte la edad a entero
        edad = int(edadInicial)
        #Verifica si está dentro del rango permitido
        if 18 <= edad <= 65:
            #Habilita el campo de edad final
            campoEdadFinal.config(state = "normal")
        else:
            #Deshabilita el campo de edad final
            campoEdadFinal.config(state = "disabled")

def generarReporteRangoEdad(campoEdadInicial, campoEdadFinal):
    """
    Funcionamiento:
    Genera un reporte HTML con los donadores
    activos que se encuentran dentro de una
    edad específica o dentro de un rango de edades.
    Entradas:
    - campoEdadInicial(Entry): Campo de edad inicial.
    - campoEdadFinal(Entry): Campo de edad final.
    Salidas:
    - Genera un archivo HTML.
    - Muestra un mensaje de confirmación.
    """
    #Importa las clases necesarias para trabajar con fechas
    from datetime import datetime, date
    #Obtiene la fecha y hora actuales
    ahora = datetime.now()
    #Genera una cadena con la fecha y hora
    fechaHora = ahora.strftime("%d-%m-%y-%H-%M-%S")
    #Crea el nombre del archivo HTML
    nombreHTML = "reporteRangoEdad_" + fechaHora + ".html"
    #Obtiene la edad inicial ingresada
    edadInicial = int(campoEdadInicial.get())
    #Obtiene la edad final ingresada
    edadFinal = campoEdadFinal.get()
    #Obtiene la fecha actual
    hoy = date.today()
    #Abre el archivo HTML para escritura
    html = open(nombreHTML, "w", encoding="utf-8")
    html.write("<!DOCTYPE html>\n<html>\n<body>\n")
    html.write("<h1>Reporte por Rango de Edad</h1>\n")
    html.write(f"<h2>{fechaHora}</h2>\n")
    html.write("<table border='1'>\n")
    html.write("<tr><th>Cédula</th><th>Nombre</th><th>Fecha Nac.</th><th>Teléfono</th><th>Correo</th></tr>\n")
    #Recorre todos los registros de la base de datos
    for fila in baseDatos:
        #Verifica que el donador esté activo
        if fila[10] == 1:
            #Calcula la edad aproximada
            edad = hoy.year - fila[6][2]
            #Determina si aún no ha cumplido años este año
            cumpleEste = (hoy.month, hoy.day) < (fila[6][1], fila[6][0])
            #Ajusta la edad si todavía no cumple años
            if cumpleEste:
                edad -= 1
            #Si no se ingresó edad final, busca una edad exacta
            if edadFinal == "":
                condicion = edad == edadInicial
            else:
                #Verifica si está dentro del rango indicado
                condicion = edadInicial <= edad <= int(edadFinal)
            #Genera el reporte únicamente si cumple la condición
            if condicion:
                #Construye el nombre completo
                nombre = fila[0] + " " + fila[1] + " " + fila[2]
                #Convierte la fecha a formato texto
                fecha = f"{fila[6][0]}/{fila[6][1]}/{fila[6][2]}"
                #Agrega la fila al reporte
                html.write(f"<tr><td>{fila[3]}</td><td>{nombre}</td><td>{fecha}</td><td>{fila[9]}</td><td>{fila[8]}</td></tr>\n")
    html.write("</table>\n</body>\n</html>")
    #Cierra el archivo
    html.close()
    #Muestra mensaje de éxito
    messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")

def reporteRangoEdad():
    """
    Funcionamiento:
    Crea una ventana que permite ingresar una
    edad inicial y una edad final para generar
    un reporte de donadores según su rango de edad.
    Entradas:
    Esta función no recibe entradas.
    Salidas:
    - Muestra una ventana para solicitar edades.
    - Ejecuta la generación del reporte por rango.
    """
    #Crea una nueva ventana para el reporte
    ventanaRangoEdad = tk.Toplevel()
    #Asigna el título de la ventana
    ventanaRangoEdad.title("Por rango de edad")
    #Define el tamaño de la ventana
    ventanaRangoEdad.geometry("400x300")
    #Etiqueta para la edad inicial
    etiquetaInicial = tk.Label(ventanaRangoEdad, text = "Edad inicial:")
    etiquetaInicial.pack()
    #Campo para ingresar la edad inicial
    campoEdadInicial = tk.Entry(ventanaRangoEdad)
    campoEdadInicial.pack()
    #Etiqueta para la edad final
    etiquetaFinal = tk.Label(ventanaRangoEdad, text = "Edad final:")
    etiquetaFinal.pack()
    #Campo para ingresar la edad final
    campoEdadFinal = tk.Entry(ventanaRangoEdad, state = "disabled")
    campoEdadFinal.pack()
    #Asocia la validación al salir del campo edad inicial
    campoEdadInicial.bind( "<FocusOut>", lambda event: validarEdadInicial(event, campoEdadInicial, campoEdadFinal))
    #Botón para generar el reporte
    botonGenerar = tk.Button(ventanaRangoEdad, text = "Generar reporte", command=lambda: generarReporteRangoEdad(campoEdadInicial, campoEdadFinal))
    botonGenerar.pack()
    #Botón para regresar
    botonRegresar = tk.Button(ventanaRangoEdad, text =" Regresar", command=ventanaRangoEdad.destroy)
    botonRegresar.pack()

def reporteQuienDonar():
    """
    Funcionamiento:
    Crea una ventana que permite seleccionar
    un tipo de sangre para generar un reporte
    de compatibilidad de donación.
    Entradas:
    Esta función no recibe entradas.
    Salidas:
    - Muestra una ventana de selección.
    - Ejecuta la generación del reporte.
    """
    #Crea una nueva ventana
    ventanaReporteQuienDonar = tk.Toplevel()
    #Asigna el título de la ventana
    ventanaReporteQuienDonar.title("¿A quién puede donar?")
    #Define el tamaño de la ventana
    ventanaReporteQuienDonar.geometry("400x500")
    #Etiqueta para seleccionar el tipo de sangre
    etiquetaTipo = tk.Label(ventanaReporteQuienDonar, text = "Seleccione el tipo de sangre: ")
    etiquetaTipo.pack()
    #Variable que almacena el tipo de sangre seleccionado
    vTipo = tk.StringVar()
    #Tipo de sangre por defecto
    vTipo.set("O+")
    #Lista desplegable de tipos sanguíneos
    listaTipo = tk.OptionMenu(ventanaReporteQuienDonar, vTipo, *tiposSangre)
    listaTipo.pack()
    #Botón para generar el reporte
    botonGenerar = tk.Button(ventanaReporteQuienDonar, text = "Generar reporte", command = lambda: generarReporteQuienDonar(vTipo, ventanaReporteQuienDonar))
    botonGenerar.pack()
    #Botón para regresar
    botonRegresar = tk.Button(ventanaReporteQuienDonar, text="Regresar", command = ventanaReporteQuienDonar.destroy)
    botonRegresar.pack()

def reportes():
    """
    Funcionamiento:
    Crea una ventana que centraliza todas las
    opciones de reportes disponibles dentro
    del sistema.
    Entradas:
    Esta función no recibe entradas.
    Salidas:
    - Muestra el menú de reportes.
    - Permite acceder a los distintos reportes.
    """
    #Crea una nueva ventana para los reportes
    ventanaReportes = tk.Toplevel()
    #Asigna el título de la ventana
    ventanaReportes.title("Reportes")
    #Define el tamaño de la ventana
    ventanaReportes.geometry("400x300")
    #Botón para reporte por rango de edad
    botonRangoEdad = tk.Button(ventanaReportes, text="Por rango de edad", command = reporteRangoEdad)
    botonRangoEdad.pack()
    #Botón para reporte de lista completa
    botonListaCompleta = tk.Button(ventanaReportes, text="Lista completa", command = reporteListaCompleta)
    botonListaCompleta.pack()
    #Botón para reporte de compatibilidad sanguínea
    botonQuienDonar = tk.Button(ventanaReportes, text="¿A quién puede donar?", command = reporteQuienDonar)
    botonQuienDonar.pack()
    #Botón para reporte de donadores no activos
    botonNoActivos = tk.Button(ventanaReportes, text="Donantes no activos", command = reporteNoActivos)
    botonNoActivos.pack()
    #Botón para regresar
    botonRegresar = tk.Button(ventanaReportes, text="Regresar", command = ventanaReportes.destroy)
    botonRegresar.pack()

def salir(ventana):
    """
    Funcionamiento:
    Muestra un mensaje de despedida y cierra
    la ventana principal de la aplicación.
    Entradas:
    - ventana(Tk): Ventana principal del sistema.
    Salidas:
    - Muestra un mensaje de despedida.
    - Finaliza la ejecución de la aplicación.
    """
    #Muestra un mensaje de despedida
    messagebox.showinfo("Hasta luego", "Donar sangre, es donar vida")
    #Cierra la ventana recibida como parámetro
    ventana.destroy()

