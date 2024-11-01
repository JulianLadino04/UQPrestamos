import customtkinter as ctk
import logica.proyecto as proyecto
import interfaces.ventanas.administrador.gestionar_empleados as ge
import tkinter as tk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Opciones obtenidas de la base de datos
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
        
        # Configuración de posicionamiento en pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (700 // 2) + 120
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"700x500+{x}+{y}")
        self.root.resizable(False, False)
        bg_color = "#2b2b2b"

        # Frame principal centrado
        main_frame = ctk.CTkFrame(self.root, width=500, height=500, fg_color=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título de la ventana
        title_label = ctk.CTkLabel(main_frame, text="Editar Empleado", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(20, 10))

        # Frame del formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configuración de las columnas
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        # Definir ancho uniforme para todos los campos
        field_width = 200

        # Etiquetas y campos de entrada
        ctk.CTkLabel(form_frame, text="Identificación", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.identificacion = ctk.CTkEntry(form_frame, width=field_width)
        self.identificacion.grid(row=0, column=1, padx=10, pady=5)
        self.identificacion.insert(0, datos[0])
        self.identificacion.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=field_width)
        self.nombre.grid(row=1, column=1, padx=10, pady=5)
        self.nombre.insert(0, datos[1])

        ctk.CTkLabel(form_frame, text="Cargo", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.cargo = ctk.CTkOptionMenu(form_frame, values=cargos_string, width=field_width)
        self.cargo.grid(row=2, column=1, padx=10, pady=5)
        self.cargo.set(datos[2])

        ctk.CTkLabel(form_frame, text="Salario", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.salario = ctk.CTkEntry(form_frame, width=field_width)
        self.salario.grid(row=3, column=1, padx=10, pady=5)
        self.salario.insert(0, str(datos[3]))

        ctk.CTkLabel(form_frame, text="ID Sucursal", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.id_sucursal = ctk.CTkOptionMenu(form_frame, values=ids_sucursales, width=field_width)
        self.id_sucursal.grid(row=4, column=1, padx=10, pady=5)
        self.id_sucursal.set(datos[4])

        ctk.CTkLabel(form_frame, text="Nivel en Sistema", font=("Roboto", 18)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.nivel_sis = ctk.CTkOptionMenu(form_frame, values=niveles_en_cadenas, width=field_width)
        self.nivel_sis.grid(row=5, column=1, padx=10, pady=5)
        self.nivel_sis.set(datos[5])

        # Etiqueta para mensajes de información
        self.info_update = ctk.CTkLabel(main_frame, text="", font=("Roboto", 14))
        self.info_update.pack(pady=(10, 0))

        # Frame de botones
        button_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        button_frame.pack(pady=(20, 10))

        edit_button = ctk.CTkButton(button_frame, text="Editar Empleado", command=self.validar_campos, height=40, width=field_width, font=("Roboto", 18, "bold"))
        edit_button.grid(row=0, column=0, padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=self.volver_principal, height=40, width=field_width, font=("Roboto", 18, "bold"))
        cancel_button.grid(row=0, column=1, padx=10)
    
    def volver_principal(self):
        self.root.destroy()
        ge.gestionar_empleados()

    def validar_campos(self):
        identificacion = self.identificacion.get()
        nombre = self.nombre.get()
        cargo = self.cargo.get()
        sucursal = self.id_sucursal.get()
        nivel = self.nivel_sis.get()

        # Validación para el campo salario
        try:
            salario = float(self.salario.get())
        except ValueError:
            self.info_update.configure(text="Salario debe ser un número válido", fg_color="red")
            return

        # Validación de campos vacíos
        if not all([identificacion, nombre, cargo, sucursal, nivel]):
            self.info_update.configure(text="Hacen falta datos por llenar", fg_color="red")
        else:
            proyecto.editar_empleado(identificacion, nombre, cargo, salario, sucursal, nivel)
            self.info_update.configure(text="Empleado editado correctamente", fg_color="green")

def gestionar_empleados():
    gestionar_empleados_window = ge.gestionar_empleados()
    gestionar_empleados_window.root.mainloop()
