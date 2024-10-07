import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
import tkinter as tk
import interfaces.ventanas.administrador.gestionar_usuarios as ge

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Obtener los IDs de las sucursales desde el módulo de lógica
ids_sucursales = [str(id_sucursal) for id_sucursal in proyecto.id_sucursales()]

niveles_sistema = proyecto.enviar_niveles()
niveles_en_cadenas = [nivel[0] for nivel in niveles_sistema]

cargos_sistema = proyecto.enviar_cargos()
cargos_string = [cargo for cargo in cargos_sistema]

datos = []

def recibir_usuario(datos_usuario):
    global datos
    datos = datos_usuario
    print(datos_usuario)
    
class EditarUsuario:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Edición Empleados")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        # Frame para los campos
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configurar las columnas de forma proporcional para alinear mejor
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)
        form_frame.grid_columnconfigure(2, weight=1)
        form_frame.grid_columnconfigure(3, weight=2)
        
        # Primera columna
        ctk.CTkLabel(form_frame, text="Identificación", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.identificacion = ctk.CTkEntry(form_frame, width=140)
        self.identificacion.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        self.identificacion.insert(0, datos[0])
        self.identificacion.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=140)
        self.nombre.grid(row=1, column=1, padx=10, pady=6, sticky="w")
        self.nombre.insert(0, datos[4])

        ctk.CTkLabel(form_frame, text="Usuario", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=6, sticky="e")
        self.usuario = ctk.CTkEntry(form_frame, width=140)
        self.usuario.grid(row=2, column=1, padx=10, pady=6, sticky="w")
        self.usuario.insert(0, datos[1])

        ctk.CTkLabel(form_frame, text="Contraseña", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=6, sticky="e")
        self.contraseña = ctk.CTkEntry(form_frame, width=140)
        self.contraseña.grid(row=3, column=1, padx=10, pady=6, sticky="w")
        self.contraseña.insert(0, datos[2])

        ctk.CTkLabel(form_frame, text="Nivel en Sistema", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=6, sticky="e")
        self.nivel_sis = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.nivel_sis, values=niveles_en_cadenas).grid(row=4, column=1, padx=10, pady=6, sticky="w")
        self.nivel_sis.set(datos[3]) 
        
        # Botón para editar empleado
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20)

        editar_button = ctk.CTkButton(button_frame, text="Editar Usuario", command=self.editar_usuario, width=140)
        editar_button.grid(row=0, column=0, padx=20)

        # Botón para salir
        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, width=140)
        salir_button.grid(row=0, column=1, padx=20)

    # Definir el método para volver al menú principal
    def volver_principal(self):
        self.root.destroy()  # Cierra la ventana actual
        ge.gestionar_usuarios()  # Llama a la función que gestiona usuarios o el menú principal

    def editar_usuario(self):
        identificacion = self.identificacion.get()
        nombre = self.nombre.get()
        usuario = self.usuario.get()
        contraseña = self.contraseña.get()
        nivel = self.nivel_sis.get()

        if identificacion == "" or nombre == ""  or contraseña == ""  or usuario == "" or nivel == "" :
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            proyecto.editar_usuario(identificacion, usuario, contraseña, nivel, nombre)
            self.info_create = ctk.CTkLabel(self.root, text="Se edito correctamente")
            self.info_create.pack()
            print(f"Registrando empleado con Identificación: {identificacion}, Nombre: {nombre}, Usuario: {usuario}, Contraseña: {contraseña}, Nivel: {nivel}")

# Función para gestionar empleados o mostrar el menú principal
def gestionar_empleados():
    gestionar_empleados_window = ge.gestionar_usuarios()
    gestionar_empleados_window.root.mainloop()
