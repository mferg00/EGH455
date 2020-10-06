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


@app.route('/get_labels',methods=['GET'])
def get_labels():
	try:
		connection = mysql.connector.connect(host='localhost',
										 database='sensors',
										 user='mysql',
										 password='mysql')
		select_label_query = "SELECT Dangerous, Corrosive, Aruco FROM Labels ORDER BY Time DESC LIMIT 1;"
		cursor = connection.cursor()
		cursor.execute(select_label_query)
		result = cursor.fetchall()
		result_labels = []
		result_labels.append(result[0][0])
		result_labels.append(result[0][1])
		aruco = result[0][2].replace('[','').replace(']','')
		aruco = [int(x) for x in aruco.split(',')]
		result_labels.append(aruco)
		
	except Error as e:
		result_labels = []
	return jsonify(result_labels)

@app.route('/get_gases',methods=['GET'])
def get_gases():
	try:
		connection = mysql.connector.connect(host='localhost',
										 database='sensors',
										 user='mysql',
										 password='mysql')
		select_gas_query = "SELECT Ox_Threshold, Red_Threshold, Nh3_Threshold, Ox, Red, Nh3  FROM UAVSensors ORDER BY Time DESC LIMIT 1;"
		cursor = connection.cursor()
		cursor.execute(select_gas_query)
		result_gases = cursor.fetchall()
		
	except Error as e:
		result_gases = []
	return jsonify(result_gases)


@app.route('/get_data',methods=['GET'])
def get_data():
	try:
		connection = mysql.connector.connect(host='localhost',
										 database='sensors',
										 user='mysql',
										 password='mysql')
		select_total_query = "SELECT Time, Pressure, Humidity, Light, Temperature, Noise_1, Noise_2, Noise_3 FROM UAVSensors ORDER BY Time ASC;"
		cursor = connection.cursor()
		cursor.execute(select_total_query)
		result = cursor.fetchall()
		connection.close()
		
	except Error as e:
		result = []
		print(e)
	return jsonify(result)


@app.route('/')
def main_page():
	return render_template('index.html')

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
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0',port=5000, debug=True)