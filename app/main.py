import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routers import data_analysis, enviroment_readings, tag_readings
from .core.config import settings
from .db.database import engine, Base
from .db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Inicializar la base de datos
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_db()

    # 2. Descargar modelo de Ollama (si no está ya)
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ollama_host}/api/pull", json={"name": ollama_model}
            )
    except Exception:
        # Error de conexión a Ollama
        pass

    yield

    # Al finalizar, cerrar conexión con la base de datos
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(
    enviroment_readings.router, prefix="/enviroment_readings", tags=["readings"]
)
app.include_router(tag_readings.router, prefix="/tag_readings", tags=["tags"])
app.include_router(data_analysis.router, prefix="/data_analysis", tags=["analysis"])


# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de datos de sensores ESP32",
        "version": "1.0",
        "docs": "/docs",
    }
