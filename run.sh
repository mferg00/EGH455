python3 img_proc/flask_camera_stream.py & python3 air_sensor/all_readings_sql.py && kill $!
#!/bin/bash

# take argv 1 as the database IP address, but if thats not there set it to 0.0.0.0
DB_HOST_IP=${1:-0.0.0.0}

python3 img_proc/flask_camera_stream.py "$DB_HOST_IP" & python3 air_sensor/all_readings_sql.py "$DB_HOST_IP" && kill $!
