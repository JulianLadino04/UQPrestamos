import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
import tkinter as tk
import interfaces.ventanas.administrador.gestionar_empleados as ge

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

ids_sucursales = [str(id_sucursal) for id_sucursal in proyecto.id_sucursales()]
niveles_sistema = proyecto.enviar_niveles()
niveles_en_cadenas = [nivel[0] for nivel in niveles_sistema]
cargos_sistema = proyecto.enviar_cargos()
cargos_string = [cargo for cargo in cargos_sistema]

datos = []

def recibir_empleado(datos_empleado):
    global datos
    datos = datos_empleado

class EditarEmpleados:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Editar Empleado")
        self.root.geometry("700x500")
        self.root.configure(background="#2b2b2b")

        # Cálculo para centrar la ventana y desplazarla hacia la derecha
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (700 // 2) + 120  # Añade 90 píxeles a la derecha
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"700x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        # Color de fondo principal
        bg_color = "#2b2b2b"  # Ajusta este color según el tema de tu ventana principal

        # Frame contenedor principal, centrado en la ventana
        main_frame = ctk.CTkFrame(self.root, width=500, height=500, fg_color=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centra el frame en la ventana

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Editar Empleado", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(20, 10))

        # Formulario de entrada de datos, centrado
        form_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Etiquetas y campos del formulario
        ctk.CTkLabel(form_frame, text="Identificación", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.identificacion = ctk.CTkEntry(form_frame, width=200)
        self.identificacion.grid(row=0, column=1, padx=10, pady=5)
        self.identificacion.insert(0, datos[0])
        self.identificacion.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=200)
        self.nombre.grid(row=1, column=1, padx=10, pady=5)
        self.nombre.insert(0, datos[1])

        ctk.CTkLabel(form_frame, text="Salario", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.salario = ctk.CTkEntry(form_frame, width=200)
        self.salario.grid(row=2, column=1, padx=10, pady=5)
        self.salario.insert(0, datos[3])

        ctk.CTkLabel(form_frame, text="Cargo", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.cargo = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.cargo, values=cargos_string, width=200).grid(row=3, column=1, padx=10, pady=5)
        self.cargo.set(datos[2])

        ctk.CTkLabel(form_frame, text="ID Sucursal", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.id_sucursal = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.id_sucursal, values=ids_sucursales, width=200).grid(row=4, column=1, padx=10, pady=5)
        self.id_sucursal.set(datos[4])

        ctk.CTkLabel(form_frame, text="Nivel en Sistema", font=("Roboto", 18)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.nivel_sis = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.nivel_sis, values=niveles_en_cadenas, width=200).grid(row=5, column=1, padx=10, pady=5)
        self.nivel_sis.set(datos[5])

        # Botones, colocados juntos y centrados
        button_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        button_frame.pack(pady=(20, 10))

        edit_button = ctk.CTkButton(button_frame, text="Editar Empleado", command=self.validar_campos, height=40, width=200, font=("Roboto", 18, "bold"))
        edit_button.grid(row=0, column=0, padx=10)

        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, height=40, width=200, font=("Roboto", 18, "bold"))
        salir_button.grid(row=0, column=1, padx=10)

    # Otros métodos sin cambios


    def volver_principal(self):
        self.root.destroy()
        gestionar_empleados()

    def validar_campos(self):
        identificacion = self.identificacion.get()
        nombre = self.nombre.get()
        cargo = self.cargo.get()
        salario = self.salario.get()
        sucursal = self.id_sucursal.get()
        nivel = self.nivel_sis.get()

        if identificacion == "" or nombre == "" or cargo == "" or salario == "" or sucursal == "" or nivel == "":
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            proyecto.editar_empleado(identificacion, nombre, cargo, salario, sucursal, nivel)
            self.info_create = ctk.CTkLabel(self.root, text="Se editó correctamente")
            self.info_create.pack()
            print(f"Registrando empleado con Identificación: {identificacion}, Nombre: {nombre}, Cargo: {cargo}, Salario: {salario}, ID Sucursal: {sucursal}")

def gestionar_empleados():
    gestionar_empleados_window = ge.gestionar_empleados()
    gestionar_empleados_window.root.mainloop()
