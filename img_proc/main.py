try:
    import RPi.GPIO
    RPI = True 
except ImportError:
    RPI = False

from camera import Camera
from symbols_ml import SymbolsMl
from aruco import Aruco
import mysql.connector
from mysql.connector import Error
from time import time 

start_time = time.time()


if RPI:
    insert_label_query = """INSERT INTO Labels (Time, Dangerous,Corrosive,Aruco) VALUES(%s,%s,%s,%s)"""
    connection = mysql.connector.connect(host='172.19.55.199',
                                    database='sensors',
                                    user='mysql',
                                    password='mysql')

    processors = [
        Aruco(),
        SymbolsMl()
    ]
    src = 'ml/training/pi-targets.avi'

    start_time = time.time()

    with Camera(processors=processors, src=0, fps=60) as cam:
        cam.start()

        while cam.running() and cam.new_processed_frame_event.wait(10):
            frame = cam.get_frame(get_processed=True)
            results = cam.get_results()

            try:                                     
                if connection.is_connected():
                    cursor = connection.cursor()
                    labels_data = [float(time.time()-start_time), int(results['dangerous']), int(results['corrosive']), str(results['aruco_ids'])] 

                    cursor.execute(insert_label_query, tuple(labels_data))
                    connection.commit()
            except Error as e:
                print("Error while connecting to MySQL", e)

else:
    pass
