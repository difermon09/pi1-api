# Fichero encargado de crear las tablas de los sensores del ambiente en la base de datos. 
# Esto incluye tambien crear sus columnas indicando sus caracteristicas

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.database import Base

# Tabla que contiene los sensores que hay
class TableEnviromentSensors(Base):
    __tablename__ = "enviroment_sensors"
    
    # Column crea una columna en la tabla con el nombre y el tipo de dato especificado.
    id = Column(Integer, primary_key=True, index=True) # Identificador del sensor. primary_key=True para que sea único y no se pueda repetir. index=True para que se pueda buscar por indices y poner el id automaticamente
    description = Column(String, nullable=False) # Descripción del sensor (sensor de x). nullable=False para que no se pueda omitir
    building = Column(String, nullable=False) # Nave donde esta el sensor
    
    enviroment_readings = relationship("TableEnviromentReadings", back_populates="enviroment_sensors", cascade="all, delete-orphan")
    # Relacion con la tabla EnviromentReadings. back_populates es el nombre de la relación en la tabla EnviromentReadings.
    # Cascade es para que cuando se elimine un sensor, se eliminen también todos los datos de los sensores.
    # delete-orphan es para que se eliminen las lecturas que no estén relacionadas con ningún sensor.

# Tabla que contiene los datos de los sensores
class TableEnviromentReadings(Base):
    __tablename__ = "enviroment_readings"
    
    id = Column(Integer, primary_key=True, index=True) 
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) # Para que se guarde la fecha y hora en la que se ha guardado la lectura segun la zona horaria del servidor
    sensor_id = Column(Integer, ForeignKey("enviroment_sensors.id"), nullable=False) # ForeignKey es para que el id del sensor que envia la info este en EnviromentSensors
    value = Column(Float, nullable=False)
    
    enviroment_sensors = relationship("TableEnviromentSensors", back_populates="enviroment_readings")
