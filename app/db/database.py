# Fichero que configura la conexión asíncrona con la base de datos PostgreSQL usando SQLAlchemy y proporciona una función para gestionar las sesiones de la base de datos.

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings

# Se crea el motor de la base de datos. Usa el driver asyncpg para conexiones asíncronas. 
engine = create_async_engine(
    settings.DATABASE_URL,
    echo = True
) 
# echo=True para ver las consultas SQL en la consola. 
# Al ser asincrono, no se espera a que se complete la consulta, sino que se sigue ejecutando el programa.

AsyncSessionLocal = sessionmaker(
    engine, # No hace falta poner bind, lo detecta solo
    class_ = AsyncSession, 
    expire_on_commit = False, # Para que no se cierre la sesión cuando se hace un commit, sino que se mantenga abierta para futuras consultas.
)

Base = declarative_base()

async def get_db():
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session: # Crea una sesión de la base de datos asyncrona, como cuando db = SessionLocal() en los no asyncronos
        try:
            yield session # Devuelve la sesión y finaliza la ejecución de la función. Con el yield, se puede usar la sesión en el endpoint.
        finally: # Siempre al finalizar lo del try, da igual si hay error o no, se ejecuta lo del finally, cerrando la sesión siempre.
            # Cierra la sesión. El await espera a que esta tarea termine, pero mientras tanto, libera el hilo de ejecución para que otras cosas puedan seguir funcionando
            await session.close() 