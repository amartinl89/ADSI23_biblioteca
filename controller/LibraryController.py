from model import Connection, Book, User, Reseña, Reserva
from model.tools import hash_password
import json
from model.Foro import Tema, Hilo, Comentario
db = Connection()

class LibraryController:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(LibraryController, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance


    def search_books(self, title="", author="", limit=6, page=0):
        count = db.select("""
                SELECT count()
                FROM Book b, Author a
                WHERE b.author=a.id
                AND b.title LIKE ?
                AND a.name LIKE ?
        """, (f"%{title}%", f"%{author}%"))[0][0]
        res = db.select("""
                SELECT b.*
                FROM Book b, Author a
                WHERE b.author=a.id
                    AND b.title LIKE ?
                    AND a.name LIKE ?
                LIMIT ? OFFSET ?
        """, (f"%{title}%", f"%{author}%", limit, limit*page))
        books = [
            Book(b[0],b[1],b[2],b[3],b[4])
            for b in res
		]
        return books, count
    def search_booksTodos(self, title="", author="",limit=100000, page=0):
        count = db.select("""
                SELECT count()
                FROM Book b, Author a
                WHERE b.author=a.id
                AND b.title LIKE ?
                AND a.name LIKE ?
        """, (f"%{title}%", f"%{author}%"))[0][0]
        res = db.select("""
                SELECT b.*
                FROM Book b, Author a
                WHERE b.author=a.id
                    AND b.title LIKE ?
                    AND a.name LIKE ?
                LIMIT ? OFFSET ?
        """, (f"%{title}%", f"%{author}%", limit, limit*page))
        books = [
            Book(b[0],b[1],b[2],b[3],b[4])
            for b in res
		]
        return books, count
    def get_user(self, email, password):
        user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2])
        else:
            return None

    def get_user_cookies(self, token, time):
        user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2])
        else:
            return None
    
    def getBook(self, idLibro):
        consulta = db.select("SELECT * FROM Book WHERE id = ?", (idLibro,))
        if len(consulta) > 0:
            libro = Book(consulta[0][0], consulta[0][1], consulta[0][2], consulta[0][3], consulta[0][4])
            return libro
        else:
            return None
    def crearUsuario(self, nombre, email, password):
        db.insert("INSERT INTO User (name, email, password) VALUES (?, ?, ?)", (nombre, email, hash_password(password)))
    def estaUsuario(self, email):
        consulta = db.select("SELECT * FROM User WHERE email = ?", (email,))
        if len(consulta) > 0:
            return True
        else:
            return False
    #GESTOR RESERVAS
    def guardarReserva(self, idUsuario, idLibro, fechaHoraReserva, fechaDevolucion):
        db.insert("INSERT INTO Reserva (idUsuario, idLibro, fechaHoraReserva, fechaDevolucion) VALUES (?, ?, ?, ?)", (idUsuario, idLibro, fechaHoraReserva, fechaDevolucion))
    
    def getReservas(self, idUsuario):
        raise NotImplemented("HACER")
    
    def getHistorial(self, idUsuario):
        consulta = db.select("SELECT Book.title, Reserva.fechaHoraReserva, Reserva.fechaDevolucion, Reserva.idLibro FROM Reserva JOIN Book ON Reserva.idLibro = Book.id WHERE Reserva.idUsuario == ?",(idUsuario,))
        if len(consulta) > 0:
            historial=[{"titulo":h[0], "fechaHoraReserva":h[1], "fechaDevolucion":h[2], "idLibro":h[3]} for h in consulta]
            return historial
        else:
            return None
        
    def libroReservado(self,idLibro, fechaHoraReserva):
        consulta = db.select("SELECT * FROM Reserva WHERE idLibro = ? AND fechaDevolucion  > ?", (idLibro, fechaHoraReserva,))
        if len(consulta) > 0:
            return True
        else:
            return False
    
    def devolverReserva(self, idUsuario, idLibro, fechaHoraReserva, hoy):
        db.update("UPDATE Reserva SET fechaDevolucion = ? WHERE idUsuario = ? AND idLibro = ? AND fechaHoraReserva = ?", (hoy, idUsuario, idLibro, fechaHoraReserva,))
    def buscarReservas(self, idUsuario):
        raise NotImplemented("HACER")
    
	#GESTOR HILOS
    def crearComentario(self, idtema, idHilos, texto, idUser):
        raise NotImplemented("HACER")
    # GESTOR FOROS
    def crear_tema(self, nombre_tema):
        db.insert("INSERT INTO Tema (nombre) VALUES (?)", (nombre_tema,))

    def get_temas(self):
        temas = db.select("SELECT rowid, nombre FROM Tema")
        return [Tema(t[0], t[1]) for t in temas]

    def crear_hilo(self, id_tema, texto, id_usuario):
        db.insert("INSERT INTO Hilo (rowid, texto, id_usuario) VALUES (?, ?, ?)", (id_tema, texto, id_usuario))

    def get_hilos(self, id_tema):
        return db.select("SELECT * FROM Hilo WHERE id_tema = ?", (id_tema,))
    
    def explorar_hilos(self, id_tema):
        hilos = db.select("SELECT rowid, id_tema, texto, id_usuario FROM Hilo WHERE id_tema = ?", (id_tema,))
        return [Hilo(h[0], h[1], h[2], h[3]) for h in hilos]

    def crear_comentario(self, id_tema, id_hilo, texto, id_usuario):
        db.insert("INSERT INTO Comentario (id_tema, id_hilo, texto, id_usuario) VALUES (?, ?, ?, ?)", (id_tema, id_hilo, texto, id_usuario))
	#GESTOR LIBROS
    def getCatalogo(self):
        raise NotImplemented("HACER")
    
    def disponible(self,idLibro):
        raise NotImplemented("HACER")
    
    def registrarLibro(self, idLibro):
        raise NotImplemented("HACER")
    
    def borrarLibro(self, idLibro):
        raise NotImplemented("HACER")
    
	#GESTOR RESEÑAS
    def getReseñasUsuario(self,idUsuario, idLibro):
        consulta = db.select("SELECT Reseña, Puntuacion FROM Reseña WHERE idUsuario= ? AND idLibro= ?",(idUsuario,idLibro,))
        #print(consulta[0][0])
        if len(consulta) > 0:
            resena = {"reseña": consulta[0][0], "puntuacion": consulta[0][1] if len(consulta[0]) > 1 else None}
            return resena
        else:
            return None
    
    def escribirReseña(self, idUsuario, idLibro, reseña, punt): 
        db.insert("INSERT INTO Reseña (idUsuario, idLibro, reseña, puntuacion) VALUES (?, ?, ?, ?)", (idUsuario, idLibro, reseña, punt))
    def modificarReseña(self, idUsuario, idLibro, reseña, punt):
        db.update("UPDATE Reseña SET idUsuario= ? , idLibro= ?, reseña = ?, puntuacion= ?" +
                             " WHERE idUsuario= ? AND idLibro= ?",(idUsuario,idLibro, reseña, punt, idUsuario, idLibro,))

    def comprobarReseña(self, idUsuario, idLibro):
        consulta = db.select("SELECT * FROM Reseña WHERE idUsuario = ? AND idLibro = ?", (idUsuario, idLibro,))
        return len(consulta)
    def getPuntuacion(self, idLibro):
        consulta = db.select("SELECT AVG(puntuacion) FROM Reseña WHERE idLibro = ?", (idLibro,))
        return consulta[0][0]

	#GESTOR USUARIOS
    def buscarUsuario(self, nombre):
        raise NotImplemented("HACER")
    
    def aceptarUsuario(idUsuario, idAmigo):
        raise NotImplemented("HACER")
    
    def añadirUsuarioGestor(idUsuario):
        raise NotImplemented("HACER")
    
    def borrarUsuario(idUsuario):
        raise NotImplemented("HACER")
    def getAmigos(self, idUsuario):
       consulta = db.select("SELECT u.* FROM User u, Amigos a WHERE u.id = a.idUsuario2 AND a.idUsuario1 = ?", (idUsuario,))
       if len(consulta) > 0:
           amigos = [User(u[0], u[1], u[2]) for u in consulta]
           return amigos
       else:
           return None