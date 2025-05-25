# Fichero que inicializa el paquete models para poder importar los modelos mas facilmente

from .model_enviroment import TableEnviromentSensors, TableEnviromentReadings
from .model_data_analysis import TableDataAnalysis
from .model_tags import TableTagSensors, TableTagReadings

'''
Gracias al __init__ se puede hacer:
from app.models import EnviromentSensor

en vez de:
from app.models.enviroment import EnviromentSensor
'''