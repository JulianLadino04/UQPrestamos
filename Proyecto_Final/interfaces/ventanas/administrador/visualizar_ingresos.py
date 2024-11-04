import customtkinter as ctk
import os
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
from PIL import Image
from tkinter import ttk
import tkinter as tk

class visualizar_ingresos:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Ingresos")

        # Tamaño y posicionamiento de la ventana
        self.root.geometry("750x500")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (750 // 2) + 120
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"750x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        # Título de la ventana en negrilla
        ctk.CTkLabel(master=self.root, text="Ingresos del Sistema", font=("Roboto", 36, "bold")).pack(pady=15)

        # Configuración de conexión a Oracle y obtención de datos
        try:
            connection = proyecto.conexion_oracle()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM INGRESO_SISTEMA")

            # Obtener nombres de columnas y filas de datos
            columnas = [desc[0] for desc in cursor.description]
            filas = cursor.fetchall()
        except Exception as e:
            print(f"Error de conexión o consulta: {e}")
            return
        finally:
            cursor.close()
            connection.close()

        # Crear tabla (Treeview) en la ventana
        self.tree = ttk.Treeview(self.root, columns=columnas, show="headings", height=10)

        # Establecer el estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')  # Tema compatible
        style.configure("Treeview",
                        background="#2e2e2e",
                        foreground="#ffffff",
                        rowheight=25,
                        fieldbackground="#2e2e2e",
                        font=("Roboto", 12))

        # Configurar el ancho de columnas para que ocupen todo el ancho de la tabla
        ancho_total = 750 - 40  # Ancho de la ventana menos los márgenes
        ancho_columnas = ancho_total // len(columnas)
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=ancho_columnas, stretch=True)

        # Insertar datos en la tabla
        for fila in filas:
            self.tree.insert('', tk.END, values=fila)

        # Empaquetar la tabla en la ventana
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Crear marco para el botón y centrarlo en la ventana
        boton_frame = ctk.CTkFrame(self.root)
        boton_frame.pack(pady=10, fill=tk.X)
        boton_frame.grid_columnconfigure(0, weight=1)

        # Botón "Ir a Opciones" centrado y en negrilla
        ir_opciones_btn = ctk.CTkButton(boton_frame, text="Ir a Opciones", command=self.ir_a_opciones, font=("Roboto", 14, "bold"))
        ir_opciones_btn.grid(row=0, column=0, pady=10)

        # Inicializar la ventana principal
        self.root.mainloop()

    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""
        self.root.destroy()
        tipo_usuario = str(proyecto.retornar_tipo_usuario())
        ventana_principal.Opciones(tipo_usuario)  # Llama a la ventana de opciones
