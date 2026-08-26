import unicodedata
from datetime import date

from django.db import transaction
from django.utils import timezone

from .models import Categoria, Empleado, Evento, EventoCategoria, Inscripcion, IntentoInscripcion


class BusinessValidationError(Exception):
    def __init__(self, code, message, status_code=400):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


def normalizar_texto(valor):
    if not valor:
        return ''
    return unicodedata.normalize('NFKD', str(valor)).encode('ascii', 'ignore').decode('ascii').lower()


def registrar_intento(documento_recibido, motivo, empleado=None, categoria=None, evento=None):
    IntentoInscripcion.objects.create(
        empleado=empleado,
        documento_recibido=documento_recibido,
        categoria=categoria,
        evento=evento,
        motivo=motivo,
        fecha_intento=timezone.now(),
    )


def validar_empleado_existe(documento, categoria=None, evento=None):
    empleado = Empleado.objects.select_related('cargo', 'ciudad').filter(documento=documento).first()
    if not empleado:

        registrar_intento(documento, 'EMPLEADO_NO_EXISTE', categoria=categoria, evento=evento)

        raise BusinessValidationError('EMPLEADO_NO_EXISTE', 'El empleado no existe.', 404)

    return empleado


def validar_empleado_es_asesor(empleado, documento, categoria=None, evento=None):

    if not empleado.cargo or empleado.cargo.nombre != 'Asesor':

        registrar_intento(documento, 'EMPLEADO_NO_AUTORIZADO', empleado=empleado, categoria=categoria, evento=evento)

        raise BusinessValidationError('EMPLEADO_NO_AUTORIZADO', 'El empleado no está autorizado para participar.', 403)


def validar_ciudad_permitida(empleado, documento, categoria=None, evento=None):
    zona = normalizar_texto(empleado.ciudad.nombre)
    if zona not in {'medellin', 'bogota'}:

        registrar_intento(documento, 'CIUDAD_NO_PERMITIDA', empleado=empleado, categoria=categoria, evento=evento)

        raise BusinessValidationError('CIUDAD_NO_PERMITIDA', 'La ciudad del empleado no está permitida para este concurso', 403)


def validar_categoria_existe(categoria_id, documento, evento=None):
    categoria = Categoria.objects.filter(id=categoria_id).first()
    if not categoria:
        registrar_intento(documento, 'CATEGORIA_NO_EXISTE', evento=evento)
        raise BusinessValidationError('CATEGORIA_NO_EXISTE', 'La categoría no existe.',  404)
    
    return categoria


def validar_inscripciones_abiertas(evento, documento, categoria=None):
    hoy = date.today()
    if hoy > evento.fecha_limite_inscripcion:

        registrar_intento(documento, 'INSCRIPCIONES_CERRADAS', categoria=categoria, evento=evento)

        raise BusinessValidationError('INSCRIPCIONES_CERRADAS', 'Las inscripciones ya cerraron', 409)


def validar_no_duplicado(empleado, evento_categoria, documento, categoria=None, evento=None):
    if Inscripcion.objects.filter(empleado=empleado, evento_categoria=evento_categoria).exists():

        registrar_intento(documento, 'DOBLE_INSCRIPCION', empleado=empleado, categoria=categoria, evento=evento)

        raise BusinessValidationError('DOBLE_INSCRIPCION', 'El  empleado ya está inscrito en esta categoría', 409)


def validar_cupo_disponible(evento_categoria, documento, categoria=None, evento=None, empleado=None):
    total = Inscripcion.objects.filter(evento_categoria=evento_categoria).count()
    if total >= evento_categoria.cupo_maximo:
        registrar_intento(documento, 'CUPO_AGOTADO', empleado=empleado, categoria=categoria, evento=evento)
        raise BusinessValidationError('CUPO_AGOTADO', 'No hay cupos disponibles para esta categoría.', 409)


def crear_inscripcion(documento_empleado, categoria_id, evento=None):
    if evento is None:
        evento = Evento.objects.order_by('id').first()

    if not evento:
        raise BusinessValidationError('EVENTO_NO_DEFINIDO', 'No existe un evento activo', 404 )

    empleado = validar_empleado_existe(documento_empleado, categoria_id, evento)
    categoria = validar_categoria_existe(categoria_id, documento_empleado, evento)
    validar_empleado_es_asesor(empleado, documento_empleado, categoria, evento)
    validar_ciudad_permitida(empleado, documento_empleado, categoria, evento)
    validar_inscripciones_abiertas(evento, documento_empleado, categoria)

    with transaction.atomic():
        evento_categoria = EventoCategoria.objects.select_for_update().get(evento=evento, categoria=categoria)
        validar_no_duplicado(empleado, evento_categoria, documento_empleado, categoria, evento)
        validar_cupo_disponible(evento_categoria, documento_empleado, categoria, evento, empleado)
        inscripcion = Inscripcion.objects.create(empleado=empleado, evento_categoria=evento_categoria, fecha_inscripcion=timezone.now())

    return inscripcion
