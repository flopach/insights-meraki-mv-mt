# Getting Insights with Meraki Cameras and Sensors
# Real demo showcase in the Cisco Frankfurt Office
#
# Flo Pachinger / flopach, Cisco Systems, Dec 2020
# Apache License 2.0

import config
import mqtt_connectivity
import flask_server
import request_helper

#run main program
if __name__ == "__main__":
    #get current defined zones from Meraki API
    request_helper.getzonesinfo() 

    #start MQTT client
    mqtt_connectivity.startmqttclient()

    #start web-app server
    #flask_server.app.run(debug=True)    
    flask_server.app.run(host="0.0.0.0")