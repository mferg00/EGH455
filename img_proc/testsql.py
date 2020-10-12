import mysql.connector
from mysql.connector import Error as SQLError
import time

from sys import argv
DB_HOST_IP = '' if len(argv) < 2 else argv[1]

insert_label_query = """INSERT INTO Labels (Time,Dangerous,Corrosive,Aruco) VALUES (%s,%s,%s,%s)"""
start_time = time.time()
connection = mysql.connector.connect(host=DB_HOST_IP,
                        database='sensors',
                        user='mysql',
                        password='mysql')

try:
    if connection.is_connected():
        cursor = connection.cursor()
        labels_data = (
            float(time.time() - start_time), 
            int(90), 
            int(40), 
            str([1, 2, 3])
        )
        cursor.execute(insert_label_query, labels_data)
        connection.commit()
except SQLError as e:
    print("Error while connecting to MySQL: ", e)
except Exception as e:
    print("Unknown exception when sending to db: ", e)