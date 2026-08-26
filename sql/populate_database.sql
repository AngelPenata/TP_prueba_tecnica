USE dpdo_concurso;
GO

set IDENTITY_INSERT Cargo ON;
INSERT INTO Cargo (id, nombre) VALUES
(1, N'Asesor'),
(2, N'Director'),
(3, N'Analista');
set IDENTITY_INSERT Cargo OFF;
GO

set IDENTITY_INSERT Ciudad ON;
INSERT INTO Ciudad (id, nombre) VALUES
(1, N'Medellin'),
(2, N'Bogota'),
(3, N'Cali');
SET IDENTITY_INSERT Ciudad OFF;
GO

set IDENTITY_INSERT Categoria ON;
insert into Categoria (id, nombre) VALUES
(1, N'Canto'),
(2, N'Baile'),
(3, N'Ilustracion');
SET IDENTITY_INSERT Categoria OFF;
GO

SET IDENTITY_INSERT Evento ON;
INSERT INTO Evento (id, nombre, fecha_evento, fecha_limite_inscripcion) VALUES
(1, N'Concurso de Asesores DPDO 2026', '2026-12-15', '2026-12-12');
SET IDENTITY_INSERT Evento OFF;
GO

SET IDENTITY_INSERT EventoCategoria ON;
INSERT INTO EventoCategoria (id, evento_id, categoria_id, cupo_maximo) VALUES
(1, 1, 1, 10),
(2, 1, 2, 5),
(3, 1, 3, 3);
SET IDENTITY_INSERT EventoCategoria OFF;
GO

SET IDENTITY_INSERT Empleado ON;
INSERT INTO Empleado (id, documento, nombre_completo, cargo_id, ciudad_id, activo) VALUES
(1, '1101010101', N'Ana Maria Lopez', 1, 1, 1),
(2, '1101010102', N'Carlos Perez', 1, 1, 1),
(3, '1101010103', N'Diana Garcia', 1, 2, 1),
(4, '1101010104', N'Felipe Torres', 1, 2, 1),
(5, '1101010105', N'Laura Rios', 1, 1, 1),
(6, '1101010106', N'Miguel Salazar', 1, 2, 1),
(7, '1101010107', N'Paola Suarez', 1, 1, 1),
(8, '1101010108', N'Santiago Mena', 1, 2, 1),
(9, '1101010109', N'Isabel Cardona', 1, 3, 1),
(10, '1101010110', N'Rodrigo Canas', 1, 3, 1),
(11, '1101010111', N'Maria Elena Gomez', 2, 1, 1),
(12, '1101010112', N'Oscar Jimenez', 3, 2, 1),
(13, '1101010113', N'Valentina Gomez', 1, 3, 1),
(14, '1101010114', N'Julian Velz', 1, 3, 1),
(15, '1101010115', N'Nicolas Henao', 1, 2, 1),
(16, '1101010116', N'Tatiana Castro', 1, 1, 1);
SET IDENTITY_INSERT Empleado OFF;
GO

set IDENTITY_INSERT Inscripcion ON;
insert into Inscripcion (id, empleado_id, evento_categoria_id, fecha_inscripcion) VALUES
(1, 1, 1, '2026-11-01 09:00:00'),
(2, 2, 1, '2026-11-02 09:00:00'),
(3, 3, 1, '2026-11-03 09:00:00'),
(4, 4, 1, '2026-11-04 09:00:00'),
(5, 5, 1, '2026-11-05 09:00:00'),
(6, 6, 1, '2026-11-06 09:00:00'),
(7, 7, 1, '2026-11-07 09:00:00'),
(8, 8, 1, '2026-11-08 09:00:00'),
(9, 15, 1, '2026-11-09 09:00:00'),
(10, 16, 1, '2026-11-10 09:00:00'),
(11, 1, 2, '2026-11-11 09:00:00'),
(12, 2, 2, '2026-11-12 09:00:00'),
(13, 3, 2, '2026-11-13 09:00:00'),
(14, 4, 2, '2026-11-14 09:00:00'),
(15, 5, 3, '2026-11-15 09:00:00'),
(16, 6, 3, '2026-11-16 09:00:00'),
(17, 7, 3, '2026-11-17 09:00:00');
SET IDENTITY_INSERT Inscripcion OFF;
GO

SET IDENTITY_INSERT Resultado ON;
INSERT INTO Resultado (id, evento_categoria_id, inscripcion_id, puesto) VALUES
(1, 1, 1, 1),
(2, 1, 2, 2),
(3, 1, 3, 3),
(4, 1, 4, 4),
(5, 1, 5, 5),
(6, 1, 6, 6),
(7, 1, 7, 7),
(8, 1, 8, 8),
(9, 1, 9, 9),
(10, 1, 10, 10);
SET IDENTITY_INSERT Resultado OFF;
GO

SET IDENTITY_INSERT IntentoInscripcion ON;
INSERT INTO IntentoInscripcion (id, empleado_id, documento_recibido, categoria_id, evento_id, motivo, fecha_intento) VALUES
(1, 12, '1101010112', 2, 1, 'EMPLEADO_NO_AUTORIZADO', '2026-11-18 09:00:00'),
(2, 13, '1101010113', 3, 1, 'CIUDAD_NO_PERMITIDA', '2026-11-19 09:00:00'),
(3, 1, '1101010101', 1, 1, 'DOBLE_INSCRIPCION', '2026-11-20 09:00:00'),
(4, 14, '1101010114', 3, 1, 'CUPO_AGOTADO', '2026-11-21 09:00:00'),
(5, NULL, '9999999999', NULL, 1, 'EMPLEADO_NO_EXISTE', '2026-11-22 09:00:00');
SET IDENTITY_INSERT IntentoInscripcion OFF;
GO
