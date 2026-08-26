# DPDO Concurso - Backend Data Engineer

Prueba desarrollada con Django + DRF para gestionar inscripciones, ganadores y estadísticas de una convocatoria interna de asesores en Medellín y Bogotá. La implementación sigue un enfoque SQL-first: el  esquema principal vive en scripts SQL de SQL Server y la API consume esa base ya creada, en lugar de depender de la creación automatica de una base de prueba por Django.

## Objetivo de la prueba
Implementar una solución que cumpla con:
- esquema relacional normalizado (3FN)
- validaciones de negocio reales sobre inscripciones
- integridad de datos con SQL Server
- procedimientos almacenados para reportes de ganadores y estadisticas
- API REST para operaciones de inscripcion y consulta
- pruebas automatizadas contra la base de datos productiva del proyecto, no contra una base de prueba recreada por Django

## Stack y tecnologías
- Python 3.11
- Django 5.2
- Django REST Framework
- SQL Server 2022 (ejecutado con Docker)
- mssql-django / pyodbc
- Docker Compose

## Arquitectura
La solución utiliza una sola app Django (`concurso`) sobre un esquema SQL Server real gestionado por scripts en `sql/`.

Principios del diseño:
- El origen del modelo es SQL (`sql/schema.sql`), no migraciones de Django.
- Los datos de prubea se cargan con `sql/populate_database.sql`.
- Las consultas de agregación y reportes se resuelven con procedimientos almacenados en `sql/procedures.sql`.
- La API se comunica con SQL Server mediante ORM + `cursor.execute` con parámetros, evitando concatenar SQL directamente.
- Las reglas de negocio se centralizan en validaciones explícitas para cubrir: empleado no autorizado, ciudad no permitida, categoría cerrada, duplicados, cupos completos y cambios de fecha restringidos.

## Estructura del repositorio
- `config/` — configuración general de Django.
- `concurso/` — modelos, validaciones, serializers, vistas, URLs y tests.
- `sql/` — esquema, procedimientos almacenados y datos de prueba.
- `docs/` — diagrama relacional y decisiones de diseño.
- `docker-compose.yml` — entorno local de SQL Server 2022.
- `manage.py` — entry point de Django.
- `requirements.txt` — dependencias del proyecto.
- `.env.example` — plantilla de variables de entorno.
- `SETUP.md` — guía completa de instalación y puesta en marcha.

## Configuración rápida
1. Crear entorno virtual
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Crear `.env` a partir del ejemplo
```powershell
Copy-Item .env.example .env
```

3. Levantar SQL Server local
```powershell
docker compose up -d
```

4. Cargar esquema y datos de prueba
```powershell
sqlcmd -S localhost,14333 -U sa -P "Password12345" -d master -i .\sql\schema.sql
sqlcmd -S localhost,14333 -U sa -P "Password12345" -d dpdo_concurso -i .\sql\procedures.sql
sqlcmd -S localhost,14333 -U sa -P "Password12345" -d dpdo_concurso -i .\sql\populate_database.sql
```

5. Ejecutar la API
```powershell
python manage.py runserver 0.0.0.0:8000
```

## Variables de entorno
El proyecto usa `.env` con la siguiente configuración base:
```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DB_ENGINE=mssql
DB_HOST=localhost
DB_PORT=14333
DB_NAME=dpdo_concurso
DB_USER=sa
DB_PASSWORD=Password12345
DB_ODBC_DRIVER=ODBC Driver 17 for SQL Server
```

## Endpoints principales
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/inscripciones/` | Registra una inscripción validando empleado, cargo, ciudad, categoria, cierre de inscripciones, duplicados y cupos. |
| `GET` | `/api/inscripciones/` | Lista inscripciones con filtros por empleado, ciudad, categoria y fecha |
| `GET` | `/api/ganadores/` | Devuelve el top 10 por categoría con identificación del podio (puestos 1-3). |
| `GET` | `/api/estadisticas/` | Devuelve estadísticas de inscripciones válidas, intentos no autorizados y dobles inscripciones. |
| `PATCH` | `/api/evento/<id>/fecha/` | Extra mile: modifica la fecha del evento solo si quien solicita la acción es Director |

## Reglas de negocio cubiertas
- Validación de empleado y rol
- Validación de ciudad permitida
- Validación de categoría y fecha del evento
- Detección de inscripciones duplicadas
- Control de cupos por categoría
- Registro de intentos inválidos en tabla de auditoría
- Respuesta HTTP acorde con el escenario: 400, 403, 404, 409 y 200/201 según corresponda

## Pruebas
La suite de pruebas está pensada para correr contra la base real configurada en `.env`, no contra una BD de pruebas separada creada automáticamente por Django.

Comando de validación:
```powershell
python manage.py test concurso.tests.test_validations concurso.tests.test_api --testrunner=concurso.test_runner.NoCreateTestRunner
```

Nota: el runner custom `NoCreateTestRunner` evita la creación automática de una base de prueba de Django y apunta a la base SQL Server ya existente, manteniendo la estrategia del proyecto "esquema SQL primero".

## Modelo de datos y decisiones de diseño
El diseño sigue una normalización 3FN con tablas de catalogos y entidades de negocio:
- `Cargo`, `Ciudad`, `Categoria`
- `Empleado`, `Evento`, `EventoCategoria`
- `Inscripcion`, `Resultado`, `IntentoInscripcion`

Tambien existen restricciones de unicidad, claves foraneas y indices orientados a:
- búsquedas por documento y empleado
- filtros por categoria y fecha
- conteos por posición y puntaje
- auditoría de intentos inválidos

La solución enfatiza la logica de reportes en SQL Server mediante stored procedures, manteniendo la capa API enfocada en exposición y validación de negocio.