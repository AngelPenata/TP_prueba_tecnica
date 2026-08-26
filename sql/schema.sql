IF DB_ID('dpdo_concurso') IS NULL
BEGIN
    CREATE DATABASE dpdo_concurso;
END;
GO
USE dpdo_concurso;
GO

create table Cargo (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL UNIQUE
);

create table Ciudad (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Categoria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL UNIQUE
);

create table Empleado (
    id INT IDENTITY(1,1) PRIMARY KEY,
    documento NVARCHAR(20) NOT NULL UNIQUE,
    nombre_completo NVARCHAR(150) NOT NULL,
    cargo_id INT NOT NULL,
    ciudad_id INT NOT NULL,
    activo BIT NOT NULL DEFAULT 1,
    CONSTRAINT FK_Empleado_Cargo FOREIGN KEY (cargo_id) REFERENCES Cargo(id),
    CONSTRAINT FK_Empleado_Ciudad FOREIGN KEY (ciudad_id) REFERENCES Ciudad(id)
);

CREATE TABLE Evento (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(150) NOT NULL,
    fecha_evento DATE NOT NULL,
    fecha_limite_inscripcion DATE NOT NULL
);

CREATE TABLE EventoCategoria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    evento_id INT NOT NULL,
    categoria_id INT NOT NULL,
    cupo_maximo INT NOT NULL CHECK (cupo_maximo > 0),
    CONSTRAINT FK_EventoCategoria_Evento FOREIGN KEY (evento_id) REFERENCES Evento(id),
    CONSTRAINT FK_EventoCategoria_Categoria FOREIGN KEY (categoria_id) REFERENCES Categoria(id),
    CONSTRAINT UQ_EventoCategoria UNIQUE (evento_id, categoria_id)
);

create table Inscripcion (
    id INT IDENTITY(1,1) PRIMARY KEY,
    empleado_id INT NOT NULL,
    evento_categoria_id INT NOT NULL,
    fecha_inscripcion DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_Inscripcion_Empleado FOREIGN KEY (empleado_id) REFERENCES Empleado(id),
    CONSTRAINT FK_Inscripcion_EventoCategoria FOREIGN KEY (evento_categoria_id) REFERENCES EventoCategoria(id),
    CONSTRAINT UQ_Inscripcion UNIQUE (empleado_id, evento_categoria_id)
);

create table Resultado (
    id INT IDENTITY(1,1) PRIMARY KEY,
    evento_categoria_id INT NOT NULL,
    inscripcion_id INT NOT NULL UNIQUE,
    puesto SMALLINT NOT NULL CHECK (puesto BETWEEN 1 AND 10),
    CONSTRAINT FK_Resultado_EventoCategoria FOREIGN KEY (evento_categoria_id) REFERENCES EventoCategoria(id),
    CONSTRAINT FK_Resultado_Inscripcion FOREIGN KEY (inscripcion_id) REFERENCES Inscripcion(id),
    CONSTRAINT UQ_Resultado_Puesto UNIQUE (evento_categoria_id, puesto)
);

CREATE TABLE IntentoInscripcion (
    id INT IDENTITY(1,1) PRIMARY KEY,
    empleado_id INT NULL,
    documento_recibido NVARCHAR(20) NOT NULL,
    categoria_id INT NULL,
    evento_id INT NULL,
    motivo NVARCHAR(30) NOT NULL CHECK (motivo IN (
        'EMPLEADO_NO_EXISTE',
        'EMPLEADO_NO_AUTORIZADO',
        'CIUDAD_NO_PERMITIDA',
        'CATEGORIA_NO_EXISTE',
        'INSCRIPCIONES_CERRADAS',
        'DOBLE_INSCRIPCION',
        'CUPO_AGOTADO'
    )),
    fecha_intento DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_IntentoInscripcion_Empleado FOREIGN KEY (empleado_id) REFERENCES Empleado(id),
    CONSTRAINT FK_IntentoInscripcion_Categoria FOREIGN KEY (categoria_id) REFERENCES Categoria(id),
    CONSTRAINT FK_IntentoInscripcion_Evento FOREIGN KEY (evento_id) REFERENCES Evento(id)
);

CREATE INDEX IX_Empleado_Documento ON Empleado(documento);
CREATE INDEX IX_Inscripcion_Empleado ON Inscripcion(empleado_id);
CREATE INDEX IX_Inscripcion_EventoCategoria ON Inscripcion(evento_categoria_id);
CREATE INDEX IX_Inscripcion_Fecha ON Inscripcion(fecha_inscripcion);
CREATE INDEX IX_Empleado_Ciudad ON Empleado(ciudad_id);
CREATE INDEX IX_Resultado_EventoCategoria_Puesto ON Resultado(evento_categoria_id, puesto);
CREATE INDEX IX_IntentoInscripcion_Motivo ON IntentoInscripcion(motivo);
GO
