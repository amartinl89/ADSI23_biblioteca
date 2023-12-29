from . import BaseTestClass
from bs4 import BeautifulSoup
from controller import LibraryController
from model import Connection

db = Connection()

class TestEscribirReseña(BaseTestClass):
    def test_insertar_resena(self):
        #Se añaden reservas al historial
        if (LibraryController.LibraryController().comprobarReseña(2, 1)<0):
            db.insert("INSERT INTO Reserva VALUES ('2','1','2021-11-11 12:12:33','2022-11-11 18:12:33')")
        # Inicia sesión
        self.login('jhon@gmail.com', '123')

        # Realiza una solicitud POST a la vista de guardar reseña con datos simulados
        datos_resena = {
            'idLibro': 1,  
            'titulo': 'Ligeros libertinajes sabaticos', 
            'nuevaResena': 'Esta es una reseña de prueba.',
            'nuevaPuntuacion': 5
        }
        res = self.client.post('/reseña', data=datos_resena, follow_redirects=True)

        # Verifica que la solicitud se procese correctamente
        self.assertEqual(200, res.status_code)

        # Verifica que la reseña se haya insertado correctamente en la base de datos
        #id_libro = datos_resena['idLibro']
        reseña_insertada =LibraryController.LibraryController().comprobarReseña(2, 1)
        self.assertIsNotNone(reseña_insertada)
        self.assertEqual(1, reseña_insertada)

    def test_ver_resenas(self):
        res=self.login('jhon@gmail.com', '123')
        res = self.client.get(res.headers['Location'])
        datos_libro = {'idLibro': 1,'titulo':'Ligeros+libertinajes+sabaticos'}
        res = self.client.get('/reseña', query_string=datos_libro)
        self.assertEqual(200, res.status_code)
        html_response =res.data
        # Parsear el HTML
        soup = BeautifulSoup(html_response, 'html.parser')

        # Encontrar todos los elementos que contienen puntuación y reseña
        reseñas_elements = soup.find_all('div', class_='reseña')
        reseñas_elements = soup.find_all('p')
        puntuacion = reseñas_elements[1]
        puntuacion = str(puntuacion)
        reseña = reseñas_elements[0]
        reseña = str(reseña)
        # Realizar assert equal
        self.assertEqual(puntuacion,"<p>Puntuación: 5 /10</p>")
        self.assertEqual(reseña,"<p>Esta es una reseña de prueba.</p>")