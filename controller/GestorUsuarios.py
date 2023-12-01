

class GestorUsuarios:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GestorUsuarios, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def buscarUsuario(self, nombre):
        raise NotImplemented("HACER")
    
    def aceptarUsuario(idUsuario, idAmigo):
        raise NotImplemented("HACER")
    
    def añadirUsuarioGestor(idUsuario):
        raise NotImplemented("HACER")
    
    def borrarUsuario(idUsuario):
        raise NotImplemented("HACER")