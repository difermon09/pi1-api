# Fichero encargado de definir la estructura de los mensajes relacionados con las lecturas de los tags, que llegan y salen de los metodos de la api

from pydantic import BaseModel
from datetime import datetime

# Base de como tiene que ser la info de la lectura (crear)
class SchemaTagReadingBase(BaseModel):
    tag_id: int  # Pydantic automáticamente maneja números grandes como int64

# Obtener lecturas de la base de datos
class SchemaTagReadingInDB(SchemaTagReadingBase):
    timestamp: datetime
    class Config:
        from_attributes = True
