import mysql.connector
from mysql.connector import Error
import simplejson as json


create_table_query = "CREATE TABLE UAVSensors (Id int(11) NOT NULL, Oxidise decimal(16,8) NOT NULL, Reducing decimal(16,8) NOT NULL, Nh3 decimal(16,8) NOT NULL, PRIMARY KEY (Id))"
delete_table_query = "DELETE FROM UAVSensors"
insert_query = """INSERT INTO UAVSensors  (Id, Oxidise, Reducing, Nh3) 
								VALUES (%s, %s, %s, %s) """
select_query = "SELECT Oxidise, Reducing, Nh3 FROM UAVSensors ORDER BY Id DESC limit 10;"
insert_label_query = "INSERT INTO Labels (Id, LabelName, Output) VALUES(%s, %s, %s)"



try:
	connection = mysql.connector.connect(host='172.19.58.168',
										 database='sensors',
										 user='mysql',
										 password='mysql')
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