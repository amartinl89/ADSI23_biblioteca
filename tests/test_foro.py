import unittest
from webServer import app, gestor_foros

class TestForo(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_crear_tema_existente(self):
        response = self.app.post('/nuevo_tema', data={'nombre': 'TemaExistente'})
        self.assertIn(b'El tema ya existe.', response.data)

    def test_buscar_tema_no_existente(self):
        response = self.app.get('/tema/100')
        self.assertIn(b'404 Not Found', response.data)

    def test_buscar_tema_existente_sin_seleccionar(self):
        response = self.app.get('/tema/1')
        self.assertIn(b'Explorar hilos', response.data)

    def test_buscar_tema_palabra_no_permitida(self):
        response = self.app.get('/tema/PalabraNoPermitida')
        self.assertIn(b'404 Not Found', response.data)

    def test_crear_hilo_sin_crear(self):
        response = self.app.post('/crear_hilo/1', data={'texto': 'HiloSinCrear'})
        self.assertIn(b'Crear hilo', response.data)

    def test_crear_hilo_correcto(self):
        self.app.post('/nuevo_tema', data={'nombre': 'TemaPrueba'})
        response = self.app.post('/crear_hilo/1', data={'texto': 'HiloCorrecto'})
        self.assertNotIn(b'Crear hilo', response.data)

    def test_hilo_palabra_no_permitida(self):
        self.app.post('/nuevo_tema', data={'nombre': 'TemaPrueba'})
        response = self.app.post('/crear_hilo/1', data={'texto': 'HiloNoPermitido'})
        self.assertIn(b'Crear hilo', response.data)

    # Añade más casos de prueba según sea necesario

if __name__ == '__main__':
    unittest.main()
