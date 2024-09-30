import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
import tkinter as tk
import interfaces.ventanas.administrador.gestionar_empleados as ge
import interfaces.ventanas.administrador.gestionar_sucursal_crear_municipio as crm
import interfaces.ventanas.administrador.gestionar_sucursales as gs

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
municipios = [str(municipios) for municipios in proyecto.enviar_municipios()]

class RegistrarSucursal:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Registro Empleados")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        # Frame para los campos
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Primera columna
        ctk.CTkLabel(form_frame, text="Id Sucursal", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.identificacion = ctk.CTkEntry(form_frame, width=140)
        self.identificacion.grid(row=0, column=1, padx=10, pady=6, sticky="w")

        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=140)
        self.nombre.grid(row=1, column=1, padx=10, pady=6, sticky="w")

        # Definir self.municipio_elegido como un tk.StringVar
        self.municipio_elegido = tk.StringVar()

        # Menú de opciones para el municipio
        ctk.CTkLabel(form_frame, text="Municipio", font=("Roboto", 18)).grid(row=0, column=2, padx=10, pady=6, sticky="e")
        ctk.CTkOptionMenu(form_frame, variable=self.municipio_elegido, values=municipios).grid(row=0, column=3, padx=10, pady=6, sticky="w")
        
        # Botón para registrar sucursal
        ctk.CTkButton(self.root, text="Registrar Sucursal", command=self.registrar_sucursal).pack(pady=20)
        ctk.CTkButton(self.root, text="Crear Municipio", command=self.crear_municipio).pack(pady=20)
        ctk.CTkButton(self.root, text="Volver", command=self.volver_sucursales).pack(pady=20)
    

    def crear_municipio(self):
        self.root.destroy()
        ingresar_ventana_creacion_sucursal = crm.CrearMunicipio()
        ingresar_ventana_creacion_sucursal.root.mainloop()
        
    # Definir el método para volver al menú principal
    def volver_sucursales(self):
        ingresar_ventana_creacion_sucursal = gs.gestionar_sucursales()
        ingresar_ventana_creacion_sucursal.root.mainloop() 

    def registrar_sucursal(self):
        id_sucursal = self.identificacion.get()
        nombre = self.nombre.get()
        municipio = self.municipio_elegido.get()
        
        if id_sucursal == "" or nombre == "" or municipio == "":
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            proyecto.crear_sucursal(id_sucursal, nombre, municipio)
            self.info_create = ctk.CTkLabel(self.root, text="Se registró correctamente")
            self.info_create.pack()
        
