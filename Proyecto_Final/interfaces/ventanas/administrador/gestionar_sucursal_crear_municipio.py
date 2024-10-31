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
        
        self.root = ctk.CTk()
        self.root.title("Crear Municipio")
        # Reducir tamaño de la ventana
        self.root.geometry("600x400")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (400 // 2)
        self.root.geometry(f"800x400+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")


        # Frame principal para contener los elementos
        main_frame = ctk.CTkFrame(self.root, width=500, height=500, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Crear Municipio", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(10, 10))

        # Mensaje de validación debajo del título
        self.validation_message = ctk.CTkLabel(main_frame, text="", font=("Roboto", 16), text_color="white", fg_color=None, corner_radius=8, padx=10, pady=5)
        self.validation_message.pack()

        # Frame para el campo de entrada
        fields_frame = ctk.CTkFrame(main_frame)
        fields_frame.pack(pady=10)

        # Campo para Nombre
        nombre_label = ctk.CTkLabel(fields_frame, text="Nombre", font=("Roboto", 18))
        nombre_label.grid(row=0, column=0, padx=(0, 10), sticky="e")
        self.nombre = ctk.CTkEntry(fields_frame, width=200)
        self.nombre.grid(row=0, column=1, pady=5)

        # Botones en un nuevo Frame debajo del campo de nombre
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)

        crear_button = ctk.CTkButton(button_frame, text="Crear Municipio", command=self.crear_municipio, height=40, width=200, font=("Roboto", 18, "bold"))
        crear_button.grid(row=0, column=0, padx=10)

        volver_button = ctk.CTkButton(button_frame, text="Volver", command=self.volver_principal, height=40, width=200, font=("Roboto", 18, "bold"))
        volver_button.grid(row=0, column=1, padx=10)

    def volver_principal(self):
        self.root.destroy()
        ingresar_ventana_creacion_sucursal = gs.gestionar_sucursales()
        ingresar_ventana_creacion_sucursal.root.mainloop()

    def crear_municipio(self):
        nombre = self.nombre.get()

        # Validación y actualización del mensaje
        if nombre == "":
            self.validation_message.configure(text="Hacen falta datos por llenar", text_color="white", fg_color="red")
        else:
            proyecto.crear_municipio(nombre)
            self.validation_message.configure(text="Se creó correctamente", text_color="white", fg_color="green")
            print(f"Creando municipio con nombre: {nombre}")

# Para iniciar la ventana
if __name__ == "__main__":
    app = CrearMunicipio()
    app.root.mainloop()
