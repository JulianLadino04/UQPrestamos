import customtkinter as ctk
import logica.proyecto as proyecto
import tkinter as tk
import interfaces.ventanas.administrador.gestionar_empleados as ge

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

ids_sucursales = [str(id_sucursal) for id_sucursal in proyecto.id_sucursales()]
niveles_sistema = proyecto.enviar_niveles()
niveles_en_cadenas = [nivel[0] for nivel in niveles_sistema]
cargos_sistema = proyecto.enviar_cargos()
cargos_string = [cargo for cargo in cargos_sistema]

class RegistrarEmpleados:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Registrar Empleado")
        
        # Tamaño y posicionamiento de la ventana
        self.root.geometry("1000x500")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (700 // 2) - 70
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"1000x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")
        
        # Color de fondo principal
        bg_color = "#2b2b2b"
        
        # Frame contenedor principal, centrado en la ventana
        main_frame = ctk.CTkFrame(self.root, width=500, height=500, fg_color=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Registrar Empleado", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(20, 10))
        
        # Etiqueta para mostrar información sobre el registro
        self.info_create = ctk.CTkLabel(main_frame, text="", font=("Roboto", 18))
        self.info_create.pack(pady=(10, 10))
        
        # Formulario de entrada de datos
        form_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Etiquetas y campos del formulario
        # Primera columna
        ctk.CTkLabel(form_frame, text="Identificación", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.identificacion = ctk.CTkEntry(form_frame, width=200)
        self.identificacion.grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=200)
        self.nombre.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Salario", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.salario = ctk.CTkEntry(form_frame, width=200)
        self.salario.grid(row=2, column=1, padx=10, pady=5)

        # Segunda columna
        ctk.CTkLabel(form_frame, text="Nivel en Sistema", font=("Roboto", 18)).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.nivel_sis = tk.StringVar()
        nivel_combobox = ctk.CTkOptionMenu(
            form_frame,
            variable=self.nivel_sis,
            values=niveles_en_cadenas,
            width=200,
            command=self.habilitar_cargo  # Evento al seleccionar un nivel
        )
        nivel_combobox.grid(row=0, column=3, padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Cargo", font=("Roboto", 18)).grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.cargo = tk.StringVar()
        self.cargo_combobox = ctk.CTkOptionMenu(
            form_frame,
            variable=self.cargo,
            values=cargos_string,
            width=200,
            state="disabled"  # Deshabilitado por defecto
        )
        self.cargo_combobox.grid(row=1, column=3, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="ID Sucursal", font=("Roboto", 18)).grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.id_sucursal = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.id_sucursal, values=ids_sucursales, width=200).grid(row=2, column=3, padx=10, pady=5)

        # Tercera columna
        ctk.CTkLabel(form_frame, text="Usuario", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.usuario = ctk.CTkEntry(form_frame, width=200)
        self.usuario.grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Contraseña", font=("Roboto", 18)).grid(row=3, column=2, padx=10, pady=5, sticky="e")
        self.contrasena = ctk.CTkEntry(form_frame, width=200, show="*")
        self.contrasena.grid(row=3, column=3, padx=10, pady=5)
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        button_frame.pack(pady=(20, 10))

        register_button = ctk.CTkButton(button_frame, text="Registrar Empleado", command=self.validar_campos, height=40, width=200, font=("Roboto", 18, "bold"))
        register_button.grid(row=0, column=0, padx=10)

        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, height=40, width=200, font=("Roboto", 18, "bold"))
        salir_button.grid(row=0, column=1, padx=10)

    def habilitar_cargo(self, nivel_seleccionado):
        """
        Habilita o deshabilita el ComboBox de Cargo según el nivel seleccionado.
        """
        if nivel_seleccionado.lower() == "empleado":  # Si el nivel es 'Empleado'
            self.cargo_combobox.configure(state="normal")
        else:
            self.cargo_combobox.configure(state="disabled")

    def volver_principal(self):
        self.root.destroy()
        gestionar_empleados()

    def validar_campos(self):
        identificacion = self.identificacion.get()
        nombre = self.nombre.get()
        cargo = self.cargo.get()
        salario = self.salario.get()
        sucursal = self.id_sucursal.get()
        nivel = self.nivel_sis.get().strip()
        usuario = self.usuario.get()
        contrasena = self.contrasena.get()

        # Verificar campos obligatorios
        if identificacion == "" or nombre == "" or salario == "" or sucursal == "" or nivel == "" or usuario == "" or contrasena == "":
            self.info_create.configure(text="Hacen falta datos por llenar", fg_color="red")
            return

        # Verificar si el cargo está vacío, pero solo si el nivel no es "Tesoreria"
        if nivel != "Tesoreria" and cargo == "":
            self.info_create.configure(text="Hacen falta datos por llenar en el campo 'Cargo'", fg_color="red")
            return

        # Si el nivel es Tesoreria, establecer cargo como None
        if nivel == "Tesoreria":
            cargo = None  # o "" dependiendo de lo que soporte tu sistema

        # Verificar si el usuario ya existe
        if proyecto.verificar_credenciales(usuario, contrasena):
            self.info_create.configure(text="El usuario ingresado ya está en uso, utilice otro", fg_color="red")
            return

        # Registrar el empleado
        proyecto.crear_empleado(identificacion, nombre, cargo, salario, sucursal, nivel, usuario, contrasena)
        self.info_create.configure(text="Se registró correctamente", fg_color="green")  # Texto verde si el registro es exitoso
        print(f"Registrando empleado con Identificación: {identificacion}, Nombre: {nombre}, Cargo: {cargo}, Salario: {salario}, ID Sucursal: {sucursal}")


def gestionar_empleados():
    gestionar_empleados_window = ge.gestionar_empleados()
    gestionar_empleados_window.root.mainloop()