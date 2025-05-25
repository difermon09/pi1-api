#cd api\app\db; python clear_db.py (Windows)
#cd api/app/db && python clear_db.py (Linux)
import asyncio
import sys
import os
from sqlalchemy import text

# Añadir el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from api.app.db.database import AsyncSessionLocal, Base, engine

async def clear_db():
    async with AsyncSessionLocal() as session:
        # Borrar todas las tablas
        await session.execute(text('DROP TABLE IF EXISTS tag_readings CASCADE'))
        await session.execute(text('DROP TABLE IF EXISTS tag_sensors CASCADE'))
        await session.execute(text('DROP TABLE IF EXISTS enviroment_readings CASCADE'))
        await session.execute(text('DROP TABLE IF EXISTS enviroment_sensors CASCADE'))
        await session.execute(text('DROP TABLE IF EXISTS data_analysis CASCADE'))
        await session.commit()
        print('Todas las tablas eliminadas correctamente.')

        # Recrear todas las tablas
        async with engine.begin() as conn:
            # Crear la tabla enviroment_sensors
            await conn.execute(text('''
                CREATE TABLE IF NOT EXISTS enviroment_sensors (
                    id SERIAL PRIMARY KEY,
                    description VARCHAR NOT NULL,
                    building VARCHAR
                )
            '''))

            # Crear la tabla enviroment_readings
            await conn.execute(text('''
                CREATE TABLE IF NOT EXISTS enviroment_readings (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    sensor_id INTEGER NOT NULL REFERENCES enviroment_sensors(id),
                    value FLOAT NOT NULL
                )
            '''))

            # Crear la tabla tag_sensors
            await conn.execute(text('''
                CREATE TABLE IF NOT EXISTS tag_sensors (
                    id BIGINT PRIMARY KEY,
                    pen VARCHAR NOT NULL,
                    building VARCHAR
                )
            '''))

            # Crear la tabla tag_readings
            await conn.execute(text('''
                CREATE TABLE IF NOT EXISTS tag_readings (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    tag_id BIGINT NOT NULL REFERENCES tag_sensors(id)
                )
            '''))

            # Crear la tabla data_analysis
            await conn.execute(text('''
                CREATE TABLE IF NOT EXISTS data_analysis (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    analysis_type VARCHAR NOT NULL,
                    result TEXT NOT NULL
                )
            '''))

            # Reiniciar todas las secuencias
            await conn.execute(text('ALTER SEQUENCE enviroment_sensors_id_seq RESTART WITH 1'))
            await conn.execute(text('ALTER SEQUENCE enviroment_readings_id_seq RESTART WITH 1'))
            await conn.execute(text('ALTER SEQUENCE tag_readings_id_seq RESTART WITH 1'))
            await conn.execute(text('ALTER SEQUENCE data_analysis_id_seq RESTART WITH 1'))

        print('Todas las tablas recreadas correctamente.')
        print('Secuencias de IDs reiniciadas.')

if __name__ == "__main__":
    asyncio.run(clear_db())
