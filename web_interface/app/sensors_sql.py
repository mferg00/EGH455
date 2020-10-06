import mysql.connector
from mysql.connector import Error

insert_query = """INSERT INTO UAVSensors  (Id, Time, Pressure, Humidity, Light, Temperature, Noise_1, Noise_2, Noise_3, Ox_Threshold, Red_Threshold, Nh3_Threshold, Ox, Red, Nh3) 
								VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s) """

try:
	connection = mysql.connector.connect(host='172.19.55.199',
										 database='sensors',
										 user='mysql',
										 password='mysql')
	num_id = 1                                     
	if connection.is_connected():
		cursor = connection.cursor()
		noise_1, noise_2, noise_3 = noise_lvl
		ox_thresh, red_thresh, nh3_thresh = gases_threshold
		ox, red, nh3 = gases
		sensor_data = [num_id,run_time, pressure,humidity,light,temperature,noise_1,noise_2,noise_3,ox_thresh,red_thresh, nh3_thresh,ox, red, nh3]
		recordTuple = tuple(sensor_data)
		try:
			cursor.execute(insert_query, recordTuple)
			connection.commit()
			num_id = num_id + 1
		except Error as e:
			print("Error while inserting to mysql", e)
except Error as e:
	print("Error while connecting to MySQL", e)
finally:
	if (connection.is_connected()):
		cursor.close()
		connection.close()
		print("MySQL connection is closed")

