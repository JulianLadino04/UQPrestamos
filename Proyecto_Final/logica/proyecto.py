import customtkinter as ctk
import os
import oracledb
from tkinter import Image
from datetime import datetime

# Importación de módulos de lógica
import logica.table_ingreso as ingreso
import logica.table_empleados as empleados
import logica.table_pagos as pagos
import logica.table_prestamos as prestamos
import logica.table_solicitud as solicitudes
import logica.table_sucursales as sucursales
import logica.table_usuarios as usuarios
import logica.table_nivel as niveles
import logica.table_cargo as cargos
import logica.table_estado as estados
import logica.table_periodo as periodos
import logica.table_municipio as municipio
import logica.consultas_multitabla as consulta_multitabla


# Variables globales
usuario_sistema = []
id_usuario_sesion = ""
carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")

def enviar_id_usuario():
    return id_usuario_sesion

def verificar_credenciales(usuario: str, contrasena: str):
    usuario = usuarios.obtener_usuario_user(usuario, contrasena)
    global id_usuario_sesion
    id_usuario_sesion = usuario
    print(id_usuario_sesion)
    
    return usuario

# Conexión a Oracle
def conexion_oracle():
    try:
        connection = oracledb.connect(
            user="SYSTEM", 
            password="0000", 
            dsn="localhost:1521/xe"
        )
        return connection
    except oracledb.DatabaseError as e:
        print(f"Error al conectar a la base de datos: {e}")

# Funciones generales para obtener datos desde la BD

def obtener_tipo_usuario(usuario: str):
    usuario_ingresado = usuarios.obtener_tipo_user(usuario)
    return usuario_ingresado['tipo'] if usuario_ingresado else None

def id_sucursales():
    ids = sucursales.get_ids_sucursales()
    return ids if ids else ["No hay sucursales aun"]

def enviar_niveles():
    niveles_sistema = niveles.obtener_niveles()
    if niveles_sistema is None:
        print("No hay niveles registrados en la BD")
    return niveles_sistema

def enviar_cargos():
    cargos_sistema = cargos.retornar_nombres_cargos()
    if cargos_sistema is None:
        print("No hay cargos registrados en el sistema")
    return cargos_sistema

def enviar_municipios():
    return municipio.obtener_nombres_municipios()

# Manejo de imágenes
def enviar_imagen(nombre_imagen: str):
    ruta_imagen = os.path.join(carpeta_imagenes, f"{nombre_imagen}.png")
    return ruta_imagen

# Funciones de usuarios
def funciones_usuario():
    usuarios.create_usuario("nestor_castelblanco", "0000", "Principal")
    
def crear_usuario(identificacion, nombre, usuario, contrasena, nivel):
    usuarios.create_usuario(identificacion, nombre, usuario, contrasena, nivel)

def editar_usuario(identificacion, usuario, contrasena, nivel, nombre):
    usuarios.update_usuario(identificacion, usuario, contrasena, nivel, nombre)

def eliminar_usuario(elementos):
    identificacion = elementos[0]
    usuarios.delete_usuario(identificacion)

def almacenar_usuario_sistema(id_usuario):
    usuario_sistema.append(id_usuario)

def enviar_usuario_sesion():
    return usuario_sistema

def obtener_cargo_usuario(id_usuario):
    return empleados.obtener_cargo(id_usuario)

# Funciones de empleados
def crear_empleado(identificacion, nombre, cargo, salario, sucursal, nivel, usuario, contrasena):
    empleados.crear_empleado(identificacion, nombre, cargo, salario, sucursal, nivel, usuario, contrasena)

def editar_empleado(identificacion, nombre, cargo, salario, sucursal, nivel):
    empleados.actualizar_empleado(identificacion, nombre, cargo, salario, sucursal, nivel)

def eliminar_empleado(elementos):
    identificacion = elementos[0]
    empleados.eliminar_empleado(identificacion)

def enviar_id_empleados():
    ids_empleados = empleados.obtener_id_empleados()
    return ids_empleados if ids_empleados else ["No hay empleados aun"]

# Funciones de sucursales
def crear_sucursal(id_sucursal, nombre, municipio):
    sucursales.create_sucursal(id_sucursal, nombre, municipio)

