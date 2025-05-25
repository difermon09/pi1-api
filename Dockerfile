FROM python:3.12-slim

LABEL maintainer="difermon09"
LABEL description="API para el sistema de monitoreo de sensores ESP32"
LABEL version="1.0"
LABEL documentation="https://github.com/difermon09/pi1"

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la API
COPY api/ .

# Exponer el puerto de la API
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]