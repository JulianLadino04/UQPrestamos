import customtkinter as ctk
import tkinter as tk
import logica.proyecto as proyecto
import interfaces.ventanas.administrador.gestionar_solicitudes as ge

# Valores predefinidos para el periodo y el estado
periodos_disponibles = ["24", "36", "48", "60", "72"]
estados_disponibles = ["Pendiente", "Aprobado", "Rechazado"]

# Datos globales que serán recibidos
datos = []

# Función para recibir datos
def recibir_solicitud(datos_recibidos):
    global datos
    datos = datos_recibidos

class EditarSolicitudAdministradores:
    def __init__(self, datos_recibidos):  # Modificado para aceptar datos
        global datos
        datos = datos_recibidos  # Asignar los datos recibidos

        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Editar Solicitud de Empleado")
        self.root.geometry("1000x500")
        self.root.configure(background="#2b2b2b")

        # Cálculo para centrar la ventana y desplazarla hacia la derecha
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1000 // 2) 
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"1000x500+{x}+{y}")
        self.root.resizable(False, False)

        bg_color = "#2b2b2b"

        main_frame = ctk.CTkFrame(self.root, width=500, height=500, fg_color=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título en la parte superior del formulario
        title_label = ctk.CTkLabel(main_frame, text="Editar Solicitud de Empleado", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configurar las columnas de forma proporcional
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        # Campo para el ID Solicitud
        ctk.CTkLabel(form_frame, text="ID Solicitud", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.id_solicitud = ctk.CTkEntry(form_frame, width=200)
        self.id_solicitud.grid(row=0, column=1, padx=10, pady=5)
        self.id_solicitud.insert(0, datos[0])  # Suponiendo que el ID está en datos[0]
        self.id_solicitud.configure(state="disabled")

        # Campo para la Fecha
        ctk.CTkLabel(form_frame, text="Fecha", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.fecha = ctk.CTkEntry(form_frame, width=200)
        self.fecha.grid(row=1, column=1, padx=10, pady=5)
        self.fecha.insert(0, datos[1])  # Suponiendo que la fecha está en datos[1]
        self.fecha.configure(state="disabled")

        # Campo para el ID del Empleado
        ctk.CTkLabel(form_frame, text="ID Empleado", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.id_empleado = ctk.CTkEntry(form_frame, width=200)
        self.id_empleado.grid(row=2, column=1, padx=10, pady=5)
        self.id_empleado.insert(0, datos[2])  # Suponiendo que el ID del empleado está en datos[2]
        self.id_empleado.configure(state="disabled")

        # Campo para el Monto
        ctk.CTkLabel(form_frame, text="Monto", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.monto = ctk.CTkEntry(form_frame, width=200)
        self.monto.grid(row=3, column=1, padx=10, pady=5)
        self.monto.insert(0, datos[3])  # Suponiendo que el monto está en datos[3]

        # Campo para el Periodo (usando OptionMenu)
        ctk.CTkLabel(form_frame, text="Periodo", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.periodo = tk.StringVar(value=datos[4])  # Suponiendo que el periodo está en datos[4]
        self.periodo_optionmenu = ctk.CTkOptionMenu(form_frame, variable=self.periodo, values=periodos_disponibles)
        self.periodo_optionmenu.grid(row=4, column=1, padx=10, pady=5)

        # Campo para el Estado (usando Entry deshabilitado en lugar de OptionMenu)
        ctk.CTkLabel(form_frame, text="Estado", font=("Roboto", 18)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.estado_label = ctk.CTkEntry(form_frame, font=("Roboto", 18), width=200)  # Cambié el ancho para igualar
        self.estado_label.grid(row=5, column=1, padx=10, pady=5)
        self.estado_label.insert(0, datos[5])  # Inserta el valor del estado en la posición 0
        self.estado_label.configure(state="disabled")  # Deshabilitamos el campo para que no sea editable

        # Campo para la Tasa de Interés
        ctk.CTkLabel(form_frame, text="Tasa de Interés", font=("Roboto", 18)).grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.tasa_interes = ctk.CTkEntry(form_frame, width=200)
        self.tasa_interes.grid(row=6, column=1, padx=10, pady=5)
        self.tasa_interes.insert(0, datos[6])  # Suponiendo que la tasa de interés está en datos[6]

        # Frame para los botones
        button_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        button_frame.pack(pady=(20, 10))

        # Botón para guardar los cambios
        self.guardar_button = ctk.CTkButton(button_frame, text="Guardar Cambios", command=self.validar_campos, height=40, width=200, font=("Roboto", 18, "bold"))
        self.guardar_button.grid(row=0, column=0, padx=10)

        # Botón para salir y volver al menú principal
        self.salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, height=40, width=200, font=("Roboto", 18, "bold"))
        self.salir_button.grid(row=0, column=1, padx=10)

        # Mensaje de información de validación inicializado como etiqueta vacía
        self.info_update = ctk.CTkLabel(main_frame, text="", font=("Roboto", 14))
        self.info_update.pack(pady=(10, 0))

    # Método para volver al menú principal
    def volver_principal(self):
        self.root.destroy()
        ingresar_ventana_solicitud = ge.gestionar_solicitudes()
        ingresar_ventana_solicitud.root.mainloop()

    def validar_campos(self):
        id_solicitud = self.id_solicitud.get()
        fecha = self.fecha.get()
        id_empleado = self.id_empleado.get()
        monto = self.monto.get()
        periodo = self.periodo.get()
        estado = self.estado_label.get()  # Cambié esto para usar el valor del estado
        tasa_interes = self.tasa_interes.get()

        if "" in [id_solicitud, fecha, id_empleado, monto, periodo, estado, tasa_interes]:
            self.info_update.configure(text="Faltan datos por llenar", fg_color="red")
        else:
            proyecto.editar_solicitud(id_empleado, id_solicitud, monto, periodo)
            self.info_update.configure(text="Datos editados correctamente", fg_color="green")

# Función para gestionar empleados o mostrar el menú principal
def gestionar_empleados():
    gestionar_empleados_window = ge.gestionar_solicitudes()
    gestionar_empleados_window.root.mainloop()
