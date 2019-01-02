from bluepy.btle import UUID, Peripheral
import struct
import time
from datetime import datetime
class Sensor:
    def __init__(self, name, uuid, format_type, unit, scale):
        self.name = name
        self.uuid = uuid
        self.format_type = format_type
        self.unit = unit
        self.scale = scale

class RadonSensor:
    def __init__(self,MAC_address):
        self.peripheral =  Peripheral(MAC_address)
        self.sensors = []
        self.sensors.append(Sensor("timestamp", UUID(0x2A08), 'HBBBBB', "", 0))
        self.sensors.append(Sensor("temperature", UUID(0x2A6E), 'h', "C", 1.0/100.0))
        self.sensors.append(Sensor("humidity", UUID(0x2A6F), 'H', "%RH", 1.0/100.0))
        self.sensors.append(Sensor("Radon_24h_avg", "b42e01aa-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3", 1.0))
        self.sensors.append(Sensor("Radon_long_term", "b42e0a4c-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3", 1.0))
    def get_data(self):
        data = {}
        timestamp = None
        for s in self.sensors:
            ch = self.peripheral.getCharacteristics(uuid=s.uuid)[0]
            if ch.supportsRead():
                val = ch.read()

                if s.name == "timestamp":
                    unpacked = struct.unpack(s.format_type, val)
                    dt = datetime(*unpacked)
                    timestamp = time.mktime(dt.timetuple())
                else:
                    data[s.name]  = {}
                    data[s.name]['value'] = struct.unpack(s.format_type, val)[0]*s.scale
                    data[s.name]['unit'] = s.unit
        return data,timestamp
