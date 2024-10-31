import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
import tkinter as tk
import interfaces.ventanas.administrador.gestionar_sucursales as gs
import interfaces.ventanas.administrador.gestionar_sucursal_crear_municipio as crm

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

datos = []

def recibir_sucursales(datos_sucursal):
    global datos
    datos = datos_sucursal

class EditarSucursal:
    def __init__(self):
        municipios = [str(municipio) for municipio in proyecto.enviar_municipios()]
        
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Registrar Sucursal")
        self.root.geometry("1000x500")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (700 // 2) - 70
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"1000x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        # Frame principal para contener los elementos
        main_frame = ctk.CTkFrame(self.root, width=500, height=500, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Editar Sucursal", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(10, 10))

        # Mensaje de validación debajo del título
        self.validation_message = ctk.CTkLabel(main_frame, text="", font=("Roboto", 16), text_color="white", fg_color=None, corner_radius=8, padx=10, pady=5)
        self.validation_message.pack()

        # Frame para los campos de entrada
        fields_frame = ctk.CTkFrame(main_frame)
        fields_frame.pack(pady=10)

        # Campo para Nombre
        nombre_label = ctk.CTkLabel(fields_frame, text="Nombre", font=("Roboto", 18))
        nombre_label.grid(row=0, column=0, padx=(0, 10), sticky="e")
        self.nombre = ctk.CTkEntry(fields_frame, width=200)
        self.nombre.grid(row=0, column=1, pady=5)
        self.nombre.insert(0, datos[1])

        # Campo para Municipio
        municipio_label = ctk.CTkLabel(fields_frame, text="Municipio", font=("Roboto", 18))
        municipio_label.grid(row=1, column=0, padx=(0, 10), sticky="e")
        self.municipio_elegido = tk.StringVar()
        ctk.CTkOptionMenu(fields_frame, variable=self.municipio_elegido, values=municipios, width=200).grid(row=1, column=1, pady=5)
        self.municipio_elegido.set(datos[2])

        # Botones en un nuevo Frame debajo de los campos
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)

        edit_button = ctk.CTkButton(button_frame, text="Editar Sucursal", command=self.editar_sucursal, height=40, width=200, font=("Roboto", 18, "bold"))
        edit_button.grid(row=0, column=0, padx=10)

        create_municipio_button = ctk.CTkButton(button_frame, text="Crear Municipio", command=self.crear_municipio, height=40, width=200, font=("Roboto", 18, "bold"))
        create_municipio_button.grid(row=0, column=1, padx=10)

        volver_button = ctk.CTkButton(button_frame, text="Volver", command=self.volver_sucursales, height=40, width=200, font=("Roboto", 18, "bold"))
        volver_button.grid(row=0, column=2, padx=10)

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
        nombre_municipio = self.nombre.get()
        municipio = self.municipio_elegido.get()

        # Validación y actualización del mensaje
        if nombre_municipio == "" or municipio == "":
            self.validation_message.configure(text="Hacen falta datos por llenar", text_color="white", fg_color="red")
        else:
            proyecto.editar_sucursal(id_sucursal, nombre_municipio, municipio)
            self.validation_message.configure(text="Se editó correctamente", text_color="white", fg_color="green")

# Para iniciar la ventana
if __name__ == "__main__":
    app = EditarSucursal()
    app.root.mainloop()
