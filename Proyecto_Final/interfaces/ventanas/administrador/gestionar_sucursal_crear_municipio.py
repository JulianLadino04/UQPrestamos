import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
import tkinter as tk
import interfaces.ventanas.administrador.gestionar_sucursales as gs
import interfaces.ventanas.administrador.gestionar_sucursal_registrar as regs
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
    
class CrearMunicipio:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Creacion Municipio")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        # Frame para los campos
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Primera columna
        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=140)
        self.nombre.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        
        # Botón para registrar empleado
        ctk.CTkButton(self.root, text="Crear Municipio", command=self.crear_municipio).pack(pady=20)
        ctk.CTkButton(self.root, text="Volver", command=self.volver_principal).pack(pady=20)
    

    # Definir el método para volver al menú principal
    def volver_principal(self):
        self.root.destroy()
        ingresar_ventana_creacion_sucursal = gs.gestionar_sucursales()
        ingresar_ventana_creacion_sucursal.root.mainloop() # Llama a la función que gestiona empleados o el menú principal

    def crear_municipio(self):
        nombre = self.nombre.get()
    
        if nombre == "":
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            proyecto.crear_municipio(nombre)
            self.info_create = ctk.CTkLabel(self.root, text="Se edito correctamente")
            self.info_create.pack()
            print(f"Creando municipio con nombre: {nombre}" )

    