import customtkinter as ctk
import logica.proyecto as proyecto
import interfaces.ventanas.administrador.gestionar_solicitudes as ge
import tkinter as tk
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Valores predefinidos para el periodo
periodos_disponibles = ["24", "36", "48", "60", "72"]

class CrearSolicitudAdministrador:
    def __init__(self):
        # Configuración de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Crear Nueva Solicitud de Empleado")
        self.root.geometry("700x500")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1000 // 2) + 120
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"700x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        # Color de fondo principal
        bg_color = "#2b2b2b"

        # Frame principal centrado
        main_frame = ctk.CTkFrame(self.root, width=500, height=500, fg_color=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Crear Nueva Solicitud", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(10, 5))

        # Información sobre el registro
        self.info_create = ctk.CTkLabel(main_frame, text="", font=("Roboto", 18))
        self.info_create.pack(pady=(5, 10))

        # Frame para los campos de entrada y etiquetas
        fields_frame = ctk.CTkFrame(main_frame)
        fields_frame.pack(pady=10)

        # Campos del formulario
        ctk.CTkLabel(fields_frame, text="ID Empleado", font=("Roboto", 18)).grid(row=0, column=0, sticky="e", padx=(0, 10))
        self.id_empleado = ctk.CTkEntry(fields_frame, width=200)
        self.id_empleado.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(fields_frame, text="Monto", font=("Roboto", 18)).grid(row=1, column=0, sticky="e", padx=(0, 10))
        self.monto = ctk.CTkEntry(fields_frame, width=200)
        self.monto.grid(row=1, column=1, pady=5)

        ctk.CTkLabel(fields_frame, text="Periodo", font=("Roboto", 18)).grid(row=2, column=0, sticky="e", padx=(0, 10))
        self.periodo = tk.StringVar()
        ctk.CTkOptionMenu(fields_frame, variable=self.periodo, values=periodos_disponibles, width=200).grid(row=2, column=1, pady=5)

        # Botones
        button_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        button_frame.pack(pady=(20, 10))

        crear_button = ctk.CTkButton(button_frame, text="Crear Solicitud", command=self.validar_campos, height=40, width=200, font=("Roboto", 18, "bold"))
        crear_button.grid(row=0, column=0, padx=10)

        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, height=40, width=200, font=("Roboto", 18, "bold"))
        salir_button.grid(row=0, column=1, padx=10)

    def validar_campos(self):
        id_empleado = self.id_empleado.get()
        monto = self.monto.get()
        periodo = self.periodo.get()

        if "" in [id_empleado, monto, periodo]:
            self.info_create.configure(text="Faltan datos por llenar", fg_color="red")
        else:
            proyecto.crear_solicitud(datetime.now(), id_empleado, monto, periodo)
            self.info_create.configure(text="Solicitud creada correctamente", fg_color="green")
            print(f"Solicitud creada: ID Empleado: {id_empleado}, Monto: {monto}, Periodo: {periodo}")

    def volver_principal(self):
        self.root.destroy()
        ingresar_ventana_solicitud = ge.gestionar_solicitudes()
        ingresar_ventana_solicitud.root.mainloop()

# Para iniciar la ventana
if __name__ == "__main__":
    app = CrearSolicitudAdministrador()
    app.root.mainloop()
