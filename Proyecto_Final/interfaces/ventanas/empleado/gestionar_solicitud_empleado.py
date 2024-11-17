import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
import interfaces.ventanas.empleado.gestionar_solicitud_empleado_registrar as reg
import interfaces.ventanas.empleado.gestionar_solicitud_empleado_editar as edt

class GestionarSolicitudEmpleado:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Gestión de Solicitudes")

        # Tamaño y posicionamiento de la ventana
        self.root.geometry("1000x500")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1000 // 2)
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f"1000x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        # Frame contenedor principal
        main_frame = ctk.CTkFrame(self.root, width=950, height=450, fg_color="#2b2b2b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Gestión de Solicitudes", font=("Arial", 24, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(20, 10))

        # Obtener el ID del usuario
        self.id_usuario = proyecto.enviar_usuario_sesion()[0]
        print("ID DEL USUARIO: ", self.id_usuario)

        # Configurar la conexión a Oracle y obtener las solicitudes
        self.solicitudes = self.obtener_solicitudes(self.id_usuario)

        # Crear la tabla (Treeview)
        self.tree = self.crear_tabla(main_frame, self.solicitudes)
        self.tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Crear botones
        self.crear_botones(main_frame)

        self.root.mainloop()

    def crear_botones(self, frame):
        """Crea los botones para las acciones disponibles."""
        botones_frame = ctk.CTkFrame(frame, fg_color="#2b2b2b")
        botones_frame.pack(pady=(10, 0))

        # Botones de acción
        ctk.CTkButton(botones_frame, text="Editar Solicitud", command=self.editar_solicitud, font=("Arial", 14), width=150).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(botones_frame, text="Eliminar Solicitud", command=self.eliminar_solicitud, font=("Arial", 14), width=150).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(botones_frame, text="Crear Solicitud", command=self.ventana_creacion, font=("Arial", 14), width=150).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(botones_frame, text="Ir a Opciones", command=self.ir_a_opciones, font=("Arial", 14), width=150).grid(row=0, column=3, padx=10, pady=10)

    def obtener_solicitudes(self, id_usuario):
        """Obtiene las solicitudes del usuario desde la base de datos."""
        try:
            with proyecto.conexion_oracle() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM SOLICITUD WHERE ID_EMPLEADO = :1", (id_usuario,))
                    columnas = [desc[0] for desc in cursor.description]
                    filas = cursor.fetchall()
                    if not filas:
                        print("No se encontraron solicitudes para el empleado.")
                    return (columnas, filas)
        except Exception as e:
            print(f"Error de conexión o consulta: {e}")
            return ([], [])

    def crear_tabla(self, frame, solicitudes):
        """Crea la tabla para mostrar las solicitudes."""
        columnas, filas = solicitudes
        tree = ttk.Treeview(frame, columns=columnas, show="headings", height=10)

        # Estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#2e2e2e", foreground="#ffffff", rowheight=25, fieldbackground="#2e2e2e")
        style.configure("Treeview.Heading", background="#444444", foreground="#ffffff", font=("Arial", 12, "bold"))

        # Configurar columnas
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150, stretch=False)

        # Insertar datos
        for fila in filas:
            tree.insert('', tk.END, values=fila)

        return tree

    def obtener_seleccion(self):
        """Obtiene la fila seleccionada en la tabla."""
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            return fila
        else:
            print("No se ha seleccionado ninguna fila")
            return None

    def editar_solicitud(self):
        """Acción para editar una solicitud seleccionada."""
        fila = self.obtener_seleccion()
        if fila and fila[5] == 'PENDIENTE':
            edt.recibir_solicitud(fila)
            self.root.destroy()
            edt.EditarSolicitudEmpleados().root.mainloop()
        else:
            print("No se puede editar la solicitud debido a que ya fue ajustada o no se ha seleccionado ninguna fila.")

    def eliminar_solicitud(self):
        """Acción para eliminar una solicitud seleccionada."""
        fila = self.obtener_seleccion()
        if fila and fila[5] == 'PENDIENTE':
            proyecto.eliminar_solicitud(fila)
            self.solicitudes = self.obtener_solicitudes(self.id_usuario)
            self.tree.delete(*self.tree.get_children())
            for fila in self.solicitudes[1]:
                self.tree.insert('', tk.END, values=fila)
        else:
            print("No se puede eliminar la solicitud debido a que ya fue ajustada o no se ha seleccionado ninguna fila.")

    def ventana_creacion(self):
        """Abre la ventana para crear una nueva solicitud."""
        self.root.destroy()
        reg.CrearSolicitudEmpleados().root.mainloop()

    def ir_a_opciones(self):
        """Regresa a la ventana principal de opciones."""
        self.root.destroy()
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)
