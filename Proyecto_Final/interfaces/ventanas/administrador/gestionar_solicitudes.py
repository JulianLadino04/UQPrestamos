import customtkinter as ctk
import os
import logica.proyecto as proyecto
from PIL import Image
from tkinter import ttk
import tkinter as tk
import interfaces.GUI as ventana_principal
import interfaces.ventanas.administrador.gestionar_solicitudes_crear as reg
import interfaces.ventanas.administrador.gestionar_solicitudes_editar as edt

class gestionar_solicitudes:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Solicitudes del Sistema")
        self.root.geometry("1000x500")
        self.centrar_ventana()
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        # Título de la ventana
        title_label = ctk.CTkLabel(master=self.root, text="Solicitudes del Sistema", font=("Roboto", 28, "bold"))
        title_label.pack(pady=(20, 10))

        # Cargar datos de la base de datos
        self.datos_solicitudes = self.cargar_datos_solicitudes()

        # Crear tabla (Treeview)
        self.tree = self.crear_tabla()
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Marco para los botones
        botones_frame = ctk.CTkFrame(self.root)
        botones_frame.pack(pady=(10, 20))

        # Botones de acción
        ctk.CTkButton(botones_frame, text="Editar Solicitud", command=self.enviar_empleado, font=("Arial", 14, "bold"), width=150).grid(row=0, column=0, padx=10)
        ctk.CTkButton(botones_frame, text="Eliminar Solicitud", command=self.eliminar_empleado, font=("Arial", 14, "bold"), width=150).grid(row=0, column=1, padx=10)
        ctk.CTkButton(botones_frame, text="Crear Solicitud", command=self.ventana_creacion, font=("Arial", 14, "bold"), width=150).grid(row=0, column=2, padx=10)
        ctk.CTkButton(botones_frame, text="Ir a Opciones", command=self.ir_a_opciones, font=("Arial", 14, "bold"), width=150).grid(row=0, column=3, padx=10)

        # Expandir columnas en el frame de botones para un diseño más equilibrado
        for i in range(4):
            botones_frame.grid_columnconfigure(i, weight=1)

        self.root.mainloop()

    def centrar_ventana(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1000 // 2)
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"1000x500+{x}+{y}")

    def cargar_datos_solicitudes(self):
        """Cargar datos de la base de datos y devolverlos como una lista."""
        try:
            connection = proyecto.conexion_oracle()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM SOLICITUD")
            columnas = [desc[0] for desc in cursor.description]
            filas = cursor.fetchall()
            cursor.close()
            connection.close()
            return columnas, filas
        except Exception as e:
            print(f"Error de conexión o consulta: {e}")
            return [], []

    def crear_tabla(self):
        """Crear y devolver el Treeview de las solicitudes."""
        columnas, filas = self.datos_solicitudes
        tree = ttk.Treeview(self.root, columns=columnas, show="headings", height=15)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#2e2e2e", foreground="#ffffff", rowheight=25, fieldbackground="#2e2e2e")

        # Cabeceras de la tabla
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150, stretch=True)
        for fila in filas:
            tree.insert('', tk.END, values=fila)
        return tree

    def obtener_seleccion(self):
        selected_item = self.tree.selection()
        return self.tree.item(selected_item)['values'] if selected_item else None

    def enviar_empleado(self):
        fila = self.obtener_seleccion()
        if fila:
            edt.recibir_solicitud(fila)
            self.root.destroy()
            edt.EditarSolicitudAdministradores(fila).root.mainloop()
        else:
            print("No se ha seleccionado ninguna fila")

    def eliminar_empleado(self):
        fila = self.obtener_seleccion()
        if fila:
            proyecto.eliminar_solicitud(fila)
            self.root.destroy()
            gestionar_solicitudes()
        else:
            print("No se ha seleccionado ninguna fila")

    def ventana_creacion(self):
        self.root.destroy()
        reg.CrearSolicitudAdministrador().root.mainloop()

    def ir_a_opciones(self):
        self.root.destroy()
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)

# Para iniciar la ventana
if __name__ == "__main__":
    gestionar_solicitudes()
