import os
import customtkinter as ctk
import oracledb
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
from reportlab.lib.pagesizes import landscape, legal
from reportlab.pdfgen import canvas
import tkinter as tk


class ver_reportes:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Reportes")
        self.root.geometry("550x300")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (550 // 2) + 200
        y = (screen_height // 2) - (300 // 2)
        self.root.geometry(f"550x300+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background="#2b2b2b")

        ctk.CTkLabel(master=self.root, text="Reportes del Sistema", font=("Roboto", 36)).pack(pady=15)

        botones_frame = ctk.CTkFrame(self.root)
        botones_frame.pack(pady=10)

        # Separar más los botones y cambiar la fuente
        ctk.CTkButton(botones_frame, text="Generar Reporte de Morosos", command=self.generar_reporte_morosos, 
                      font=("Arial", 12, "bold")).grid(row=0, column=0, padx=20, pady=10)
        ctk.CTkButton(botones_frame, text="Generar Reporte Total Prestado por Sucursal", command=self.generar_reporte_total_prestado_por_sucursal, 
                      font=("Arial", 12, "bold")).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(botones_frame, text="Generar Reporte Total Prestado por Municipio",
              command=self.generar_reporte_total_prestado_por_municipio, 
              font=("Arial", 12, "bold")).grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(botones_frame, text="Ir a opciones",
              command=self.ir_a_opciones, 
              font=("Arial", 12, "bold")).grid(row=3, column=0, padx=20, pady=10)


        self.root.mainloop()

    # Función para conectarse a la base de datos
    def get_connection(self):
        try:
            connection = oracledb.connect(
                user="SYSTEM",
                password="Arango2004",
                dsn="localhost:1521/xe"
            )
            return connection
        except oracledb.DatabaseError as e:
            print(f"Error al conectar a la base de datos: {e}")

    def obtener_morosos(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            sql = '''SELECT PR.ID_PRESTAMO, PA.NUMERO_CUOTA, PA.FECHA_PAGO, PA.VALOR_PAGO, 
                             E.ID_EMPLEADO, E.NOMBRE, PR.MONTO
                      FROM PAGO PA
                      JOIN PRESTAMO PR ON PA.ID_PRESTAMO = PR.ID_PRESTAMO
                      JOIN EMPLEADO E ON PR.EMPLEADO_ID = E.ID_EMPLEADO
                      WHERE PA.MOROSO = 'Y' '''
            cursor.execute(sql)
            morosos = cursor.fetchall()
            return morosos  # Retornar los datos de morosos para ser utilizados en el reporte
        except Exception as e:
            print(f"Error al mostrar los morosos: {e}")
        finally:
            cursor.close()
            connection.close()

    def generar_reporte_morosos(self):
        morosos = self.obtener_morosos()

        if not morosos:
            print("No hay empleados morosos.")
            return

        pdf_file = os.path.join(os.path.expanduser("~"), "Documents", "reporte_morosos.pdf")
        c = canvas.Canvas(pdf_file, pagesize=landscape(legal))  # Cambiamos a tamaño oficio y orientación horizontal
        width, height = landscape(legal)

        c.drawString(50, height - 50, "Reporte de Empleados Morosos")
        c.drawString(50, height - 70, f"{'ID Préstamo':<20} {'Número de Cuota':<20} {'Fecha de Pago':<20} {'Valor':<10} {'ID Empleado':<15} {'Nombre':<20} {'Monto Préstamo':<15}")
        c.drawString(50, height - 90, "-" * 140)  # Ajustamos el guion para que se vea mejor

        y_position = height - 110

        for moroso in morosos:
            numero_prestamo, numero_cuota, fecha_pago, valor_pago, id_empleado, nombre, monto_prestamo = moroso
            fecha_pago = fecha_pago.strftime("%Y-%m-%d") if fecha_pago else "N/A"  # Formateo de fecha
            c.drawString(50, y_position, f"{numero_prestamo:<20} {numero_cuota:<20} {fecha_pago:<20} {valor_pago:<10} {id_empleado:<15} {nombre:<20} {monto_prestamo:<15}")
            y_position -= 20

            if y_position < 50:
                c.showPage()
                y_position = height - 50

        try:
            c.save()
            print("Reporte de Morosos generado en el archivo:", pdf_file)
        except Exception as e:
            print(f"Error al generar el PDF: {e}")

    def obtener_total_prestado_por_sucursal(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            sql = '''SELECT S.NOMBRE, SUM(PR.MONTO) AS TOTAL_PRESTADO
                     FROM PRESTAMO PR
                     JOIN EMPLEADO E ON PR.EMPLEADO_ID = E.ID_EMPLEADO
                     JOIN SUCURSAL S ON E.ID_SUCURSAL = S.ID_SUCURSAL
                     GROUP BY S.NOMBRE'''
            cursor.execute(sql)
            total_prestado = cursor.fetchall()
            return total_prestado  # Retornar los datos de total prestado por sucursal
        except Exception as e:
            print(f"Error al obtener el total prestado por sucursal: {e}")
        finally:
            cursor.close()
            connection.close()

    def generar_reporte_total_prestado_por_sucursal(self):
        total_prestado = self.obtener_total_prestado_por_sucursal()

        if not total_prestado:
            print("No hay datos de préstamos por sucursal.")
            return

        pdf_file = os.path.join(os.path.expanduser("~"), "Documents", "reporte_total_prestado_por_sucursal.pdf")
        c = canvas.Canvas(pdf_file, pagesize=landscape(legal))  # Cambiamos a tamaño oficio y orientación horizontal
        width, height = landscape(legal)

        c.drawString(50, height - 50, "Reporte del Total Prestado por Sucursal")
        c.drawString(50, height - 70, f"{'Sucursal':<30} {'Total Prestado':<20}")
        c.drawString(50, height - 90, "-" * 50)  # Línea de separación

        y_position = height - 110

        for sucursal in total_prestado:
            nombre_sucursal, total = sucursal
            c.drawString(50, y_position, f"{nombre_sucursal:<30} {total:<20}")
            y_position -= 20

            if y_position < 50:
                c.showPage()
                y_position = height - 50

        try:
            c.save()
            print("Reporte del Total Prestado por Sucursal generado en el archivo:", pdf_file)
        except Exception as e:
            print(f"Error al generar el PDF: {e}")

    def obtener_total_prestado_por_municipio(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            sql = '''SELECT S.MUNICIPIO AS MUNICIPIO, SUM(PR.MONTO) AS TOTAL_PRESTADO
                    FROM PRESTAMO PR
                    JOIN EMPLEADO E ON PR.EMPLEADO_ID = E.ID_EMPLEADO
                    JOIN SUCURSAL S ON E.ID_SUCURSAL = S.ID_SUCURSAL
                    GROUP BY S.MUNICIPIO'''
            cursor.execute(sql)
            total_prestado = cursor.fetchall()
            return total_prestado  # Retornar los datos del total prestado por municipio
        except Exception as e:
            print(f"Error al obtener el total prestado por municipio: {e}")
        finally:
            cursor.close()
            connection.close()

    def generar_reporte_total_prestado_por_municipio(self):
        total_prestado = self.obtener_total_prestado_por_municipio()

        if not total_prestado:
            print("No hay datos de préstamos por municipio.")
            return

        pdf_file = os.path.join(os.path.expanduser("~"), "Documents", "reporte_total_prestado_por_municipio.pdf")
        c = canvas.Canvas(pdf_file, pagesize=landscape(legal))  # Cambiamos a tamaño oficio y orientación horizontal
        width, height = landscape(legal)

        c.drawString(50, height - 50, "Reporte del Total Prestado por Municipio")
        c.drawString(50, height - 70, f"{'Municipio':<30} {'Total Prestado':<20}")
        c.drawString(50, height - 90, "-" * 50)  # Línea de separación

        y_position = height - 110

        for municipio in total_prestado:
            nombre_municipio, total = municipio
            c.drawString(50, y_position, f"{nombre_municipio:<30} {total:<20}")
            y_position -= 20

            if y_position < 50:
                c.showPage()
                y_position = height - 50

        try:
            c.save()
            print("Reporte del Total Prestado por Municipio generado en el archivo:", pdf_file)
        except Exception as e:
            print(f"Error al generar el PDF: {e}")

    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""
        self.root.destroy()
        tipo_usuario = str(proyecto.retornar_tipo_usuario())
        ventana_principal.Opciones(tipo_usuario)  # Llama a la ventana de opciones


if __name__ == "__main__":
    ver_reportes()
