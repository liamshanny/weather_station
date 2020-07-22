from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.utils.db_connector import db
from datetime import datetime

router = APIRouter()


class LightData(BaseModel):
    r: float
    g: float
    b: float
    intensity: int


class WindData(BaseModel):
    speed: float
    direction: str


class WeatherData(BaseModel):
    startTime: int
    sampleInterval: int
    lpsTemp: List[float]
    siTemp: List[float]
    relativeHumidity: List[float]
    pressure: List[float]
    lightData: List[LightData]
    rainFall: List[float]
    windData: List[WindData]
    lastIp: str


@router.post('/full-send')
def full_send(message: WeatherData):
    processed_entries = []
    for index in range(len(message.lpsTemp)):
        sample_timestamp = message.startTime + (message.sampleInterval * index)
        processed_entries.append({
            "timestamp": datetime.utcfromtimestamp(sample_timestamp),
            "lpsTemp": message.lpsTemp[index],
            "siTemp": message.siTemp[index],
            "relativeHumidity": message.relativeHumidity[index],
            "pressure": message.pressure[index],
            "lightIntensity": message.lightData[index].intensity,
            "lightR": message.lightData[index].r,
            "lightG": message.lightData[index].g,
            "lightB": message.lightData[index].b,
            "rainFall": message.rainFall[index],
            "windSpeed": message.windData[index].speed,
            "windDirection": message.windData[index].direction,
            "lastIp": message.lastIp
        })
    for entry in processed_entries:
        with db.get_connection() as (cur, conn):
            cur.execute('''insert into weather_data (id,"timestamp", "lpsTemp", "siTemp", "relativeHumidity", 
            "pressure", "lightIntensity", "lightR", "lightG", "lightB", "rainFall", "windSpeed", "windDirection",
            "lastIp") values (default, %(timestamp)s, %(lpsTemp)s, %(siTemp)s, %(relativeHumidity)s, %(pressure)s, 
            %(lightIntensity)s, %(lightR)s, %(lightG)s, %(lightB)s, %(rainFall)s, %(windSpeed)s, %(windDirection)s, 
            %(lastIp)s)''', entry)
        db.wait(conn)
