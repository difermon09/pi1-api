# Fichero encargado de crear las tablas de los tafs de los cerdos en la base de datos
# Esto incluye tambien crear sus columnas indicando sus caracteristicas

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.database import Base

# Tabla que contiene los tags que hay
class TableTagSensors(Base):
    __tablename__ = "tag_sensors"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=False) # Identificador del tag, no autoincremental para que no se cree automatiamente
    pen = Column(String, nullable=False) # Corral donde esta el cerdo
    building = Column(String, nullable=True) # Nave donde esta el cerdo
    
    tag_readings = relationship("TableTagReadings", back_populates="tag_sensors", cascade="all, delete-orphan")

# Tabla que contiene las lecturas de los tags
class TableTagReadings(Base):
    __tablename__ = "tag_readings"
    
    id = Column(Integer, primary_key=True, index=True) 
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    tag_id = Column(BigInteger, ForeignKey("tag_sensors.id"), nullable=False) 
    
    tag_sensors = relationship("TableTagSensors", back_populates="tag_readings")