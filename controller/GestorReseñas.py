

class GestorReseñas:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GestorReseñas, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
	
    def getReseñasUsuario(self,idUsuario, idLibro):
        raise NotImplemented("HACER")
    
    def escribirReseña(self, idUsuario, idLibro, reseña, punt):
        raise NotImplemented("HACER")
    
    def modificarReseña(self, idUsuario, idLibro, reseña, punt):
        raise NotImplemented("HACER")