from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime, timedelta


from ..db.database import get_db
from ..models.model_tags import TableTagReadings, TableTagSensors
from ..schemas.schema_tag_readings import SchemaTagReadingBase, SchemaTagReadingInDB

router = APIRouter()

# Crear una lectura nueva
@router.post("/", status_code=status.HTTP_201_CREATED) 
async def create_sensor_reading(reading: SchemaTagReadingBase, db: AsyncSession = Depends(get_db)):
    print(f"[API] Recibida lectura de tag con ID: {reading.tag_id}")
    
    result = await db.execute(select(TableTagSensors).filter(TableTagSensors.id == reading.tag_id))
    sensor = result.scalars().first()
    
    if sensor is None:
        print(f"[API] Tag no encontrado en la base de datos: {reading.tag_id}")
        raise HTTPException(status_code=404, detail="Tag sensor not found")
    
    print(f"[API] Tag encontrado: {sensor.id} en {sensor.pen}, {sensor.building}")
    
    db_reading = TableTagReadings(**reading.model_dump()) 
    db.add(db_reading)
    await db.commit()
    await db.refresh(db_reading)
    return db_reading

# Obtener todas las lecturas que hay de la ultima semana
@router.get("/", response_model=List[SchemaTagReadingInDB])
async def read_sensor_readings(db: AsyncSession = Depends(get_db)):
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    result = await db.execute(
        select(TableTagReadings)
        .where(TableTagReadings.timestamp >= one_week_ago)
        .order_by(TableTagReadings.timestamp.asc())
    )
    readings = result.scalars().all()
    return readings


