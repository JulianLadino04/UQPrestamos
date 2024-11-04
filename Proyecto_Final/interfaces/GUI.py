from datetime import datetime
import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
from tkinter import ttk
import tkinter as tk

import interfaces.ventanas.empleado.gestionar_solicitud_empleado as gse
import interfaces.ventanas.empleado.gestionar_pagos_empleado as gpe
import interfaces.ventanas.empleado.gestionar_estado_empleado as gee
import interfaces.ventanas.parametrico.gestionar_pagos_parametrico as gpp
import interfaces.ventanas.parametrico.gestionar_solicitud_parametrico as gsp
import interfaces.ventanas.administrador.gestionar_empleados as ge
import interfaces.ventanas.administrador.gestionar_pagos as gp
import interfaces.ventanas.administrador.gestionar_prestamos as gpre
import interfaces.ventanas.administrador.gestionar_solicitudes as gs
import interfaces.ventanas.administrador.gestionar_sucursales as gsc
import interfaces.ventanas.administrador.gestionar_usuarios as gu
import interfaces.ventanas.administrador.multitabla as mul
import interfaces.ventanas.administrador.ver_reportes as vr
import interfaces.ventanas.administrador.visualizar_ingresos as vi
import interfaces.ventanas.administrador.historial_solicitudes as hi

carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Login:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Proyecto Final Bases de Datos")

        # Tamaño y posicionamiento de la ventana
        self.root.geometry("750x500")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (750 // 2) + 150
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"750x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        logo = ctk.CTkImage(
            light_image=Image.open(os.path.join(carpeta_imagenes, "registrar.png")),
            dark_image=Image.open(os.path.join(carpeta_imagenes, "registrar.png")),
            size=(200, 200)
        )

        # Crear un marco principal para centrar los elementos
        main_frame = ctk.CTkFrame(self.root, fg_color=self.root.cget("bg"))
        main_frame.pack(expand=True)  # Permitir que el marco se expanda para centrar

        etiqueta = ctk.CTkLabel(master=main_frame, image=logo, text="")
        etiqueta.pack(pady=15)

        # Etiquetas y entradas con fuente más grande en Arial y negrita
        ctk.CTkLabel(main_frame, text="Usuario", font=("Arial", 14, "bold")).pack()
        self.usuario = ctk.CTkEntry(main_frame, font=("Arial", 14), width=150)
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, "end"))
        self.usuario.pack(pady=(0, 5))

        ctk.CTkLabel(main_frame, text="Contraseña", font=("Arial", 14, "bold")).pack()
        self.contrasena = ctk.CTkEntry(main_frame, show="*", font=("Arial", 14), width=150)
        self.contrasena.insert(0, "*********")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, "end"))
        self.contrasena.pack(pady=(0, 15))

        # Botón con fuente más grande en Arial y negrita
        ctk.CTkButton(main_frame, text="Entrar", command=self.validar_login, font=("Arial", 14, "bold"), width=150).pack(pady=10)

        self.root.mainloop()

    def validar_login(self):
        usuario = self.usuario.get()
        contrasena = self.contrasena.get()

        id_usuario_sesion = proyecto.verificar_credenciales(usuario, contrasena)

        if id_usuario_sesion is None:
            if hasattr(self, "info_login"):
                self.info_login.destroy()
            self.info_login = ctk.CTkLabel(self.root, text="Credenciales incorrectas", text_color="red", font=("Arial", 12))
            self.info_login.pack()
        else:
            if hasattr(self, "info_login"):
                self.info_login.destroy()
            self.info_login = ctk.CTkLabel(self.root, text="Usuario encontrado", text_color="green", font=("Arial", 12))
            self.info_login.pack()

            proyecto.almacenar_usuario_sistema(id_usuario_sesion)
            proyecto.hora_ingreso_usuario()

            self.root.destroy()
            tipo_usuario = proyecto.obtener_tipo_usuario(usuario)
            Opciones(tipo_usuario)

#FUNCIONES BOTONES USUARIO PARAMETRICOS
def gestionar_solicitud_parametrico():
    gestionar_solicitud_parametrico_window = gsp.gestionar_solicitud_parametrico()
    gestionar_solicitud_parametrico_window.root.mainloop()
      
def gestionar_pagos_parametrico():
    gestionar_pagos_parametrico_window = gpp.gestionar_pagos_parametricos()
    gestionar_pagos_parametrico_window.root.mainloop()
    
# FUNCIONES BOTONES USUARIO ADMINISTRADOR
def gestionar_usuarios():
    gestionar_usuarios_window = gu.gestionar_usuarios()
    gestionar_usuarios_window.root.mainloop()

def gestionar_sucursales(): 
    gestionar_sucursales_window = gsc.gestionar_sucursales()
    gestionar_sucursales_window.root.mainloop()

def gestionar_empleados():
    gestionar_empleados_window = ge.gestionar_empleados()
    gestionar_empleados_window.root.mainloop()

def gestionar_solicitudes():
    gestionar_solicitudes_window = gs.gestionar_solicitudes()
    gestionar_solicitudes_window.root.mainloop()

def gestionar_prestamos():
    gestionar_prestamos_window = gpre.gestionar_prestamos()
    gestionar_prestamos_window.root.mainloop()

def gestionar_pagos():
    gestionar_pagos_window = gp.gestionar_pagos()
    gestionar_pagos_window.root.mainloop()

