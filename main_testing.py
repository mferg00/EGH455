from threading import Thread
from img_proc.flask_camera_stream import run as run_stream

def main():
    Thread(target=run_stream()).start()
    

if __name__ == '__main__':
    main()