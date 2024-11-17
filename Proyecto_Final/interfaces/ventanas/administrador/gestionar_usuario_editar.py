import customtkinter as ctk
import os
import logica.proyecto as proyecto
import interfaces.ventanas.administrador.gestionar_usuarios as gu
import tkinter as tk

datos_usuario = []
niveles_sistema = proyecto.enviar_niveles()
niveles_en_cadenas = [nivel[0] for nivel in niveles_sistema]

def recibir_usuario(datos):
    global datos_usuario
    datos_usuario = datos

class EditarUsuario:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Editar Usuario")
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

        title_label = ctk.CTkLabel(main_frame, text="Editar Usuario", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configurar las columnas de forma proporcional
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        # Etiquetas y campos del formulario
        ctk.CTkLabel(form_frame, text="ID Usuario", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.id_usuario = ctk.CTkEntry(form_frame, width=200)
        self.id_usuario.grid(row=0, column=1, padx=10, pady=5)
        self.id_usuario.insert(0, datos_usuario[0])
        self.id_usuario.configure(state="disabled")

        ctk.CTkLabel(form_frame, text="Username", font=("Roboto", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.username = ctk.CTkEntry(form_frame, width=200)
        self.username.grid(row=1, column=1, padx=10, pady=5)
        self.username.insert(0, datos_usuario[1])

        ctk.CTkLabel(form_frame, text="Password", font=("Roboto", 18)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password = ctk.CTkEntry(form_frame, width=200, show="*")
        self.password.grid(row=2, column=1, padx=10, pady=5)
        self.password.insert(0, datos_usuario[2])

        ctk.CTkLabel(form_frame, text="Nivel en Sistema", font=("Roboto", 18)).grid(row=3, column=0, padx=10, pady=6, sticky="e")
        self.nivel = tk.StringVar()
        ctk.CTkOptionMenu(form_frame, variable=self.nivel, values=niveles_en_cadenas).grid(row=3, column=1, padx=10, pady=5)
        self.nivel.set(datos_usuario[3])

        ctk.CTkLabel(form_frame, text="Nombre", font=("Roboto", 18)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.nombre = ctk.CTkEntry(form_frame, width=200)
        self.nombre.grid(row=4, column=1, padx=10, pady=5)
        self.nombre.insert(0, datos_usuario[4])

        button_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
        button_frame.pack(pady=(20, 10))

        edit_button = ctk.CTkButton(button_frame, text="Editar Usuario", command=self.validar_campos, height=40, width=200, font=("Roboto", 18, "bold"))
        edit_button.grid(row=0, column=0, padx=10)

        salir_button = ctk.CTkButton(button_frame, text="Salir", command=self.volver_principal, height=40, width=200, font=("Roboto", 18, "bold"))
        salir_button.grid(row=0, column=1, padx=10)

        # Mensaje de información de validación inicializado como etiqueta vacía
        self.info_update = ctk.CTkLabel(main_frame, text="", font=("Roboto", 14))
        self.info_update.pack(pady=(10, 0))

    def volver_principal(self):
        self.root.destroy()
        gu.gestionar_usuarios()

    def validar_campos(self):
        id_usuario = self.id_usuario.get()
        username = self.username.get()
        password = self.password.get()
        nivel = self.nivel.get()
        nombre = self.nombre.get()

        if id_usuario == "" or username == "" or password == "" or nivel == "" or nombre == "":
            self.info_update.configure(text="Hacen falta datos por llenar", fg_color="red")
        else:
            proyecto.editar_usuario(id_usuario, username, password, nivel, nombre)
            self.info_update.configure(text="Usuario editado correctamente", fg_color="green")


# Función para gestionar empleados o mostrar el menú principal
def gestionar_usuarios():
    gestionar_usuarios_window = gu.gestionar_usuarios()
    gestionar_usuarios_window.root.mainloop()