# cd api; python run.py (Windows)
# cd api && python run.py (Linux)

import uvicorn
import os
import sys

# Agregar el directorio actual al path para importar app
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)