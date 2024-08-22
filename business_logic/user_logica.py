from data_access.data_access_db import userCRUD
from data_access.data_access_db import EmpleadoCRUD
from entities.entities import User
import re

class User_logica:
    def __init__(self):
        self.data_access = userCRUD()
        self.empleado_data_access = EmpleadoCRUD()
        
    def crear_user(self, user:User):
        self.data_access.insertar_user(user=user)
    
    def get_user(self, id) -> User:
        return self.data_access.obtener_user_por_id(id=id)
    
    def update_user(self, userEditado: User, id:int):
        user = self.get_user(id)
        user.nombre = userEditado.nombre
        user.apellido = userEditado.apellido
        user.compania = userEditado.compania
        user.telefono = userEditado.telefono
        user.email = userEditado.email
        self.data_access.actualizar_user(user=user)
   
    def deleteUser(self, id):
        self.empleado_data_access.eliminar_empleados_por_usuario(id)
        self.data_access.eliminar_user(id)

    def login(self, email, contrasena) -> User:
        return self.data_access.login(email=email, contrasena=contrasena)
    
    def verificar_contrasena(self, contrasena, id) -> bool:
        user = self.get_user(id)
        if user.contrasena == contrasena:
            return True
        else:
            return False
        
    def update_contrasena(self, contrasena = None, id = None):
        user = self.get_user(id)
        self.data_access.actualizar_contrasena(contrasena=contrasena,id=id)
    
    def confirmar_contrasena(self, contrasena1 = None, contrasena2 = None)->bool:
        if contrasena1 == contrasena2:
            return True
        else:
            return False
        
    def verificar_caracteres(self, contrasena = None) -> bool:
        if contrasena is None:
            return False
        
        if len(contrasena) < 8:
            return False

        if not re.search(r'\d', contrasena):
            return False

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contrasena):
            return False
        
        if not re.search(r'[A-Z]', contrasena):
            return False

        return True