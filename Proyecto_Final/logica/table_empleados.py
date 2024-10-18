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

def crear_empleado(ID_EMPLEADO, nombre, cargo, salario, id_sucursal, nivel, usuario, contrasena):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        
        cursor.execute("SELECT COUNT(*) FROM CREDENCIALES WHERE USERNAME = :1 ", (usuario,) )
        if cursor.fetchone()[0] > 0:
            print ("El usuario ingresado ya esta en uso, utilice otro")
            return
        
        # Verificar si la identificación ya existe
        cursor.execute("SELECT COUNT(*) FROM Empleado WHERE ID_EMPLEADO = :1", (ID_EMPLEADO,))
        if cursor.fetchone()[0] > 0:
            print("La identificación ya existe. Elija otra.")
            return

        sql = '''INSERT INTO Empleado (ID_EMPLEADO, nombre, cargo, salario, id_sucursal,NIVEL_SISTEMA) 
                 VALUES (:1, :2, :3, :4, :5, :6)'''
        cursor.execute(sql, (ID_EMPLEADO, nombre, cargo, salario, id_sucursal, nivel))
        
        
        sql = '''INSERT INTO CREDENCIALES (USERNAME, PASSWORD, USUARIO) 
                 VALUES (:1, :2, :3)'''
        cursor.execute(sql, (usuario, contrasena, ID_EMPLEADO))
        
        connection.commit()
        print(f"Empleado '{nombre}' creado correctamente.")
    except Exception as e:
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

def actualizar_empleado(ID_EMPLEADO, nuevo_nombre=None, nuevo_cargo=None, nuevo_salario=None, nueva_sucursal=None, nivel=None):
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

        # Ejecutamos la consulta con los parámetros
        cursor.execute(sql, params)
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
        sql = "DELETE FROM Empleado WHERE ID_EMPLEADO = :1"
        cursor.execute(sql, (ID_EMPLEADO,))
        connection.commit()
        print(f"Empleado con identificación '{ID_EMPLEADO}' eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar el empleado: {e}")
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
