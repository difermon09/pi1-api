# Script para inicializar la base de datos con los sensores y tags

from sqlalchemy import select

from ..models.model_enviroment import TableEnviromentSensors
from ..models.model_tags import TableTagSensors
from .database import AsyncSessionLocal

# Datos iniciales para los sensores ambientales
ENVIRONMENT_SENSORS = [
    {"description": "Sensor de temperatura", "building": "Nave A"},
    {"description": "Sensor de humedad", "building": "Nave A"},
    {"description": "Sensor de luz", "building": "Nave A"},
    {"description": "Sensor de Amoniaco", "building": "Nave B"},
    {"description": "Sensor de CO2", "building": "Nave B"},
]

# Datos iniciales para los tags
TAG_SENSORS = [
    {"id": 3253706107, "pen": "Corral 3", "building": "Nave A"},
    {"id": 4150240901, "pen": "Corral 9", "building": "Nave A"},
    {"id": 3, "pen": "Corral 2", "building": "Nave B"},
    {"id": 4, "pen": "Corral 5", "building": "Nave B"},
]

async def init_db():
    """Inicializa la base de datos con los datos por defecto"""
    print('>>> Ejecutando init_db()')
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TableEnviromentSensors))
        first_sensor = result.first()
        print('>>> Sensores encontrados:', first_sensor)
        if first_sensor is not None:
            print('>>> Ya existen sensores, no se inicializa.')
            return

        # Insertar sensores ambientales
        for sensor_data in ENVIRONMENT_SENSORS:
            sensor = TableEnviromentSensors(**sensor_data)
            session.add(sensor)
        
        # Insertar tags
        for tag_data in TAG_SENSORS:
            tag = TableTagSensors(**tag_data)
            session.add(tag)
        
        await session.commit()
        print('>>> Sensores creados')

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db()) 