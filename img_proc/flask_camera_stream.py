from flask import Flask, render_template, request, jsonify, Response
from camera import Camera, html_frame_gen

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    camera = Camera(**(request.args.to_dict()))
    return Response(html_frame_gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def test():
    return 'hello world'

def run():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
	run()