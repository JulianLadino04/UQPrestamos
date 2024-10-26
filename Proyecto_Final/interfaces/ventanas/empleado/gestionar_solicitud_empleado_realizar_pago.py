import customtkinter as ctk
import tkinter as tk
import logica.proyecto as proyecto
from datetime import datetime
import interfaces.ventanas.empleado.gestionar_solicitud_empleado as ge

class RealizarPagoPrestamo:
    def __init__(self, id_prestamo_seleccionado):
        self.root = ctk.CTk()
        self.root.title("Pago de préstamo")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        self.ultima_cuota = False  # Atributo de instancia
        id = proyecto.enviar_usuario_sesion()# Asignar el ID del usuario directamente
        self.id_usuario = id[0]
        # Crear el frame del formulario
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Campo para el ID del Empleado
        ctk.CTkLabel(form_frame, text="Identificación", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.id_empleado = ctk.CTkEntry(form_frame, width=140)
        self.id_empleado.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.id_empleado.insert(0, str(self.id_usuario))  
        self.id_empleado.configure(state="disabled")

        # Campo para el ID del Préstamo
        ctk.CTkLabel(form_frame, text="Número de Préstamo", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.id_prestamo = ctk.CTkEntry(form_frame, width=140)
        self.id_prestamo.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.id_prestamo.insert(0, str(id_prestamo_seleccionado))  
        self.id_prestamo.configure(state="disabled")

        # Campo para el Número de Cuota (se llenará automáticamente)
        ctk.CTkLabel(form_frame, text="Número de Cuota", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.numero_cuota = ctk.CTkEntry(form_frame, width=140)
        self.numero_cuota.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Campo para la Fecha de Pago
        ctk.CTkLabel(form_frame, text="Fecha de Pago", font=("Roboto", 18)).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.fecha_pago = ctk.CTkEntry(form_frame, width=140)
        self.fecha_pago.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.fecha_pago.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Campo para el Monto
        ctk.CTkLabel(form_frame, text="Cantidad", font=("Roboto", 18)).grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.monto = ctk.CTkEntry(form_frame, width=140)
        self.monto.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Botón para realizar el pago
        ctk.CTkButton(self.root, text="Realizar Pago", command=self.validar_campos).pack(pady=20)

        # Botón para salir y volver al menú principal
        ctk.CTkButton(
            master=self.root,
            text="Salir",
            height=40,
            width=200,
            command=self.volver_principal
        ).pack(pady=10)

        # Llenar automáticamente el campo del Número de Cuota
        self.cargar_datos_prestamo(id_prestamo_seleccionado)

    def cargar_datos_prestamo(self, id_prestamo):
        pagos = proyecto.obtener_pagos_prestamos(id_prestamo)
        numero_total_cuotas = proyecto.obtener_cuotas_prestamo(id_prestamo)

        if pagos:
            ultimo_pago = max(pagos, key=lambda x: x[3])  # Asumiendo que x[3] es la fecha
            siguiente_cuota = ultimo_pago[3] + 1  # Asumiendo que x[3] es el número de cuota
            if siguiente_cuota >= numero_total_cuotas:
                self.ultima_cuota = True  # Marca como última cuota
            else:
                self.ultima_cuota = False
        else:
            siguiente_cuota = 1  # Si no hay pagos, la siguiente cuota es la primera

        self.numero_cuota.insert(0, str(siguiente_cuota))
        self.monto.insert(0, proyecto.obtener_cuota_prestamo(id_prestamo))

    def mostrar_mensaje(self, mensaje, color="green"):
        if hasattr(self, "info_create"):
            self.info_create.destroy()
        self.info_create = ctk.CTkLabel(self.root, text=mensaje, text_color=color)
        self.info_create.pack()

    def validar_campos(self):
        monto = self.monto.get()
        if not monto.isdigit():
            self.mostrar_mensaje("Error: Monto inválido.", color="red")
            return

        if self.ultima_cuota:
            # Confirmar si realmente es la última cuota antes de proceder
            self.mostrar_mensaje("¡Es la Última Cuota del Préstamo!, ¡Pagad!", color="blue")
            # Realiza el pago
            proyecto.pagar_prestamo_ultimo(self.id_prestamo.get(), self.numero_cuota.get(), self.fecha_pago.get(), monto)
            self.mostrar_mensaje("¡Última cuota pagada con éxito!", color="green")
        else:
            # Procesar como un pago normal
            proyecto.pagar_prestamo(self.id_prestamo.get(), self.numero_cuota.get(), self.fecha_pago.get(), monto)
            self.mostrar_mensaje("Pago realizado con éxito.", color="green")

    def volver_principal(self):
        self.root.destroy()
        ingresar_ventana_solicitud = ge.gestionar_solicitud_empleado()
        ingresar_ventana_solicitud.root.mainloop()
