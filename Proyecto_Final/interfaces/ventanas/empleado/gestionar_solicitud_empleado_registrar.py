import customtkinter as ctk
import tkinter as tk
import logica.proyecto as proyecto
from datetime import datetime
import interfaces.ventanas.empleado.gestionar_solicitud_empleado as ge

# Valores predefinidos para el periodo y el estado
periodos_disponibles = ["24", "36", "48", "60", "72"]
estados_disponibles = ["Pendiente", "Aprobado", "Rechazado"]

# Obtener el ID del usuario desde el sistema
id_usuario = proyecto.enviar_usuario_sesion()

class CrearSolicitudEmpleados:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Crear Nueva Solicitud de Empleado")
        self.root.geometry("500x500")  # Ajustamos el tamaño de la ventana
        self.root.resizable(False, False)

        # Crear el frame del formulario
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Campo para el ID del Empleado
        ctk.CTkLabel(form_frame, text="Identificación", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.id_empleado = ctk.CTkEntry(form_frame, width=140)
        self.id_empleado.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.id_empleado.insert(0, str(id_usuario[0]))  # Asignamos el ID del usuario
        self.id_empleado.configure(state="disabled")  # Deshabilitamos para que no se pueda editar

        # Campo para el Monto
        ctk.CTkLabel(form_frame, text="Monto", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.monto = ctk.CTkEntry(form_frame, width=140)
        self.monto.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Campo para el Periodo (usando OptionMenu)
        ctk.CTkLabel(form_frame, text="Periodo", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.periodo = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.periodo, values=periodos_disponibles).grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Botón para crear la nueva solicitud
        ctk.CTkButton(self.root, text="Crear Solicitud", command=self.validar_campos).pack(pady=20)

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
        ingresar_ventana_solicitud = ge.gestionar_solicitud_empleado()
        ingresar_ventana_solicitud.root.mainloop()

    def validar_campos(self):
        id_empleado = self.id_empleado.get()
        monto = self.monto.get()
        periodo = self.periodo.get()

        if "" in [monto, periodo]:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Faltan datos por llenar", text_color="red")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
        
            # Asumiendo que proyecto tiene una función para crear una nueva solicitud
            crear_solicitud(datetime.now(), id_empleado, monto, periodo)
            self.info_create = ctk.CTkLabel(self.root, text="Solicitud creada correctamente, en proceso de verificación", text_color="green")
            self.info_create.pack()
            print(f"Solicitud creada: ID Empleado: {id_empleado}, Monto: {monto}, Periodo: {periodo}")

def crear_solicitud(fecha_solicitud, empleado_id, monto, periodo):
    cargo = proyecto.obtener_cargo_usuario(empleado_id)

    # Definir los límites según el cargo
    limites_prestamo = {
        'Operario': 10000000.0,
        'Administrativo': 15000000.0,
        'Ejecutivo': 20000000.0,
        'Otros': 12000000.0
    }

    # Convertir monto a float si es necesario
    try:
        monto = float(monto)
    except ValueError:
        print(f"El monto '{monto}' no es un número válido.")
        return False  # Salir si el monto no es válido

    # Verificar si el monto solicitado es mayor al permitido
    if monto > limites_prestamo.get(cargo,float (0)):
        proyecto.crear_solicitud(fecha_solicitud, empleado_id, monto, periodo)
        print(f"La solicitud fue reprobada. El monto solicitado excede el límite permitido para el cargo {cargo}.")
    else:
        # Si el monto es válido, registrar la solicitud
        proyecto.crear_solicitud(fecha_solicitud, empleado_id, monto, periodo)
        print("Solicitud registrada con éxito.")
        return True  # Retorna True indicando que la solicitud se aprobó

# Función para gestionar empleados o mostrar el menú principal
def gestionar_empleados():
    gestionar_empleados_window = ge.gestionar_solicitud_empleado()
    gestionar_empleados_window.root.mainloop()

def calcular_fecha_desembolso():
    # Obtener el mes y año actuales
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.month
    ano_actual = fecha_actual.year
    
    # Calcular el siguiente mes
    if mes_actual == 12:
        # Si es diciembre, el siguiente mes es enero del próximo año
        siguiente_mes = 1
        ano_siguiente = ano_actual + 1
    else:
        # Caso general, simplemente sumamos un mes
        siguiente_mes = mes_actual + 1
        ano_siguiente = ano_actual

    # Crear la fecha para el día 3 del siguiente mes
    fecha_desembolso = datetime(ano_siguiente, siguiente_mes, 3)
    
    return fecha_desembolso