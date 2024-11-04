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
periodos_disponibles = ["24", "36", "48", "60", "72"]

class RegistrarPrestamo:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Registro de Préstamos")
        self.root.geometry("700x500")
        self.root.configure(background="#2b2b2b")

        # Cálculo para centrar la ventana en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (700 // 2) + 120  # Ajustar a 1000 de ancho
        y = (screen_height // 2) - (500 // 2)  # Ajustar a 600 de alto
        self.root.geometry(f"700x500+{x}+{y}")
        self.root.resizable(False, False)

        bg_color = "#2b2b2b"

        # Marco principal
        form_frame = ctk.CTkFrame(self.root, fg_color=bg_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Título
        title_label = ctk.CTkLabel(form_frame, text="Registro de Préstamos", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(20, 10))

        # Etiquetas y campos del formulario
        ctk.CTkLabel(form_frame, text="Empleado ID", font=("Roboto", 18)).pack(pady=6)
        self.empleado_id = ctk.CTkOptionMenu(form_frame, values=empleados_ids, width=140)
        self.empleado_id.pack(pady=2)

        ctk.CTkLabel(form_frame, text="Monto", font=("Roboto", 18)).pack(pady=6)
        self.monto = ctk.CTkEntry(form_frame, width=140)
        self.monto.pack(pady=2)

        ctk.CTkLabel(form_frame, text="Periodo (en meses)", font=("Roboto", 18)).pack(pady=6)
        self.periodo = ctk.CTkOptionMenu(form_frame, values=periodos_disponibles, width=140)
        self.periodo.pack(pady=2)

        # Botones
        button_frame = ctk.CTkFrame(self.root, fg_color=bg_color)
        button_frame.pack(pady=20)

        registrar_button = ctk.CTkButton(button_frame, text="Registrar Préstamo", command=self.registrar_prestamo, width=140, height=40, font=("Roboto", 18, "bold"))
        registrar_button.grid(row=0, column=0, padx=20)

        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, width=140, height=40, font=("Roboto", 18, "bold"))
        salir_button.grid(row=0, column=1, padx=20)

    def registrar_prestamo(self):
        # Obtener los valores de los campos
        empleado_id = self.empleado_id.get()
        monto_str = self.monto.get()
        periodo_str = self.periodo.get()

        # Verificar si todos los campos están llenos
        if (empleado_id == "" or monto_str == "" or periodo_str == ""):
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Hacen falta datos por llenar", fg_color="red")
            self.info_create.pack(pady=(10, 0))
            return  # Salir si hay campos vacíos

        try:
            # Convertir los valores a tipos numéricos
            monto = float(monto_str)  # Convertir el monto a float
            periodo = int(periodo_str)  # Convertir el período a int

            # Lógica de cálculo del préstamo (Ejemplo: cálculo de intereses)
            tasa_interes = 0.07  # Tasa de interés del 7%
            total_a_pagar = monto * (1 + tasa_interes * periodo)  # Ejemplo de cálculo total a pagar

            # Registrar el préstamo (ajusta la función según tus necesidades)
            proyecto.crear_prestamo(datetime.now(), empleado_id, monto, periodo)
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Préstamo registrado correctamente", fg_color="green")
            self.info_create.pack(pady=(10, 0))
            print(f"Registrando préstamo con Empleado ID: {empleado_id}, Monto: {monto}, Periodo: {periodo}, Total a Pagar: {total_a_pagar}")

        except ValueError as e:
            if hasattr(self, "info_create"):
                self.info_create.destroy()
            self.info_create = ctk.CTkLabel(self.root, text="Error en los datos de entrada", fg_color="red")
            self.info_create.pack(pady=(10, 0))
            print(f"Error al registrar el préstamo: {e}")


    def volver_principal(self):
        self.root.destroy()
        gestionar_prestamos_ventana = gp.gestionar_prestamos()
        gestionar_prestamos_ventana.root.mainloop()
