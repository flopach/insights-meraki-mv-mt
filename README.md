# Getting Insights with Meraki Cameras and Sensors

This real showcase from the Cisco Frankfurt office highlights the possibilities of the Meraki MV cameras and Meraki MT sensors.

Currently there are 2 use-cases in one Python application implemented:

* **Person detection within pre-defined zones**: If one or more persons are standing within the pre-defined zone (setting in the Meraki-dashboard), the camera is sending out an MQTT message to the python script. Then, only if the person stays for at least x seconds, the data (how many persons, what timeframe, for how long) will be stored in a time-series database.
* **Open/Close MT20 Sensor + Meraki Camera Snapshot**: The webapp shows who has opened the door. It requests the last x events from the Open/Close Meraki MT20 sensor and downloads snapshots from the time where the sensor has been triggered (=door was opened) from a Meraki MV camera.

![](cbc-mt-snapshot.png)

## Architecture

The script uses several components:

* Meraki MT sensors + Meraki MV camera 2nd generation
* MQTT broker Mosquitto: to send and receive the object detection messages from the MV cameras
* Time series database InfluxDB 2.0: To store the information (this script is not compatible with InfluxDB 1.x!)
* Grafana for visualisation
* Python
	* Flask web-framework
	* Paho-MQTT client

![](architecture.png)

## Configuration

1. Setup your Meraki equipment accordingly, define zones in the camera settings
2. Install & setup Mosquitto, InfluxDB 2.0, Grafana on a Linux system
3. Clone this repo and deploy the python files in your virtual environment. I would recommend to use [pipenv](https://pypi.org/project/pipenv/) (Pipfile is included).
4. Edit the `config.py`file and insert your credentials and modify you configuration.
5. Setup your Grafana dashboard according to your zones and data.
6. Start the script and let it run.

## Versioning

**1.0** - inital features: person detection with zones and open/close snapshot feature

## Contributors

* **Florian Pachinger** - *Code* - [flopach](https://github.com/flopach)
* **Stephan Luhn** - *Meraki & Hardware*
* **Rasim Yigit** - *Meraki & Hardware* - [rayigit](https://github.com/rayigit)

## License

This project is licensed under the MIT license - see the [LICENSE.md](LICENSE.md) file for details.