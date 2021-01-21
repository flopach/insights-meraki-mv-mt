from flask import Flask, render_template, request, Response
import threading
import config
import request_helper 

"""
FLASK Web-Framework
"""

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/entranceobserver",methods = ['POST', 'GET'])
def entranceobserver():
    if request.method == 'POST':
        result = request.form
        select_data = json.loads(result["mt_sensor"])

        #do some threading - user does not need to wait for the process to finish in the same browser window
        thread = threading.Thread(target=request_helper.get_snapshot_by_mt_door_event,args=(select_data["mt_door_serial"],select_data["snapshot_cam_serial"],int(result["num_entries"])))
        thread.start()

        return render_template("entranceobserver.html",result = result,snapshot_data = request_helper.get_cached_entrances())
    else:
        return render_template("entranceobserver.html",form_request_data = config.mt_sensors, snapshot_data = request_helper.get_cached_entrances())

@app.route("/peopledetection")
def peopledetection():
    return render_template("peopledetection.html")