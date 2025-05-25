# ESP32 Sensor Monitoring API

FastAPI for the ESP32 sensor monitoring system. This API allows:
- Register and manage sensors
- Store sensor readings
- Process data with Llama 3.2
- Query analysis results

## Project Structure

```
api/
├── app/              # Main API code
│   ├── core/         # Core configurations
│   ├── db/           # Database configuration
│   ├── models/       # SQLAlchemy models
│   ├── routers/      # API endpoints
│   ├── schemas/      # Pydantic schemas
│   └── main.py       # API entry point
├── .env             # Environment variables
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile       # Docker configuration
├── requirements.txt  # Project dependencies
└── run.py           # Script to run the API
```

## Requirements

- Docker
- PostgreSQL installed and running
- Ollama installed and running with llama2 model

## Installation

### Using Docker (Recommended)

1. Download the image:
```bash
docker pull difermon09/pi1-api:latest
```

2. Create a `docker-compose.yml` file:
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

3. Start the API:
```bash
docker-compose up
```

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. The `.env` file is already included in the repository with default configuration:
```
POSTGRES_SERVER=localhost
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_DB=sensor_data
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

4. Run the API:
```bash
python run.py
```

### Database Cleanup

The project includes a `clear_db.py` script to clean and reinitialize the database. This script is useful in two scenarios:

#### During Development
If you're developing locally and need to reset the database:
```bash
# Windows
cd api\app\db
python clear_db.py

# Linux/Mac
cd api/app/db
python clear_db.py
```

#### In Production (Docker)
If you're using the Docker image and need to clean the database:
```bash
# Enter the container
docker exec -it pi1-db-1 psql -U admin -d sensor_data

# Inside psql, execute:
DROP TABLE IF EXISTS tag_readings CASCADE;
DROP TABLE IF EXISTS tag_sensors CASCADE;
DROP TABLE IF EXISTS enviroment_readings CASCADE;
DROP TABLE IF EXISTS enviroment_sensors CASCADE;
DROP TABLE IF EXISTS data_analysis CASCADE;

# Exit psql
\q
```

The `clear_db.py` script:
- Deletes all existing tables
- Recreates tables with their original structures
- Resets ID sequences to 1
- Useful for testing and development

## Endpoints

- `GET /`: Welcome page
- `GET /docs`: API documentation
- `POST /enviroment_readings/`: Create a sensor reading
- `GET /enviroment_readings/sensors/`: List sensors
- `POST /tag_readings/`: Create a tag reading
- `GET /tag_readings/`: List tag readings

## Examples

### Create a sensor reading
```bash
curl -X POST "http://localhost:8000/enviroment_readings/" \
     -H "Content-Type: application/json" \
     -d '{"sensor_id": 1, "value": 25.5}'
```

### List sensors
```bash
curl "http://localhost:8000/enviroment_readings/sensors/"
```

## Troubleshooting

1. **If PostgreSQL doesn't connect**
   - Verify PostgreSQL is running
   - Check that username and password are correct
   - Verify that the `sensor_data` database exists

2. **If Ollama doesn't respond**
   - Verify Ollama is running
   - Check that llama2 model is installed
   - Verify port 11434 is available

## Contact

For support or questions, contact:
- GitHub: [difermon09](https://github.com/difermon09)
- Docker Hub: [difermon09](https://hub.docker.com/u/difermon09) 