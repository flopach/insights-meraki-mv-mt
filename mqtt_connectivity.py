import paho.mqtt.client as mqtt
import json
import config
import influxdb_connect

"""
=== MQTT Handling ===
"""

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# disconnect message
def on_disconnect(client, userdata, flags, rc=0):
    print("DISconnected with result code "+str(rc))

#print the log
def on_log(client, userdata, level, buf):
    print("log: "+buf)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    split_topic = msg.topic.split("/", 3)
    zoneid = str(split_topic[3])

    # if persons appear the first time in the zone, save the zoneid and start time in the dict zones
    if (int(data["counts"]["person"]) >= 1 and zoneid not in config.zones):
        config.zones[zoneid] = { "starttime" : int(data["ts"]), "max_personcount" : { "number" : int(data["counts"]["person"]), "time" : int(data["ts"]) }  }
    
    # if zone is already in the dict zones, add the person count
    if (zoneid in config.zones):
        if int(data["counts"]["person"]) > int(config.zones[zoneid]["max_personcount"]["number"]):
            config.zones[zoneid]["max_personcount"] = { "number" : int(data["counts"]["person"]), "time" : int(data["ts"]) }

    # if there is no person in the zone and zoneid is in the dictionary zones, calculate the timestamp difference from start
    if (int(data["counts"]["person"]) == 0) and zoneid in config.zones:
        difference = int(data["ts"]) - int(config.zones[zoneid]["starttime"])
        max_personcount = config.zones[zoneid]["max_personcount"]["number"]
        if int(difference) >= int(config.time_until_count):
            zone_label = config.zonesinfo[zoneid]["label"]
            print(f"{max_personcount} person(s) were longer than {config.time_until_count} milliseconds in the zone: {zone_label} - for {difference} miliseconds.")
            # write data into the influxdb
            influxdbd_connect.write_api.write(bucket=config.influx_bucket,org=config.influx_org,record=Point("person_count_zones").tag("zone", zone_label).field("time_duration", difference).field("max_personcount", max_personcount).time(datetime.utcnow()))
            if int(max_personcount) > 2:
                print("More than 2 persons were in the zone at {}".format(config.zones[zoneid]["max_personcount"]["time"]))
        del config.zones[zoneid]

def startmqttclient():
    try:
        print("Start MQTT")
        client = mqtt.Client(client_id="pythonscript",protocol=mqtt.MQTTv311)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        #client.on_log = on_log
        client.on_message = on_message
        client.connect("127.0.0.1", port=1883)

        # subscribe to each zone's MQTT topic
        for item in config.zonesinfo:
            cam_serial = config.zonesinfo[item]["cam_serial"]
            zoneid = item
            client.subscribe(f"/merakimv/{cam_serial}/{zoneid}")

        # run the MQTT connection forever
        #client.loop_forever()
        client.loop_start()

    except Exception as e:
        print("MQTT Connection error: {}".format(e))