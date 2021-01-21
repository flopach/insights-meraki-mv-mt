from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import config

#influxdb connect
influx_client = InfluxDBClient(url="http://localhost:8086", token=config.influx_token, org=config.influx_org) #debug=True
write_api = influx_client.write_api(write_options=SYNCHRONOUS)