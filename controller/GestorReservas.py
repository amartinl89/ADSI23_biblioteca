

class GestorReservas:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GestorReservas, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def guardarReserva(self, idUsuario, idLibro, fechaHoraReserva, fechaDevolucion):
        raise NotImplemented("HACER")
    
    def getReservas(self, idUsuario):
        raise NotImplemented("HACER")
    
    def getHistorial(self, idUsuario):
        raise NotImplemented("HACER")
    
    def cancelarReserva(self, idUsuario, idLibrom, fechaHoraReserva):
        raise NotImplemented("HACER")
    def buscarReservas(self, idUsuario):
        raise NotImplemented("HACER")
