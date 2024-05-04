from .LibraryController import LibraryController
from flask import Flask, render_template, request, make_response, redirect
from datetime import datetime, timedelta
app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = LibraryController()


@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = library.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token


@app.after_request
def add_cookies(response):
	if 'user' in dir(request) and request.user and request.user.token:
		session = request.user.validate_session(request.user.token)
		response.set_cookie('token', session.hash)
		response.set_cookie('time', str(session.time))
	return response


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/catalogue')
def catalogue():
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(title=title, author=author, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('catalogue.html', books=books, title=title, author=author, current_page=page,
	                       total_pages=total_pages, max=max, min=min)

@app.route('/historial')
def historial():
	if 'user' not in dir(request) or not request.user:
		return redirect('/login')
	usuarioId = request.user.id
	historial = library.getHistorial(usuarioId)
	hoy = datetime.now().strftime('%Y-%m-%d')
	return render_template('historial.html', historial = historial, hoy=hoy)
@app.route('/reseña')
def resena():
	if 'user' not in dir(request) or not request.user:
		return redirect('/login')
	idLibro = request.values.get('idLibro')
	titulo = request.values.get("titulo")
	libro = {"titulo":titulo, "idLibro": idLibro}
	usuarioId = request.user.id
	resena = library.getReseñasUsuario(idUsuario=usuarioId, idLibro=idLibro)
	return render_template('reseña.html', resena = resena, libro=libro)
@app.route('/reseña', methods=['POST'])
def guardarResena():
	if 'user' not in dir(request) or not request.user:
		return redirect('/login')
	idLibro = request.values.get('idLibro')
	titulo = request.values.get("titulo")
	nuevaPuntuacion = request.form.get('nuevaPuntuacion')
	if(library.comprobarReseña(idUsuario=request.user.id, idLibro=idLibro)>0):
		library.modificarReseña(idUsuario=request.user.id, idLibro=idLibro, reseña=request.form.get('nuevaResena'), punt=nuevaPuntuacion)
	else:
		library.escribirReseña(idUsuario=request.user.id, idLibro=idLibro, reseña=request.form.get('nuevaResena'), punt=nuevaPuntuacion)
	historial = library.getHistorial(idUsuario=request.user.id)
	return render_template('historial.html', historial = historial)
@app.route('/escribirReseña')
def escribirResena():
	if 'user' not in dir(request) or not request.user:
		return redirect('/login')
	idLibro = request.values.get('idLibro')
	titulo = request.values.get("titulo")
	libro = {"titulo":titulo, "idLibro": idLibro}
	usuarioId = request.user.id
	resena = library.getReseñasUsuario(idUsuario=usuarioId, idLibro=idLibro)
	return render_template('escribirReseña.html', resena = resena, libro=libro)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = library.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp

@app.route('/hacerReserva')
def reservar():
	hoy = datetime.now().strftime('%Y-%m-%d')
	manana = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
	limite = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
	idLibro = request.values.get('idLibro')
	libro = library.getBook(idLibro)
	reservado = library.libroReservado(idLibro, hoy)
	return render_template('hacerReserva.html', libro=libro, hoy=hoy, manana=manana, limite=limite, reservado=reservado)

@app.route('/confirmarReserva', methods=['POST'])
def confirmarReserva():
	idLibro = request.values.get('idLibro')
	fechaReserva = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	fechaDevolucion = request.values.get('endDate')
	library.guardarReserva(request.user.id, idLibro, fechaReserva, fechaDevolucion)
	return redirect('/historial')

@app.route('/register', methods=['POST'])
def registrar():
	email = request.values.get("email")
	password = request.values.get("password")
	name = request.values.get("name")
	if library.estaUsuario(email):
		return render_template('register.html',esta=True)
	library.crearUsuario(name, email, password)
	user = library.get_user(email, password)

	session = user.new_session()
	resp = redirect("/")
	resp.set_cookie('token', session.hash)
	resp.set_cookie('time', str(session.time))
	return resp

@app.route('/register', methods=['GET'])
def register():
	return render_template('register.html',esta=False)

@app.route('/devlolverReserva', methods=['POST'])
def devolverReserva():
	idLibro = request.values.get('idLibro')
	hoy = datetime.now().strftime('%Y-%m-%d')
	fechaHoraReserva = request.values.get('fechaHoraReserva')
	library.devolverReserva(request.user.id, idLibro, fechaHoraReserva ,hoy)
	return redirect('/historial')


#Xabi
def es_nombre_valido(nombre):
    palabras_prohibidas = ["racista", "sexista"]
    return all(palabra.lower() not in nombre.lower() for palabra in palabras_prohibidas)

@app.route('/foros')
def lista_foros():
	if 'user' not in dir(request) or not request.user:
		return redirect('/login')
	temas = library.get_temas()
	return render_template('foros.html', temas=temas)

temas = library.get_temas()
@app.route('/nuevo_tema', methods=['GET', 'POST'])
def nuevo_tema():
	if 'user' not in dir(request) or not request.user:
		return redirect('/login')
	temas = library.get_temas()  # Recupera la lista de temas existentes

	if request.method == 'POST':
		nombre = request.form.get('nombre')
		if nombre and es_nombre_valido(nombre):
			# Crea un nuevo tema utilizando el gestor de temas
			library.crear_tema(nombre)
			# Recupera la lista de temas después de crear uno nuevo
			temas = library.get_temas()
			# Después de crear el tema, redirige al usuario a la página de exploración de temas
			return redirect('/explorar_temas')

	return render_template('nuevoTema.html', temas=temas)

@app.route('/explorar_temas')
def explorar_temas():
	if 'user' not in dir(request) or not request.user:
		return redirect('/login')
	temas = library.get_temas()
	return render_template('temas.html', temas=temas)

@app.route('/temas/<int:id_tema>')
def ver_hilos(id_tema):
	if 'user' not in dir(request) or not request.user:
		return redirect('/login')
	hilos = library.get_hilos(id_tema)
	return render_template('verHilo.html', hilos=hilos)