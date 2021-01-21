import requests
import json
import datetime
import dateutil.parser
import time
from datetime import timezone
import os
import pytz
import config

def getzonesinfo():
    """
    Get all zones via the Meraki Dashboard API from all cameras which are defined by the user in the settings
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": config.meraki_api_key
    }

    for serial in config.cam_serials:
        try:
            msg = requests.request('GET', f"{config.base_url}/devices/{serial}/camera/analytics/zones", headers=headers)
            data = msg.json()
        except Exception as e:
            print("MQTT Connection error: {}".format(e))

        for item in data:
            if item["zoneId"] != "0":
                config.zonesinfo[item["zoneId"]] = {
                    "cam_serial" : serial,
                    "label" : item["label"]
                }


def get_snapshot_by_mt_door_event(mt_door_serial, mv_snapshot_camera, num_entries):
    """
    Download the snapshot images of the Meraki camera when the door sensor is being triggered
    Select MT Door Sensor and the MV Camera where to take the snapshots from + number of events from now
    """

    ### Meraki API: Get 20 Evironmental Events by MT serial number
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": config.meraki_api_key
    }
    params = {
        "includedEventTypes[]" : "mt_door",
        "perPage" : num_entries,
        "gatewaySerial" : mt_door_serial
    }
    
    r_envevents = requests.request('GET', f"{config.base_url}/networks/{config.network_id}/environmental/events", headers=headers, params=params)
    r_envevents_json = r_envevents.json()


    #Parse events where door was opened and add a timedelta
    #Meraki API: For each timestamp get the snapshot URL and download the image
    for item in r_envevents_json:
        if item["eventData"]["value"] == "1.0":
            print("Getting Snapshot")
            time_plus_delta = dateutil.parser.parse(item["occurredAt"]) + datetime.timedelta(0,2) #add 2 seconds to generate snapshot
            new_ts_iso = datetime.datetime.isoformat(time_plus_delta)
            new_ts_unix = time_plus_delta.timestamp()

            headers = {
                "Content-Type": "application/json",
                "X-Cisco-Meraki-API-Key": config.meraki_api_key
            }
            data = {
                "timestamp" : new_ts_iso
            }
            
            try:
                r_snapshoturl = requests.request('POST', f"{config.base_url}/devices/{mv_snapshot_camera}/camera/generateSnapshot", headers=headers, data=json.dumps(data))
                r_snapshoturl_json = r_snapshoturl.json()
            except Exception as e:
                print(f"Error when getting image URL: {e}")

            time.sleep(5) #wait at least 5 seconds before trying to download the image
            os.makedirs(os.path.dirname(f"static/images/{mv_snapshot_camera}/"), exist_ok=True) #create folders if not exists

            retries = 0
            success = False
            while success == False:
                try:
                    r_img = requests.get(r_snapshoturl_json["url"])
                    if r_img.status_code == 200:
                        with open(f"static/images/{mv_snapshot_camera}/{new_ts_unix}.jpeg", 'wb') as f:
                            f.write(r_img.content)
                        success = True
                except Exception as e:
                    retries += 1
                    print(f"Error when downloading images: {e}")
                    print(f"Status-Code: {r_img.status_code} / Retry: {retries}")
                    time.sleep(30)
                    if retries > 5:
                        print("Error: Avoid endless loop")
                        success = True

"""
=== Local Functions ===
"""

def get_cached_entrances():
    """
    Get all downloaded images - iterating through images folder
    static/images/ < serial number MV camera > / < timestamp-unix-time-format > .jpeg
    """
    snapshot_data = {}
    try:
        for cam_serial_folder in os.listdir("static/images/"):
            snapshot_data[cam_serial_folder] = {}
            # get name for door/camera snapshot feature from config above
            for key,value in config.mt_sensors.items():
                if cam_serial_folder in value["snapshot_cam_serial"]:
                    snapshot_data[cam_serial_folder]["name"] = value["name"]
            # iterating through the folders, sort filename by name reversed (highest on top)
            snapshot_data[cam_serial_folder]["images"] = []
            for cam_snapshot in sorted(os.listdir(f"static/images/{cam_serial_folder}"),reverse=True):
                img_url = f"static/images/{cam_serial_folder}/"+cam_snapshot
                img_time_unix = cam_snapshot[:-7]
                img_time_human = datetime.datetime.fromtimestamp(int(img_time_unix)).replace(tzinfo=config.local_timezone).strftime("%Y-%m-%d %H:%M:%S")
                img_meta_data = { "img_url" : img_url, "img_time" : img_time_human }
                snapshot_data[cam_serial_folder]["images"].append(img_meta_data)
        return snapshot_data
    except:
        print("Folders not yet created")  