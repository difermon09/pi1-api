# Fichero que crea una instancia de una clase que almacena los datos del .env para poder imporatar-la y usar-la en otros ficheros.

import os # Para poder buscar ficheros en la carpeta
from dotenv import load_dotenv # Para poder cargar las variables de entorno (las que estan en el .env)

load_dotenv() # Se carga las variables de entorno (lo del .env)

class Settings: #Se guarda los datos del .env en una clase para poder acceder a ellos des de los otros archivos

    API_V1_STR = "/api/v1" # Ruta base de la API
    PROJECT_NAME = "Projecte integrat" # Nombre del proyecto

    # Se coge los datos de el .env, si no existe alguno, se pone el valor por defecto de la derecha
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "farm_database") 
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434") 
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2") 

    # Se crea la URL de la base de datos. Se usa el driver asyncpg para conexiones asíncronas
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}" 

    # Usar simulación en lugar de Ollama para pruebas
    USE_SIMULATION = os.getenv("USE_SIMULATION", "false").lower() == "true"

# Se crea una instancia de la clase para poder importar-la i usar-la en otros ficheros
settings = Settings()