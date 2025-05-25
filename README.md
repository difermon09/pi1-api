# API de Monitoreo de Sensores ESP32

API FastAPI para el sistema de monitoreo de sensores ESP32. Esta API permite:
- Registrar y gestionar sensores
- Almacenar lecturas de sensores
- Procesar datos con Llama 3.2
- Consultar resultados de análisis

## Estructura del Proyecto

```
api/
├── app/              # Código principal de la API
│   ├── core/         # Configuraciones centrales
│   ├── db/           # Configuración de base de datos
│   ├── models/       # Modelos SQLAlchemy
│   ├── routers/      # Endpoints de la API
│   ├── schemas/      # Esquemas Pydantic
│   └── main.py       # Punto de entrada de la API
├── .env             # Variables de entorno
├── docker-compose.yml # Configuración de Docker Compose
├── Dockerfile       # Configuración de Docker
├── requirements.txt  # Dependencias del proyecto
└── run.py           # Script para ejecutar la API
```

## Requisitos

- Docker
- PostgreSQL instalado y corriendo
- Ollama instalado y corriendo con el modelo llama2

## Instalación

### Usando Docker (Recomendado)

1. Descargar la imagen:
```bash
docker pull difermon09/pi1-api:latest
```

2. Crear un archivo `docker-compose.yml`:
```yaml
services:
  api:
    image: difermon09/pi1-api:latest
    restart: always
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_SERVER=localhost
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=sensor_data
      - OLLAMA_HOST=http://localhost:11434
      - OLLAMA_MODEL=llama2
```

3. Iniciar la API:
```bash
docker-compose up
```

### Desarrollo Local

1. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. El archivo `.env` ya está incluido en el repositorio con la configuración por defecto:
```
POSTGRES_SERVER=localhost
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_DB=sensor_data
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

4. Ejecutar la API:
```bash
python run.py
```

### Limpieza de la Base de Datos

El proyecto incluye un script `clear_db.py` para limpiar y reinicializar la base de datos. Este script es útil en dos escenarios:

#### Durante el Desarrollo
Si estás desarrollando localmente y necesitas reiniciar la base de datos:
```bash
# Windows
cd api\app\db
python clear_db.py

# Linux/Mac
cd api/app/db
python clear_db.py
```

#### En Producción (Docker)
Si estás usando la imagen Docker y necesitas limpiar la base de datos:
```bash
# Entrar al contenedor
docker exec -it pi1-db-1 psql -U admin -d sensor_data

# Dentro de psql, ejecutar:
DROP TABLE IF EXISTS tag_readings CASCADE;
DROP TABLE IF EXISTS tag_sensors CASCADE;
DROP TABLE IF EXISTS enviroment_readings CASCADE;
DROP TABLE IF EXISTS enviroment_sensors CASCADE;
DROP TABLE IF EXISTS data_analysis CASCADE;

# Salir de psql
\q
```

El script `clear_db.py`:
- Elimina todas las tablas existentes
- Recrea las tablas con sus estructuras originales
- Reinicia las secuencias de IDs a 1
- Es útil para pruebas y desarrollo

## Endpoints

- `GET /`: Página de bienvenida
- `GET /docs`: Documentación de la API
- `POST /enviroment_readings/`: Crear una lectura de sensor
- `GET /enviroment_readings/sensors/`: Listar sensores
- `POST /tag_readings/`: Crear una lectura de tag
- `GET /tag_readings/`: Listar lecturas de tags

## Ejemplos

### Crear una lectura de sensor
```bash
curl -X POST "http://localhost:8000/enviroment_readings/" \
     -H "Content-Type: application/json" \
     -d '{"sensor_id": 1, "value": 25.5}'
```

### Listar sensores
```bash
curl "http://localhost:8000/enviroment_readings/sensors/"
```

## Solución de Problemas

1. **Si PostgreSQL no se conecta**
   - Verificar que PostgreSQL esté corriendo
   - Comprobar que el usuario y contraseña son correctos
   - Verificar que la base de datos `sensor_data` existe

2. **Si Ollama no responde**
   - Verificar que Ollama esté corriendo
   - Comprobar que el modelo llama2 está instalado
   - Verificar que el puerto 11434 está disponible

## Contacto

Para soporte o preguntas, contacta con:
- GitHub: [difermon09](https://github.com/difermon09)
- Docker Hub: [difermon09](https://hub.docker.com/u/difermon09) 