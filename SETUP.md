# Setup del proyecto

## 1. Prerrequisitos
- Python 3.11+
- Docker Desktop / Docker Engine
- Docker Compose
- ODBC Driver 17/18 for SQL Server instalado en el host

## 2. Clonar y preparar entorno
```powershell
cd .\TP_prueba_tecnica
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Variables de entorno
Copia el ejemplo y ajusta los valores según tu entorno local.
```powershell
Copy-Item .env.example .env
```

Variables:
- `DJANGO_SECRET_KEY`: clave secreta de Django.
- `DJANGO_DEBUG`: activa depuración local.
- `DB_HOST`: host de SQL Server (por defecto `localhost`).
- `DB_PORT`: puerto del contenedor (`14333`).
- `DB_NAME`: nombre de la base `dpdo_concurso`.
- `DB_USER`: usuario `sa`.
- `DB_PASSWORD`: contraseña del entorno local (`Password12345`).
- `DB_ODBC_DRIVER`: driver ODBC 17/18 para SQL Server.

## 4. Levantar SQL Server
```powershell
docker compose up -d
```

Verificar:
```powershell
docker compose ps
```

## 5. Crear la base de datos y cargar el esquema
```powershell
sqlcmd -S localhost,14333 -U sa -P "Password12345" -d master -i .\sql\schema.sql
sqlcmd -S localhost,14333 -U sa -P "Password12345" -d dpdo_concurso -i .\sql\procedures.sql
sqlcmd -S localhost,14333 -U sa -P "Password12345" -d dpdo_concurso -i .\sql\populate_database.sql
```

## 6. Sincronizar Django con el esquema existente
```powershell
python manage.py migrate --fake-initial
```

## 7. Levantar la API
```powershell
python manage.py runserver 0.0.0.0:8000
```

## 8. Ejecutar pruebas unitarias
```powershell
python manage.py test concurso.tests.test_validations --testrunner=concurso.test_runner.NoCreateTestRunner
```

## 9. Ejecutar pruebas de integración
```powershell
python manage.py test concurso.tests.test_api --testrunner=concurso.test_runner.NoCreateTestRunner
```

## 10. Ejecutar la suite completa del proyecto
```powershell
python manage.py test concurso.tests.test_validations concurso.tests.test_api --testrunner=concurso.test_runner.NoCreateTestRunner
```

> Las pruebas corren contra la base SQL Server configurada en `.env` y no crean una base de prueba temporal. El esquema del proyecto es propietario de `sql/schema.sql`, y Django solo consume esa BD ya creada.

## 11. Verificación manual
Se recomienda consultar directamente la base con `sqlcmd` para confirmar que las inserciones realizadas desde la API quedan en SQL Server real:
```powershell
sqlcmd -S localhost,14333 -U sa -P "Password12345" -d dpdo_concurso -Q "SELECT TOP 10 * FROM Inscripcion;"
```
