import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from interfaces.ventanas.empleado.gestionar_solicitud_empleado_realizar_pago import RealizarPagoPrestamo
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
import interfaces.ventanas.empleado.gestionar_solicitud_empleado as ge


class gestionar_pagos_empleado:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Solicitud Empleado")
        self.root.geometry("750x550")
        self.root.resizable(True, True)

        # Encabezado
        ctk.CTkLabel(master=self.root, text="Vista de pagos de Empleado", font=("Roboto", 36)).grid(row=0, column=0, columnspan=2, pady=15)

        # Crear variable para almacenar el préstamo seleccionado
        self.prestamo = tk.StringVar(value="Seleccione un préstamo")  # Inicializar la variable

        # Obtener los pagos del cliente
        pagos_cliente = proyecto.obtener_pagos_cliente(proyecto.enviar_id_usuario())  # Obtener los pagos del cliente
        print(f"Pagos Prestamo del cliente: {pagos_cliente}")  # Depuración

        # Ajustar aquí según el formato retornado
        if isinstance(pagos_cliente, list) and all(isinstance(p, tuple) and len(p) == 4 for p in pagos_cliente):
            prestamos_cliente_str = [str(prestamo[0]) for prestamo in pagos_cliente]  # Usar el ID_PRESTAMO para el menú
        else:
            print("Error: El formato de pagos no es el esperado.")
            prestamos_cliente_str = []

        # Menú desplegable para seleccionar el préstamo
        ctk.CTkOptionMenu(master=self.root, variable=self.prestamo, values=prestamos_cliente_str, command=self.cargar_pagos).grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Crear la tabla (Treeview) vacía al inicio
        self.tree = ttk.Treeview(self.root, columns=("ID_Prestamo", "Valor_Pago", "Moroso", "Numero_Cuota"), show="headings", height=10)

        # Estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#2e2e2e", foreground="#ffffff", rowheight=25, fieldbackground="#2e2e2e")

        # Empaquetar la tabla vacía
        self.tree.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")

        # Crear el marco para los botones
        botones_frame = ctk.CTkFrame(self.root)
        botones_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Añadir los botones alineados en fila usando grid
        ctk.CTkButton(botones_frame, text="Pagar Prestamo", command=self.obtener_seleccion).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.root, text="Ir a Opciones", command=self.ir_a_opciones).grid(row=4, column=0, columnspan=2, pady=10)

        self.root.mainloop()

    def cargar_pagos(self, *args):
        """Cargar todos los pagos del empleado y actualizar la tabla."""
        try:
            # Obtener el ID del empleado
            id_empleado = proyecto.enviar_id_usuario()  # Asumiendo que esta función devuelve el ID del empleado actual
            pagos = proyecto.obtener_pagos_cliente(id_empleado)

            # Imprimir los pagos obtenidos
            print(f"Pagos obtenidos para el empleado {id_empleado}: {pagos}")

            if pagos is None or len(pagos) == 0:
                print(f"No se encontraron pagos para el empleado: {id_empleado}")
                return

            self.tree.delete(*self.tree.get_children())

            # Configurar las columnas del Treeview
            columnas = ["ID_Prestamo", "Valor_Pago", "Moroso", "Numero_Cuota"]
            print(f"Columnas para la tabla: {columnas}")

            for col in columnas:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.CENTER, width=120, stretch=False)

            for pago in pagos:
                self.tree.insert('', tk.END, values=pago)

        except Exception as e:
            print(f"Error al obtener pagos del empleado: {e}")

    def obtener_seleccion(self):
        selected_prestamo = self.prestamo.get()  # Obtener el valor seleccionado del OptionMenu
        if selected_prestamo:
            print(f"Préstamo seleccionado: {selected_prestamo}")
            # Abrir la ventana para realizar el pago y pasar el ID del préstamo seleccionado
            self.root.destroy()
            realizar_pago_prestamo = RealizarPagoPrestamo(selected_prestamo)
            realizar_pago_prestamo.root.mainloop()
        else:
            print("No se ha seleccionado ningún préstamo")
    
    def ir_a_opciones(self):
        self.root.destroy()
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)
        
    def volver_principal(self):
        self.root.destroy()
        ingresar_ventana_solicitud = ge.gestionar_solicitud_empleado()
        ingresar_ventana_solicitud.root.mainloop()