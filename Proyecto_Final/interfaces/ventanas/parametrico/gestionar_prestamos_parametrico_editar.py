import customtkinter as ctk
import os
import logica.proyecto as proyecto
import tkinter as tk
import interfaces.ventanas.parametrico.gestionar_prestamos_parametrico as gp

# Obtener los valores requeridos desde el módulo de lógica
empleados_ids = [str(id_empleado) for id_empleado in proyecto.enviar_id_empleados()]  # IDs de empleados disponibles
estados_disponibles = ["Pendiente", "Aprobado", "Rechazado"]

datos_prestamo = []

def recibir_prestamo(datos_prestamo_param):
    global datos_prestamo
    datos_prestamo = datos_prestamo_param
    print(datos_prestamo)

class EditarPrestamoParametrico:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Edición Préstamos")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        # Frame para los campos
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configurar las columnas de forma proporcional para alinear mejor
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)
        form_frame.grid_columnconfigure(2, weight=1)
        form_frame.grid_columnconfigure(3, weight=2)

        # Campos para el préstamo
        ctk.CTkLabel(form_frame, text="ID Solicitud", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.id_solicitud = ctk.CTkEntry(form_frame, width=140)
        self.id_solicitud.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        self.id_solicitud.insert(0, datos_prestamo[0])
        self.id_solicitud.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Fecha Solicitud", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.fecha_solicitud = ctk.CTkEntry(form_frame, width=140)
        self.fecha_solicitud.grid(row=1, column=1, padx=10, pady=6, sticky="w")
        self.fecha_solicitud.insert(0, datos_prestamo[1])
        self.fecha_solicitud.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Empleado ID", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=6, sticky="e")
        self.empleado_id = ctk.CTkOptionMenu(form_frame, values=empleados_ids)
        self.empleado_id.grid(row=2, column=1, padx=10, pady=6, sticky="w")
        self.empleado_id.set(datos_prestamo[2])
        self.empleado_id.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Monto", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=6, sticky="e")
        self.monto = ctk.CTkEntry(form_frame, width=140)
        self.monto.grid(row=3, column=1, padx=10, pady=6, sticky="w")
        self.monto.insert(0, datos_prestamo[3])

        ctk.CTkLabel(form_frame, text="Periodo", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=6, sticky="e")
        self.periodo = ctk.CTkEntry(form_frame, width=140)
        self.periodo.grid(row=4, column=1, padx=10, pady=6, sticky="w")
        self.periodo.insert(0, datos_prestamo[4])

        # Campo para el Estado (usando Entry deshabilitado en lugar de OptionMenu)
        ctk.CTkLabel(form_frame, text="Estado", font=("Roboto", 18)).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.estado_label = ctk.CTkEntry(form_frame, font=("Roboto", 18))  # Creamos el Entry
        self.estado_label.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Insertamos el valor del estado y luego lo deshabilitamos
        self.estado_label.insert(0, datos_prestamo[5])  # Inserta el valor del estado en la posición 0
        self.estado_label.configure(state="disabled")  # Deshabilitamos el campo para que no sea editable

        ctk.CTkLabel(form_frame, text="Tasa Interés", font=("Roboto", 18)).grid(row=6, column=0, padx=10, pady=6, sticky="e")
        self.tasa_interes = ctk.CTkEntry(form_frame, width=140)
        self.tasa_interes.grid(row=6, column=1, padx=10, pady=6, sticky="w")
        self.tasa_interes.insert(0, datos_prestamo[6])
        self.tasa_interes.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Fecha Desembolso", font=("Roboto", 18)).grid(row=7, column=0, padx=10, pady=6, sticky="e")
        self.fecha_desembolso = ctk.CTkEntry(form_frame, width=140)
        self.fecha_desembolso.grid(row=7, column=1, padx=10, pady=6, sticky="w")
        self.fecha_desembolso.insert(0, datos_prestamo[7])
        self.fecha_desembolso.configure(state="disabled")

        # Botón para editar el préstamo
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20)

        editar_button = ctk.CTkButton(button_frame, text="Editar Préstamo", command=self.editar_prestamo, width=140)
        editar_button.grid(row=0, column=0, padx=20)

        # Botón para salir
        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, width=140)
        salir_button.grid(row=0, column=1, padx=20)

    # Definir el método para volver al menú principal
    def volver_principal(self):
        self.root.destroy()  # Cierra la ventana actual
        gp.gestionar_prestamos_parametrico()  # Llama a la función que gestiona préstamos o el menú principal

    def editar_prestamo(self):
        id_solicitud = self.id_solicitud.get()
        fecha_solicitud = self.fecha_solicitud.get()
        empleado_id = self.empleado_id.get()
        monto = self.monto.get()
        periodo = self.periodo.get()
        estado = self.estado.get()
        tasa_interes = self.tasa_interes.get()
        fecha_desembolso = self.fecha_desembolso.get()

        if (id_solicitud == "" or fecha_solicitud == "" or empleado_id == "" or monto == "" or 
            periodo == "" or estado == "" or tasa_interes == "" or fecha_desembolso == ""):
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            proyecto.editar_prestamo(id_solicitud, monto, periodo)
            self.info_create = ctk.CTkLabel(self.root, text="Se editó correctamente")
            self.info_create.pack()
            print(f"Editando préstamo con ID: {id_solicitud}, Fecha Solicitud: {fecha_solicitud}, Empleado ID: {empleado_id}, Monto: {monto}, Periodo: {periodo}, Estado: {estado}, Tasa Interés: {tasa_interes}, Fecha Desembolso: {fecha_desembolso}")

# Función para gestionar préstamos o mostrar el menú principal
def gestionar_prestamos():
    gestionar_prestamos_window = gp.gestionar_prestamos_parametrico()
    gestionar_prestamos_window.root.mainloop()
