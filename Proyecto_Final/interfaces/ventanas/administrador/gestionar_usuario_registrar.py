import customtkinter as ctk
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
import interfaces.ventanas.administrador.gestionar_usuarios as gu
import tkinter as tk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Obtener datos necesarios
ids_sucursales = [str(id_sucursal) for id_sucursal in proyecto.id_sucursales()]
niveles_sistema = proyecto.enviar_niveles()
niveles_en_cadenas = [nivel[0] for nivel in niveles_sistema]

class RegistrarUsuarios:
    def __init__(self):
        # Configuración de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Registrar Usuario")
        self.root.geometry("1000x500")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1000 // 2) - 70
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
        title_label = ctk.CTkLabel(main_frame, text="Registrar Usuario", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(20, 10))

        # Información sobre el registro
        self.info_create = ctk.CTkLabel(main_frame, text="", font=("Roboto", 18))
        self.info_create.pack(pady=(10, 10))

        # Formulario de entrada de datos
        form_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Campos del formulario
        # Primera columna
        ctk.CTkLabel(form_frame, text="Identificación", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.identificacion = ctk.CTkEntry(form_frame, width=200)
        self.identificacion.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=200)
        self.nombre.grid(row=1, column=1, padx=10, pady=5)

        # Segunda columna
        ctk.CTkLabel(form_frame, text="Usuario", font=("Roboto", 18)).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.usuario = ctk.CTkEntry(form_frame, width=200)
        self.usuario.grid(row=0, column=3, padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Contraseña", font=("Roboto", 18)).grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.contrasena = ctk.CTkEntry(form_frame, width=200, show="*")
        self.contrasena.grid(row=1, column=3, padx=10, pady=5)

        # Tercera columna
        ctk.CTkLabel(form_frame, text="Nivel en Sistema", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.nivel_sis = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.nivel_sis, values=niveles_en_cadenas, width=200).grid(row=2, column=1, padx=10, pady=5)

        # Botones
        button_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        button_frame.pack(pady=(20, 10))

        register_button = ctk.CTkButton(button_frame, text="Registrar Usuario", command=self.registrar_usuario, height=40, width=200, font=("Roboto", 18, "bold"))
        register_button.grid(row=0, column=0, padx=10)

        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, height=40, width=200, font=("Roboto", 18, "bold"))
        salir_button.grid(row=0, column=1, padx=10)

    def registrar_usuario(self):
        # Validación y registro del usuario
        identificacion = self.identificacion.get()
        nombre = self.nombre.get()
        nivel = self.nivel_sis.get()
        usuario = self.usuario.get()
        contrasena = self.contrasena.get()

        if identificacion == "" or nombre == "" or nivel == "" or usuario == "" or contrasena == "":
            self.info_create.configure(text="Hacen falta datos por llenar", fg_color="red")
        elif proyecto.verificar_credenciales(usuario, contrasena):
            self.info_create.configure(text="El usuario ingresado ya está en uso, utilice otro", fg_color="red")
        else:
            proyecto.crear_usuario(identificacion, nombre, usuario, contrasena, nivel)
            self.info_create.configure(text="Se registró correctamente", fg_color="green")
            print(f"Registrando usuario con Identificación: {identificacion}, Nombre: {nombre}, Usuario: {usuario}")

    def volver_principal(self):
        self.root.destroy()
        gestionar_usuarios()

def gestionar_usuarios():
    gestionar_usuarios_window = gu.gestionar_usuarios()
    gestionar_usuarios_window.root.mainloop()

# Para iniciar la ventana
if __name__ == "__main__":
    app = RegistrarUsuarios()
    app.root.mainloop()
