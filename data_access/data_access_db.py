import pymysql
from entities.entities import User
from entities.entities import Empleado

def obtener_conexion():
    return pymysql.connect(host='',
                                user='',
                                password='',
                                db='')

#Conexio tabla user o empleador
class userCRUD:
    def insertar_user(self, user:User):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO user(nombre, apellido, correo, telefono, compania, contrasena) VALUES (%s, %s,%s,%s, %s, %s)",
                       (user.nombre, user.apellido, user.email, user.telefono, user.compania,user.contrasena,))
        conexion.commit()
        conexion.close()

    def eliminar_user(self, id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM user WHERE id = %s", (id,))
        conexion.commit()
        conexion.close()

    def obtener_user_por_id(self, id) -> User:
        conexion = obtener_conexion()
        user = None
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nombre, apellido, correo, telefono, compania, contrasena FROM user WHERE id = %s", (id,))
                resultado = cursor.fetchone()
                if resultado:
                    user = User(
                        id=resultado[0],
                        nombre=resultado[1],
                        apellido=resultado[2],
                        email=resultado[3],
                        telefono=resultado[4],
                        compania=resultado[5],
                        contrasena=resultado[6]
                    )
                else:
                    print("No se encontró un usuario con el ID proporcionado.")
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
        finally:
            conexion.close()
        return user

    def actualizar_user(self, user:User):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE user SET nombre = %s, apellido = %s, correo = %s, telefono = %s, compania = %s WHERE id = %s",
                        (user.nombre, user.apellido, user.email, user.telefono, user.compania, user.id))
        conexion.commit()
        conexion.close()

    def actualizar_contrasena(self, contrasena:str, id:int):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE user SET contrasena = %s WHERE id = %s",
                        (contrasena, id))
        conexion.commit()
        conexion.close()

    def login(self, email, contrasena) -> User:
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                sql = """
                SELECT id, nombre, apellido, correo, contrasena, compania, telefono
                FROM user
                WHERE correo = %s AND contrasena = %s
                """
                cursor.execute(sql, (email, contrasena))
                resultado = cursor.fetchone()
                if resultado:
                    user = User(
                    id=resultado[0],
                    nombre=resultado[1],
                    apellido=resultado[2],
                    email=resultado[3],
                    contrasena=resultado[4],
                    compania=resultado[5],
                    telefono=resultado[6])
                    return user
                else:
                    print("No se encontró un usuario con el correo y contraseña proporcionados.")
                    return None
        except pymysql.MySQLError as e:
            print(f"Error al obtener el usuario: {e}")
        finally:
            conexion.close()    

#Conexion con la tabla de empleados
class EmpleadoCRUD:
    def insertar_empleados(self, empleado:Empleado):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO empleado(nombre, apellidos, email, numero_telefono, salario_bruto_mensual, posicion, user_id) VALUES (%s, %s,%s,%s, %s,%s, %s)",
                       (empleado.nombre, empleado.apellido, empleado.email, empleado.telefono, empleado.salarioBruto, empleado.posicion ,empleado.userId,))
        conexion.commit()
        conexion.close()
    
    def obtener_empleados_por_user_id(self, user_id: int):
        conexion = obtener_conexion()
        empleados = []
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM empleado WHERE user_id = %s", (user_id,))
                resultados = cursor.fetchall()
                for fila in resultados:
                    empleado = Empleado(
                        id=fila[0],
                        nombre=fila[1],
                        apellido=fila[2],
                        email=fila[3],
                        telefono=fila[4],
                        salarioBruto=fila[5],
                        posicion=fila[6],
                        userId=fila[7]
                    )
                    empleados.append(empleado)
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
        finally:
            conexion.close()
        return empleados

    def obtener_empleados_por_id(self, id) -> Empleado:
        conexion = obtener_conexion()
        empleado = None
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nombre, apellidos, email, numero_telefono, salario_bruto_mensual, user_id , posicion FROM empleado WHERE id = %s", (id,))
                resultado = cursor.fetchone()
                if resultado:
                    empleado = Empleado(
                        id=resultado[0],
                        nombre=resultado[1],
                        apellido=resultado[2],
                        email=resultado[3],
                        telefono=resultado[4],
                        salarioBruto=resultado[5],
                        userId=resultado[6],
                        posicion=resultado[7]
                    )
                else:
                    print("No se encontró un usuario con el ID proporcionado.")
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
        finally:
            conexion.close()
        return empleado

    def obtener_cantidad_empleados_por_user_id(self, user_id: int) -> int:
        conexion = obtener_conexion()
        cantidad_empleados = 0
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM empleado WHERE user_id = %s", (user_id,))
                cantidad_empleados = cursor.fetchone()[0]
        except Exception as e:
            print(f"Error al obtener la cantidad de empleados: {e}")
        finally:
            conexion.close()
        return cantidad_empleados

    def obtener_suma_salarios_por_user_id(self, user_id: int) -> float:
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT SUM(salario_bruto_mensual) FROM empleado WHERE user_id = %s", (user_id,))
                resultado = cursor.fetchone()
                suma_salarios = resultado[0] if resultado[0] is not None else 0.0
        except Exception as e:
            print(f"Error al obtener la suma de salarios: {e}")
            suma_salarios = 0.0
        finally:
            conexion.close()
        return suma_salarios
    
    def actualizar_empleado(self, empleado: Empleado):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "UPDATE empleado SET nombre = %s, apellidos = %s, email = %s, numero_telefono = %s, salario_bruto_mensual = %s, posicion = %s, user_id = %s WHERE id = %s",
                    (empleado.nombre, empleado.apellido, empleado.email, empleado.telefono, empleado.salarioBruto, empleado.posicion, empleado.userId, empleado.id))
            conexion.commit()
        except Exception as e:
            print(f"Error al actualizar el empleado: {e}")
        finally:
            conexion.close()
            
    def eliminar_empleado(self, id: int):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM empleado WHERE id = %s", (id,))
            conexion.commit()
        except Exception as e:
            print(f"Error al eliminar el empleado: {e}")
        finally:
            conexion.close()

    def eliminar_empleados_por_usuario(self,user_id):
            connection = obtener_conexion()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM empleado WHERE user_id = %s", (user_id,))
            connection.commit()
            connection.close()