def editar_sucursal(id_sucursal, nombre, municipio):
    sucursales.update_sucursal(id_sucursal, nombre, municipio)

def eliminar_sucursal(fila):
    id_sucursal = fila[0]
    sucursales.delete_sucursal(id_sucursal)

# Funciones de solicitudes
def crear_solicitud(fecha_solicitud, empleado_id, monto, periodo):
    solicitudes.registrar_solicitud(fecha_solicitud, empleado_id, monto, periodo)

def editar_solicitud(id_empleado, id_solicitud, monto, periodo):
    solicitudes.update_solicitud(id_empleado, id_solicitud, monto, periodo)

def eliminar_solicitud(elementos):
    identificacion = elementos[0]
    solicitudes.eliminar_solicitud(identificacion)

# Funciones de préstamos
def crear_prestamo(fecha_solicitud, empleado_id, monto, periodo):
    prestamos.create_prestamo(fecha_solicitud, empleado_id, monto, periodo)

def editar_prestamo(id_prestamo, monto, periodo):
    prestamos.update_prestamo(id_prestamo, monto, periodo)

def eliminar_prestamo(fila):
    id_prestamo = fila[0]
    prestamos.delete_prestamo(id_prestamo)

def crear_prestamo_solicitud(id_solicitud, fecha, id_empleado, monto, periodo, estado, tasa_interes, fecha_desembolso):
    prestamos.pasar_solicitud_prestamo(id_solicitud, fecha, id_empleado, monto, periodo, estado, tasa_interes, fecha_desembolso)

def obtener_historial_prestamos(empleado_id):
    try:
        return prestamos.read_prestamos(empleado_id)
    except Exception as e:
        print(f"Error al obtener historial de préstamos: {e}")
        return []

# Manejo de la sesión del usuario
def hora_ingreso_usuario():
    global usuario_sistema
    usuario_sistema.append(datetime.now())

def hora_salida_usuario():
    global usuario_sistema
    usuario_sistema.append(datetime.now())
    ingresar_ingreso_sistema()

def ingresar_ingreso_sistema():
    id_usuario_sistema = usuario_sistema[0]
    hora_ingreso = usuario_sistema[1]
    hora_salida = usuario_sistema[2]
    ingreso.create_ingreso(id_usuario_sistema, hora_ingreso, hora_salida)
    usuario_sistema.clear()

def retornar_tipo_usuario():
    tipo = usuarios.obtener_tipo_user_ID(usuario_sistema[0])
    return tipo

def obtener_tasa_interes(periodo):
    return periodos.buscar_por_cuotas(periodo)

def enviar_prestamos_cliente():
    prestamos_cliente = prestamos.read_prestamos(id_usuario_sesion) 
    return prestamos_cliente

def enviar_prestamos_cliente_pendientes():
    prestamos_cliente = prestamos.read_prestamos_pendientes(id_usuario_sesion) 
    return prestamos_cliente
   
def enviar_pagos_prestamo(prestamo_seleccionado):
    return pagos.enviar_pagos_prestamo(prestamo_seleccionado)

def obtener_pagos_cliente(id_usuario_sesion):
    return consulta_multitabla.obtener_pagos_cliente(id_usuario_sesion)

def obtener_pagos_prestamos(id_solicitud):
    return consulta_multitabla.obtener_pagos_prestamo(id_solicitud)

def editar_estado_solicitud(solicitud, estado):
    solicitudes.update_estado_solicitud(solicitud, estado)
    
def obtener_cuota_prestamo(id_prestamo):
    return prestamos.obtener_cuota_prestamo(id_prestamo)

def obtener_cuotas_prestamo(id_prestamo):
    return prestamos.obtener_cantidad_cuotas_prestamo(id_prestamo)

def pagar_prestamo(numero_prestamo, numero_pago, fecha_pago, valor):
    pagos.registrar_pago(numero_prestamo, numero_pago, fecha_pago, valor)
    
def pagar_prestamo_ultimo(numero_prestamo, numero_pago, fecha_pago, valor):
    pagos.registrar_pago(numero_prestamo, numero_pago, fecha_pago, valor)
    prestamos.prestamo_finalizado(numero_prestamo)