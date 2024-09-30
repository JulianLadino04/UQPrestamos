import customtkinter as ctk
import os
import interfaces.GUI as ventana_principal
import logica.proyecto as proyecto
import tkinter as tk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Obtener los IDs de las sucursales desde el módulo de lógica
ids_sucursales = [str(id_sucursal) for id_sucursal in proyecto.id_sucursales()]

niveles_sistema = proyecto.enviar_niveles()
niveles_en_cadenas = [nivel[0] for nivel in niveles_sistema]

class RegistrarUsuarios:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Registro de Usuarios")
        self.root.geometry("750x450")
    
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Primera columna
        ctk.CTkLabel(form_frame, text="Identificación", font=("Roboto", 18)).pack( pady=6)
        self.identificacion = ctk.CTkEntry(form_frame, width=140)
        self.identificacion.pack(pady = 2)

        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).pack(pady=6)
        self.nombre = ctk.CTkEntry(form_frame, width=140)
        self.nombre.pack(pady = 2)

        ctk.CTkLabel(form_frame, text="Usuario", font=("Roboto", 18)).pack(pady=6)
        self.usuario = ctk.CTkEntry(form_frame, width=140)
        self.usuario.pack(pady = 2)

        ctk.CTkLabel(form_frame, text="Contraseña", font=("Roboto", 18)).pack(pady=6)
        self.contrasena = ctk.CTkEntry(form_frame, width=140)
        self.contrasena.pack(pady = 2)

        ctk.CTkLabel(form_frame, text="Nivel en Sistema", font=("Roboto", 18)).pack(pady=6)
        self.nivel_sis = tk.StringVar()
        
        ctk.CTkOptionMenu(form_frame, variable=self.nivel_sis, values=niveles_en_cadenas).pack(pady=6)
        # Botón para registrar empleado
        ctk.CTkButton(self.root, text="Registrar Usuario", command=self.registrar_usuario).pack(pady=20)
        # Botón para ir a la ventana de opciones
        ctk.CTkButton(self.root, text="Ir a Opciones", command=self.ir_a_opciones).pack(pady=10)


    def registrar_usuario(self):
        identificacion = self.identificacion.get()
        nombre = self.nombre.get()
        nivel = self.nivel_sis.get()
        usuario = self.usuario.get()
        contrasena = self.contrasena.get()

        if identificacion == "" or nombre == "" or nivel == "" or usuario == "" or contrasena == "":
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            proyecto.crear_usuario(identificacion, nombre, usuario, contrasena, nivel)
            self.info_create = ctk.CTkLabel(self.root, text="Se registró correctamente")
            self.info_create.pack()
            print(f"Registrando empleado con Identificación: {identificacion}, Nombre: {nombre}")

    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""
        self.root.destroy()  # Cierra la ventana de gestión de empleados
        tipo_usuario = proyecto.retornar_tipo_usuario()
        ventana_principal.Opciones(tipo_usuario)  # Llama a la ventana de opciones
        
    # Método de ejemplo para volver al menú principal
    def volver_principal(self):
        self.root.destroy()  # Cierra la ventana actual
        RegistrarUsuarios()

