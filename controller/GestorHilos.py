

class GestorHilos:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GestorHilos, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def crearComentario(self, idtema, idHilos, texto, idUser):
        raise NotImplemented("HACER")