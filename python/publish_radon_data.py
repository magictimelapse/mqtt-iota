#!/usr/bin/env python
import paho.mqtt.client as paho
import json
import random
import time
import radon_sensor

def create_location():
    latitude = 2*(random.random()-0.5)*90.
    longitude = 2*(random.random()-0.5)*180.
    location = {'latitude' :{'value':latitude , 'unit':'deg'},
                'longitude':{'value':longitude, 'unit':'deg'}}
    return location


if __name__ == "__main__":
    broker = 'localhost'
    port = 1883
    client = paho.Client()
    client.connect(broker,port)
    location = create_location()
    sensor_id = 'radon sensor'
    MAC_address = "a0:e6:f8:23:70:32"
    radon_sensor = radon_sensor.RadonSensor(MAC_address)
    while True:
        data,timestamp = radon_sensor.get_data()

        json_object = {'id': sensor_id,
                       'location': location,
                       'timestamp': timestamp,
                       'data': data}
        # stringify the json data:
        print('sending data to mqtt broker...')
        print(json_object)
        stringified_json_object = json.dumps(json_object, separators=(',',':'))
        ret = client.publish('sensors/data',stringified_json_object)
        time.sleep(30.)
