import os 

import cv2
from flask import Flask, render_template, request, jsonify, Response

from img_proc.utils import yield_frames

# Initialize Flask web app
app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(yield_frames(post_url=None), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def test():
    return 'hello world'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
