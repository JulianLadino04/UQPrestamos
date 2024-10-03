import customtkinter as ctk
import os
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
from PIL import Image
from tkinter import ttk
import tkinter as tk
import interfaces.ventanas.parametrico.gestionar_prestamos_parametrico_crear as regUS
import interfaces.ventanas.parametrico.gestionar_prestamos_parametrico_editar as edtUs
           
class gestionar_prestamos_parametrico: 
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Solicitud Empleado")
        self.root.geometry("750x550")
        self.root.resizable(True, True)

        ctk.CTkLabel(master=self.root, text="Vista de prestamos empleado parametrico", font=("Roboto", 36)).pack(pady=15)

        # Configurar la conexión a Oracle
        try:
            connection = proyecto.conexion_oracle()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM PRESTAMO")

            columnas = [desc[0] for desc in cursor.description]
            filas = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error de conexión o consulta: {e}")
            return

        # Crear la tabla (Treeview) en la ventana
        self.tree = ttk.Treeview(self.root, columns=columnas, show="headings", height=10)

        # Establecer el estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')  # Cambia a un tema compatible
        style.configure("Treeview",
                        background="#2e2e2e",  # Fondo oscuro
                        foreground="#ffffff",  # Texto blanco
                        rowheight=25,
                        fieldbackground="#2e2e2e")  # Fondo de las filas

        # Crear las cabeceras de la tabla y ajustar el ancho de las columnas
        ancho_columnas = 88
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=ancho_columnas, stretch=False)

        # Insertar los datos en la tabla
        for fila in filas:
            self.tree.insert('', tk.END, values=fila)

        # Empaquetar la tabla
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Crear un marco (frame) para organizar los botones en fila
        botones_frame = ctk.CTkFrame(self.root)
        botones_frame.pack(pady=10)

        # Añadir los botones alineados en fila utilizando grid
        ctk.CTkButton(botones_frame, text="Editar Solicitud", command=self.enviar_usuario).grid(row=0, column=0, padx=10)
        ctk.CTkButton(botones_frame, text="Eliminar Solicitud", command=self.eliminar_usuario).grid(row=0, column=1, padx=10)
        ctk.CTkButton(botones_frame, text="Crear Solicitud", command=self.ventana_creacion).grid(row=0, column=2, padx=10)
        ctk.CTkButton(self.root, text="Ir a Opciones", command=self.ir_a_opciones).pack(pady=10)

        self.root.mainloop()

    def obtener_seleccion(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
        else:
            print("No se ha seleccionado ninguna fila")

    def ventana_creacion(self):
        self.root.destroy()
        ingresar_ventana_creacion_usuario = regUS.RegistrarPrestamoParametrico()
        ingresar_ventana_creacion_usuario.root.mainloop()   

    def enviar_usuario(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            edtUs.recibir_prestamo(fila)
            self.root.destroy() 
            ingresar_ventana_edicion_usuario = edtUs.EditarPrestamoParametrico()
            ingresar_ventana_edicion_usuario.root.mainloop()
        else:
            print("No se ha seleccionado ninguna fila")    

    def eliminar_usuario(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            self.root.destroy()
            proyecto.eliminar_prestamo(fila)
            gestionar_prestamos_parametrico()
        else:
            print("No se ha seleccionado ninguna fila")   
    
    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""
        self.root.destroy()  # Cierra la ventana de gestión de empleados
        tipo_usuario = proyecto.retornar_tipo_usuario()
        ventana_principal.Opciones(tipo_usuario)  # Llama a la ventana de opciones
        
    # Método de ejemplo para volver al menú principal
    def volver_principal(self):
        self.root.destroy()  # Cierra la ventana actual
        gestionar_prestamos_parametrico()