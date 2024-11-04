import customtkinter as ctk
import os
import logica.proyecto as proyecto
import interfaces.ventanas.administrador.gestionar_prestamos as gp
import tkinter as tk

datos_prestamo = []  # Se llenará con los datos del préstamo a editar

def recibir_prestamo(datos):
    global datos_prestamo
    datos_prestamo = datos

class EditarPrestamo:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Editar Préstamo")
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

        title_label = ctk.CTkLabel(main_frame, text="Editar Préstamo", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configurar las columnas de forma proporcional
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        # Etiquetas y campos del formulario
        ctk.CTkLabel(form_frame, text="ID Solicitud", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.id_solicitud = ctk.CTkEntry(form_frame, width=200)
        self.id_solicitud.grid(row=0, column=1, padx=10, pady=5)
        self.id_solicitud.insert(0, datos_prestamo[0])
        self.id_solicitud.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Fecha Solicitud", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.fecha_solicitud = ctk.CTkEntry(form_frame, width=200)
        self.fecha_solicitud.grid(row=1, column=1, padx=10, pady=5)
        self.fecha_solicitud.insert(0, datos_prestamo[1])
        self.fecha_solicitud.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Empleado ID", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.empleado_id = ctk.CTkEntry(form_frame, width=200)
        self.empleado_id.grid(row=2, column=1, padx=10, pady=5)
        self.empleado_id.insert(0, datos_prestamo[2])
        self.empleado_id.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Monto", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.monto = ctk.CTkEntry(form_frame, width=200)
        self.monto.grid(row=3, column=1, padx=10, pady=5)
        self.monto.insert(0, datos_prestamo[3])

        ctk.CTkLabel(form_frame, text="Periodo", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.periodo = ctk.CTkEntry(form_frame, width=200)
        self.periodo.grid(row=4, column=1, padx=10, pady=5)
        self.periodo.insert(0, datos_prestamo[4])

        ctk.CTkLabel(form_frame, text="Estado", font=("Roboto", 18)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.estado = ctk.CTkEntry(form_frame, width=200)
        self.estado.grid(row=5, column=1, padx=10, pady=5)
        self.estado.insert(0, datos_prestamo[5])
        self.estado.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Tasa Interés", font=("Roboto", 18)).grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.tasa_interes = ctk.CTkEntry(form_frame, width=200)
        self.tasa_interes.grid(row=6, column=1, padx=10, pady=5)
        self.tasa_interes.insert(0, datos_prestamo[6])

        ctk.CTkLabel(form_frame, text="Fecha Desembolso", font=("Roboto", 18)).grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.fecha_desembolso = ctk.CTkEntry(form_frame, width=200)
        self.fecha_desembolso.grid(row=7, column=1, padx=10, pady=5)
        self.fecha_desembolso.insert(0, datos_prestamo[7])

        button_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        button_frame.pack(pady=(20, 10))

        editar_button = ctk.CTkButton(button_frame, text="Editar Préstamo", command=self.validar_campos, height=40, width=200, font=("Roboto", 18, "bold"))
        editar_button.grid(row=0, column=0, padx=10)

        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, height=40, width=200, font=("Roboto", 18, "bold"))
        salir_button.grid(row=0, column=1, padx=10)

        # Mensaje de información de validación inicializado como etiqueta vacía
        self.info_update = ctk.CTkLabel(main_frame, text="", font=("Roboto", 14))
        self.info_update.pack(pady=(10, 0))

    def volver_principal(self):
        self.root.destroy()
        gp.gestionar_prestamos()

    def validar_campos(self):
        id_solicitud = self.id_solicitud.get()
        fecha_solicitud = self.fecha_solicitud.get()
        empleado_id = self.empleado_id.get()
        monto = self.monto.get()
        periodo = self.periodo.get()
        estado = self.estado.get()
        tasa_interes = self.tasa_interes.get()
        fecha_desembolso = self.fecha_desembolso.get()

        if id_solicitud == "" or fecha_solicitud == "" or empleado_id == "" or monto == "" or periodo == "" or tasa_interes == "" or fecha_desembolso == "":
            self.info_update.configure(text="Hacen falta datos por llenar", fg_color="red")
        else:
            proyecto.editar_prestamo(id_solicitud, monto, periodo)
            self.info_update.configure(text="Préstamo editado correctamente", fg_color="green")


# Función para gestionar préstamos o mostrar el menú principal
def gestionar_prestamos():
    gestionar_prestamos_window = gp.gestionar_prestamos()
    gestionar_prestamos_window.root.mainloop()
