import customtkinter as ctk
import tkinter as tk
import logica.proyecto as proyecto
import interfaces.ventanas.empleado.gestionar_solicitud_empleado as ge

# Valores predefinidos para el periodo y el estado
periodos_disponibles = ["24", "36", "48", "60", "72"]
estados_disponibles = ["PENDIENTE", "APROBADO", "RECHAZADO"]

# Datos globales que serán recibidos
datos = []

# Función para recibir datos (similar a recibir_empleado)
def recibir_solicitud(datos_recibidos):
    global datos
    datos = datos_recibidos
    print(datos)

class EditarSolicitudEmpleados:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Editar Solicitud de Empleado")
        self.root.geometry("500x500")  # Ajustamos el tamaño de la ventana

        # Centrar la ventana en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"500x500+{x}+{y}")
        
        self.root.resizable(False, False)

        # Crear el frame del formulario
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Campo para el ID
        ctk.CTkLabel(form_frame, text="ID Solicitud", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.id_solicitud = ctk.CTkEntry(form_frame, width=140)
        self.id_solicitud.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.id_solicitud.insert(0, datos[0])  # Suponiendo que el ID está en datos[0]
        self.id_solicitud.configure(state="disabled")

        # Campo para la Fecha
        ctk.CTkLabel(form_frame, text="Fecha", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.fecha = ctk.CTkEntry(form_frame, width=140)
        self.fecha.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.fecha.insert(0, datos[1])  # Suponiendo que la fecha está en datos[1]
        self.fecha.configure(state="disabled")

        # Campo para el ID del Empleado
        ctk.CTkLabel(form_frame, text="ID Empleado", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.id_empleado = ctk.CTkEntry(form_frame, width=140)
        self.id_empleado.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.id_empleado.insert(0, datos[2])  # Suponiendo que el ID del empleado está en datos[2]
        self.id_empleado.configure(state="disabled")

        # Campo para el Monto
        ctk.CTkLabel(form_frame, text="Monto", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.monto = ctk.CTkEntry(form_frame, width=140)
        self.monto.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.monto.insert(0, datos[3])  # Suponiendo que el monto está en datos[3]

        # Campo para el Periodo (usando OptionMenu)
        ctk.CTkLabel(form_frame, text="Periodo", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.periodo = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.periodo, values=periodos_disponibles).grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.periodo.set(datos[4])  # Suponiendo que el periodo está en datos[4]

        # Campo para el Estado (usando Entry deshabilitado en lugar de OptionMenu)
        ctk.CTkLabel(form_frame, text="Estado", font=("Roboto", 18)).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.estado_label = ctk.CTkEntry(form_frame, font=("Roboto", 18))  # Creamos el Entry
        self.estado_label.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Insertamos el valor del estado y luego lo deshabilitamos
        self.estado_label.insert(0, datos[5])  # Inserta el valor del estado en la posición 0
        self.estado_label.configure(state="disabled")  # Deshabilitamos el campo para que no sea editable



        # Campo para la Tasa de Interés
        ctk.CTkLabel(form_frame, text="Tasa de Interés", font=("Roboto", 18)).grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.tasa_interes = ctk.CTkEntry(form_frame, width=140)
        self.tasa_interes.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        self.tasa_interes.insert(0, datos[6])  # Suponiendo que la tasa de interés está en datos[6]
        self.tasa_interes.configure(state="disabled")

        # Botón para guardar los cambios
        ctk.CTkButton(self.root, text="Guardar Cambios", command=self.validar_campos).pack(pady=20)

        # Botón para salir y volver al menú principal
        salir_button = ctk.CTkButton(
            master=self.root,
            text="Salir",
            height=40,
            width=200,
            command=self.volver_principal  # Asignamos la función aquí
        )
        salir_button.pack(pady=10)

    # Método para volver al menú principal
    def volver_principal(self):
        self.root.destroy()
        ingresar_ventana_solicitud = ge.GestionarSolicitudEmpleado()
        ingresar_ventana_solicitud.root.mainloop()

    def validar_campos(self):
        id_solicitud = self.id_solicitud.get()
        fecha = self.fecha.get()
        id_empleado = self.id_empleado.get()
        monto = self.monto.get()
        periodo = self.periodo.get()
        estado = self.estado_label.get()
        tasa_interes = self.tasa_interes.get()

        if "" in [id_solicitud, fecha, id_empleado, monto, periodo, estado, tasa_interes]:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Faltan datos por llenar", text_color="red")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            # Asumiendo que proyecto tiene una función para editar todos estos campos
            if (estado == 'PENDIENTE'):
                proyecto.editar_solicitud(datos[2], id_solicitud, monto, periodo)
                self.info_create = ctk.CTkLabel(self.root, text="Datos editados correctamente", text_color="green")
                self.info_create.pack()
                print(f"Editando solicitud ID: {id_solicitud}, Fecha: {fecha}, ID Empleado: {id_empleado}, Monto: {monto}, Periodo: {periodo}, Estado: {estado}, Tasa de Interés: {tasa_interes}")
            else:
                self.info_create = ctk.CTkLabel(self.root, text="La solicitud no se puede editar", text_color="red")
                self.info_create.pack()
                

# Función para gestionar empleados o mostrar el menú principal
def gestionar_empleados():
    gestionar_empleados_window = ge.gestionar_solicitud_empleado()
    gestionar_empleados_window.root.mainloop()
