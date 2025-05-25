from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime, timedelta

from ..db.database import get_db
from ..models.model_enviroment import TableEnviromentReadings, TableEnviromentSensors
from ..schemas.schema_enviroment_readings import SchemaEnviromentReadingBase, SchemaEnviromentReadingInDB

router = APIRouter()

# Crear una lectura nueva
@router.post("/", status_code=status.HTTP_204_NO_CONTENT) # Responde al cliente con 204 para recibir una respuesta vacia. Normalmente con el post se usa 201 devolviendo lo que se ha creado. 204 suele ser para delete
async def create_sensor_reading(reading: SchemaEnviromentReadingBase, db: AsyncSession = Depends(get_db)):

    # Verificar que el sensor existe
    # Hacer una consulta a la base de datos que busca en TableEnviromentSensors los sensores con ese id
    result = await db.execute(select(TableEnviromentSensors).filter(TableEnviromentSensors.id == reading.sensor_id)) # Devuelve las filas completas 
    sensor = result.scalars().first() # Scalars pasa a TableEnviromentSensors para poder coger cosas en concreto i first solo coge el primer valor, por si acaso hay mas de uno con el mismo id.
    if sensor is None: # first devuelve none si no hay ninguno con ese id
        raise HTTPException(status_code=404, detail="Enviroment sensor not found")
    
    db_reading = TableEnviromentReadings(**reading.model_dump()) # Convertir el modelo de entrada en diccionario i despues al modelo de la columna
    db.add(db_reading) # Añadirlo a la cola para subirlo a la base de datos
    await db.commit() # Subir-lo a la base de datos
    await db.refresh(db_reading) # Refrescar la base de datos
    return None 

# Obtener todas las lecturas de un sensor en concreto que hay de la ultima semana
@router.get("/{sensor_id}", response_model=List[SchemaEnviromentReadingInDB]) # get y put tienen el codigo general 200 que significa todo ok
async def read_sensor_readings(sensor_id: int, db: AsyncSession = Depends(get_db)):
    one_week_ago = datetime.utcnow() - timedelta(days=7) # Calcular la hora de hace una semana

    # Hacer una consulta a la base de datos que busca en TableEnviromentReadings todas las lecturas de la ultima semana, quedando las mas recientes abajo
    result = await db.execute(
        select(TableEnviromentReadings)
        .where(TableEnviromentReadings.sensor_id == sensor_id, TableEnviromentReadings.timestamp >= one_week_ago)
        .order_by(TableEnviromentReadings.timestamp.asc())
    )
    readings = result.scalars().all() # all lo convierte en una lista
    return readings

# Obtener lista de sensores
@router.get("/sensors/", response_model=List[dict])
async def get_sensors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TableEnviromentSensors))
    sensors = result.scalars().all()
    return [{"id": sensor.id, "description": sensor.description, "building": sensor.building} for sensor in sensors]