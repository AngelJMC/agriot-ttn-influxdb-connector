# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


setup(name='ttn2influxdb',
      version='0.1.0',
      description='Subscribes to the MQTT broker of The Things Network and saves incoming data into InfluxDB.',
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: System :: Networking :: Monitoring",
        "Operating System :: Unix",
        ],
      author='Angel Maldonado',
      author_email='angelgesus@gmail.com',
      url='https://github.com/AngelJMC/agriot-ttn-influxdb-connector',
      keywords= 'ttn mqtt influxdb',
      packages=find_packages(),
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      install_requires= [ 'influxdb', 'paho-mqtt', 'configparser'],
      entry_points={
          'console_scripts': [
              'ttn2influxdb = ttn2influxdb.ttn_influxdb:run',
          ],
      },
)
