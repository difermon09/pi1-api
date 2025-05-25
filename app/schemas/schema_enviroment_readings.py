# Fichero encargado de definir la estructura de los mensajes relacionados con las lecturas de los sensores, que llegan y salen de los metodos de la api

from pydantic import BaseModel
from datetime import datetime

# Base de como tiene que ser una lectura (crear)
class SchemaEnviromentReadingBase(BaseModel):
    sensor_id: int
    value: float

# Obtener lecturas de la base de datos
class SchemaEnviromentReadingInDB(SchemaEnviromentReadingBase):
    timestamp: datetime
    
    class Config:
        from_attributes = True
