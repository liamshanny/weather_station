from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import logging
from utils.db_connector import db
from datetime import datetime

# logger = logging.getLogger(__name__)
router = APIRouter()
logger = logging.getLogger("gunicorn.error")


class LightData(BaseModel):
    r: int
    g: int
    b: int
    intensity: int


class WindData(BaseModel):
    speed: float
    direction: str


class WeatherData(BaseModel):
    timeStamp: int
    lpsTemp: float
    siTemp: float
    relativeHumidity: float
    lpsPressure: float
    lightData: LightData
    rainFall: float
    windData: WindData
    lastIp: str

class data(BaseModel):
    data: WeatherData
    command: str


{'command': 'sendStandardData',
 'data': {'timeStamp': 1595817930, 'lpsTemp': 524.28, 'lpsPressure': -0.043701171875, 'siTemp': 23.38866455078125,
          'relativeHumidity': 49.461883544921875, 'lightData': {'r': 255, 'g': 255, 'b': 255, 'intensity': 255},
          'rainFall': 0.1, 'windData': {'speed': 2.2, 'direction': 'nw'}, 'lastIp': '169.254.255.255'}}


@router.post('/full-send')
def full_send(data: data):
    message = data.data
    weather_data = {
        "timestamp": datetime.utcfromtimestamp(message.timeStamp),
        "lpsTemp": message.lpsTemp,
        "siTemp": message.siTemp,
        "relativeHumidity": message.relativeHumidity,
        "pressure": message.lpsPressure,
        "lightIntensity": message.lightData.intensity,
        "lightR": message.lightData.r,
        "lightG": message.lightData.g,
        "lightB": message.lightData.b,
        "rainFall": message.rainFall,
        "windSpeed": message.windData.speed,
        "windDirection": message.windData.direction,
        "lastIp": message.lastIp
    }
    logger.error(weather_data)
    with db.get_connection() as (cur, conn):
        cur.execute('''insert into weather_data (id,"timestamp", "lpsTemp", "siTemp", "relativeHumidity", 
        "pressure", "lightIntensity", "lightR", "lightG", "lightB", "rainFall", "windSpeed", "windDirection",
        "lastIp") values (default, %(timestamp)s, %(lpsTemp)s, %(siTemp)s, %(relativeHumidity)s, %(pressure)s, 
        %(lightIntensity)s, %(lightR)s, %(lightG)s, %(lightB)s, %(rainFall)s, %(windSpeed)s, %(windDirection)s, 
        %(lastIp)s)''', weather_data)
    db.wait(conn)

    return {"status": "OK"}
