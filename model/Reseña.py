

class Reseña:
    def __init__(self, idUsuario, idLibro, reseña, puntuacion, idReseña):
        self.idUsuario = idUsuario
        self.idLibro = idLibro
        self.reseña = reseña
        self.puntuacion = puntuacion
        self.idReseña = idReseña
    def __str__(self):
        return f"{self.idUsuario} ({self.idLibro}) ({self.reseña}) ({self.puntuacion}) ({self.idReseña})"