from model.Foro import Tema, Hilo, Comentario

class GestorForos:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GestorForos, cls).__new__(cls)
            cls.__instance.__initialized = False
            cls.__instance.temas = []  # Inicializar lista de temas
        return cls.__instance
    
    def crear_tema(self, nombre):
        id_tema = len(self.temas) + 1
        tema = Tema(id_tema, nombre)
        self.temas.append(tema)
        return tema

    def get_temas(self):
        return [{'nombre': tema.nombre} for tema in self.temas]

    def crear_hilo(self, id_tema, texto, id_user):
        tema = next((tema for tema in self.temas if tema.id_tema == id_tema), None)
        if tema:
            id_hilo = len(tema.hilos) + 1
            hilo = Hilo(id_hilo, id_tema, texto, id_user)
            tema.hilos.append(hilo)
            return hilo

    def get_hilos(self, id_tema):
        tema = next((tema for tema in self.temas if tema.id_tema == id_tema), None)
        if tema:
            return [{'id_hilo': hilo.id_hilo, 'texto': hilo.texto} for hilo in tema.hilos]

    def crear_comentario(self, id_tema, id_hilo, texto, id_user):
        tema = next((tema for tema in self.temas if tema.id_tema == id_tema), None)
        hilo = next((hilo for hilo in tema.hilos if hilo.id_hilo == id_hilo), None)
        if tema and hilo:
            comentario_id = len(hilo.comentarios) + 1
            comentario = Comentario(comentario_id, id_tema, id_hilo, texto, id_user)
            hilo.comentarios.append(comentario)
            return comentario