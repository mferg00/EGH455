from typing import Iterator
from flask import Flask, render_template, request, jsonify, Response
import cv2
import mysql.connector
from mysql.connector import Error as SQLError
import time 

from camera import Camera
from symbols_ml import SymbolsMl
from aruco import Aruco

from sys import argv
DB_HOST_IP = '0.0.0.0' if len(argv) < 2 else argv[1]

app = Flask(__name__)

def yield_frames(cam: Camera, get_processed: bool = True, send_to_db: bool = True) -> Iterator[str]:
    """Yield frames from camera for html usage.

    Args:
        cam (Camera): Camera object to get frames from.
        get_processed (bool, optional): Whether to get raw or processed frames. Defaults to True.

    Yields:
        Iterator[str]: A string to embed in html to play video.
    """
    try:
        cam.start()

        if send_to_db:
            start_time = time.time()
            insert_label_query = """INSERT INTO Labels (Time, Dangerous,Corrosive,Aruco) VALUES(%s,%s,%s,%s)"""
            connection = mysql.connector.connect(host=DB_HOST_IP,
                                    database='sensors',
                                    user='mysql',
                                    password='mysql')

        while cam.running() and cam.new_processed_frame_event.wait(10):
            frame = cam.get_frame(get_processed=get_processed)

            if send_to_db:
                results = cam.get_results()
                
                try:                                     
                    if connection.is_connected():
                        cursor = connection.cursor()
                        labels_data = [float(time.time()-start_time), int(results['dangerous']), int(results['corrosive']), str(results['aruco_ids'])] 

                        cursor.execute(insert_label_query, tuple(labels_data))
                        connection.commit()
                except SQLError as e:
                    print("Error while connecting to MySQL", e)
                
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tostring() + b'\r\n')

    finally:
        cam.stop()
        if send_to_db:
            connection.close()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    processors = [
        SymbolsMl(), Aruco()
    ]
    cam = Camera(processors=processors)
    return Response(yield_frames(cam, get_processed=True), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def test():
    return 'hi'

def run():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
	run()