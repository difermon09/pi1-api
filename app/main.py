from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routers import data_analysis, enviroment_readings, tag_readings
from .core.config import settings
from .db.database import engine, Base
from .db.init_db import init_db

# Context manager para inicializar y limpiar durante el ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización: crear tablas en la base de datos
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Inicializar datos por defecto
    await init_db()
    
    yield
    # Limpieza al cerrar la aplicación
    await engine.dispose()

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes concretos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(enviroment_readings.router,prefix="/enviroment_readings", tags=["readings"])
app.include_router(tag_readings.router, prefix="/tag_readings",tags=["tags"])
app.include_router(data_analysis.router, prefix="/data_analysis", tags=["analysis"])

# Prueba de la API
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de datos de sensores ESP32",
        "version": "1.0",
        "docs": f"/docs"
    } 