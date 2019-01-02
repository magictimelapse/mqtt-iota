#!/usr/bin/env python
import paho.mqtt.client as paho
import json
broker = 'localhost'
port = 1883

client = paho.Client()
client.connect(broker,port)
data = {'temperature':22, 'humidity': 15}
# stringify the json data:
stringified_data = json.dumps(data, separators=(',',':'))
ret = client.publish('sensors/data',stringified_data)
