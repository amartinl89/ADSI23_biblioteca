class Reserva:
    def __init__(self, idUsuario, idLibro, fechaHoraReserva, fechaDevolucion):
        self.idUsuario = idUsuario
        self.idLibro = idLibro
        self.fechaHoraReserva = fechaHoraReserva
        self.fechaDevolucion = fechaDevolucion

    def añadirReservaGestor(self,idUsuario, idLibro, fechaHRes, fechaDev):
        raise NotImplemented("HACER")
    def __str__(self):
        return f"{self.idUsuario}"