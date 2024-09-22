import oracledb

#Importacion de logica de bd
import logica.table_ingreso as ingreso
import logica.table_empleados as empleados
import logica.table_pagos as pagos
import logica.table_prestamos as prestamos
import logica.table_solicitud as solicitudes
import logica.table_sucursales as sucursales
import logica.table_usuarios as usuarios

from datetime import datetime

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

def verificar_credenciales(usuario: str, contrasena: str):
    # Obtener el usuario desde la base de datos
    usuario_ingresado = usuarios.obtener_usuario_user(usuario)
    
    # Verificar si el usuario existe
    if usuario_ingresado is None:
        return False
    else:
        # Comparar usuario y contraseña ingresados
        if usuario_ingresado['username'] == usuario and usuario_ingresado['password'] == contrasena:
            return True
        else:
            return False
        
def obtener_tipo_usuario(usuario: str):
    # Obtener el usuario desde la base de datos
    usuario_ingresado = usuarios.obtener_tipo_user(usuario)
    
    # Verificar si el usuario existe
    if usuario_ingresado is None:
        return None
    else:
        return usuario_ingresado['tipo']
    
def funciones_usuario():
    usuarios.create_usuario("nestor_castelblanco", "0000", "Principal")
    # usuarios.create_usuario("NCF", "0000", "Principal")
    # usuarios.obtener_usuario_user(1)
    # usuarios.update_usuario(1, "nestor_castelblanco", "0000", "Empleado")
    # usuarios.delete_usuario(3)
    
def funciones_sucursal():
    sucursales.create_sucursal("Central", "Armenia")
    sucursales.obtener_sucursal(1)
    sucursales.update_sucursal(6, "Central", "Quibdo")
    sucursales.mostrarSucursales()
    sucursales.delete_sucursal(6)
    
def funciones_ingresos():
    ingreso.create_ingreso(1, datetime.now(), datetime.now())
    ingreso.create_ingreso(2, datetime.now(), datetime.now()) 
    ingreso.read_ingreso()
    ingreso.delete_ingreso(1)
    
def funciones_empleados():
    empleados.crear_empleado(1104697502, "Nicolas Rincon", "Operario", 2500000, 1)
    empleados.crear_empleado(1104697503, "Nicolas Rincon 1", "Operario", 2500000, 1)
    empleados.actualizar_empleado(1104697502, "Nicolas Loaiza", "Administrativo", 3500000, 2)
    empleados.eliminar_empleado(1104697503)
    empleados.leer_empleados()

def funciones_solicitud():
    # solicitudes.registrar_solicitud(datetime.now(),1104697502, 12000000, 72)
    # solicitudes.eliminar_solicitud(5)
    # solicitudes.mostrar_solicitudes()
    solicitudes.actualizar_solicitud(8, "aprobada")
    
def funciones_pago():
    pagos.registrar_pago(8, 1, datetime.now(), 750000)

#funciones_usuario()
#funciones_pago()
#funciones_solicitud()
#funciones_empleados()
#funciones_ingresos()    
#funciones_sucursal()
#funciones_auditoria()
##funciones_usuario()asd