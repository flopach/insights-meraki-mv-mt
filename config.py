# Getting Insights with Meraki Cameras and Sensors
# Real demo showcase in the Cisco Frankfurt Office
#
# Flo Pachinger / flopach, Cisco Systems, Dec 2020
# Apache License 2.0
import pytz

"""
CONFIGURATION FILE
"""

### Meraki API Parameter ###
base_url = ""
meraki_api_key = ""
local_timezone = pytz.timezone("Europe/Berlin")
organization_id = ""
network_id = ""
cam_serials = ["xxx","xxx","..."]

### Config for snapshot function
# Serial of MT sensor, serial of MV camera, human-readable name for the snapshot function
mt_sensors = { "serial_mt" : { "name" : "myname", "snapshot_cam_serial" : "serial_mv" },
               "serial_mt" : { "name" : "myname", "snapshot_cam_serial" : "serial_mv" }
}

### InfluxDB 2.0 Config ###
# Does not work with InfluxDB 1.x!
influx_token = ""
influx_org = ""
influx_bucket = ""

### Misc Config ###
time_until_count = 20000 #in milliseconds - change to when the camera should insert the person(s) in the database

### Do NOT edit - temporary data ###
zones = {} #temp zones - used as cache for counting if persons are in the zone for time_until_count milliseconds - LEAVE EMPTY!
zonesinfo = {} #meta data of zones (used once) - LEAVE EMPTY!