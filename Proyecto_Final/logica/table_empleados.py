import oracledb

# Función para conectarse a la base de datos
def get_connection():
    try:
        connection = oracledb.connect(
            user="SYSTEM", 
            password="0000", 
            dsn="localhost:1521/xe"
        )
        return connection
    except oracledb.DatabaseError as e:
        print(f"Error al conectar a la base de datos: {e}")


## ----------- EMPLEADO ----------- ##
def obtener_cargo(id_usuario: str):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Consulta para buscar el usuario por su ID_EMPLEADO
        sql = """
        SELECT CARGO
        FROM EMPLEADO 
        WHERE ID_EMPLEADO = :1
        """
        cursor.execute(sql, (id_usuario,))  # Asegúrate de que esto sea una tupla

        # Obtener la fila completa de resultados
        fila = cursor.fetchone()

        if fila is None:
            print(f"No se encontró ningún usuario con el ID_EMPLEADO {id_usuario}.")
            return None
        else: 
            # Desempaquetar los resultados
            return fila[0]

    except Exception as e:
        print(f"Ocurrió un error al buscar el usuario: {str(e)}")

    finally:
        cursor.close()
        connection.close()
    
def crear_empleado(ID_EMPLEADO, nombre, cargo, salario, id_sucursal, nivel, usuario, contrasena, correo):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Verificar si el usuario ya existe en la tabla de credenciales
        cursor.execute("SELECT COUNT(*) FROM CREDENCIALES WHERE USERNAME = :1", (usuario,))
        if cursor.fetchone()[0] > 0:
            print("El usuario ingresado ya está en uso, utilice otro.")
            return
        
        # Verificar si la identificación ya existe
        cursor.execute("SELECT COUNT(*) FROM Empleado WHERE ID_EMPLEADO = :1", (ID_EMPLEADO,))
        if cursor.fetchone()[0] > 0:
            print("La identificación ya existe. Elija otra.")
            return
        
        # Insertar en la tabla Empleado
        sql_empleado = '''INSERT INTO Empleado (ID_EMPLEADO, nombre, cargo, salario, id_sucursal, NIVEL_SISTEMA, CORREO) 
                  VALUES (:1, :2, :3, :4, :5, :6, :7)'''
        cursor.execute(sql_empleado, (ID_EMPLEADO, nombre, cargo, salario, id_sucursal, nivel, correo))
        
        # Insertar en la tabla Credenciales
        sql_credenciales = '''INSERT INTO CREDENCIALES (USERNAME, PASSWORD, USUARIO) 
                               VALUES (:1, :2, :3)'''
        cursor.execute(sql_credenciales, (usuario, contrasena, ID_EMPLEADO))
        
        # Insertar en la tabla Usuario
        sql_usuario = '''INSERT INTO Usuario (ID_USUARIO, USERNAME, PASSWORD, NIVEL, NOMBRE) 
                         VALUES (:1, :2, :3, :4, :5)'''
        cursor.execute(sql_usuario, (ID_EMPLEADO, usuario, contrasena, nivel, nombre))
        
        # Confirmar los cambios
        connection.commit()
        print(f"Empleado '{nombre}' creado correctamente con usuario '{usuario}'.")
    except Exception as e:
        # Revertir la transacción en caso de error
        connection.rollback()
        print(f"Error al crear el empleado: {e}")
    finally:
        cursor.close()
        connection.close()



def leer_empleados():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Empleado")
        empleados = cursor.fetchall()
        for empleado in empleados:
            print(empleado)
    except Exception as e:
        print(f"Error al leer empleados: {e}")
    finally:
        cursor.close()
        connection.close()

