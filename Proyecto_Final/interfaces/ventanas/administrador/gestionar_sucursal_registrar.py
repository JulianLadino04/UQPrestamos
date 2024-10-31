import customtkinter as ctk
import logica.proyecto as proyecto
import interfaces.ventanas.administrador.gestionar_empleados as ge
import interfaces.ventanas.administrador.gestionar_sucursal_crear_municipio as crm
import interfaces.ventanas.administrador.gestionar_sucursales as gs
import tkinter as tk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class RegistrarSucursal:
    def __init__(self):
        municipios = [str(municipio) for municipio in proyecto.enviar_municipios()]

        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Registrar Sucursal")
        self.root.geometry("1000x500")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (700 // 2) - 70
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"1000x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        # Color de fondo principal
        bg_color = "#2b2b2b"

        # Frame principal centrado
        main_frame = ctk.CTkFrame(self.root, width=500, height=500, fg_color=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Registrar Sucursal", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(10, 5))  # Espacio ajustado sobre y debajo del título

        # Información sobre el registro
        self.info_create = ctk.CTkLabel(main_frame, text="", font=("Roboto", 18))
        self.info_create.pack(pady=(5, 10))

        # Frame para los campos de entrada y etiquetas
        fields_frame = ctk.CTkFrame(main_frame)
        fields_frame.pack(pady=10)

        # ID Sucursal
        id_label = ctk.CTkLabel(fields_frame, text="Id Sucursal", font=("Roboto", 18))
        id_label.grid(row=0, column=0, sticky="e", padx=(0, 10))
        self.identificacion = ctk.CTkEntry(fields_frame, width=200)
        self.identificacion.grid(row=0, column=1, pady=5)

        # Nombre
        nombre_label = ctk.CTkLabel(fields_frame, text="Nombre", font=("Roboto", 18))
        nombre_label.grid(row=1, column=0, sticky="e", padx=(0, 10))
        self.nombre = ctk.CTkEntry(fields_frame, width=200)
        self.nombre.grid(row=1, column=1, pady=5)

        # Municipio
        municipio_label = ctk.CTkLabel(fields_frame, text="Municipio", font=("Roboto", 18))
        municipio_label.grid(row=2, column=0, sticky="e", padx=(0, 10))
        self.municipio_elegido = tk.StringVar()
        ctk.CTkOptionMenu(fields_frame, variable=self.municipio_elegido, values=municipios, width=200).grid(row=2, column=1, pady=5)

        # Botones
        button_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        button_frame.pack(pady=(20, 10))

        register_button = ctk.CTkButton(button_frame, text="Registrar Sucursal", command=self.registrar_sucursal, height=40, width=200, font=("Roboto", 18, "bold"))
        register_button.grid(row=0, column=0, padx=10)

        create_municipio_button = ctk.CTkButton(button_frame, text="Crear Municipio", command=self.crear_municipio, height=40, width=200, font=("Roboto", 18, "bold"))
        create_municipio_button.grid(row=0, column=1, padx=10)

        volver_button = ctk.CTkButton(button_frame, text="Volver", command=self.volver_sucursales, height=40, width=200, font=("Roboto", 18, "bold"))
        volver_button.grid(row=0, column=2, padx=10)

    def crear_municipio(self):
        self.root.destroy()
        ingresar_ventana_creacion_municipio = crm.CrearMunicipio()
        ingresar_ventana_creacion_municipio.root.mainloop()

    def volver_sucursales(self):
        self.root.destroy()
        ingresar_ventana_gestionar_sucursales = gs.gestionar_sucursales()
        ingresar_ventana_gestionar_sucursales.root.mainloop()

    def registrar_sucursal(self):
        id_sucursal = self.identificacion.get()
        nombre = self.nombre.get()
        municipio = self.municipio_elegido.get()

        if id_sucursal == "" or nombre == "" or municipio == "":
            self.info_create.configure(text="Hacen falta datos por llenar", fg_color="red")
        else:
            proyecto.crear_sucursal(id_sucursal, nombre, municipio)
            self.info_create.configure(text="Se registró correctamente", fg_color="green")
            print(f"Registrando sucursal con Id: {id_sucursal}, Nombre: {nombre}, Municipio: {municipio}")

# Para iniciar la ventana
if __name__ == "__main__":
    app = RegistrarSucursal()
    app.root.mainloop()
