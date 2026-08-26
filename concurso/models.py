from django.db import models


class Cargo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'Cargo'


class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'Ciudad'


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'Categoria'


class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    documento = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=150)
    cargo = models.ForeignKey('Cargo', on_delete=models.DO_NOTHING, db_column='cargo_id', related_name='empleados')
    ciudad = models.ForeignKey('Ciudad', on_delete=models.DO_NOTHING, db_column='ciudad_id', related_name='empleados')
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'Empleado'


class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    fecha_evento = models.DateField()
    fecha_limite_inscripcion = models.DateField()

    class Meta:
        managed = False
        db_table = 'Evento'


class EventoCategoria(models.Model):
    id = models.AutoField(primary_key=True)
    evento = models.ForeignKey('Evento', on_delete=models.DO_NOTHING, db_column='evento_id', related_name='categorias')
    categoria = models.ForeignKey('Categoria', on_delete=models.DO_NOTHING, db_column='categoria_id', related_name='eventos')
    cupo_maximo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'EventoCategoria'
        constraints = [
            models.UniqueConstraint(fields=['evento', 'categoria'], name='UQ_EventoCategoria')
        ]


class Inscripcion(models.Model):
    id = models.AutoField(primary_key=True)
    empleado = models.ForeignKey('Empleado', on_delete=models.DO_NOTHING, db_column='empleado_id', related_name='inscripciones')
    evento_categoria = models.ForeignKey('EventoCategoria', on_delete=models.DO_NOTHING, db_column='evento_categoria_id', related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Inscripcion'
        constraints = [
            models.UniqueConstraint(fields=['empleado', 'evento_categoria'], name='UQ_Inscripcion')
        ]


class Resultado(models.Model):
    id = models.AutoField(primary_key=True)
    evento_categoria = models.ForeignKey('EventoCategoria', on_delete=models.DO_NOTHING, db_column='evento_categoria_id', related_name='resultados')
    inscripcion = models.OneToOneField('Inscripcion', on_delete=models.DO_NOTHING, db_column='inscripcion_id', related_name='resultado')
    puesto = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'Resultado'
        constraints = [
            models.UniqueConstraint(fields=['evento_categoria', 'puesto'], name='UQ_Resultado_Puesto')
        ]


class IntentoInscripcion(models.Model):
    id = models.AutoField(primary_key=True)
    empleado = models.ForeignKey('Empleado', null=True, blank=True, on_delete=models.DO_NOTHING, db_column='empleado_id', related_name='intentos')
    documento_recibido = models.CharField(max_length=20)
    categoria = models.ForeignKey('Categoria', null=True, blank=True, on_delete=models.DO_NOTHING, db_column='categoria_id', related_name='intentos')
    evento = models.ForeignKey('Evento', null=True, blank=True, on_delete=models.DO_NOTHING, db_column='evento_id', related_name='intentos')
    motivo = models.CharField(max_length=30)
    fecha_intento = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'IntentoInscripcion'
