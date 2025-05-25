# Fichero encargado de definir la estructura de los mensajes relacionados con la IA, que llegan y salen de los metodos de la api

from pydantic import BaseModel

# Base de como tiene que ser un analisis (crear)
class SchemaDataAnalysisBase(BaseModel): 
    analysis: dict

# Obtener analysis de la base de datos
class SchemaDataAnalysisInDB(SchemaDataAnalysisBase):
    class Config:
        from_attributes = True
        # Los schemas (Pydantic) definen la estructura de los datos que se envían y reciben en la API
        # Los models (SQLAlchemy) definen la estructura de las tablas en la base de datos
        # La configuración from_attributes=True permite convertir automáticamente de models a schemas
