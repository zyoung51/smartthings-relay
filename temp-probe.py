from os import environ
from time import sleep
from prometheus_client import Counter, start_http_server
import requests

HEADERS = {'Authorization': 'Bearer {}'.format(environ.get('SMARTTHINGS_BEARER_TOKEN'))}
POLLING_INTERVAL = 120
HTTP_PORT = 9909

sensor_temp_fahrenheit = Counter("sensor_temp_fahrenheit", "Sensor temperature", ["device"])
sensor_power_watts = Counter("sensor_power_watts", "Sensor Power", ["device"])

def create_poll_list():
  poll_list=[]
  url='https://api.smartthings.com/v1/devices'
  response=requests.get(url, headers=HEADERS)
  for item in response.json()['items']:
    if item.get('deviceTypeName') == 'Xiaomi Aqara Temperature Humidity Sensor':
      poll_list.append( (item['deviceId'], item['label'].replace(' ', '_'), "temp") )
    if item.get('deviceTypeName') == 'Aeon Home Energy Meter':
      poll_list.apped( (item['deviceId'], item['label'].replace(' ', '_'), "power") )
  return poll_list

def poll_metrics(poll_list):
  while True:
    for item in poll_list:
      (deviceId, label,type) = item
      status_url='https://api.smartthings.com/v1/devices/{}/status'.format(deviceId)
      status=requests.get(status_url, headers=HEADERS)
      if type=="temp":
        temperature=status.json()['components']['main']['temperatureMeasurement']['temperature']['value']
        sensor_temp_fahrenheit.labels(label)._value.set(temperature)
      if type=="power":
        power=status.json()['components']['main']['powerMeter']['power']['value']
        sensor_power_watts.labels(label)._value.set(power)
    sleep(POLLING_INTERVAL)

if __name__ == "__main__":
  start_http_server(HTTP_PORT)
  poll_list = create_poll_list()
  poll_metrics(poll_list)

