import mysql.connector
from mysql.connector import Error
import simplejson as json
import time


create_table_query = "CREATE TABLE UAVSensors (Time decimal(16,8) NOT NULL, Pressure decimal(16,8) NOT NULL, Humidity decimal(16,8) NOT NULL,  Light decimal(16,8) NOT NULL, Temperature decimal(16,8) NOT NULL, Noise_1 decimal(16,8) NOT NULL, Noise_2 decimal(16,8) NOT NULL, Noise_3 decimal(16,8) NOT NULL, Ox_Threshold decimal(16,8) NOT NULL, Red_Threshold decimal(16,8) NOT NULL, Nh3_Threshold decimal(16,8) NOT NULL, Ox decimal(16,8) NOT NULL, Red decimal(16,8) NOT NULL, Nh3 decimal(16,8) NOT NULL,PRIMARY KEY (Id))"
delete_table_query = "DELETE FROM UAVSensors"
insert_query = """INSERT INTO UAVSensors  (d, Time, Pressure, Humidity, Light, Temperature, Noise_1, Noise_2, Noise_3, Ox_Threshold, Red_Threshold, Nh3_Threshold, Ox, Red, Nh3) 
								VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s) """
select_query = "SELECT Oxidise, Reducing, Nh3 FROM UAVSensors ORDER BY Id DESC limit 10;"
insert_label_query = "INSERT INTO Labels (Id, LabelName, Output) VALUES(%s, %s, %s)"



create_label = "CREATE TABLE Labels (Id int(11), LabelName varchar(50), Output varchar(50), PRIMARY KEY (Id))"
insert_label_query = """INSERT INTO Labels (Id, LabelName,Output) VALUES(%s,%s,%s)"""

try:
	connection = mysql.connector.connect(host='172.19.58.168',
										 database='sensors',
										 user='mysql',
										 password='mysql')
<<<<<<< HEAD
	# if connection.is_connected():
	# 	cursor = connection.cursor()
	# 	# cursor.execute(create_table_query)
	# 	sensors_file = open("readings.txt","r")
	# 	lines = sensors_file.readlines()
	# 	num_id = 0
	# 	for line in lines:
	# 		if line.find(',') >= 0:
	# 			# data_list = []
	# 			# data_list.append(num_id)
	# 			line = line.replace("\n","").replace("]","").replace("[","").replace(" ", ",").replace(",,",",")
	# 			recordTuple = tuple([num_id]) + tuple(x for x in line.split(',') if x)
	# 			print(recordTuple)
	# 			time.sleep(5)
		# 		cursor.execute(insert_query, recordTuple)
		# 		connection.commit()
		# 		num_id = num_id + 1
		
		# print("Insert data into table UavSensors successfully ")
	cursor = connection.cursor()
	# cursor.execute(select_query)
	cursor.execute(insert_label_query,tuple([1,"Harry","Harry"]))
	connection.commit()
=======
	if connection.is_connected():
		cursor = connection.cursor()
		# sensors_file = open("readings.txt","r")
		# lines = sensors_file.readlines()
		# num_id = 0
		# for line in lines:
		# 	if line.find(',') >= 0:
		# 		line = line.replace("\n","")
		# 		recordTuple = tuple([num_id]) + tuple(line.split(','))
		# 		print(recordTuple)
		# 		cursor.execute(insert_query, recordTuple)
		# 		connection.commit()
		# 		num_id = num_id + 1
		test_data = [0,"Harry","Harry"]
		# counter, label, outout
		cursor.execute("SHOW TABLES;")
		result = cursor.fetchall()
		print(result)
		
	# 	print("Insert data into table UavSensors successfully ")
	# cursor = connection.cursor()
	# cursor.execute(select_query)
	# cursor.execute(create_table_query)
>>>>>>> 077fa5d4c92754339ad63597268f545f69e01d18
	# result = cursor.fetchall()
	# data = json.dumps(result,use_decimal=True)
	# data = json.loads(data)
	# print(type(data))
	# for x in data:
	# 	print(x[0])

		# db_Info = connection.get_server_info()
		# print("Connected to MySQL Server version ", db_Info)
		# cursor = connection.cursor()
		# cursor.execute("select database();")
		# record = cursor.fetchone()
		# print("You're connected to database: ", record)
		# cursor = connection.cursor()
		# result = cursor.execute(create_table_query)
		# print("UavSensors Table created successfully ")

except Error as e:
	print("Error while connecting to MySQL", e)
finally:
	if (connection.is_connected()):
		cursor.close()
		connection.close()
		print("MySQL connection is closed")