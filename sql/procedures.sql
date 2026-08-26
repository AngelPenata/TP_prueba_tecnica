USE dpdo_concurso;
GO

CREATE OR ALTER PROCEDURE sp_ObtenerGanadores
    @EventoID INT,
    @CategoriaID INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        r.puesto,
        e.id AS empleado_id,
        e.documento,
        e.nombre_completo,
        c.nombre AS categoria,
        ec.id AS evento_categoria_id
    FROM Resultado r
    INNER JOIN Inscripcion i ON i.id = r.inscripcion_id
    INNER JOIN Empleado e ON e.id = i.empleado_id
    INNER JOIN EventoCategoria ec ON ec.id = i.evento_categoria_id
    INNER JOIN Categoria c ON c.id = ec.categoria_id
    WHERE ec.evento_id = @EventoID
      AND (@CategoriaID IS NULL OR ec.categoria_id = @CategoriaID)
    ORDER BY ec.categoria_id, r.puesto;
END;
GO

CREATE OR ALTER PROCEDURE sp_ObtenerEstadisticas
    @EventoID INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @InscripcionesAsesores INT;
    DECLARE @IntentosNoAutorizados INT;
    DECLARE @IntentosDobleInscripcion INT;

    SELECT @InscripcionesAsesores = COUNT(*)
    FROM Inscripcion i
    INNER JOIN EventoCategoria ec ON ec.id = i.evento_categoria_id
    INNER JOIN Empleado e ON e.id = i.empleado_id
    INNER JOIN Cargo c ON c.id = e.cargo_id
    WHERE ec.evento_id = @EventoID
      AND c.nombre = 'Asesor';

    SELECT @IntentosNoAutorizados = COUNT(*)
    FROM IntentoInscripcion ti
    WHERE ti.evento_id = @EventoID
      AND ti.motivo IN ('EMPLEADO_NO_AUTORIZADO', 'CIUDAD_NO_PERMITIDA');

    SELECT @IntentosDobleInscripcion = COUNT(*)
    FROM IntentoInscripcion ti
    WHERE ti.evento_id = @EventoID
      AND ti.motivo = 'DOBLE_INSCRIPCION';

    SELECT
        @InscripcionesAsesores AS inscripciones_realizadas_por_asesores,
        @IntentosNoAutorizados AS intentos_no_autorizados,
        @IntentosDobleInscripcion AS intentos_doble_inscripcion;
END;
GO
