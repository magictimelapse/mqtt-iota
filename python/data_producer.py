#!/usr/bin/env python
import paho.mqtt.client as paho
import json
import random
import time
def create_data():
    humidity = random.random()*100.
    temperature = random.random()*50-30.
    radon_activity = random.random()*200
    data = {'humidity'   : {'value': humidity, 'unit':'%RH'},
            'temperature': {'value': temperature, 'unit':'C'},
            'radon_activity': {'value':radon_activity, 'unit':'Bq'}}
    return data

def create_location():
    latitude = 2*(random.random()-0.5)*90.
    longitude = 2*(random.random()-0.5)*180.
    location = {'latitude' :{'value':latitude , 'unit':'deg'},
                'longitude':{'value':longitude, 'unit':'deg'}}
    return location

def get_timestamp():
    return time.time() # unix timestamp in utc

if __name__ == "__main__":
    broker = 'localhost'
    port = 1883
    client = paho.Client()
    client.connect(broker,port)
    location = create_location()
    sensor_id = 'radon sensor'
    while True:
        data = create_data()
        timestamp = get_timestamp()
        json_object = {'id': sensor_id,
                       'location': location,
                       'timestamp': timestamp,
                       'data': data}
        # stringify the json data:
        stringified_json_object = json.dumps(json_object, separators=(',',':'))
        ret = client.publish('sensors/data',stringified_json_object)
        time.sleep(30.)
