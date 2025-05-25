# Fichero encargado de crear la tabla que contiene los analisis hechos por la IA en la base de datos
# Esto incluye tambien crear sus columnas indicando sus caracteristicas

from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func

from ..db.database import Base

# Tabla que contiene los analisis hechos por la IA
class TableDataAnalysis(Base):
    __tablename__ = "data_analysis"
    
    id = Column(Integer, primary_key=True, index=True) 
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    analysis = Column(Text, nullable=False)