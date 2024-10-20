import customtkinter as ctk
import tkinter as tk
import logica.proyecto as proyecto
from datetime import datetime
import interfaces.ventanas.empleado.gestionar_solicitud_empleado as ge

# Obtener el ID del usuario desde el sistema
id_usuario = proyecto.enviar_usuario_sesion()

class RealizarPagoPrestamo:
    def __init__(self, id_prestamo_seleccionado):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Pago de prestamo")
        self.root.geometry("500x500")
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

        # Campo para el ID del Préstamo
        ctk.CTkLabel(form_frame, text="Número de Préstamo", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.id_prestamo = ctk.CTkEntry(form_frame, width=140)
        self.id_prestamo.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.id_prestamo.insert(0, str(id_prestamo_seleccionado))  # Insertar el ID del préstamo seleccionado
        self.id_prestamo.configure(state="disabled")  # Deshabilitamos para que no se pueda editar

        # Campo para el Número de Cuota
        ctk.CTkLabel(form_frame, text="Número de Cuota", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.numero_cuota = ctk.CTkEntry(form_frame, width=140)
        self.numero_cuota.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Campo para la Fecha de Pago
        ctk.CTkLabel(form_frame, text="Fecha de Pago", font=("Roboto", 18)).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.fecha_pago = ctk.CTkEntry(form_frame, width=140)
        self.fecha_pago.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.fecha_pago.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Insertar la fecha actual por defecto

        # Campo para el Monto
        ctk.CTkLabel(form_frame, text="Cantidad", font=("Roboto", 18)).grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.monto = ctk.CTkEntry(form_frame, width=140)
        self.monto.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Botón para realizar el pago
        ctk.CTkButton(self.root, text="Realizar Pago", command=self.validar_campos).pack(pady=20)

        # Botón para salir y volver al menú principal
        salir_button = ctk.CTkButton(
            master=self.root,
            text="Salir",
            height=40,
            width=200,
            command=self.volver_principal  # Asignamos la función aquí
        )
        salir_button.pack(pady=10)

    def validar_campos(self):
        # Aquí puedes agregar la validación para los campos y registrar el pago.
        pass
    
    def volver_principal(self):
        self.root.destroy()
        ingresar_ventana_solicitud = ge.gestionar_solicitud_empleado()
        ingresar_ventana_solicitud.root.mainloop()
