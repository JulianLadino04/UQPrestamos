import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import logica.proyecto as proyecto
import interfaces.ventanas.empleado.gestionar_solicitud_empleado as ge

class RealizarPagoPrestamo:
    def __init__(self, id_prestamo_seleccionado):
        self.root = ctk.CTk()
        self.root.title("Realizar Pago de Préstamo")
        self.root.geometry("500x500")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"500x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        self.ultima_cuota = False
        self.id_usuario = proyecto.enviar_usuario_sesion()[0]  # ID del usuario en sesión

        # Frame contenedor principal, centrado en la ventana
        main_frame = ctk.CTkFrame(self.root, width=450, height=450, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Realizar Pago", font=("Arial", 24, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(10, 20))

        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="#3b3b3b")
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.crear_formulario(form_frame, id_prestamo_seleccionado)

        # Botones
        ctk.CTkButton(main_frame, text="Realizar Pago", command=self.validar_campos, font=("Arial", 14, "bold"), width=200).pack(pady=10)
        ctk.CTkButton(main_frame, text="Salir", command=self.volver_principal, font=("Arial", 14, "bold"), width=200).pack(pady=10)

        self.cargar_datos_prestamo(id_prestamo_seleccionado)

    def crear_formulario(self, frame, id_prestamo_seleccionado):
        """Crea los campos del formulario para el pago."""
        # ID del Empleado
        ctk.CTkLabel(frame, text="Identificación", font=("Roboto", 16), text_color="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.id_empleado = ctk.CTkEntry(frame, width=160)
        self.id_empleado.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.id_empleado.insert(0, str(self.id_usuario))
        self.id_empleado.configure(state="disabled")

        # Número de Préstamo
        ctk.CTkLabel(frame, text="Número de Préstamo", font=("Roboto", 16), text_color="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.id_prestamo = ctk.CTkEntry(frame, width=160)
        self.id_prestamo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.id_prestamo.insert(0, str(id_prestamo_seleccionado))
        self.id_prestamo.configure(state="disabled")

        # Número de Cuota
        ctk.CTkLabel(frame, text="Número de Cuota", font=("Roboto", 16), text_color="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.numero_cuota = ctk.CTkEntry(frame, width=160)
        self.numero_cuota.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Fecha de Pago
        ctk.CTkLabel(frame, text="Fecha de Pago", font=("Roboto", 16), text_color="#FFFFFF").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.fecha_pago = ctk.CTkEntry(frame, width=160)
        self.fecha_pago.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.fecha_pago.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Monto
        ctk.CTkLabel(frame, text="Cantidad", font=("Roboto", 16), text_color="#FFFFFF").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.monto = ctk.CTkEntry(frame, width=160)
        self.monto.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    def cargar_datos_prestamo(self, id_prestamo):
        """Obtiene y carga los datos del préstamo para el pago."""
        pagos = proyecto.obtener_pagos_prestamos(id_prestamo)
        numero_total_cuotas = proyecto.obtener_cuotas_prestamo(id_prestamo)

        if pagos:
            ultimo_pago = max(pagos, key=lambda x: x[3])  # Asumiendo que x[3] es el número de cuota
            siguiente_cuota = ultimo_pago[3] + 1
            self.ultima_cuota = siguiente_cuota >= numero_total_cuotas
        else:
            siguiente_cuota = 1

        self.numero_cuota.insert(0, str(siguiente_cuota))
        self.monto.insert(0, proyecto.obtener_cuota_prestamo(id_prestamo))

    def mostrar_mensaje(self, mensaje, color="green"):
        """Muestra un mensaje en la ventana."""
        if hasattr(self, "info_create"):
            self.info_create.destroy()
        self.info_create = ctk.CTkLabel(self.root, text=mensaje, text_color=color)
        self.info_create.pack(pady=10)

    def validar_campos(self):
        """Valida los campos antes de realizar el pago."""
        monto = self.monto.get()
        if not monto.isdigit():
            self.mostrar_mensaje("Error: Monto inválido.", color="red")
            return

        if self.ultima_cuota:
            proyecto.pagar_prestamo_ultimo(self.id_prestamo.get(), self.numero_cuota.get(), self.fecha_pago.get(), monto)
            self.mostrar_mensaje("¡Última cuota pagada con éxito!", color="green")
        else:
            proyecto.pagar_prestamo(self.id_prestamo.get(), self.numero_cuota.get(), self.fecha_pago.get(), monto)
            self.mostrar_mensaje("Pago realizado con éxito.", color="green")

    def volver_principal(self):
        """Regresa al menú principal."""
        self.root.destroy()
        ge.GestionarSolicitudEmpleado()
