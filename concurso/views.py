from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .db_procedures import obtener_estadisticas, obtener_ganadores
from .models import Categoria, Empleado, Evento, Inscripcion
from .serializers import EstadisticasSerializer, GanadorSerializer, InscripcionInputSerializer, InscripcionOutputSerializer
from .validations import BusinessValidationError, crear_inscripcion


class InscripcionView(APIView):
    def get(self, request):
        qs = Inscripcion.objects.select_related('empleado', 'empleado__ciudad', 'evento_categoria', 'evento_categoria__categoria', 'evento_categoria__evento')

        empleado = request.query_params.get('empleado')
        if empleado:
            qs = qs.filter(empleado__documento__icontains=empleado)

        ciudad = request.query_params.get('ciudad')
        if ciudad:
            qs = qs.filter(empleado__ciudad__nombre__icontains=ciudad)

        categoria = request.query_params.get('categoria')
        if categoria:
            qs = qs.filter(evento_categoria__categoria_id=categoria)

        fecha = request.query_params.get('fecha')
        if fecha:
            qs = qs.filter(fecha_inscripcion__date=fecha)

        serializer = InscripcionOutputSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InscripcionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'PARAMETROS_INVALIDOS', 'detail': 'Los parámetros enviados son inválidos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            inscripcion = crear_inscripcion(serializer.validated_data['documento_empleado'], serializer.validated_data['categoria_id'])
        except BusinessValidationError as exc:
            return Response({'error': exc.code, 'detail': exc.message}, status=exc.status_code)

        return Response(InscripcionOutputSerializer(inscripcion).data, status=status.HTTP_201_CREATED)


class GanadoresView(APIView):
    def get(self, request):
        evento = Evento.objects.order_by('id').first()
        if not evento:
            return Response({'error': 'EVENTO_NO_DEFINIDO', 'detail': 'No haay evento activo.'}, status=status.HTTP_404_NOT_FOUND)

        categoria_id = request.query_params.get('categoria')
        rows = []

        if categoria_id:
            rows = obtener_ganadores(evento.id, int(categoria_id))
        else:
            for categoria in Categoria.objects.all():
                rows.extend(obtener_ganadores(evento.id, categoria.id))

        data = []

        for row in rows:
            row['es_podio'] = row.get('puesto', 0) <= 3
            data.append(row)

        serializer = GanadorSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EstadisticasView(APIView):
    def get(self, request):
        evento = Evento.objects.order_by('id').first()
        if not evento:
            return Response({'error': 'EVENTO_NO_DEFINIDO', 'detail': 'No hay evento activo.'}, status=status.HTTP_404_NOT_FOUND)

        rows = obtener_estadisticas(evento.id)
        if not rows:
            return Response({'error': 'SIN_ESTADISTICAS', 'detail': 'No se encontraron  estadísticas.'}, status=status.HTTP_404_NOT_FOUND)

        payload = rows[0]
        serializer = EstadisticasSerializer(payload)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventoFechaView(APIView):
    def patch(self, request, pk):
        
        empleado_id = request.data.get('empleado_id')
        nueva_fecha = request.data.get('fecha_evento')

        if not empleado_id or not nueva_fecha:
            return Response({'error': 'PARAMETROS_INVALIDOS', 'detail': 'Debe incluir empleado_id y fecha_evento.'}, status=status.HTTP_400_BAD_REQUEST)

        empleado = Empleado.objects.select_related('cargo').filter(id=empleado_id).first()
        if not empleado:
            return Response({'error': 'EMPLEADO_NO_EXISTE', 'detail': 'El empleado no existe.'}, status=status.HTTP_404_NOT_FOUND)

        if empleado.cargo.nombre != 'Director':
            return Response({'error': 'EMPLEADO_NO_AUTORIZADO', 'detail': 'Solo un Director puede modificar la fecha del evento.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            fecha = datetime.strptime(nueva_fecha, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'PARAMETROS_INVALIDOS', 'detail': 'La fecha_evento debe estar en formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        evento = Evento.objects.filter(id=pk).first()
        if not evento:
            return Response({'error': 'EVENTO_NO_DEFINIDO', 'detail': 'Evento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        evento.fecha_evento = fecha
        evento.fecha_limite_inscripcion = fecha - timedelta(days=3)
        evento.save(update_fields=['fecha_evento', 'fecha_limite_inscripcion'])
        return Response({'id': evento.id, 'fecha_evento': evento.fecha_evento, 'fecha_limite_inscripcion': evento.fecha_limite_inscripcion}, status=status.HTTP_200_OK)
