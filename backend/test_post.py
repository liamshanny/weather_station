import requests
import umsgpack

testWeatherData = {'command': 'test','data': {'timeStamp': 1595817930, 'lpsTemp': 524.28, 'lpsPressure': -0.043701171875,
                               'siTemp': 23.38866455078125,
                               'relativeHumidity': 49.461883544921875,
                               'lightData': {'r': 255, 'g': 255, 'b': 255, 'intensity': 255},
                               'rainFall': 0.1, 'windData': {'speed': 2.2, 'direction': 'nw'},
                               'lastIp': '169.254.255.255'}}

data = umsgpack.packb(testWeatherData)
headers = {"content-type": "application/x-msgpack"}
cert = ('certs/user.crt', 'certs/user_unencrypted.key')
r = requests.post('https://weather.shanny.tools/api/v1/full-send', data=data, headers=headers, cert=cert, verify=True)
print(r.reason)

