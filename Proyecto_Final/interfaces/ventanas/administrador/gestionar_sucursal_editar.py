import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
import tkinter as tk
import interfaces.ventanas.administrador.gestionar_sucursales as gs
import interfaces.ventanas.administrador.gestionar_sucursal_crear_municipio as crm

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Obtener los IDs de las sucursales desde el módulo de lógica


datos = []

def recibir_sucursales(datos_sucursal):
    global datos
    datos = datos_sucursal
    
class EditarSucursal:
    def __init__(self):
        municipios = [str(municipios) for municipios in proyecto.enviar_municipios()]
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Edición Sucursal")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        # Frame para los campos
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Inicializar self.municipio antes de usarlo
        self.nombre = ctk.StringVar()  # Crear una variable de control para el campo del municipio

        # Primera columna
        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=140)
        self.nombre.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        self.nombre.insert(0, datos[1])

         # Menú de opciones para el municipio
        ctk.CTkLabel(form_frame, text="Municipio", font=("Roboto", 18)).grid(row=0, column=2, padx=10, pady=6, sticky="e")
        
        self.municipio_elegido = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.municipio_elegido, values=municipios).grid(row=0, column=3, padx=10, pady=6, sticky="w")
        self.municipio_elegido.set(datos[2])
        # Botón para editar la sucursal
        ctk.CTkButton(self.root, text="Editar Sucursal", command=self.editar_sucursal).pack(pady=20)
        ctk.CTkButton(self.root, text="Crear Municipio", command=self.crear_municipio).pack(pady=20)
        ctk.CTkButton(self.root, text="Volver", command=self.volver_sucursales).pack(pady=20)

    # Definir el método para volver al menú principal
    def volver_sucursales(self):
        self.root.destroy()
        ingresar_ventana_creacion_sucursal = gs.gestionar_sucursales()
        ingresar_ventana_creacion_sucursal.root.mainloop()

    def crear_municipio(self):
        self.root.destroy()
        ingresar_ventana_creacion_sucursal = crm.CrearMunicipio()
        ingresar_ventana_creacion_sucursal.root.mainloop()

    def editar_sucursal(self):
        id_sucursal = datos[0]
        print(id_sucursal)
        nombre_municipio = self.nombre.get()
        print(nombre_municipio)
        municipio = self.municipio_elegido.get()
        print(municipio)
    
        if nombre_municipio == "" or municipio == "":
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            proyecto.editar_sucursal(id_sucursal, nombre_municipio, municipio)
            self.info_create = ctk.CTkLabel(self.root, text="Se editó correctamente")
            self.info_create.pack()
            print(f"Editando sucursal con nombre: {nombre_municipio}")