def actualizar_empleado(ID_EMPLEADO, nuevo_nombre=None, nuevo_cargo=None, nuevo_salario=None, nueva_sucursal=None, nivel=None, nuevo_usuario=None, nueva_contrasena=None):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Verificamos qué campos se quieren actualizar y construimos dinámicamente la sentencia SQL
        sql = "UPDATE Empleado SET "
        updates = []
        params = []

        # Actualizar nombre
        if nuevo_nombre:
            updates.append("nombre = :1")
            params.append(nuevo_nombre)

        # Actualizar cargo con validación
        if nuevo_cargo:
            if nuevo_cargo not in ["Operario", "Administrativo", "Ejecutivo", "Otro"]:
                print("El cargo no es válido. Debe ser uno de los siguientes: Operario, Administrativo, Ejecutivo, Otro.")
                return
            updates.append("cargo = :2")
            params.append(nuevo_cargo)

        # Actualizar salario
        if nuevo_salario:
            updates.append("salario = :3")
            params.append(nuevo_salario)

        # Actualizar sucursal
        if nueva_sucursal:
            updates.append("id_sucursal = :4")
            params.append(nueva_sucursal)

        # Actualizar nivel con validación y usando el nombre correcto de la columna
        if nivel:
            if nivel not in ["Tesoreria", "Principal", "Empleado"]:
                print("El nivel no es válido. Debe ser uno de los siguientes: Tesoreria, Principal, Empleado.")
                return
            updates.append("nivel_sistema = :5")
            params.append(nivel)

        # Unimos las partes de la consulta
        if not updates:
            print("No se especificó ningún campo para actualizar.")
            return

        sql += ", ".join(updates) + " WHERE ID_EMPLEADO = :6"
        params.append(ID_EMPLEADO)

        # Ejecutamos la consulta para actualizar la tabla Empleado
        cursor.execute(sql, params)

        # Si el usuario o la contraseña también necesitan actualizarse
        if nuevo_usuario and nueva_contrasena:
            sql_usuario = "UPDATE Usuario SET USERNAME = :1, PASSWORD = :2 WHERE ID_USUARIO = :3"
            cursor.execute(sql_usuario, (nuevo_usuario, nueva_contrasena, ID_EMPLEADO))

        # Confirmamos la transacción
        connection.commit()
        print(f"Empleado con identificación '{ID_EMPLEADO}' actualizado correctamente.")
    
    except Exception as e:
        print(f"Error al actualizar el empleado: {e}")
    
    finally:
        cursor.close()
        connection.close()

def eliminar_empleado(ID_EMPLEADO):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Iniciar la transacción
        connection.begin()
        
        # Eliminar las credenciales relacionadas del Usuario y Credenciales
        sql_usuario = "DELETE FROM Usuario WHERE ID_USUARIO = :1"
        cursor.execute(sql_usuario, (ID_EMPLEADO,))

        sql_credenciales = "DELETE FROM Credenciales WHERE USUARIO = :1"
        cursor.execute(sql_credenciales, (ID_EMPLEADO,))
        
        # Eliminar al empleado
        sql_empleado = "DELETE FROM Empleado WHERE ID_EMPLEADO = :1"
        cursor.execute(sql_empleado, (ID_EMPLEADO,))
        
        # Confirmar los cambios
        connection.commit()
        print(f"Empleado con identificación '{ID_EMPLEADO}' y sus credenciales eliminados correctamente.")
    except Exception as e:
        connection.rollback()  # Revertir en caso de error
        print(f"Error al eliminar el empleado y sus credenciales: {e}")
    finally:
        cursor.close()
        connection.close()

def mostrarEmpleados():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT * FROM Empleado"
        cursor.execute(sql)
        records = cursor.fetchall()
        for x in records:
            print(x)
    except Exception as e:
        print(f"Error al mostrar empleados: {e}")
    finally:
        cursor.close()
        connection.close()

def obtener_id_empleados():
    connection = get_connection()  # Asumiendo que esta función devuelve una conexión válida
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT ID_EMPLEADO 
            FROM EMPLEADO
            ORDER BY ID_EMPLEADO ASC
        """)

        ids = cursor.fetchall()  # Obtener todos los resultados

        if ids:
            # Retornar una lista con solo los valores de los IDs
            return [id_empleado[0] for id_empleado in ids]
        else:
            return []

    except Exception as e:
        print(f"Ocurrió un error al obtener los IDs de empleados: {str(e)}")
        return []

    finally:
        cursor.close()
        connection.close()

def obtenerCorreoEmpleado(idEmpleado):
    connection = get_connection()  # Asumiendo que esta función devuelve una conexión válida
    cursor = connection.cursor()

    try:
        # Consulta parametrizada para evitar inyección SQL
        cursor.execute("""
            SELECT CORREO 
            FROM EMPLEADO 
            WHERE ID_EMPLEADO = :idEmpleado
        """, {"idEmpleado": idEmpleado})

        # Obtener el resultado
        correo = cursor.fetchone()

        if correo:
            # Retorna el correo como una cadena
            return correo[0]
        else:
            # Retorna None si no se encontró el empleado
            return None

    except Exception as e:
        print(f"Ocurrió un error al obtener el correo del empleado: {str(e)}")
        return None

    finally:
        cursor.close()
        connection.close()
