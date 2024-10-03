import customtkinter as ctk
import os
import interfaces.GUI as ventana_principal
import logica.proyecto as proyecto
import tkinter as tk
from datetime import datetime
import interfaces.ventanas.administrador.gestionar_prestamos as gp

# Obtener los valores requeridos desde el módulo de lógica
estados_disponibles = ["Pendiente", "Aprobado", "Rechazado"]  # Estados posibles del préstamo
empleados_ids = [str(id_empleado) for id_empleado in proyecto.enviar_id_empleados()]  # IDs de empleados disponibles

class RegistrarPrestamo:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Registro de Préstamos")
        self.root.geometry("750x600")  # Ajuste del tamaño de la ventana
        
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="Empleado ID", font=("Roboto", 18)).pack(pady=6)
        self.empleado_id = ctk.CTkOptionMenu(form_frame, values=empleados_ids, width=140)
        self.empleado_id.pack(pady=2)

        ctk.CTkLabel(form_frame, text="Monto", font=("Roboto", 18)).pack(pady=6)
        self.monto = ctk.CTkEntry(form_frame, width=140)
        self.monto.pack(pady=2)

        ctk.CTkLabel(form_frame, text="Periodo (en meses)", font=("Roboto", 18)).pack(pady=6)
        self.periodo = ctk.CTkEntry(form_frame, width=140)
        self.periodo.pack(pady=2)

        ctk.CTkLabel(form_frame, text="Tasa de Interés (%)", font=("Roboto", 18)).pack(pady=6)
        self.tasa_interes = ctk.CTkEntry(form_frame, width=140)
        self.tasa_interes.pack(pady=2)

        ctk.CTkLabel(form_frame, text="Fecha Desembolso (YYYY-MM-DD)", font=("Roboto", 18)).pack(pady=6)
        self.fecha_desembolso = ctk.CTkEntry(form_frame, width=140)
        self.fecha_desembolso.pack(pady=2)

        # Botón para registrar préstamo
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20)

        registrar_button = ctk.CTkButton(button_frame, text="Registrar Préstamo", command=self.registrar_prestamo, width=140)
        registrar_button.grid(row=0, column=0, padx=20)

        # Botón para salir
        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, width=140)
        salir_button.grid(row=0, column=1, padx=20)

    def registrar_prestamo(self):
        # Obtener los valores de los campos
        id_solicitud = self.id_solicitud.get()
        empleado_id = self.empleado_id.get()
        monto = self.monto.get()
        periodo = self.periodo.get()
        tasa_interes = self.tasa_interes.get()
        fecha_desembolso = self.fecha_desembolso.get()

        # Verificar si todos los campos están llenos
        if (id_solicitud == "" or empleado_id == "" or monto == "" or 
            periodo == "" or tasa_interes == "" or fecha_desembolso == ""):
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar")
            self.info_create.pack()
        else:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            # Registrar el préstamo
            proyecto.crear_prestamo(datetime.now(), empleado_id, monto, periodo, tasa_interes, fecha_desembolso)
            self.info_create = ctk.CTkLabel(self.root, text="Préstamo registrado correctamente")
            self.info_create.pack()
            print(f"Registrando préstamo con ID: {id_solicitud}, Empleado ID: {empleado_id}, Monto: {monto}, Periodo: {periodo}, Tasa Interés: {tasa_interes}, Fecha Desembolso: {fecha_desembolso}")

    def volver_principal(self):
        self.root.destroy()
        gestionar_prestamos_ventana = gp.gestionar_prestamos()
        gestionar_prestamos_ventana.root.mainloop()
