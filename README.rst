#########
ttn2influxdb
#########


Python program to subscribes to the MQTT broker of The Things Network (v3 stack) and saves incoming data into InfluxDB.

TTN (`The Things Network`_) is building a global open LoRaWAN™ network.





Configuration file
---------------------
The configuration file contains the basic parameters to establish a connection to The Things Network's MQTT broker and the influxdb database. The schema of this file is as follows:
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

More than one configuration file can be added to establish different connections to the MQTT broker.

*****
Setup
*****

Clone the repository and create a new python virtual environment in which to install the ttn2influxdb package.
::
    git clone https://github.com/AngelJMC/agriot-ttn-influxdb-connector
    cd agriot-ttn-influxdb-connector
    sudo python3 -m venv /opt/ttn2influxdb/pyenv
    source /opt/ttn2influxdb/pyenv/bin/activate
    sudo /opt/ttn2influxdb/pyenv/bin/python3 setup.py install

Copy the configuration file to the installation directory and add the configuration parameters.
::
    # Copy configurations
    sudo mkdir /opt/ttn2infuxdb/connections
    sudo cp connections/config-example.ini /opt/ttn2influxdb/connections
    
    # Edit configuration file
    sudo nano /opt/ttn2influxdb/connections/config-example.ini


Configure program execution
::
    sudo cp etc/systemd/ttn2influxdb.service /opt/ttn2influxdb
    ln -sr /opt/ttn2influxdb/ttn2influxdb.service /usr/lib/systemd/system/
    
    systemctl enable ttn2influxdb
    systemctl start ttn2influxdb
    systemctl status ttn2influxdb
    journalctl -u ttn2influxdb -f



.. _The Things Network: https://www.thethingsnetwork.org/
.. _MQTT: https://mqtt.org/
.. _InfluxDB: https://github.com/influxdata/influxdb
