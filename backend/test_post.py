import requests
import umsgpack

testWeatherData = {
    "startTime": 1595382642,
    "sampleInterval": 60,
    "lpsTemp": [40.3213, 23.54],
    "siTemp": [40.3213, 54.43],
    "relativeHumidity": [60.60, 30.00],
    "pressure": [123.321, 232.0932],
    "lightData": [{"r": 5451.5, "g": 5456.516, "b": 15.1, "intensity": 5}, {"r": 5451.5, "g": 5456.516, "b": 15.1,
                                                                            "intensity": 5}],
    "rainFall": [34234.3423, 4382.232],
    "windData": [{"speed": 54156.5416, "direction": "north"}, {"speed": 54156.5416, "direction": "north"}],
    "lastIp": "10.1.10.54"
    }

data = umsgpack.packb(testWeatherData)
headers = {"content-type": "application/x-msgpack"}
cert = ('certs/user.crt', 'certs/user_unencrypted.key')
r = requests.post('https://weather.shanny.tools/api/v1/full-send', data=data, headers=headers, cert=cert)
print(r.reason)
