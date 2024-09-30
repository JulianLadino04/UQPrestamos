import customtkinter as ctk
import os
import interfaces.GUI as ventana_principal
import logica.proyecto as proyecto
import interfaces.ventanas.administrador.gestionar_sucursal_editar as eds
import interfaces.ventanas.administrador.gestionar_sucursal_registrar as regs
from PIL import Image
from tkinter import ttk
import tkinter as tk
   
class gestionar_sucursales:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sucursales")
        self.root.geometry("750x550")
        self.root.resizable(True, True)

        ctk.CTkLabel(master=self.root, text="Vista de Sucursales del Sistema", font=("Roboto", 36)).pack(pady=15)

        # Configurar la conexión a Oracle
        try:
            connection = proyecto.conexion_oracle()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM SUCURSAL")

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
        ancho_columnas = 240
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
        ctk.CTkButton(botones_frame, text="Editar Sucursal", command=self.editar_sucursal).grid(row=0, column=0, padx=10)
        ctk.CTkButton(botones_frame, text="Eliminar Sucursal", command=self.eliminar_sucursal).grid(row=0, column=1, padx=10)
        ctk.CTkButton(botones_frame, text="Crear Sucursal", command=self.crear_sucursal).grid(row=0, column=2, padx=10)
        ctk.CTkButton(self.root, text="Ir a Opciones", command=self.ir_a_opciones).pack(pady=10)

        self.root.mainloop()

    def obtener_seleccion(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
        else:
            print("No se ha seleccionado ninguna fila")
            
    def crear_sucursal(self):
        self.root.destroy()
        ingresar_ventana_creacion_sucursal = regs.RegistrarSucursal()
        ingresar_ventana_creacion_sucursal.root.mainloop()
                   
    def editar_sucursal(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            eds.recibir_sucursales(fila)
            self.root.destroy()
            ingresar_ventana_edicion_sucursal = eds.EditarSucursal()
            ingresar_ventana_edicion_sucursal.root.mainloop()
        else:
            print("No se ha seleccionado ninguna fila")   

    def eliminar_sucursal(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            self.root.destroy()
            proyecto.eliminar_sucursal(fila)
            gestionar_sucursales()
        else:
            print("No se ha seleccionado ninguna fila")   
            
    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""
        self.root.destroy()  # Cierra la ventana de gestión de empleados
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)  # Llama a la ventana de opciones
        