def visualizar_ingresos():
    visualizar_ingresos_window = vi.visualizar_ingresos()
    visualizar_ingresos_window.root.mainloop()

def ver_reportes():
    ver_reportes_window = vr.ver_reportes()
    ver_reportes_window.root.mainloop()

def multitabla():
    multitabla_window = mul.multitabla()
    multitabla_window.root.mainloop()

def historial_solicitudes():
    historial_solicitudes = hi.HistorialPrestamos()
    historial_solicitudes.root.mainloop()

# FUNCIONES BOTONES USUARIO EMPLEADO
def gestionar_solicitud_empleado():
    gestionar_solicitud_empleado_window = gse.GestionarSolicitudEmpleado()
    gestionar_solicitud_empleado_window.root.mainloop()

def gestionar_pagos_empleado():
    gestionar_pagos_empleado_window = gpe.gestionar_pagos_empleado()
    gestionar_pagos_empleado_window.root.mainloop()

def gestionar_estado_empleado():
    gestionar_estado_empleado_window = gee.gestionar_estado_empleado()
    gestionar_estado_empleado_window.root.mainloop()

# Botones según tipo de usuario
botones_administrador = ['Gestionar Usuarios', 'Gestionar Sucursales', 'Gestionar Empleados', 'Gestionar Solicitudes',
                         'Gestionar Prestamos', 'Gestionar Pagos', 'Visualizar Ingresos',
                         'Ver Reportes', 'Historial Prestamos']

botones_parametrico = ['Gestionar Solicitudes', 'Gestionar Pagos']

botones_empleado = ['Gestionar Solicitudes', 'Gestionar Pagos']

# Funciones asociadas a los botones
funciones_botones_administrador = [gestionar_usuarios,gestionar_sucursales, gestionar_empleados,
                                   gestionar_solicitudes, gestionar_prestamos, gestionar_pagos,
                                   visualizar_ingresos, ver_reportes, historial_solicitudes]

funciones_botones_parametrico = [gestionar_solicitud_parametrico,
                                 gestionar_pagos_parametrico]

funciones_botones_empleado = [gestionar_solicitud_empleado, gestionar_pagos_empleado]

import customtkinter as ctk
from PIL import Image
import os

import customtkinter as ctk
from PIL import Image
import os

# Ventana de opciones según el tipo de usuario
class Opciones:
    def __init__(self, tipo: str):
        self.root = ctk.CTk()
        self.root.title("Opciones")
        self.root.geometry("1000x600")  # Aumenta el tamaño de la ventana
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))

        # Centrar la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1000 // 2) + 100
        y = (screen_height // 2) - (600 // 2)  # Aumenta el margen superior
        self.root.geometry(f"1000x600+{x}+{y}")

        # Configuración de la cuadrícula
        self.root.grid_rowconfigure(0, weight=1)  # Fila para el título
        self.root.grid_rowconfigure(1, weight=2)  # Fila para el logo
        self.root.grid_rowconfigure(2, weight=1)  # Fila para los botones
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Título en negrita
        titulo = ctk.CTkLabel(master=self.root, text="Funciones de " + tipo, height=32, font=("Roboto", 30, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(30, 10), sticky="nsew")  # Aumenta el padding superior

        # Logo
        logo = ctk.CTkImage(
            light_image=Image.open(os.path.join(carpeta_imagenes, "logo.png")),
            dark_image=Image.open(os.path.join(carpeta_imagenes, "logo.png")),
            size=(150, 150)  # Ajusta el tamaño del logo si es necesario
        )
        etiqueta = ctk.CTkLabel(master=self.root, image=logo, text="")
        etiqueta.grid(row=1, column=0, columnspan=3, pady=15, sticky="nsew")

        # Frame para contener los botones
        self.frame_botones = ctk.CTkFrame(master=self.root)
        self.frame_botones.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self._crear_botones(tipo)

        self.root.mainloop()

    def _crear_botones(self, tipo):
        botones = {
            "Empleado": botones_empleado,
            "Tesoreria": botones_parametrico,
            "Principal": botones_administrador
        }.get(tipo, [])

        funciones = {
            "Empleado": funciones_botones_empleado,
            "Tesoreria": funciones_botones_parametrico,
            "Principal": funciones_botones_administrador
        }.get(tipo, [])

        # Crear botones
        for contador, (texto_boton, funcion) in enumerate(zip(botones, funciones)):
            button = ctk.CTkButton(
                master=self.frame_botones,
                text=texto_boton,
                height=50,  # Altura fija
                width=120,  # Ancho fijo
                command=lambda f=funcion: [self.root.destroy(), f()],
                font=("Arial", 12, "bold")  # Botones en negrita
            )
            row = contador // 3
            column = contador % 3
            button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            # Configurar la columna para que tenga el mismo peso
            self.frame_botones.grid_columnconfigure(column, weight=1)

        # Botón Salir
        salir_button = ctk.CTkButton(
            master=self.frame_botones,
            text="Salir",
            height=50,  # Altura fija
            width=120,  # Ancho fijo
            command=self.volver_al_login,
            font=("Arial", 12, "bold")  # Botón Salir en negrita
        )
        salir_button.grid(row=row + 1, column=1, padx=10, pady=(20, 10), sticky="nsew")

    def volver_al_login(self):
        proyecto.hora_salida_usuario()
        self.root.destroy()
        Login()
