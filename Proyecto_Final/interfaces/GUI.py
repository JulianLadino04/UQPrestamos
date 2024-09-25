import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
from tkinter import ttk
import tkinter as tk

import interfaces.ventanas.empleado.gestionar_solicitud_empleado as gse
import interfaces.ventanas.empleado.gestionar_pagos_empleado as gpe
import interfaces.ventanas.empleado.gestionar_estado_empleado as gee

import interfaces.ventanas.parametrico.consulta_multitabla_parametrico as cmp
import interfaces.ventanas.parametrico.gestionar_pagos_parametrico as gpp
import interfaces.ventanas.parametrico.gestionar_prestamos_parametrico as gprp
import interfaces.ventanas.parametrico.gestionar_solicitud_parametrico as gsp
import interfaces.ventanas.parametrico.ver_reportes_parametrico as vrp

import interfaces.ventanas.administrador.gestionar_empleados as ge
import interfaces.ventanas.administrador.gestionar_pagos as gp
import interfaces.ventanas.administrador.gestionar_prestamos as gpre
import interfaces.ventanas.administrador.gestionar_solicitudes as gs
import interfaces.ventanas.administrador.gestionar_sucursales as gsc
import interfaces.ventanas.administrador.gestionar_usuarios as gu
import interfaces.ventanas.administrador.multitabla as mul
import interfaces.ventanas.administrador.ver_reportes as vr
import interfaces.ventanas.administrador.visualizar_ingresos as vi

carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Login:
    def __init__(self):
        print(carpeta_principal)
        print(carpeta_imagenes)
        self.root = ctk.CTk()
        self.root.title("Proyecto Final Bases de Datos")
        print(self.root.iconbitmap(os.path.join(carpeta_imagenes, "registrar.ico")))
        self.root.geometry("750x450")
        self.root.resizable(False, False)

        logo = ctk.CTkImage(
            light_image=Image.open(os.path.join(carpeta_imagenes, "registrar.png")),
            dark_image=Image.open(os.path.join(carpeta_imagenes, "registrar.png")),
            size=(200, 200)
        )

        etiqueta = ctk.CTkLabel(master=self.root, image=logo, text="")
        etiqueta.pack(pady=15)

        ctk.CTkLabel(self.root, text="Usuario").pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, "end"))
        self.usuario.pack()

        ctk.CTkLabel(self.root, text="Contraseña").pack()
        self.contrasena = ctk.CTkEntry(self.root, show="*")
        self.contrasena.insert(0, "*********")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, "end"))
        self.contrasena.pack()

        ctk.CTkButton(self.root, text="Entrar", command=self.validar_login).pack(pady=10)

        self.root.mainloop()

    def validar_login(self):
        usuario = self.usuario.get()
        contrasena = self.contrasena.get()
        if proyecto.verificar_credenciales(usuario, contrasena):
            if hasattr(self, "info_login"):
                self.info_login.destroy()
            self.info_login = ctk.CTkLabel(self.root, text="Usuario encontrado")
            self.info_login.pack()
            # Cerrar la ventana de login
            self.root.destroy()
            tipo_usuario = proyecto.obtener_tipo_usuario(usuario)
            # Iniciar la ventana de opciones
            Opciones(tipo_usuario)
        else:
            if hasattr(self, "info_login"):
                self.info_login.destroy()
            self.info_login = ctk.CTkLabel(self.root, text="Credenciales incorrectas")
            self.info_login.pack()

#FUNCIONES BOTONES USUARIO PARAMETRICOS
def gestionar_solicitud_parametrico():
    gestionar_solicitud_parametrico_window = gsp.gestionar_solicitud_parametrico()
    gestionar_solicitud_parametrico_window.root.mainloop()
    
def gestionar_prestamos_parametrico():
    gestionar_prestamos_parametrico_window = gprp.gestionar_prestamos_parametrico()
    gestionar_prestamos_parametrico_window.root.mainloop()
    
def gestionar_pagos_parametrico():
    gestionar_pagos_parametrico_window = gpp.gestionar_pagos_parametrico()
    gestionar_pagos_parametrico_window.root.mainloop()
    
def ver_reportes_parametrico():
    ver_reportes_parametrico_window = vrp.ver_reportes_parametrico()
    ver_reportes_parametrico_window.root.mainloop()
    
def consulta_multitabla_parametrico():
    consulta_multitabla_parametrico_window = cmp.consulta_multitabla_parametrico()
    consulta_multitabla_parametrico_window.root.mainloop()

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

# FUNCIONES BOTONES USUARIO EMPLEADO
def gestionar_solicitud_empleado():
    gestionar_solicitud_empleado_window = gse.gestionar_solicitud_empleado()
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
                         'Ver Reportes', 'Consulta Multitabla']

botones_parametrico = ['Gestionar Solicitudes', 'Gestionar Prestamos', 'Gestionar Pagos',
                       'Ver Reportes', 'Consulta Multitabla']

botones_empleado = ['Gestionar Solicitudes', 'Gestionar Pagos', 'Estado Cuenta']

# Funciones asociadas a los botones
funciones_botones_administrador = [gestionar_usuarios,gestionar_sucursales, gestionar_empleados,
                                   gestionar_solicitudes, gestionar_prestamos, gestionar_pagos,
                                   visualizar_ingresos, ver_reportes, multitabla]

funciones_botones_parametrico = [gestionar_solicitud_parametrico, gestionar_prestamos_parametrico,
                                 gestionar_pagos_parametrico, ver_reportes_parametrico, consulta_multitabla_parametrico]

funciones_botones_empleado = [gestionar_solicitud_empleado, gestionar_pagos_empleado, gestionar_estado_empleado]

# Ventana de opciones según el tipo de usuario
class Opciones:
    def __init__(self, tipo: str):
        self.root = ctk.CTk()
        self.root.title("Opciones")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))
        self.root.geometry("750x450")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        titulo = ctk.CTkLabel(master=self.root, text="Funciones de usuario " + tipo, height=32, font=("Roboto", 30))
        titulo.grid(row=0, column=0, columnspan=3, pady=15, sticky="nsew")

        logo = ctk.CTkImage(
            light_image=Image.open(os.path.join(carpeta_imagenes, "logo.png")),
            dark_image=Image.open(os.path.join(carpeta_imagenes, "logo.png")),
            size=(200, 200)
        )
        etiqueta = ctk.CTkLabel(master=self.root, image=logo, text="")
        etiqueta.grid(row=1, column=0, columnspan=3, pady=15, sticky="nsew")

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

        for contador, (texto_boton, funcion) in enumerate(zip(botones, funciones)):
            button = ctk.CTkButton(
                master=self.root,
                text=texto_boton,
                height=40,
                width=200,
                command=lambda f=funcion: [self.root.destroy(), f()]  # Cierra la ventana actual y luego ejecuta la función
            )
            button.grid(row=2 + contador // 3, column=contador % 3, padx=10, pady=10, sticky="nsew")
            self.root.grid_columnconfigure(contador % 3, weight=1)
