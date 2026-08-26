from django.test import TestCase

from concurso.models import Categoria, Empleado, Evento
from concurso.validations import BusinessValidationError, validar_ciudad_permitida, validar_empleado_es_asesor


class ValidationTests(TestCase):
    def setUp(self):
        self.evento = Evento.objects.order_by('id').first()
        self.categoria = Categoria.objects.get(id=1)

    def test_empleado_no_autorizado(self):
        empleado = Empleado.objects.get(documento='1101010112')
        with self.assertRaises(BusinessValidationError):
            validar_empleado_es_asesor(empleado, empleado.documento, self.categoria, self.evento)

    def test_ciudad_no_permitida(self):
        empleado = Empleado.objects.get(documento='1101010113')
        with self.assertRaises(BusinessValidationError):
            validar_ciudad_permitida(empleado, empleado.documento, self.categoria, self.evento)
