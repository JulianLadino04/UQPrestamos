import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from interfaces.ventanas.parametrico.gestionar_solicitud_parametrico_realizar_pago import RealizarPagoParametricoPrestamo
import interfaces.ventanas.parametrico.gestionar_solicitud_parametrico as gsp
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal

class gestionar_pagos_parametricos:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Solicitud Empleado")
        self.root.geometry("750x550")
        self.root.resizable(True, True)

        # Encabezado
        ctk.CTkLabel(master=self.root, text="Vista de pagos de Empleado", font=("Roboto", 36)).grid(row=0, column=0, columnspan=2, pady=15)

        # Crear variable para almacenar el préstamo seleccionado
        self.prestamo = tk.StringVar(value="Seleccione un préstamo")

        # Obtener los préstamos del cliente
        prestamos_cliente = proyecto.enviar_prestamos_cliente_pendientes()
        print(f"Préstamos del cliente: {prestamos_cliente}")

        # Preparar los IDs de préstamos para el OptionMenu con la verificación mejorada
        prestamos_cliente_str = []
        if isinstance(prestamos_cliente, list) and all(isinstance(p, (tuple, int)) for p in prestamos_cliente):
            prestamos_cliente_str = [str(prestamo[0] if isinstance(prestamo, tuple) else prestamo) for prestamo in prestamos_cliente]
        else:
            print("Error: El formato de préstamos no es el esperado.")
        
        # Comprobar si hay datos antes de configurar el OptionMenu
        if not prestamos_cliente_str:
            prestamos_cliente_str = ["No hay préstamos disponibles"]

        # Menú desplegable para seleccionar el préstamo
        self.option_menu = ctk.CTkOptionMenu(
            master=self.root,
            variable=self.prestamo,
            values=prestamos_cliente_str,
            command=self.cargar_pagos  # Llamada a cargar pagos cada vez que se selecciona un préstamo
        )
        self.option_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

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

    def cargar_pagos(self, selected_prestamo):
        """Cargar los pagos asociados al préstamo seleccionado y actualizar la tabla."""
        try:
            # Verificar que se ha seleccionado un préstamo válido
            if selected_prestamo == "Seleccione un préstamo" or selected_prestamo == "No hay préstamos disponibles":
                print("No se ha seleccionado un préstamo válido.")
                return

            # Obtener los pagos para el préstamo seleccionado
            pagos = proyecto.obtener_pagos_prestamos(selected_prestamo)
            print(f"Pagos obtenidos para el préstamo {selected_prestamo}: {pagos}")

            # Limpiar la tabla antes de insertar los nuevos datos
            self.tree.delete(*self.tree.get_children())

            # Configurar las columnas del Treeview si no se han configurado
            columnas = ["ID_Prestamo", "Valor_Pago", "Moroso", "Numero_Cuota"]
            for col in columnas:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.CENTER, width=120, stretch=False)

            # Insertar los pagos obtenidos en la tabla
            for pago in pagos:
                self.tree.insert('', tk.END, values=pago)

        except Exception as e:
            print(f"Error al cargar los pagos para el préstamo {selected_prestamo}: {e}")

    def obtener_seleccion(self):
        selected_prestamo = self.prestamo.get()
        if selected_prestamo and selected_prestamo != "Seleccione un préstamo" and selected_prestamo != "No hay préstamos disponibles":
            print(f"Préstamo seleccionado para pago: {selected_prestamo}")
            # Abrir la ventana para realizar el pago y pasar el ID del préstamo seleccionado
            self.root.destroy()
            realizar_pago_prestamo = RealizarPagoParametricoPrestamo(selected_prestamo)
            realizar_pago_prestamo.root.mainloop()
        else:
            print("No se ha seleccionado ningún préstamo válido")
    
    def ir_a_opciones(self):
        self.root.destroy()
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)
        
    def volver_principal(self):
        self.root.destroy()
        ingresar_ventana_solicitud = gsp.gestionar_solicitud_parametrico()
        ingresar_ventana_solicitud.root.mainloop()
