# Foro.py
class Tema:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class Hilo:
    def __init__(self, id, id_tema, texto, id_usuario):
        self.id = id
        self.id_tema = id_tema
        self.texto = texto
        self.id_usuario = id_usuario

class Comentario:
    def __init__(self, id, id_tema, id_hilo, texto, id_usuario):
        self.id = id
        self.id_tema = id_tema
        self.id_hilo = id_hilo
        self.texto = texto
        self.id_usuario = id_usuario