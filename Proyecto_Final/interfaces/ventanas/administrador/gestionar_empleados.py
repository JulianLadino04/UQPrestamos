import customtkinter as ctk
import os
import interfaces.GUI as ventana_principal
import logica.proyecto as proyecto
from tkinter import ttk
import tkinter as tk
import interfaces.ventanas.administrador.gestionar_empleado_registrar as reg
import interfaces.ventanas.administrador.gestionar_empleado_editar as edt

class gestionar_empleados:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Empleados")
        
        # Tamaño y posicionamiento de la ventana
        self.root.geometry("700x500")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (700 // 2) - 70
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
        title_label = ctk.CTkLabel(main_frame, text="Empleados", font=("Arial", 24, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(20, 10))

        # Configurar la conexión a Oracle
        try:
            connection = proyecto.conexion_oracle()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM EMPLEADO")

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

        # Añadir los botones alineados en fila utilizando grid
        ctk.CTkButton(botones_frame, text="Editar Empleado", command=self.enviar_empleado, font=("Arial", 14, "bold"), width=150).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkButton(botones_frame, text="Eliminar Empleado", command=self.eliminar_empleado, font=("Arial", 14, "bold"), width=150).grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkButton(botones_frame, text="Crear Empleado", command=self.ventana_creacion, font=("Arial", 14, "bold"), width=150).grid(row=0, column=2, padx=10, sticky="ew")
        ctk.CTkButton(botones_frame, text="Ir a Opciones", command=self.ir_a_opciones, font=("Arial", 14, "bold"), width=150).grid(row=0, column=3, padx=10, sticky="ew")

        # Hacer que los botones se expandan igualmente
        for i in range(4):  # Cambiar a 4 para incluir el nuevo botón
            botones_frame.grid_columnconfigure(i, weight=1)

        self.root.mainloop()

    def obtener_seleccion(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
        else:
            print("No se ha seleccionado ninguna fila")   

    # En gestionar_empleados, método enviar_empleado
    def enviar_empleado(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            edt.recibir_empleado(fila)
            self.root.destroy() 
            ingresar_ventana_edicion_empleado = edt.EditarEmpleados()
            ingresar_ventana_edicion_empleado.root.mainloop()
        else:
            print("No se ha seleccionado ninguna fila")   

    def eliminar_empleado(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            self.root.destroy()
            proyecto.eliminar_empleado(fila)
            gestionar_empleados()
        else:
            print("No se ha seleccionado ninguna fila")   
            
    def ventana_creacion(self):
        self.root.destroy() 
        ingresar_ventana_creacion_empleado = reg.RegistrarEmpleados()
        ingresar_ventana_creacion_empleado.root.mainloop()       
         
    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""  
        self.root.destroy()  # Cierra la ventana de gestión de empleados
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)  # Llama a la ventana de opciones
        
    # Método de ejemplo para volver al menú principal
    def volver_principal(self):
        self.root.destroy()  # Cierra la ventana actual
        gestionar_empleados()
