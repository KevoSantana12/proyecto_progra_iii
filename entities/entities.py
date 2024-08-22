class User:
    def __init__(self, id = None, nombre = None, apellido = None, compania = None, telefono = None, email = None, contrasena = None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasena = contrasena
        self.compania = compania
        self.telefono = telefono

class Empleado:
    def __init__(self, id = None, nombre = None, apellido = None, email = None, telefono = None, salarioBruto = None, userId = None, posicion = None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.salarioBruto = salarioBruto
        self.userId = userId
        self.posicion = posicion