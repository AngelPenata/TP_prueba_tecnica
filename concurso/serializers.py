from rest_framework import serializers

from .models import Inscripcion


class InscripcionInputSerializer(serializers.Serializer):
    documento_empleado = serializers.CharField(max_length=20)
    categoria_id = serializers.IntegerField(min_value=1)


class InscripcionOutputSerializer(serializers.ModelSerializer):
    empleado_documento = serializers.CharField(source='empleado.documento', read_only=True)
    categoria = serializers.CharField(source='evento_categoria.categoria.nombre', read_only=True)
    evento = serializers.CharField(source='evento_categoria.evento.nombre', read_only=True)

    class Meta:
        model = Inscripcion
        fields = ['id', 'empleado_documento', 'categoria', 'evento', 'fecha_inscripcion']


class GanadorSerializer(serializers.Serializer):
    puesto = serializers.IntegerField()
    empleado_id = serializers.IntegerField()
    documento = serializers.CharField()
    nombre_completo = serializers.CharField()
    categoria = serializers.CharField()
    evento_categoria_id = serializers.IntegerField()
    es_podio = serializers.SerializerMethodField()

    def get_es_podio(self, obj):
        return obj.get('puesto', 0) <= 3


class EstadisticasSerializer(serializers.Serializer):
    inscripciones_realizadas_por_asesores = serializers.IntegerField()
    intentos_no_autorizados = serializers.IntegerField()
    intentos_doble_inscripcion = serializers.IntegerField()
