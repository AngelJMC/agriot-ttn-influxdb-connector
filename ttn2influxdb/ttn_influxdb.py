# -*- coding: utf-8 -*-
# (c) 2022 Angel Maldonado <angelgesus@gmail.com>
# License: GNU Affero General Public License, Version 3
import logging
import sys
import json
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
from configparser import ConfigParser
import argparse
import threading
from pathlib import Path



logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class TTNClient:

    def __init__(self, app_id, access_key, callback_msg, url="eu1.cloud.thethings.network",port=8883):
        self.app_id = app_id
        self.access_key = access_key
        self.url = url
        self.port = port
        self.mqtt_client = None
        self.msg_process = callback_msg
        self.connected = False
        

    def loop_forever(self):
        self.mqtt_client.loop_forever()
 

    def connect(self):
        logging.info('Connecting to TTN MQTT broker')

        # Start MQTT client and wire event callbacks.
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.connect_callback
        self.mqtt_client.on_message = self.uplink_callback
        self.mqtt_client.tls_set()
        self.mqtt_client.username_pw_set(self.app_id, password=self.access_key)
        self.mqtt_client.connect(self.url, self.port, 60)
        

    def connect_callback(self, client, userdata, flags, rc):
        logging.info('Connected with result code '+str(rc))
        client.subscribe('v3/+/devices/+/up')

    #def disconnect_callback(self, res, client):
    #    address = client._MQTTClient__mqtt_address
    #    print('Disconnected from MQTT broker at "{}"'.format(address))
    #    self.connected = False

    def uplink_callback(self, client, userdata, msg):
        ergebnis = json.loads(msg.payload)
        self.msg_process(ergebnis)


class InfluxDatabase:

    def __init__(self, database, measurement, user, password, url='localhost', port=8086 ):

        assert database, 'Database name missing or empty'
        assert measurement, 'Measurement name missing or empty'

        self.database = database
        self.measurement = measurement
        self.user = user
        self.password = password
        self.url = url
        self.port = port

    def connect(self):
        self.client = InfluxDBClient(self.url, self.port, self.user, self.password, self.database )


    def store(self, ttn_message):

        timestamp = ttn_message['received_at']

        # Add application and device id as tags.
        tags = dict()
        tags['dev_id'] = ttn_message['end_device_ids']['device_id']
        tags['dev_addr'] = ttn_message['end_device_ids']['dev_addr']

        data = dict()

        # Pick up telemetry values from gateway information.
        num_gtws = len(ttn_message['uplink_message']['rx_metadata'] )
        logging.debug('Message received from ' + str(num_gtws) + ' gateway(s)')
        data['rssi'] = 0
        data['snr'] = 0.0

        for i in range(num_gtws):
            snr = float(ttn_message['uplink_message']['rx_metadata'][i]['snr'])
            if snr > data['snr']:         
                data['rssi'] = int(ttn_message['uplink_message']['rx_metadata'][i]['rssi'])
                data['snr']  = snr

        # Pick up telemetry values from main data payload.
        payload = ttn_message['uplink_message']['decoded_payload']
        for field in payload:
            value = payload[field]
            if float == type(value):
                data[field] = value 
            elif dict == type(value):
                for fild in value:
                    if float == type(value[fild]):
                        data[fild] = value[fild]
  
        point = {
            "measurement": self.measurement,
            "tags": tags,
            "time": timestamp,
            "fields": data,
        }

        logging.debug(point)
        self.client.write_points([point])




class connector:

    def __init__(self, config):

        dbcfg = config['influxdb']
        self.influxdb = InfluxDatabase(dbcfg['database'], dbcfg['measurement'], dbcfg['user'], dbcfg['password'] )
        ttncfg = config['ttn']
        self.ttn = TTNClient(ttncfg['app_id'], ttncfg['access_key'], self.influxdb.store)
        

    def run(self):
        
        self.influxdb.connect()
        self.ttn.connect()
        self.ttn.loop_forever()



def run():
    parser = argparse.ArgumentParser(description='Subscribes to the MQTT broker of The Things Network and saves incoming data into InfluxDB.')
    parser.add_argument('--dir', metavar='path' ,help='Path to the configuration directory', default='./')

    args = parser.parse_args()
    
    #Loop for all .ini file in directory

    p = Path(args.dir)
    logging.debug(p.name)
    threads = []
    for file in list(p.glob('*.ini')):
        logging.info('Load configuration file: ' + file.name)
        # multiprocessing support
        config = ConfigParser()
        config.read(file)
        con = connector(config)
        t = threading.Thread(target=con.run )
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

  
    

