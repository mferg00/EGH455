import mysql.connector
from mysql.connector import Error

insert_label_query = """INSERT INTO Labels (Id, Dangerous,Corrosive,Aruco) VALUES(%s,%s,%s,%s)"""

connection = mysql.connector.connect(host='localhost',
										 database='sensors',
										 user='mysql',
										 password='mysql')

try:
	num_id = 1                                     
	if connection.is_connected():
		cursor = connection.cursor()
		labels_data = [num_id,int(dangerous),int(corrosive),"-".join(aruco)] 

		cursor.execute(insert_label_query, tuple(labels_data))
		connection.commit()
		num_id = num_id + 1
except Error as e:
	print("Error while connecting to MySQL", e)