import customtkinter as ctk
import os
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
from PIL import Image
from tkinter import ttk
import tkinter as tk
import interfaces.ventanas.administrador.gestionar_usuario_registrar as regUS
import interfaces.ventanas.administrador.gestionar_usuario_editar as edtUs

class gestionar_usuarios:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Usuarios")
        
        # Tamaño y posicionamiento de la ventana
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
        
        # Frame contenedor principal, centrado en la ventana
        main_frame = ctk.CTkFrame(self.root, width=700, height=500, fg_color=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Usuarios del Sistema", font=("Arial", 24, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(20, 10))

        # Configurar la conexión a Oracle
        try:
            connection = proyecto.conexion_oracle()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM USUARIO")

            columnas = [desc[0] for desc in cursor.description]
            filas = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error de conexión o consulta: {e}")
            return

        # Crear la tabla (Treeview) en la ventana
        self.tree = ttk.Treeview(main_frame, columns=columnas, show="headings", height=15)  # Aumentar la altura

        # Establecer el estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')  # Cambia a un tema compatible
        style.configure("Treeview",
                        background="#2e2e2e",  # Fondo oscuro
                        foreground="#ffffff",  # Texto blanco
                        rowheight=25,
                        fieldbackground="#2e2e2e")  # Fondo de las filas

        # Crear las cabeceras de la tabla y ajustar el ancho de las columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, stretch=True)  # Las columnas se ajustan para llenar el espacio

        # Insertar los datos en la tabla
        for fila in filas:
            self.tree.insert('', tk.END, values=fila)

        # Empaquetar la tabla directamente en el marco principal
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Crear un marco (frame) para organizar los botones en fila
        botones_frame = ctk.CTkFrame(main_frame)  # Cambiar a main_frame
        botones_frame.pack(pady=10)

        # Aquí se deshabilitan los botones de "Editar Usuario", "Eliminar Usuario" y "Crear Usuario"
        # Solamente se muestra el botón "Ir a Opciones"
        ctk.CTkButton(botones_frame, text="Ir a Opciones", command=self.ir_a_opciones, font=("Arial", 14, "bold"), width=150).grid(row=0, column=0, padx=10, sticky="ew")

        # Hacer que los botones se expandan igualmente
        botones_frame.grid_columnconfigure(0, weight=1)

        self.root.mainloop()

    def ventana_creacion(self):
        self.root.destroy()
        ingresar_ventana_creacion_usuario = regUS.RegistrarUsuarios()
        ingresar_ventana_creacion_usuario.root.mainloop()   

    def obtener_seleccion(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
        else:
            print("No se ha seleccionado ninguna fila")   

    def editar_usuario(self):
        selected_item = self.tree.selection()  # Verificar si hay una fila seleccionada
        if selected_item:
            fila = self.tree.item(selected_item)['values']  # Obtener los datos de la fila
            print(f"Usuario seleccionado: {fila}")
        
            edtUs.recibir_usuario(fila)  # Pasar los datos del usuario a la ventana de edición
            self.root.destroy()  # Cerrar la ventana actual
        
            ingresar_ventana_edicion_usuario = edtUs.EditarUsuario()  # Crear la ventana de edición
            ingresar_ventana_edicion_usuario.root.mainloop()  # Iniciar la ventana de edición
        else:
            print("No se ha seleccionado ningún usuario")

    def enviar_usuario(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            edtUs.recibir_usuario(fila)
            self.root.destroy() 
            ingresar_ventana_edicion_usuario = edtUs.EditarUsuario()
            ingresar_ventana_edicion_usuario.root.mainloop()
        else:
            print("No se ha seleccionado ninguna fila")    

    def eliminar_usuario(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            self.root.destroy()
            proyecto.eliminar_usuario(fila)
            gestionar_usuarios()
        else:
            print("No se ha seleccionado ninguna fila")   

    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""
        self.root.destroy()
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)

    # Método de ejemplo para volver al menú principal
    def volver_principal(self):
        self.root.destroy()
        gestionar_usuarios()
