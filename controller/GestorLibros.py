
class GestorLibros:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GestorLibros, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def getCatalogo(self):
        raise NotImplemented("HACER")
    
    def disponible(self,idLibro):
        raise NotImplemented("HACER")
    
    def registrarLibro(self, idLibro):
        raise NotImplemented("HACER")
    
    def borrarLibro(self, idLibro):
        raise NotImplemented("HACER")