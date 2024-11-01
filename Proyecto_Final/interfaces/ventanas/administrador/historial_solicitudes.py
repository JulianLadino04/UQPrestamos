import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import interfaces.GUI as ventana_principal
from tkinter import ttk  # Importar ttk para Treeview
import logica.proyecto as proyecto

def recibir_prestamo(datos_prestamo_param):
    global datos_prestamo
    datos_prestamo = datos_prestamo_param
    print(datos_prestamo)

class HistorialPrestamos:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Historial de Préstamos")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        # IDs de empleados disponibles
        self.empleados_ids = [str(id_empleado) for id_empleado in proyecto.enviar_id_empleados()]

        # Frame para los campos
        self.form_frame = ctk.CTkFrame(self.root)
        self.form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Combobox para seleccionar el ID del empleado
        self.selected_empleado_id = tk.StringVar()
        ctk.CTkLabel(self.form_frame, text="Seleccione ID Empleado", font=("Roboto", 18)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.empleado_combo = ctk.CTkOptionMenu(self.form_frame, variable=self.selected_empleado_id, values=self.empleados_ids, command=lambda empleado_id: self.cargar_historial(empleado_id))
        self.empleado_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")


        # Frame para mostrar el historial de préstamos
        self.table_frame = ctk.CTkFrame(self.root)
        self.table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Crear el Treeview
        self.tree = ttk.Treeview(self.table_frame, columns=("id_solicitud", "fecha_solicitud", "id_empleado", "monto", "periodo", "estado", "tasa_interes"), show='headings')
        self.tree.pack(side="left", fill="both", expand=True)

        # Configurar las columnas
        self.tree.heading("id_solicitud", text="ID Solicitud")
        self.tree.heading("fecha_solicitud", text="Fecha Solicitud")
        self.tree.heading("id_empleado", text="ID Empleado")
        self.tree.heading("monto", text="Monto")
        self.tree.heading("periodo", text="Periodo")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("tasa_interes", text="Tasa de Interés")

        # Establecer el ancho de las columnas
        self.tree.column("id_solicitud", width=100, anchor="center")
        self.tree.column("fecha_solicitud", width=120, anchor="center")
        self.tree.column("id_empleado", width=100, anchor="center")
        self.tree.column("monto", width=100, anchor="center")
        self.tree.column("periodo", width=100, anchor="center")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.column("tasa_interes", width=100, anchor="center")

        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscroll=scrollbar.set)

        # Botón para salir
        ctk.CTkButton(self.root, text="Salir", command=self.salir).pack(pady=20)

    def cargar_historial(self, empleado_id):
        # Limpiar la tabla antes de mostrar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Obtener los datos del historial del préstamo
        datos = proyecto.obtener_historial_prestamos(empleado_id)

        if datos:
            # Rellenar la tabla con los datos de los préstamos
            for fila in datos:
                self.tree.insert("", "end", values=fila)  # Insertar fila en la tabla
        else:
            messagebox.showinfo("Información", "No se encontraron datos para este empleado.")

    def salir(self):
        self.root.destroy()
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)  # Llama a la ventana de opciones

# Ejemplo de uso
if __name__ == "__main__":
    app = HistorialPrestamos()
    app.root.mainloop()
