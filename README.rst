#########
ttn2influxdb
#########

********
About
********

Python program to subscribes to the MQTT broker of The Things Network (v3 stack) and saves incoming data into InfluxDB.

TTN (`The Things Network`_) is building a global open LoRaWAN™ network.





configuration file
---------------------
::

    [ttn]

        app_id = 
        access_key = 
        broker_url = eu1.cloud.thethings.network
        broker_port = 1883

    [influxdb]

        user = 
        password = 
        database = 
        measurement = 


*****
Setup
*****
::

    git clone https://github.com/AngelJMC/agriot-ttn-influxdb-connector
    cd agriot-ttn-influxdb-connector
    sudo python3 -m venv /opt/ttn2influxdb/pyenv
    source /opt/ttn2influxdb/pyenv/bin/activate
    sudo /opt/ttn2influxdb/pyenv/bin/python3 setup.py install


    sudo cp etc/systemd/ttn2influxdb.service /opt/ttn2influxdb
    ln -sr /opt/ttn2influxdb/ttn2influxdb.service /usr/lib/systemd/system/

    # Copy configurations
    sudo mkdir /opt/ttn2infuxdb/connections
    sudo cp connections/config-example.ini /opt/ttn2influxdb/connections
    
    # Edit configuration file
    sudo nano /opt/ttn2influxdb/connections/config-example.ini

    systemctl enable ttn2influxdb
    systemctl start ttn2influxdb
    systemctl status ttn2influxdb
    journalctl -u ttn2influxdb -f



.. _The Things Network: https://www.thethingsnetwork.org/
.. _MQTT: https://mqtt.org/
.. _InfluxDB: https://github.com/influxdata/influxdb
