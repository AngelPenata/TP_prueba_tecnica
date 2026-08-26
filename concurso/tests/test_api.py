from rest_framework.test import APITestCase

from concurso.models import EventoCategoria, Inscripcion


class InscripcionApiTests(APITestCase):
    def tearDown(self):
        Inscripcion.objects.filter(
            empleado__documento__in=['1101010115', '1101010116'],
            evento_categoria__categoria_id=2,
        ).delete()
        EventoCategoria.objects.filter(evento_id=1, categoria_id=2).update(cupo_maximo=5)
        super().tearDown()

    def test_crear_inscripcion_exitosa(self):
        evento_categoria = EventoCategoria.objects.get(evento_id=1, categoria_id=2)
        evento_categoria.cupo_maximo = 6
        evento_categoria.save(update_fields=['cupo_maximo'])

        response = self.client.post('/api/inscripciones/', {'documento_empleado': '1101010116', 'categoria_id': 2}, format='json')
        self.assertEqual(response.status_code, 201)

    def test_ciudad_no_permitida(self):
        response = self.client.post('/api/inscripciones/', {'documento_empleado': '1101010113', 'categoria_id': 3}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_ganadores_por_categoria(self):
        response = self.client.get('/api/ganadores/?categoria=1')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_estadisticas(self):
        response = self.client.get('/api/estadisticas/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('inscripciones_realizadas_por_asesores', data)
