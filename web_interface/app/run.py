"""Minimal flask application."""
import os
import simplejson as json
from flask import Flask, render_template, request, jsonify, Response
import mysql.connector
from mysql.connector import Error
# emulated camera
from camera import Camera
# Initialize Flask web app
app = Flask(__name__)
# MySQL connection 
connection = mysql.connector.connect(host='localhost',
										 database='sensors',
										 user='mysql',
										 password='mysql')


@app.route('/')
def main_page():
	try:
		select_query = "SELECT Oxidise, Reducing, Nh3 FROM UAVSensors ORDER BY Id DESC limit 6;"
		cursor = connection.cursor()
		cursor.execute(select_query)
		result = cursor.fetchall()
		data = json.dumps(result,use_decimal=True)
		data = json.loads(data)
	except Error as e:
		data = []
	return render_template('index.html',data=data)

@app.route('/process',methods=['POST'])
def process_result():
	content = request.json
	if content['aruco']:
		if len(content['aruco']) > 0:
			print('Found label aruco')
		for id in content['aruco']:
			print(id)
	return jsonify(content) 

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000, debug=True)