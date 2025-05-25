from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import httpx
import json
from datetime import datetime, timezone

from ..db.database import get_db
from ..models.model_enviroment import TableEnviromentSensors
from ..models.model_data_analysis import TableDataAnalysis
from ..core.config import settings

router = APIRouter()

async def process_with_llama(sensor_data: dict, db: AsyncSession) -> dict:
    """Procesa los datos con el modelo de lenguaje."""
    try:
        # Crear cliente HTTP con timeout más largo
        client = httpx.AsyncClient(timeout=300.0)  # 5 minutos de timeout
        
        # Preparar prompt
        prompt = f"""
        You are an expert in analyzing sensor data from pig farms. Your task is to analyze the following sensor data and provide a detailed weekly report about PIG FARM conditions and PIG behavior.

        {json.dumps(sensor_data, indent=2)}

        CRITICAL REQUIREMENTS:
        1. This analysis MUST be about PIGS and PIG FARM conditions
        2. DO NOT mention any other animals
        3. You MUST include ALL these measurements in your report, in this exact order:
           - Start with "This week has had an average temperature of X degrees Celsius"
           - Then "an average humidity of X%"
           - Then "average CO2 levels of X ppm"
           - Then "and average ammonia levels of X ppm"
           - Finally, analyze the relationship between light intensity and feeding patterns
        4. Use actual values from the data
        5. Keep the report concise and clear
        6. Write the report as a single, flowing text that includes both analysis and recommendations
        7. NEVER skip any of the required measurements (temperature, humidity, CO2, ammonia)
        8. ONLY report average values, DO NOT include ranges or min/max values
        9. DO NOT use phrases like "with a range of" or "ranging from"

        Format your response as a JSON object:
        {{
            "report": "Write a concise report that flows naturally from analysis to recommendations. Include specific values and clear analysis, with recommendations integrated into the text."
        }}

        VALIDATION CHECK:
        Before submitting your response, verify that:
        - The report starts with "This week has had..."
        - ALL measurements are included in this exact order:
          1. Temperature (average only)
          2. Humidity (average only)
          3. CO2 levels (average only)
          4. Ammonia levels (average only)
        - The report mentions the relationship between light and feeding patterns
        - The analysis is ONLY about pigs and pig farm conditions
        - DO NOT mention specific hours of sunlight or other unmeasured values
        - Recommendations are integrated naturally into the text
        - NO ranges or min/max values are included
        """
        
        # Procesar con Ollama
        ollama_response = await client.post(
            f"{settings.OLLAMA_HOST}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json"  # Forzar formato JSON
            }
        )
        
        ollama_response.raise_for_status()
        ollama_result = ollama_response.json()
        response_text = ollama_result.get("response", "")
        
        # Intentar extraer y validar el JSON
        try:
            # Primero intentar parsear directamente
            ai_data = json.loads(response_text)
        except json.JSONDecodeError:
            # Si falla, intentar extraer el JSON del texto
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            
            if start_idx < 0 or end_idx <= start_idx:
                # Si no se encuentra JSON, crear una respuesta por defecto
                ai_data = {
                    "report": "No se pudo generar un análisis válido. Por favor, intente nuevamente.",
                    "recommendations": [
                        "Verificar la conexión con el modelo de IA",
                        "Asegurarse de que hay datos suficientes para el análisis",
                        "Reintentar el análisis en unos minutos"
                    ]
                }
            else:
                try:
                    json_str = response_text[start_idx:end_idx]
                    ai_data = json.loads(json_str)
                except json.JSONDecodeError:
                    # Si aún falla, usar la respuesta por defecto
                    ai_data = {
                        "report": "Error al procesar la respuesta del modelo. Por favor, intente nuevamente.",
                        "recommendations": [
                            "Verificar la conexión con el modelo de IA",
                            "Asegurarse de que hay datos suficientes para el análisis",
                            "Reintentar el análisis en unos minutos"
                        ]
                    }
        
        # Guardar análisis en la base de datos
        analysis = TableDataAnalysis(
            timestamp=datetime.now(timezone.utc),
            analysis=json.dumps(ai_data)
        )
        db.add(analysis)
        await db.commit()
        
        return ai_data
        
    except Exception as e:
        print("ERROR EN ANALISIS IA:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar datos con IA: {str(e)}"
        )
    finally:
        await client.aclose()

@router.post("/process", response_model=None)
async def trigger_analysis(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    # Obtener todos los sensores de ambiente
    result = await db.execute(select(TableEnviromentSensors))
    sensors = result.scalars().all()
    
    # Obtener lecturas de todos los sensores de la última semana
    all_env_readings = []
    async with httpx.AsyncClient() as client:
        for sensor in sensors:
            response = await client.get(f"http://localhost:8000/enviroment_readings/{sensor.id}")
            if response.status_code == 200:
                readings = response.json()
                all_env_readings.extend(readings)

        # Obtener lecturas de tags recientes
        response = await client.get("http://localhost:8000/tag_readings/")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al obtener lecturas de tags")
        tag_readings = response.json()

    # Agrupar lecturas por sensor
    readings_by_sensor = {}
    for reading in all_env_readings:
        sensor_id = reading["sensor_id"]
        if sensor_id not in readings_by_sensor:
            readings_by_sensor[sensor_id] = []
        readings_by_sensor[sensor_id].append(reading)

    # Obtener información de los sensores
    result = await db.execute(select(TableEnviromentSensors))
    sensors = {sensor.id: sensor for sensor in result.scalars().all()}

    # Preparar datos para la IA
    sensor_data = {
        "sensors": [
            {
                "sensor_id": sensor_id,
                "readings": readings,
                "sensor_type": sensors[sensor_id].description if sensor_id in sensors else "unknown",
                "building": sensors[sensor_id].building if sensor_id in sensors else "unknown",
                "total_readings": len(readings)
            }
            for sensor_id, readings in readings_by_sensor.items()
        ],
        "tag_readings": tag_readings
    }

    # Ejecutar el análisis IA y devolver el resultado como string JSON
    background_tasks.add_task(process_with_llama, sensor_data, db)
    return {"message": "Análisis iniciado. Los resultados estarán disponibles en el endpoint /data_analysis/latest"}

@router.get("/latest")
async def read_latest_analysis(db: AsyncSession = Depends(get_db)):
    # Obtener el timestamp actual
    current_time = datetime.now(timezone.utc)
    
    # Buscar el análisis más reciente
    result = await db.execute(
        select(TableDataAnalysis)
        .order_by(TableDataAnalysis.timestamp.desc())
        .limit(1)
    )
    analysis = result.scalars().first()
    
    if analysis is None:
        raise HTTPException(status_code=404, detail="No analysis found")
    
    # Verificar si el análisis es reciente (menos de 30 segundos)
    time_diff = current_time - analysis.timestamp
    if time_diff.total_seconds() > 30:  # 30 segundos
        raise HTTPException(status_code=404, detail="No recent analysis found")
    
    # Deserializar el análisis antes de devolverlo
    return {"analysis": json.loads(analysis.analysis)}
