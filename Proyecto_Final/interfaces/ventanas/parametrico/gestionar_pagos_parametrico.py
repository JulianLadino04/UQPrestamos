import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
from interfaces.ventanas.parametrico.gestionar_solicitud_parametrico_realizar_pago import RealizarPagoParametricoPrestamo

class gestionar_pagos_parametricos:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Pagos")

        # Tamaño y posicionamiento de la ventana
        self.root.geometry("1000x500")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1000 // 2)
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"1000x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        # Frame contenedor principal, centrado en la ventana
        main_frame = ctk.CTkFrame(self.root, width=900, height=450, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Pagos Paramétricos del Sistema", font=("Arial", 24, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(20, 10))

        # Configurar la conexión a Oracle
        try:
            connection = proyecto.conexion_oracle()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM PAGO")

            columnas = [desc[0] for desc in cursor.description]
            filas = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error de conexión o consulta: {e}")
            return

        # Crear la tabla (Treeview) en la ventana
        self.tree = ttk.Treeview(main_frame, columns=columnas, show="headings", height=15)

        # Establecer el estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background="#2e2e2e",
                        foreground="#ffffff",
                        rowheight=25,
                        fieldbackground="#2e2e2e")
        style.map("Treeview", background=[("selected", "#4a4a4a")])

        # Crear las cabeceras de la tabla y ajustar el ancho de las columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, stretch=True)

        # Insertar los datos en la tabla
        for fila in filas:
            self.tree.insert('', tk.END, values=fila)

        # Empaquetar la tabla en el marco principal
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Crear un marco para los botones
        botones_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b")
        botones_frame.pack(pady=10)

        # Añadir botones en fila
        ctk.CTkButton(botones_frame, text="Eliminar Pago", command=self.eliminar_pago, font=("Arial", 14, "bold"), width=150).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkButton(botones_frame, text="Ir a Opciones", command=self.ir_a_opciones, font=("Arial", 14, "bold"), width=150).grid(row=0, column=1, padx=10, sticky="ew")

        # Configurar expansión equitativa de botones
        botones_frame.grid_columnconfigure(0, weight=1)
        botones_frame.grid_columnconfigure(1, weight=1)

        self.root.mainloop()

    def obtener_seleccion(self):
        """Obtiene la fila seleccionada en la tabla."""
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
        else:
            print("No se ha seleccionado ninguna fila")

    def eliminar_pago(self):
        """Elimina el pago seleccionado de la tabla."""
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Pago seleccionado: {fila}")
            self.root.destroy()
            proyecto.eliminar_pago(fila)
            gestionar_pagos_parametricos()
        else:
            print("No se ha seleccionado ninguna fila")

    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""
        self.root.destroy()
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)
