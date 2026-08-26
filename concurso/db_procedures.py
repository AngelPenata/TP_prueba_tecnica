from django.db import connection


def obtener_ganadores(evento_id, categoria_id=None):
    with connection.cursor() as cursor:
        cursor.execute('EXEC sp_ObtenerGanadores @EventoID = %s, @CategoriaID = %s', [evento_id, categoria_id])
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return rows


def obtener_estadisticas(evento_id):
    with connection.cursor() as cursor:
        cursor.execute('EXEC sp_ObtenerEstadisticas @EventoID = %s', [evento_id])
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return rows
