import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
import tkinter as tk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Obtener los IDs de las sucursales desde el módulo de lógica
ids_sucursales = [str(id_sucursal) for id_sucursal in proyecto.id_sucursales()]

niveles_sistema = proyecto.enviar_niveles()
niveles_en_cadenas = [nivel[0] for nivel in niveles_sistema]

cargos_sistema = proyecto.enviar_cargos()
cargos_string = [cargo[0] for cargo in cargos_sistema]


class RegistrarEmpleados:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Registro Empleados")
        self.root.geometry("750x450")
        self.root.resizable(False, False)
        print(cargos_sistema)
        
        # logo = ctk.CTkImage(
        #     light_image=Image.open(proyecto.enviar_imagen("registrar")),
        #     dark_image=Image.open(proyecto.enviar_imagen("registrar")),
        #     size=(200, 200)
        # )

        # etiqueta = ctk.CTkLabel(master=self.root, image=logo, text="GH")
        # etiqueta.pack(pady=15)
        # Frame para los campos
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Primera columna
        ctk.CTkLabel(form_frame, text="Identificación", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.identificacion = ctk.CTkEntry(form_frame, width=140)
        self.identificacion.grid(row=0, column=1, padx=10, pady=6, sticky="w")

        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=140)
        self.nombre.grid(row=1, column=1, padx=10, pady=6, sticky="w")

        ctk.CTkLabel(form_frame, text="Salario", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=6, sticky="e")
        self.salario = ctk.CTkEntry(form_frame, width=140)
        self.salario.grid(row=2, column=1, padx=10, pady=6, sticky="w")

        # Segunda columna
        ctk.CTkLabel(form_frame, text="Cargo", font=("Roboto", 18)).grid(row=0, column=2, padx=10, pady=6, sticky="e")
        self.cargo = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.cargo, values=cargos_string).grid(row=0, column=3, padx=10, pady=6, sticky="w")

        ctk.CTkLabel(form_frame, text="ID Sucursal", font=("Roboto", 18)).grid(row=1, column=2, padx=10, pady=6, sticky="e")
        self.id_sucursal = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.id_sucursal, values=ids_sucursales).grid(row=1, column=3, padx=10, pady=6, sticky="w")

        ctk.CTkLabel(form_frame, text="Nivel en Sistema", font=("Roboto", 18)).grid(row=2, column=2, padx=10, pady=6, sticky="e")
        self.nivel_sis = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.nivel_sis, values=niveles_en_cadenas).grid(row=2, column=3, padx=10, pady=6, sticky="w")

        # Botón para registrar empleado
        ctk.CTkButton(self.root, text="Registrar Empleado", command=self.validar_campos).pack(pady=20)

    def validar_campos(self):
        identificacion = self.identificacion.get()
        nombre = self.nombre.get()
        cargo = self.cargo.get()
        salario = self.salario.get()
        sucursal = self.id_sucursal.get()

        if identificacion == "" or nombre == "" or cargo == "" or salario == "" or sucursal == "":
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Se registró correctamente")
            self.info_create.pack()
            print(f"Registrando empleado con Identificación: {identificacion}, Nombre: {nombre}, Cargo: {cargo}, Salario: {salario}, ID Sucursal: {sucursal}")
    

